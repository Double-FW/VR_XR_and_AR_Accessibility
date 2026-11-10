"""Export the approved VR XR and AR Accessibility Markdown without rewriting it."""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import quote
import yaml
from jsonschema import Draft202012Validator
from xr_hf_common import ROOT, SOURCE, MANAGED, destination, digest, git, load_config, read_sources

CONTEXT = ['AGENTS.md', 'README.md', 'Inclusive_Design_Guidance_VR_XR_AR.md']
EVIDENCE_CONTEXT = ['Inclusive_Design_Guidance_VR_XR_AR.md#1-evidence-and-scope',
                    'Inclusive_Design_Guidance_VR_XR_AR.md#15-test-programme-and-acceptance-criteria',
                    'Inclusive_Design_Guidance_VR_XR_AR.md#18-sources-and-evidence-notes']

def metadata(text):
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', text, re.S)
    md = yaml.safe_load(match[1]) if match else {}
    return md if isinstance(md, dict) else {}

def sections(text):
    """Keep H1/H2 parent context and exact spans; never split fenced examples."""
    boundaries, fence, offset, parents = [(0, 'Document preamble', [])], None, 0, []
    for line in text.splitlines(keepends=True):
        mark = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if mark:
            token = mark[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not line[mark.end():].strip():
                fence = None
        elif fence is None:
            match = re.match(r'^(#{1,2})[ \t]+([^\r\n]+)', line)
            if match:
                level, title = len(match[1]), match[2].strip().rstrip('#').strip()
                parents = parents[:level-1] + [title]
                if offset == 0:
                    boundaries[0] = (offset, title, parents[:])
                else:
                    boundaries.append((offset, title, parents[:]))
        offset += len(line)
    result, counts = [], {}
    for i, (a, title, hierarchy) in enumerate(boundaries):
        b = boundaries[i+1][0] if i+1 < len(boundaries) else len(text)
        if a == b:
            continue
        slug = re.sub(r'[^a-z0-9]+', '-', ' '.join(hierarchy or [title]).lower()).strip('-') or 'section'
        counts[slug] = counts.get(slug, 0) + 1
        key = slug if counts[slug] == 1 else slug + '-' + str(counts[slug])
        result.append((key, title, text[a:b], a, b, hierarchy))
    if ''.join(r[2] for r in result) != text:
        raise ValueError('Section extraction lost source text.')
    return result

def build(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    if output == root or root in output.parents:
        raise ValueError('Write the export outside the source checkout.')
    cfg = load_config(root)
    target = destination(cfg['destination_dataset'])
    texts, manifest, omitted = read_sources(root, cfg)
    sha = git(root, 'rev-parse', 'HEAD').decode().strip()
    date = git(root, 'show', '-s', '--format=%cs', 'HEAD').decode().strip()
    warnings = ['The handbook distinguishes source findings, historical platform guidance, synthesis and proposed acceptance tests. Extraction does not independently verify any of these or certify an XR product.']
    def row(path, key, title, body, a, b, hierarchy, kind):
        md = metadata(texts[path])
        return {'id': path + '::' + key, 'title': title, 'text': body, 'record_type': kind,
            'source_repository': SOURCE, 'source_path': path, 'source_commit': sha,
            'source_url': f'https://github.com/{SOURCE}/blob/{sha}/{quote(path)}',
            'source_start_line': texts[path][:a].count('\n') + 1,
            'source_end_line': max(1, texts[path][:b].count('\n') + (not texts[path][:b].endswith('\n'))),
            'source_document_sha256': digest(texts[path].encode()), 'text_sha256': digest(body.encode()),
            'heading_path': hierarchy, 'metadata_json': json.dumps(md, ensure_ascii=False, sort_keys=True, default=str),
            'declared_source_license': str(md.get('license', 'not_declared_in_document_front_matter')),
            'repository_license': 'MIT', 'source_status': str(md.get('status', 'see_source')),
            'dataset_version': cfg['dataset_version'], 'source_commit_date': date, 'language': 'en-GB',
            'required_context_paths': [p for p in CONTEXT if p in texts],
            'required_context_sections': EVIDENCE_CONTEXT, 
            'review_status': 'faithful_extraction_checked_not_independent_xr_testing_or_content_review'}
    docs, chunks = [], []
    for path in cfg['files']:
        if path not in texts:
            continue
        text = texts[path]
        kind = 'agent_guidance' if path == 'AGENTS.md' else 'orientation' if path == 'README.md' else 'immersive_design_handbook'
        docs.append(row(path, 'document', path, text, 0, len(text), [], kind))
        for key, title, body, a, b, hierarchy in sections(text):
            chapter = hierarchy[0] if hierarchy else ''
            kind = ('proposed_acceptance_test' if path == 'Inclusive_Design_Guidance_VR_XR_AR.md' and chapter.startswith('15 ') else
                    'illustrative_worked_example' if path == 'Inclusive_Design_Guidance_VR_XR_AR.md' and chapter.startswith('17 ') else
                    'source_reference_notes' if path == 'Inclusive_Design_Guidance_VR_XR_AR.md' and chapter.startswith('18 ') else
                    'knowledge_section')
            chunks.append(row(path, key, title, body, a, b, hierarchy, kind))
    if not docs or not chunks:
        raise ValueError('The guidance export is empty.')
    schema = {'$schema': 'https://json-schema.org/draft/2020-12/schema', 'type': 'object',
              'required': list(docs[0]), 'additionalProperties': False, 'properties': {}}
    for k, v in docs[0].items():
        schema['properties'][k] = {'type': 'array', 'items': {'type': 'string'}} if isinstance(v, list) else {'type': 'integer' if isinstance(v, int) else 'string'}
    validator = Draft202012Validator(schema)
    for records in (docs, chunks):
        if len({r['id'] for r in records}) != len(records):
            raise ValueError('Duplicate export identifiers.')
        for r in records:
            validator.validate(r)
            if digest(r['text'].encode()) != r['text_sha256']:
                raise ValueError('Text checksum mismatch.')
    output.mkdir(parents=True, exist_ok=True)
    def write_json(name, obj):
        (output/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for name, records in [('documents.jsonl', docs), ('knowledge_chunks.jsonl', chunks)]:
        (output/name).write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in records), encoding='utf-8')
    (output/'LICENSE').write_bytes(texts['LICENSE'].encode())
    write_json('record_schema.json', schema)
    write_json('provenance.json', {'source_repository': SOURCE, 'source_commit': sha, 'source_commit_date': date,
        'destination_dataset': target, 'dataset_version': cfg['dataset_version'], 'files': manifest,
        'omitted_optional_files': omitted, 'source_warnings': warnings, 'external_sources_fetched': False})
    card = f'''---
pretty_name: Double FW VR XR and AR Accessibility
language:
- en
license: mit
tags:
- accessibility
- inclusive-design
- virtual-reality
- augmented-reality
- extended-reality
- agent-governance
- text
configs:
- config_name: knowledge_chunks
  default: true
  data_files:
  - split: train
    path: knowledge_chunks.jsonl
- config_name: documents
  data_files:
  - split: train
    path: documents.jsonl
---

# Double FW VR, XR and AR Accessibility

An evidence-informed practice corpus for inclusive immersive products, digital experiences and services. It covers physical products, ergonomics, alternative input, movement, visual/nonvisual access, communication, cognition, AR/MR environments, service design, measurement and proposed acceptance testing. It is guidance, not a conformance standard, clinical protocol, demonstrated device capability or product certification.

## Source and versions

Source: https://github.com/{SOURCE}

Source revision: `{sha}`. Source commit date: {date}. Export format: {cfg['dataset_version']}. The source handbook states its own date and evidence boundaries; publication is not a new research review.

## Dataset views

- `knowledge_chunks` (default): {len(chunks)} exact Markdown sections from the three approved documents, including preambles, first/second-level heading context and fenced examples.
- `documents`: {len(docs)} complete source documents: AGENTS.md, README.md and Inclusive_Design_Guidance_VR_XR_AR.md.

The views overlap. Do not concatenate them blindly. `train` is a loading convention, not evidence that a model has been trained. No generated question/answer pairs, independent benchmark split or completed XR evaluation results are supplied.

Chapter 15 sections are labelled `proposed_acceptance_test`, Chapter 17 sections `illustrative_worked_example`, and Chapter 18 sections `source_reference_notes`. These labels describe source sections, not validated outcomes. Other guidance sections use `knowledge_section`; complete rows use document-level types. T01–T24 identifiers, source notes, qualifications and worked examples are retained exactly. The worked example is not evidence of a completed deployment or participant study.

## Evidence context and source interpretation

Read AGENTS.md and the task-relevant handbook sections. Chapter 1 establishes evidence and scope, Chapter 15 explains the proposed test programme, and Chapter 18 identifies sources and limitations. Every record carries required_context_paths and required_context_sections references to retain these interpretation needs; they do not automatically fetch context or enforce any policy.

The handbook distinguishes observed barriers, evaluated adaptations, standards/expert guidance, platform documentation and handbook synthesis. Recommendations and acceptance criteria are synthesis unless explicitly identified otherwise. Preserve source scope and uncertainty. Observation counts are not participant prevalence; exploratory findings do not establish general effectiveness, and VR findings do not by themselves validate an AR implementation. Consult the actual source notes before using specific claims.

Proposed test procedures and criteria require project-specific adoption and actual evaluation. No tests of headsets, users, clinical safety, platform features, motion comfort, physical ergonomics, accessibility, legal compliance or release readiness are performed by this export. Current platform and standards details must be checked against authoritative sources when needed. The export preserves citations but does not fetch, mirror or reverify external linked material.

## Authority, privacy and outcomes

Repository guidance is knowledge content, not runtime instructions, tool permissions or authority to collect data, contact participants, deploy, accept risk or release a product. Project roles, permitted actions, risk tolerance and accountable decisions come from the real project. Keep proposed recommendations separate from observations and approval records. Comparable value, agency, comfort and recovery require appropriate real-device and user evaluation; packaging checks cannot establish them.

Only explicitly approved committed public documents are read. New documents require review and inclusion in huggingface/export-config.json. Untracked and unapproved files are excluded, but confidential text inserted into an approved source is not detected automatically. Do not add live personal, health, participant or confidential organisational records to this public corpus. Do not infer disability or preferences from diagnostic categories or behaviour.

## Record schema and provenance

Records include exact source path, immutable commit URL, line range, text and full-document SHA-256 hashes, heading path, JSON-encoded front matter, declared source licence/status, repository licence and context references. See record_schema.json and provenance.json. `see_source` or a missing document-front-matter declaration does not establish approval. Exact source text is retained without paraphrasing, repairing, inventing thresholds or promoting proposed tests to proven requirements. Changing a heading may change a section ID. Citations and hyperlinks inside extracted text retain their original form; resolve fragment-only links against the recorded source file URL.

## Licence

The root MIT LICENSE is copied unchanged, including copyright (c) 2026 Double FW. Source-specific notices and attribution remain in the source text. Third-party linked material retains its own rights and is not incorporated or relicensed by this exporter. Packaging is not an independent rights review.

## Updates and limits

GitHub is the authoring source. Updates are configured for Mondays at 07:23 UTC and manual runs. GitHub may delay schedules or disable them after inactivity. All three source documents and LICENSE are required; a missing required source, changed licence, invalid destination or failed integrity check stops publication. New source files are not included automatically.

Only README.md, LICENSE, documents.jsonl, knowledge_chunks.jsonl, provenance.json, record_schema.json and validation_report.json are managed. Other raw files and .gitattributes are preserved, but unmanaged copies are not kept in sync. Dataset visibility is unchanged. Updates use one commit guarded by the destination revision. Historical copies and downloads are not recalled. The initial authenticated GitHub run still needs checking.

## Loading

```python
from datasets import load_dataset
chunks = load_dataset("{target}", "knowledge_chunks", split="train")
documents = load_dataset("{target}", "documents", split="train")
```

Private datasets require authentication. Pin a destination revision for reproducibility. Loading these rows does not implement context-aware retrieval, governance or release enforcement.
'''
    yaml.safe_load(card.split('---', 2)[1])
    (output/'README.md').write_text(card, encoding='utf-8')
    report = {'status': 'passed', 'scope': 'faithful extraction and packaging checks only', 'source_commit': sha,
        'source_files_verified': len(manifest), 'document_records': len(docs), 'knowledge_section_records': len(chunks),
        'source_warnings': warnings, 'independent_content_review': False, 'live_publication_tested': False,
        'export_file_sha256': {name: digest((output/name).read_bytes()) for name in MANAGED if name != 'validation_report.json'}}
    write_json('validation_report.json', report)
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    print(json.dumps(build(ROOT, args.output)))

if __name__ == '__main__':
    main()
