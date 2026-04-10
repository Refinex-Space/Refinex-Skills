# Doctype: Deep-dive / Mechanism Autopsy

A deep-dive opens up a system, a library, a protocol, or a piece of source code and walks the reader through its internals. The goal is not to describe what the thing does — that is what reference documentation is for — but to explain *how* it does what it does, with enough specificity that the reader leaves with a mental model they can use to predict future behavior.

The canonical voice for a deep-dive is Mechanism Autopsy, and the voice's central discipline applies to the whole document: every claim about internals is backed by a specific file path, line number, version tag, or reproducible command. The reader should be able to follow the writer's steps on their own machine and land on the same evidence. Authority in a deep-dive comes from specificity, and specificity cannot be faked — it either exists in the piece or it does not.

## The core promise

A deep-dive promises the reader that by the end, they will understand something about a system that they did not understand at the start, and that this understanding will generalize. The generalization is the payoff: a deep-dive that explains one specific case without yielding a reusable mental model is a waste of the reader's time, because the reader is unlikely to encounter that exact case again. The writer's job is to pick a specific case, walk the reader through it in enough detail that the walkthrough is credible, and then step back at the end and extract the pattern that applies beyond the specific case.

The choice of which specific case to use is important. Strong deep-dives pick a case that is simultaneously (a) small enough to walk through fully in the space available, (b) non-trivial enough that the walkthrough teaches something, and (c) representative enough that the mental model generalizes. A deep-dive that picks a case too small will not teach anything; one that picks a case too large will bog down in details; one that picks an unrepresentative case will teach the wrong lesson.

## Structure

The structure of a deep-dive is flexible, but the following elements must appear in roughly this order.

The opening hooks the reader on a misconception or a surprising observation. Strong openings name something the reader probably believes — "everyone says Spring Boot auto-configuration is magic" — and then promise to dismantle it. The misconception hook works because it gives the reader an immediate reason to read on: they want to find out whether their mental model was wrong. A deep-dive that opens with "let's look at how X works" has squandered this advantage.

The setup section names the specific version of the code being examined, the specific case being walked through, and the specific tools used to follow along. Version matters because source code changes between releases, and a deep-dive that is ambiguous about version is a deep-dive whose claims cannot be verified. The setup section should be short — one or two paragraphs — but it must be concrete. Name the version. Name the file. Name the command you ran.

The walkthrough section is the body of the deep-dive. It follows the execution path or the data flow through the system, stopping at each interesting point to show the reader what the code actually does. Every substantive claim in the walkthrough is anchored to a specific location in the source — a file path, a line number, a function signature — and where possible, the relevant code is quoted inline so the reader can see the claim and the evidence simultaneously.

The walkthrough is where most deep-dives succeed or fail. The common failure mode is to describe the code rather than quote it, which forces the reader to take the writer's word for what the code does. The strong move is to quote the code, point at the specific part that does the interesting thing, and explain that specific part in the writer's own words. The reader should feel that they are looking over the writer's shoulder at the source.

The insight section is where the specific case becomes a general mental model. After walking the reader through the specific case, the writer steps back and names the pattern: "here is the picture you can carry away, and here is how it lets you predict behavior in related cases". The insight section is short — usually a few paragraphs — but it is what distinguishes a deep-dive from a walkthrough-for-its-own-sake.

The closing is a specific reusable takeaway. Not a summary. A named mental model, a rule of thumb, a diagnostic heuristic, or a concrete prediction the reader can now make. The closing answers the question "what do I do differently now that I have read this".

## Voice discipline

The Mechanism Autopsy voice has three rules that are particularly strict in a deep-dive.

First, no hand-waving. The words "magic", "under the hood", "somehow", "automatically", and "behind the scenes" are banned unless they appear inside a quotation the writer is about to dismantle. These words are the absence of a mechanism, and the whole point of a deep-dive is to replace them with specific mechanisms.

Second, every version-sensitive claim is version-tagged. "Spring Boot reads this file" is too vague; "Spring Boot 3.2.0 reads `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`; in earlier versions this was `META-INF/spring.factories`" is specific. Version tagging prevents the deep-dive from going stale silently — a reader on a different version can tell immediately whether the claims still apply.

Third, no speculation unless labeled as speculation. A deep-dive that shifts between observed behavior and the writer's guess about why the behavior exists will confuse the reader and erode trust. If the writer is speculating, the speculation is labeled: "I suspect this is because of reason X, though I have not confirmed it by reading the commit history." Labeled speculation is honest; unlabeled speculation is a bug in the piece.

## Length

Deep-dives are usually longer than blog posts — 2000 to 5000 words is common, and longer is acceptable when the subject matter genuinely requires it. The length is driven by the need for specificity: quoting source, showing call chains, and walking through the reasoning all take space. A deep-dive that feels too short is usually one where the writer summarized instead of quoted, and the fix is to add the missing quotations.

## Gates specific to deep-dives

The first gate checks version-tagging. Every substantive claim about internals should be traceable to a specific version of the source code. Scan the draft for claims that are version-agnostic ("Spring reads the file") and either version-tag them or rewrite them to be version-agnostic for a reason the writer can defend.

The second gate checks for code anchors. For every claim about what the code does, verify that the piece either quotes the relevant code inline or provides a specific enough pointer — file path with line number — that the reader can find the code themselves. Claims that lack code anchors are weak even when they are correct.

The third gate checks the "magic" vocabulary. Search the draft for "magic", "under the hood", "somehow", "automatically handles", "behind the scenes", "just works". Each hit is a candidate for dismantling. Some will survive — for example, a sentence like "everyone thinks Spring auto-configuration is magic" is fine because the deep-dive is about to show it is not — but most should be replaced with the actual mechanism.

The fourth gate checks the insight section. Verify that the deep-dive ends on a generalizable mental model rather than a summary. Read the closing paragraph and ask: "would a reader who skipped the walkthrough but read this closing still learn something useful?" If the answer is no, the closing is a summary and needs to be rewritten as an insight.

The fifth gate checks that the specific case is representative. Ask whether the reader, after reading the piece, could correctly predict behavior in a related case that the piece did not cover. If not, the piece has either chosen an unrepresentative case or failed to extract the pattern.

## Common failure patterns

The **walkthrough-without-payoff** failure produces a document that follows the code faithfully but never steps back to extract the mental model. The reader finishes with a sense of having been shown a lot of code but without a takeaway they can use. The fix is to add or strengthen the insight section, and to make sure the insight applies to cases beyond the specific one walked through.

The **summary-without-walkthrough** failure produces a document that describes the internals at a high level but never shows the code. The reader has no way to verify the claims, and the writer has not demonstrated that they actually read the source. The fix is to quote the code at the key points, not to describe it.

The **version-amnesia** failure produces a document whose claims are untagged and therefore unverifiable. A reader on a different version cannot tell whether the piece still applies. The fix is simple but requires discipline: tag the version in the setup section and reconfirm for any major claim whose behavior is version-dependent.

The **lost-in-the-trees** failure produces a document that follows the code so faithfully that the reader loses the thread. Every function call is examined; every edge case is traced; the walkthrough becomes an exhaustive tour of the code rather than a focused investigation. The fix is to cut aggressively — a deep-dive is not an attempt to explain every line, it is an attempt to explain the specific lines that matter for the central claim.

The **misread-the-code** failure is rare but catastrophic. The writer claims the code does something it does not do. The fix is discipline during drafting: quote the code inline, then explain the specific part of the quotation that does the claimed thing. If the writer cannot point at the specific part, the claim is probably wrong and needs to be reverified against the actual source.