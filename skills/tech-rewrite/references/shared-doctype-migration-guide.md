# Doctype: Migration field guide

A migration guide walks the reader through an upgrade, a technology migration, or the adoption of a new tool. The reader is not learning; the reader is doing. They have decided to make the change, or they are evaluating whether to make the change, and they need a map that matches the territory well enough to get them safely to the other side.

The canonical voice for a migration guide is Migration Field Guide, and its central discipline is the pit list. A migration guide earns its name by warning the reader about the traps the writer fell into. Without the pits, the document is a happy-path walkthrough that is indistinguishable from marketing. With the pits, it is a genuine field guide that saves the reader hours or days.

## The core promise

A migration guide promises the reader that if they follow the steps, they will end up at the intended destination with their system still working. The promise is serious: a reader who follows a broken migration guide loses time, confidence, and sometimes data. The weight of the promise shapes the document. Every step must be correct. Every known pit must be flagged. Every place where the migration can go wrong must be called out before the reader walks into it.

Migration guides are among the hardest technical documents to write well, because the writer has the luxury of hindsight — they already know where the pits are — and the reader does not. The writer's job is to project their hindsight onto the reader's path, warning them at the points where the warnings matter, not earlier and not later.

## Required structure

A migration guide opens by naming the migration precisely: from what version to what version, for which audience, under which conditions. The reader needs to know within the first few sentences whether this guide applies to them.

Immediately after the precise naming, the guide includes a "do this migration if" section and a "do not do this migration if" section. The second section is the more important one and is almost always undervalued by writers who want their guide to be widely applicable. A migration guide that honestly describes the conditions under which the migration is a bad idea builds trust with the reader, because the reader can tell that the writer is looking out for them rather than trying to sell the migration.

The "do not do this migration if" section names specific conditions: dependency versions that are incompatible, operational patterns that do not carry across, feature usage that is not supported on the new side, or team situations where the migration effort exceeds the benefit. Each condition is specific enough that the reader can check it against their own situation. "Don't migrate if you have complex custom code" is not specific; "Don't migrate if your code imports from `com.old.framework.internal.*`, which is not a public API and has no equivalent on the new side" is specific.

The overview section describes the migration at a high level, typically as a sequence of phases. For each phase, the overview names what will be done, roughly how long it will take, and whether it can be done incrementally or requires a full cutover. The phase structure helps the reader plan the work and, critically, helps them understand which phases are reversible and which are not.

The detailed steps section walks through the migration phase by phase. Each phase has its own subsection that covers the specific commands to run, the specific files to change, the specific configurations to update, and the verification steps to confirm the phase completed successfully. The level of detail is high — a migration guide is not the place to hand-wave.

The pit list section is the load-bearing contribution of a migration guide. It catalogs the specific places where the migration commonly goes wrong, with enough detail that a reader encountering one of the pits can recognize what happened and fix it. Each pit is described with its symptom (what the reader will see), its cause (why it happens), and its fix (what the reader should do). The pits are ordered by the phase in which they occur, so a reader hitting a problem in phase two can go straight to the phase-two pit list.

The rollback plan section describes how to undo the migration if it fails. Every migration guide has a rollback plan — the ones that do not are the ones whose writers never had to roll back, which is either a sign of unusual luck or a sign that the writer has not deployed the migration to production. A rollback plan that is missing is a red flag; a rollback plan that says "just revert the deployment" is usually also a red flag, because non-trivial migrations involve schema changes, data migrations, or configuration changes that cannot be rolled back by reverting code alone.

The verification section describes how the reader knows the migration succeeded. This is separate from the per-phase verification steps because it covers the whole-system checks — the things the reader should test after all phases are done, before declaring the migration complete. Examples include running the full test suite against the migrated code, running smoke tests against staging, and checking that the key business metrics in production still look normal for at least a day after cutover.

## Voice discipline

Migration Field Guide voice has a few rules that apply strictly.

First, imperative mood. The writer is telling the reader what to do: "run this command, update this file, restart the service". Not "we will run this command", not "you should consider running this command", but the direct imperative. The imperative mood is what makes the guide feel like a guide rather than a description.

