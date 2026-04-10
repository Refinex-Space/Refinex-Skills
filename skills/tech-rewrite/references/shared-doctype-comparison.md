# Doctype: Technology comparison (X vs Y)

A comparison document weighs two or more technologies against each other and recommends one for a specific context. It is the most commonly abused document type in technical writing, because the temptation to hedge — to give both sides a fair hearing and decline to pick a winner — is strong. That temptation must be resisted. A comparison that does not pick a winner has failed.

## The core principle

Every comparison is a comparison *for* something. There is no universal best database, best framework, best programming language. There is only the best choice for a specific context, against specific criteria. The first job of a comparison document is to name the context and the criteria explicitly. Once those are on paper, the comparison becomes a mechanical exercise of applying the criteria to each option, and the verdict follows from the exercise.

A comparison that cannot name the context is not a comparison; it is a feature tour. A comparison that cannot name the criteria is not a comparison; it is an opinion piece. Both are weaker than a real comparison, and both are what comparisons slide into when the writer has not done the work up front.

## Required structure

A comparison document should open by stating the context and the criteria, then evaluate each option against the criteria, then deliver a verdict, then name the conditions under which the verdict would flip.

The opening section establishes the context. Who is making this decision? What problem are they solving? What constraints are non-negotiable? The answer to these questions determines which criteria matter. A ledger service with a 30ms latency budget and a multi-region requirement weighs databases differently than an internal analytics service where correctness matters more than latency. The reader must know which situation the comparison is about before they can evaluate whether the verdict applies to them.

The criteria section names the specific axes on which the comparison will be made. Good criteria are measurable, relevant, and ordered by importance. "Performance" is too abstract to be a criterion; "p99 write latency at 2k TPS" is measurable. "Ease of use" is too abstract; "time for a new engineer to ship their first feature, estimated from onboarding experience at similar teams" is measurable. The criteria list should have between three and six items; fewer than three and the comparison is too narrow, more than six and the analysis becomes diffuse.

The evaluation section applies each criterion to each option. The structure can be option-by-option ("here is how Option A performs on all criteria, then Option B, then Option C") or criterion-by-criterion ("here is how all options perform on Criterion 1, then Criterion 2"). The criterion-by-criterion structure is usually stronger for comparisons because it makes the weighing visible — the reader sees the options directly compared on each axis rather than having to hold both in mind and reconstruct the comparison themselves.

The verdict section names the winner. The winner is qualified with the context and criteria from the opening. "For our ledger service, given the 30ms p99 latency budget and multi-region requirement, PostgreSQL is the right choice." Not "PostgreSQL is the best database", which is not a claim the comparison can support. The qualified verdict is both more honest and more useful — it tells the reader not just what to pick but under which conditions the recommendation applies to them.

The conditions section describes the circumstances under which the verdict would flip. This is where the comparison earns the reader's trust. A comparison that names only the winner looks dogmatic; a comparison that says "we chose X, but if your latency budget were 100ms rather than 30ms, Y would win, because Y's consistency model would then be the dominant criterion" demonstrates that the writer understood the tradeoffs and did not just pick a favorite. The conditions section also tells readers in different situations how to apply the reasoning to their own case.

## Voice

Comparisons use the Design Tribunal voice almost exclusively. The writer is sitting in judgment over the options and delivering a verdict, which is exactly what the voice is designed for. Any temptation to slide into a different voice — to describe the internals of one option in Mechanism Autopsy voice, for example — is voice drift and should be resisted. If the comparison requires understanding the internals of one option, either summarize the internals in service of the verdict or split the piece into a comparison and a separate deep-dive.

## What "both have pros and cons" really means

When a writer concludes that "both options have their pros and cons", they are usually signaling one of three things. The first possibility is that the context was not specified tightly enough. "Which database is better?" has no answer; "which database is better for a ledger service with a 30ms p99 budget and strict serializable isolation requirements?" has an answer. If the comparison cannot reach a verdict, check the context first.

The second possibility is that the criteria were not named or not weighted. "Both are good on latency and both are good on consistency" may be true but is not a verdict — something else has to break the tie, and the comparison has to name what. If the comparison cannot reach a verdict with the current criteria, either the criteria are missing a dimension or the weighting between criteria has not been made explicit.

The third possibility is that the writer does not actually have a verdict and is hedging. This is the most common case. The fix is to return to the Anchor Sheet, strengthen the criteria, and commit to a position. If after strengthening the criteria the writer genuinely believes the options are tied, the honest move is to say "for this context, either option works; we recommend choosing based on team familiarity" or to narrow the context until one option wins.

The move that is never acceptable is "both have pros and cons, choose the one that fits your needs". That sentence communicates nothing the reader did not already know, and it wastes the reader's time.

## Length

Comparison documents are usually 1500 to 4000 words. Shorter than 1500 and the analysis has probably been too shallow to support a confident verdict; longer than 4000 and the piece has probably absorbed material that belongs elsewhere — feature tours, tutorials, or deep-dives into the internals of one option.

## Gates specific to comparisons

The comparison must name a specific context in its opening. Confirm that the reader can tell, within the first few paragraphs, what situation the comparison is addressing. A comparison with no context has no verdict worth trusting.

The criteria must be explicit and measurable where possible. Count them: between three and six is the right range. For each criterion, verify that it is concrete enough to be applied — "performance" and "ease of use" are not criteria until they are refined into specific, measurable dimensions.

The evaluation must apply every criterion to every option. Missing evaluations are a sign that the writer has not done the full comparison and is hoping the reader will not notice. If a criterion cannot be evaluated for one of the options because data is unavailable, say so explicitly — "we could not measure Option B's p99 write latency because we did not have production access during evaluation" is honest and acceptable; silently skipping the evaluation is not.

The verdict must name a winner, and the verdict must be qualified by the context and criteria from the opening. A universal verdict ("X is the best") is wrong; a qualified verdict ("for our context, X wins because of criterion Y") is right.

The conditions under which the verdict would flip must be named. This is the gate that separates good comparisons from dogmatic ones. If the writer cannot name the conditions, either the writer does not understand the options deeply enough or the criteria are too narrow to admit any counterfactual.

## Common failure patterns

The **feature tour disguised as a comparison** is the most common failure. The document describes all the features of Option A, then all the features of Option B, with no criteria and no weighing. The reader finishes with a sense that the writer knows both options but no idea which one to pick. The fix is to add explicit criteria at the start and weigh the features against those criteria rather than listing them.

The **asymmetric depth** failure happens when the writer knows one option much better than the others and evaluates the known option in depth while treating the other options superficially. The superficial treatment usually slides into straw versions of the other options — claims that sound plausible but would not survive scrutiny from someone who actually used those options. The fix is honest: either do the work to understand the other options at the same depth, or scope the comparison down to only the options the writer can evaluate rigorously.

The **criteria shopping** failure happens when the writer has a preferred option in mind and picks criteria that favor it. This is hard to detect from inside the writer's own perspective; the fix is to ask whether a reader who preferred a different option would accept the criteria as reasonable. If the answer is no, the criteria are biased and need to be broadened.

The **buried verdict** failure happens when the writer has reached a real conclusion but hedges it into invisibility. The verdict appears in a single subordinate clause midway through the final paragraph, so a reader scanning the piece misses it. The fix is to state the verdict clearly and prominently — in the opening as a preview, and again at the end as the conclusion. A reader who reads only the opening and the closing paragraph should walk away knowing the verdict and the context.