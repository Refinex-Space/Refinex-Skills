# Doctype: API reference documentation

API reference documentation describes an API for developers who will consume it. The reader is almost always in a specific mode: they are writing code right now, they have a specific question, and they need an accurate answer in under a minute. Reference documentation is evaluated by how quickly and reliably it can answer that kind of question.

The canonical voice for API reference is Reference Librarian. Every endpoint is described in the same shape, every field is listed with the same schema, every error is documented in the same place. The reader comes to trust the document precisely because it never surprises them with a missing section or a different layout.

## Reference is not tutorial, and not explanation

The Diátaxis framework is particularly useful for API documentation, because it distinguishes the three kinds of writing that API docs are commonly confused with. A tutorial teaches a new user how to accomplish a first meaningful task. A how-to guide helps a user accomplish a specific task they already know they need. Reference material describes the API exhaustively and neutrally. Explanation material describes the design philosophy and the reasons for choices.

These four kinds of writing should not be blended in the same document. A reference that is also a tutorial is worse at both; a reference that is also an explanation is worse at both. The strong move is to write the reference as reference, and link out to separate tutorials, how-to guides, and explanation pieces for readers who need them. Stripe's and Twilio's docs both exemplify this separation — the reference is reference, and the tutorials are elsewhere, and each is allowed to be good at its own job.

## Required structure

API reference documentation has a rigid structure, and the rigidity is a feature. Each endpoint follows the same layout, so readers can find the information they need without reading the prose.

Every endpoint has a heading that names the HTTP verb and the path, followed by a one-sentence description of what the endpoint does. The one-sentence description is written in neutral prose and begins with a verb: "Creates a new customer record", "Retrieves the current state of a subscription", "Cancels a pending invoice and refunds any captured charges". The description is not a selling point; it is a statement of fact.

Every endpoint has an Authentication section that describes the credentials required. If authentication is the same across the whole API, the section can refer to a central authentication document rather than repeating the details, but the reference should never be silent about authentication — the reader should be able to find the answer without guessing.

Every endpoint has a Parameters section that lists each parameter the endpoint accepts. For each parameter, the reference names the parameter, its type, whether it is required or optional, its default value if optional, and a short description of what it means. The format is identical across every endpoint in the API, so a reader who has read one endpoint's Parameters section knows exactly where to look in every other endpoint.

Every endpoint has a Request Body section if the endpoint accepts a body, describing the expected structure. The structure is shown in schema form, not as English prose — a developer can read a schema faster than they can read a paragraph describing the same structure, and the schema is less ambiguous.

Every endpoint has a Response section that describes the shape of the successful response. Again, shown in schema form. Every field in the response is listed with its type and a short description.

Every endpoint has an Errors section that enumerates the possible error responses, with the status code, the error code if the API uses structured error codes, and a short description of when this error occurs. The errors section is exhaustive — not "these are some errors you might see" but "these are the errors this endpoint can return". A developer trying to handle errors needs a complete list, not a sample.

Every endpoint has a working example, shown as both a request and the corresponding response. The example is concrete, with real-looking values, and it is verified to work against the current version of the API. Examples that are silently broken are worse than no examples at all, because they mislead readers into building broken clients.

## Voice discipline

Reference Librarian voice has a few rules that are particularly strict for API documentation.

First, no opinions. The reference does not tell the reader whether to use an endpoint, whether the endpoint is recommended for new code, or whether an older endpoint is preferred over a newer one. If those opinions are relevant, they belong in a separate explanation document, or in a clearly marked callout inside the reference. The reference proper is neutral.

Second, no tutorial voice. Phrases like "let's create a customer", "now we will send a request", or "you should see" do not belong in reference. The reader is not following along; the reader is looking something up. The prose is declarative and third-person: "The request creates a customer with the specified fields. The response contains the created customer's ID and the server-assigned timestamp."

Third, absolute consistency. Every endpoint uses the same heading structure, the same parameter table format, the same error listing format, and the same example format. The consistency is what makes the reference fast to scan. A reference that uses different layouts for different endpoints forces the reader to re-learn the document for each new endpoint, which is exactly the opposite of what reference material should do.

## The working example rule

Every endpoint has at least one working example. The example shows a real HTTP request and the real response the API would return for that request. Both are verified against the current version of the API before publication.

Working examples are the single highest-value element of API reference documentation. Developers use them to bootstrap their own code, and a developer who can copy a working example is a developer who can ship faster than one who has to synthesize a request from a parameter table. The cost of maintaining working examples is real — they have to be updated when the API changes — but the alternative is examples that silently drift out of sync with the API, which is worse than no examples at all.

## Length

API reference documentation is long in the aggregate but short per endpoint. A single endpoint's reference is usually one to two screens. If it is longer, the endpoint probably needs to be split into multiple endpoints, or the reference has absorbed explanation material that belongs elsewhere.

## Gates specific to API reference

The first gate checks consistency across endpoints. Pick three or four endpoints at random from the reference and compare their layouts. If the layouts differ — if one has a Parameters section and another has a "Request Fields" section, or if one has an Errors section and another does not — the reference has a consistency problem that will degrade the reader experience.

The second gate checks error exhaustiveness. For each endpoint, verify that the Errors section lists every error the endpoint can return, not a selection of common ones. A developer handling errors needs the complete list; an incomplete list produces clients that crash in production when they encounter an undocumented error.

The third gate checks working examples. For each endpoint, verify that at least one request-and-response example is present, and that the example reflects the current API. Stale examples are a trap; delete or update them.

The fourth gate checks for tutorial drift. Scan the prose for phrases like "let's", "now we will", "you can see", or "next, we send". Each hit is a sign that the reference has drifted into tutorial voice and should be rewritten in declarative form.

The fifth gate checks for opinion drift. Scan for words like "recommended", "preferred", "best practice", "you should". Each hit is a candidate for relocation — if the opinion is valuable, it belongs in a separate explanation document or an explicitly marked callout, not mixed into the reference.

The sixth gate checks that authentication, rate limits, versioning, and other cross-cutting concerns are documented somewhere the reader can find them. A reference that covers individual endpoints but is silent on how to authenticate is missing critical information.

## Common failure patterns

The **reference-that-is-also-a-tutorial** failure produces a document that tries to teach new users while serving as a reference. The result is worse at both jobs: new users get lost in the reference detail, and experienced developers have to wade through tutorial prose to find the information they need. The fix is separation — write a separate getting-started tutorial and a separate reference, and link between them.

The **incomplete error documentation** failure produces a reference that lists a few common errors and ignores the rest. Developers build clients that break when they encounter undocumented errors in production, and they lose trust in the reference. The fix is to enumerate all errors, not just the common ones.

The **stale examples** failure produces examples that no longer match the current API. A developer copies the example, finds it does not work, and has to reverse-engineer the correct request from the parameter table. The fix is to treat example maintenance as a first-class part of API documentation, not an afterthought.

The **inconsistent layout** failure produces a reference where different endpoints use different section structures, making the document hard to scan. The fix is to pick one layout and apply it mechanically to every endpoint, even if some endpoints have empty sections as a result.

The **missing cross-cutting concerns** failure produces a reference that covers individual endpoints but is silent on authentication, rate limits, versioning, pagination conventions, and error formats. Developers have to hunt for this information, and when they cannot find it they guess, and their guesses are sometimes wrong. The fix is a top-level document that covers these concerns once and links from every endpoint.