Second, the pits are specific. A pit described as "you may encounter issues with custom configurations" is not a pit, it is a hedge. A real pit reads like: "If your `application.yml` contains a `spring.security.oauth2.client.registration.custom-provider` block, the migration will silently drop it, because Spring Boot 3 changed the location to `spring.security.oauth2.client.registration[custom-provider]`. You will notice this only when your login flow stops working after the migration. The fix is to update the configuration key to the new bracket syntax before running the migration."

Third, honesty about scope. A migration guide should not pretend to cover every possible situation. Strong migration guides are explicit about what they cover and what they do not: "This guide covers migrations of standard Spring Boot 2.7 applications using Maven; it does not cover Gradle builds, and it does not cover applications that use Spring Security's legacy XML configuration." The scope statement lets readers who fall outside the scope go looking for a different guide instead of following an inappropriate one.

## Length

Migration guides are usually long. A guide for a non-trivial migration — moving from Spring Boot 2 to Spring Boot 3, migrating from a legacy ORM to a modern one, upgrading across a major database version — is routinely several thousand words. The length is driven by the need for specificity: every step has to be explicit, every pit has to be described in detail, and the rollback plan has to cover the non-obvious cases.

A migration guide that feels too short is usually one whose writer has glossed over the hard parts. The hard parts are where the migration actually fails, and glossing over them produces a guide that is useless exactly when the reader needs it.

## Gates specific to migration guides

The first gate checks for the "do not do this migration if" section. Verify that it exists and that it names specific conditions rather than generic warnings. A guide without this section has assumed that every reader should migrate, which is almost never true.

The second gate checks the pit list for specificity. Each pit should describe a concrete symptom, a specific cause, and an actionable fix. Pits that are vague ("watch out for issues with dependencies") do not count; replace them with specific pits or remove them.

The third gate checks the rollback plan. Verify that it exists, that it covers the non-obvious cases like schema changes and data migrations, and that it is concrete enough to follow under stress. A rollback plan that will only be readable by a calm reader is a plan that will fail, because the reader who needs it will not be calm.

The fourth gate checks the verification steps. Each phase should have verification steps that let the reader confirm the phase succeeded before moving to the next phase. A guide that defers all verification to the end is a guide that will let the reader walk deep into a broken state before noticing.

The fifth gate checks the scope statement. Verify that the guide is explicit about what it covers and what it does not. A guide that implicitly claims to cover everything is a guide that will mislead readers in unusual situations.

## Common failure patterns

The **happy-path failure** produces a guide that walks through the migration as if everything will go smoothly. The writer forgot to include the pits, or could not remember them, or did not want to make the guide look harder than the writer's own experience. The reader follows the guide, hits a pit, and discovers that the guide is silent on what to do next. The fix is to add the pit list from memory, from the writer's own notes, and from discussions with other people who have done the same migration.

The **missing rollback plan** failure produces a guide that assumes the migration will succeed. When the migration fails — and sometimes it does — the reader is stranded without a way back. The fix is discipline: every migration guide has a rollback plan, and the rollback plan is tested by walking through it mentally and asking "if I had to do this at 3am while production was down, would I succeed?"

The **scope creep** failure produces a guide that tries to cover every variant of every migration path. The guide becomes too long to follow, too general to be specific about any variant, and the reader cannot tell which parts apply to their situation. The fix is to narrow the scope — write separate guides for separate variants, or be explicit about which variant the guide covers.

The **stale guide** failure is specific to migration guides and particularly painful. The guide was written for a version of the target system that no longer exists, and the commands or configurations no longer work. Migration guides decay faster than other kinds of technical documentation because they are version-specific by nature. The fix is to version-tag the guide clearly at the top ("This guide covers migration from Spring Boot 2.7.x to Spring Boot 3.2.x"), and to mark the guide as obsolete when the target version changes significantly.

The **marketing tone** failure produces a guide that reads like a sales pitch for the new technology. Phrases like "modernize your stack", "unlock new capabilities", or "take advantage of the latest features" creep in, and the reader senses that the guide is trying to persuade rather than inform. The fix is to cut the marketing language and let the migration stand on its technical merits. A reader reading a migration guide has already decided to consider the migration, and further persuasion is counterproductive.