# Doctype: Technical blog post

A technical blog post is a public-facing argument aimed at engineers outside the writer's own team. The reader has found the piece through search, a newsletter, or a link from a peer. The reader is giving the piece about 60 seconds to prove it is worth reading. That time budget shapes everything.

## Core constraint — one central idea

A blog post covers exactly one central idea. Not two. Not "three related ideas loosely connected". One. The test: can you state the idea in a single sentence that would fit in a tweet? If not, the post is trying to do too much and must be narrowed or split.

The one-idea constraint is what lets a blog post be strong. A post that covers one thing in depth teaches the reader something they did not know before. A post that covers three things shallowly teaches nothing, because the reader has a vague sense that some things were discussed but cannot name any of them a week later.

## Required structure

Blog posts have more structural freedom than ADRs or design docs, but the following elements must all be present, in roughly this order:

1. **Title that carries the argument.** Not "Exploring Spring AI's ChatClient" but "Spring AI's ChatClient is clean until you turn on streaming tool-call — then AdvisorChain breaks in four specific ways".

2. **Hook (opening paragraph, 3–6 sentences).** The hook has one job: convince a reader who gives you 60 seconds to give you the next 60 seconds. The hook works by committing to something specific and surprising. Strong hooks open with a concrete symptom, a counter-intuitive claim, or a misconception the writer is about to correct. Weak hooks open with history, definition, or restating the question.

3. **Stake-setting (who should read this, why it matters, what you will claim).** One paragraph, immediately after the hook. The reader learns whether they are the intended audience and what they will get if they keep reading. This is the blog-post equivalent of the design doc's "goals / non-goals" section and serves the same purpose: honest scope-setting.

4. **Body.** The body proves the claim from the hook. Its structure depends on the voice — a Production War Story body will be chronological, a Design Tribunal body will be criterion-by-criterion, a Mechanism Autopsy body will follow the call chain. Whatever the structure, every section in the body exists to advance the central claim; sections that do not advance the claim are cut.

5. **Concrete ending move.** The last paragraph is not a summary. It is one of four moves (pick one, not several):
   - **A mental model** — "here is the picture you should carry away, so you can predict behavior of similar systems."
   - **A structural lesson** — "here is what we would do differently, and what generalizes beyond this specific case."
   - **An open question** — "here is what I still do not know, and what experiment would settle it." Only use this one if the question is a real open question, not a disguised "thanks for reading".
   - **A concrete recommendation** — "if you are in situation X, do Y; if you are in situation Z, do not."

The ending must do one of these four. A summary is not an option — summaries tell the reader that the middle taught nothing.

## Voice fit

Blog posts accept any voice except Reference Librarian. The most common voices, by document type:

| Post type                           | Typical voice                  |
|-------------------------------------|--------------------------------|
| Post-mortem / incident write-up     | Production War Story           |
| "We chose X over Y" / decision post | Design Tribunal                |
| Source code / internals deep-dive   | Mechanism Autopsy              |
| "How we migrated from X to Y"       | Migration Field Guide          |
| "Is X faster than Y" benchmark post | Benchmarker's Notebook         |

Mixing voices in a single blog post is the most common failure mode for experienced writers (it is how a Design Tribunal post turns into a Mechanism Autopsy halfway through, when the writer gets interested in the internals). If you notice this happening mid-draft, either restart in the other voice or cut the section that drifted. Do not publish a two-voice post.

## Length

There is no minimum. There is a practical maximum of about 3000 words for a single blog post; beyond that, the reader's attention falls off a cliff, and the piece should either be split or republished as a whitepaper.

The right length is "exactly long enough to prove the central claim, and no longer". Strong posts are often 1200–2000 words. Posts that feel like they are reaching for length almost always benefit from aggressive cutting.

## Gates specific to blog posts (run in addition to the main checklist)

- [ ] **One-central-idea test.** Can the central idea be stated in a single tweet-length sentence? If not, the post is trying to do too much.
- [ ] **Hook test.** If you read only the first paragraph, do you know what the post will claim and why you should care? If not, rewrite the hook.
- [ ] **30-second test.** A reader who skims only the title, hook, and section headings should still know what the post's argument is. Do the headings carry meaning, or are they generic ("Introduction", "Background", "Conclusion")? Generic headings fail the test.
- [ ] **Ending move test.** Does the last paragraph do one of the four moves? If it is a summary, rewrite it.
- [ ] **Senior-engineer test, per section.** Every section teaches something the target reader could not get from the official docs in five minutes. If a section fails this test, deepen it or delete it.
- [ ] **No marketing vocabulary.** Search for "powerful", "elegant", "seamless", "robust", "cutting-edge". Every hit is a candidate for deletion.

## Specific failure patterns unique to blog posts

**The "I'll fix it in the conclusion" pattern.** The writer knows the post is rambling but hopes to pull it together at the end. It never works. The conclusion cannot do the work the body failed to do. Fix: the body must stand on its own; the conclusion is a payoff, not a rescue.

**The "look how much I know" pattern.** The post describes every related detail the writer remembers, not because each detail advances the argument but because the writer wants credit for knowing them. Every detail not in service of the central claim is padding. Cut.

**The "SEO keyword dressing" pattern.** The post has been written with search ranking in mind, which shows up as unnatural keyword repetition and lists of loosely related terms. Technical readers bounce from posts that feel SEO-optimized. Write for the reader, not the crawler.

**The "imaginary audience" pattern.** The post is written for "developers who want to learn about X", which is not an audience, it is a stock phrase. Real audiences are specific: "backend engineers who are already using Spring Boot 3 and are considering whether to add Spring AI for a customer-facing chat feature". The specific audience enables specific examples; the stock audience forces generic examples.