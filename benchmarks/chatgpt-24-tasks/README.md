# 24-task ChatGPT benchmark

Created October 3, 2026. Research-only; nothing is installed or scheduled.

Files:
- benchmark.json: 24 exact prompts, acceptance criteria, failures, six exact instruction variants, and ranking mappings.
- fixtures.json: synthetic inputs. Example emails use example.test; these are not real recipients.
- results_template.json: 144 empty result records (24 tasks x six configurations). NULL means unmeasured, not zero performance.
- feasibility_pilot.py and feasibility_results.json: local arithmetic/code checks actually run. These are not model-comparison results.

Run protocol:
1. Keep model, reasoning, tools, source inputs and effort/output budgets constant for instruction comparison. Use fresh conversations and record unavoidable memory contamination.
2. Give every variant the same synthetic fixtures; current-information tasks must use a dated source snapshot or record any change during the experiment.
3. Baseline retains normal product tools. Do not disable tools just to make the proposed configuration appear better.
4. Randomize run order; blind output labels to reviewers. Use executable known-answer checks and human review. Record misses, questions, latency, retries and user rework.
5. Test E's organized knowledge/native installed workflows separately and count setup/maintenance cost. Inline workflow instructions are not native installed skills.
6. An unpersonalized Temporary Chat disables plugins; do not use it for a purported equivalent full app/skill trial. A dedicated controlled account/workspace or evaluation environment provides stronger isolation. An API evaluation is a separate system comparison.
7. Full single-pass comparison: 144 runs. Three replicates: 432. A smaller screen is allowed, but report it as a screen.
8. Promote only after critical authorization/evidence failures are absent, paired usefulness/task-success improves, simple-task behavior does not regress, and added effort/cost is justified.

No performance percentages or latency scores have been generated. The feasibility pilot verifies selected known-answer fixtures and code paths, not superiority of E or the base model's behavior across configurations.
