# Teaching guide — preserve project work in GitHub

Task date: 2026-10-03. Destination: claudenunc/Self-Evolving-AI. Workflow reused: Teach and Repeat. This is a written guide from actual work, with verification receipts linked below; no new screen recording is claimed.

## Intended result

Preserve the existing research, configuration, workflow sources, benchmark, and teaching package in the exact user-selected repository. Give the next task enough current context to continue without treating old research or synthetic test examples as current authority.

Prerequisites: an explicit destination, write access, current project sources, available deliverable bytes, and a publication scope that covers those files. Keep sign-in and credentials in the supported secure surfaces.

## Actual process

| Action | Purpose and observed result | Completion signal |
| --- | --- | --- |
| Read the current brief, decisions, backlog, and handoff | Recovered the completed setup and boundaries. Latest user request authorized the named repository upload. | Source content read; current task scope recorded |
| Inspect the destination | Connected GitHub metadata showed public visibility and push permission; branch list was empty. | Exact owner/name, audience, and empty state confirmed |
| Inventory local deliverables and workflow sources | Found prior outputs and five installed workflow folders. All six attached sources byte-matched the corresponding outputs. | File sizes and source comparisons completed |
| Inspect teaching screenshots | One screenshot exposed account identity and unrelated chat titles. Three others were suitable for this public project export. | The identified screenshot excluded; guide builder confirmed it was not used in the preserved PDF |
| Copy relevant source groups | Kept original bytes, historical state, benchmark templates, workflow examples, and source-script provenance. | Dated archive, five skills, benchmark, and examples present |
| Add current continuation records | Recorded the user's broader vision while keeping integrations, new schedules, and commercial launch as proposals. | Root brief, decisions, backlog, handoff, and proposed roadmap readable |
| Add repeatable verification | Created a manifest with sizes, SHA-256 hashes, and expected Git blob IDs; checked links, archives, and common secret patterns. | [Local verification](../../verification/export_local_validation.json) reports actual checks |
| Publish and independently verify | Publish the checked tree with the authenticated repository connection; confirm the branch commit and every exported blob. | [Remote verification](../../verification/remote_verification.json) identifies the checked commit; final handoff records success |

The final row completed: main pointed to payload commit 8efe56dd18f620bdb4ec921a71ac94f604a33349, and an independent recursive-tree read matched all 78 file paths, byte sizes, and Git blob IDs. The linked receipt records that check. A closing metadata commit adds the receipt and this completed handoff; the final task also checks that latest branch state. A prepared local commit or an upload attempt alone does not establish remote persistence.

## Observed failure and recovery

The first integrity run found a link to its own result receipt before that file existed. The run wrote the receipt, then verification was repeated with the file present. The failed result is preserved in verification/export_validation_attempts.json; the final local receipt records the rerun. This demonstrates why a failed check should be corrected and repeated before publication.

The shell push failed because no shell GitHub credential was available. The connected GitHub plugin supplies the authorized write route. The first staged whitespace check also treated ReportLab PDFs as text; adding binary file attributes prevents that unsuitable check from interpreting PDF data as prose. The archive bytes are verified by hashes.

## Repeat recipe

1. Confirm the latest requested task, destination, existing remote state, and publication audience. Read current records before copying recommendations from an archive.
2. Gather complete relevant source files and supporting resources. Reconcile duplicates by byte comparison. Keep test fixtures separate from actual authority.
3. Check text and media for credentials, private source data, account identity, and unrelated history. Record omissions. Never commit login/session files or expand visibility to solve an access problem.
4. Preserve original outputs in a dated location. Write compact current goals, decisions, completed state, blockers, and next action. Use relative links and readable source-folder names.
5. Generate and check an integrity manifest. Verify archive readability and meaningful functional fixtures; retain unmeasured fields as unmeasured.
6. Inspect the pending changes. Commit to the authorized branch and push without forcing history. If shell authentication is unavailable, use a supported authenticated repository tool; do not request passwords in chat.
7. Fetch or query the published branch independently. Compare its tree entries and blob IDs against the exact local payload. Record the verified commit and any failures; do not infer persistence from an attempted command.
8. Refresh the handoff and guide from real results. Reuse the existing workflow; create a new skill only when a distinct repeated procedure warrants one.

## Checks and interpretation

```bash
python3 scripts/verify_repository.py
python3 scripts/check_workflows.py
```

After fetching the published main branch, repeat the complete remote comparison:

```bash
git fetch origin main
python3 scripts/verify_repository.py --remote-ref origin/main
```

This compares every tracked local path, byte size, and Git blob ID with the fetched commit, including the manifest and receipts. It reports the exact checked commit. It does not fetch or publish automatically.

The first checks this export; the second repeats 11 deterministic fixture assertions. The prior benchmark contains 14 local feasibility assertions, separate from model-comparison trials. This backup performs no new six-way model benchmark.

The manifest excludes itself and verification receipts to avoid circular hashes. Every published file is still included in the remote tree check. Refresh the manifest after reviewed content changes, then rerun verification. Retain original feasibility timing records when reproducing checks in a disposable copy.

The earlier MP4 is a reconstructed chapter-card terminal replay; its scope and omissions are retained in the original guide. This written preservation lesson includes no authentication recording, private reasoning, unrelated account content, or unobserved success claim.
