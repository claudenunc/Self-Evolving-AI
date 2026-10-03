# Self-Evolving-AI

A working record for turning naturally expressed goals into completed, verified projects, reusable workflows, and teaching materials.

## Start here

Read [PROJECT_BRIEF.md](PROJECT_BRIEF.md) and [HANDOFF.md](HANDOFF.md) before continuing work. [DECISIONS_AND_EVIDENCE.md](DECISIONS_AND_EVIDENCE.md) records decisions and evidence; [BACKLOG_AND_EXPERIMENTS.md](BACKLOG_AND_EXPERIMENTS.md) distinguishes the next experiments from completed setup. [AGENTS.md](AGENTS.md) carries the existing working agreement into repository tasks.

## Preserved work

| Location | Contents |
| --- | --- |
| [Original research and implementation](archive/chatgpt-os-2026-10-03/) | Research Markdown/PDF, copy-paste configuration, applied instructions, original project records, intelligence pilot, teaching guide/PDF, three reviewed screenshots, terminal capture, and MP4 replay |
| [Five workflow sources](skills/) | Evidence Research, Decision and Experiment, Verified Execution, Research to Implementation, Teach and Repeat; metadata, icons, and supporting references |
| [Benchmark](benchmarks/chatgpt-24-tasks/) | 24 tasks, six configurations, synthetic fixtures, unmeasured results template, and deterministic feasibility checks |
| [Workflow examples](examples/workflow-checks/) | Prior bounded evaluation artifacts, kept separate from real project authority |
| [Teaching guide for this backup](docs/teaching/GitHub_Preservation_Guide.md) | Actual export process, verification signals, exclusions, and repeat recipe |
| [Provenance](docs/PROVENANCE.md) | Source mapping, privacy omissions, and interpretation of historical records |
| [Verification](verification/) | Historical evidence and checks for this export |
| [Proposed direction](docs/ROADMAP_PROPOSAL.md) | A draft for discussion; broader orchestration and new schedules are not activated |

The 2026-10-03 research was followed by implementation. Statements such as “nothing activated” inside the original research describe that earlier stage. The current handoff and dated implementation records describe the later setup.

The MP4 is a reconstructed chapter-card replay from authentic terminal output, with expanded timing and no audio. It is not continuous screen footage. Copying the skill folders does not install them in another account or runtime.

## Checks

From the repository root, use Python 3:

```bash
python3 scripts/verify_repository.py
python3 scripts/check_workflows.py
```

Run the feasibility checks in a disposable copy if you want to retain the original timing record unchanged:

```bash
python3 benchmarks/chatgpt-24-tasks/feasibility_pilot.py
```

The previous 14 local arithmetic/coding checks passed. The six-configuration model comparison remains unrun; no productivity gain is claimed.

## Scope and privacy

This is a public repository. Credentials, login/session data, unrelated chats, temporary rendering duplicates, and one screenshot containing account identity and unrelated chat titles are excluded. The preserved deliverables are indexed by content hashes. No repository license has been selected in this handoff.

The system evolves through checked changes to project records, skills, tools, and processes. It does not imply changes to model weights, perfect recall, unattended availability, or automatic access to other AI accounts.
