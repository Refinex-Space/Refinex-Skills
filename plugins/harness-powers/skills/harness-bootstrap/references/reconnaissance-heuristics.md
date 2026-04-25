# Reconnaissance Heuristics

Detection matrix for Phase 1 of harness-bootstrap. Use these patterns to identify the repository's tech stack, build system, test framework, and operational conventions.

## Language & Framework Detection

| Indicator File | Language | Framework / Ecosystem | Build Command (typical) |
|----------------|----------|----------------------|------------------------|
| `package.json` | JavaScript / TypeScript | Node.js | `npm run build` or `yarn build` or `pnpm build` |
| `tsconfig.json` | TypeScript | — | `tsc` or `npx tsc` |
| `next.config.*` | TypeScript / JavaScript | Next.js | `npm run build` → `next build` |
| `nuxt.config.*` | TypeScript / JavaScript | Nuxt | `npm run build` → `nuxt build` |
| `vite.config.*` | TypeScript / JavaScript | Vite | `npm run build` → `vite build` |
| `angular.json` | TypeScript | Angular | `ng build` |
| `pom.xml` | Java | Maven | `mvn clean install` or `./mvnw clean install` |
| `build.gradle` / `build.gradle.kts` | Java / Kotlin | Gradle | `./gradlew build` |
| `Cargo.toml` | Rust | Cargo | `cargo build` |
| `go.mod` | Go | Go modules | `go build ./...` |
| `pyproject.toml` | Python | Modern Python | `pip install -e .` or `poetry install` or `uv sync` |
| `setup.py` / `setup.cfg` | Python | Setuptools | `pip install -e .` |
| `requirements.txt` | Python | pip | `pip install -r requirements.txt` |
| `Gemfile` | Ruby | Bundler | `bundle install` |
| `*.csproj` / `*.sln` | C# | .NET | `dotnet build` |
| `mix.exs` | Elixir | Mix | `mix compile` |
| `build.zig` | Zig | Zig | `zig build` |
| `CMakeLists.txt` | C / C++ | CMake | `cmake --build .` |
| `Makefile` | Various | Make | `make` |
| `composer.json` | PHP | Composer | `composer install` |
| `pubspec.yaml` | Dart | Dart / Flutter | `dart compile` or `flutter build` |
| `Package.swift` | Swift | Swift PM | `swift build` |

## Package Manager Detection

| Lock File | Package Manager | Install Command |
|-----------|----------------|-----------------|
| `package-lock.json` | npm | `npm install` or `npm ci` |
| `yarn.lock` | Yarn | `yarn install` or `yarn` |
| `pnpm-lock.yaml` | pnpm | `pnpm install` |
| `bun.lockb` / `bun.lock` | Bun | `bun install` |
| `Cargo.lock` | Cargo | `cargo build` (auto) |
| `go.sum` | Go modules | `go mod download` |
| `poetry.lock` | Poetry | `poetry install` |
| `uv.lock` | uv | `uv sync` |
| `Pipfile.lock` | Pipenv | `pipenv install` |
| `Gemfile.lock` | Bundler | `bundle install` |
| `composer.lock` | Composer | `composer install` |

## Test Framework Detection

| Indicator | Test Framework | Run Command |
|-----------|---------------|-------------|
| `jest.config.*` or `"jest"` in package.json | Jest | `npm test` or `npx jest` |
| `vitest.config.*` or `"vitest"` in package.json | Vitest | `npm test` or `npx vitest` |
| `cypress.config.*` | Cypress | `npx cypress run` |
| `playwright.config.*` | Playwright | `npx playwright test` |
| `src/test/` (Java) | JUnit | `./gradlew test` or `mvn test` |
| `*_test.go` files | Go testing | `go test ./...` |
| `tests/` or `test/` (Python) + `pytest.ini` / `pyproject.toml[tool.pytest]` | pytest | `pytest` |
| `tests/` (Python) + `unittest` imports | unittest | `python -m unittest discover` |
| `spec/` (Ruby) | RSpec | `bundle exec rspec` |
| `_test.rs` files or `tests/` (Rust) | Rust test | `cargo test` |
| `*_test.exs` files | ExUnit | `mix test` |
| `**/*.test.ts` or `**/*.spec.ts` | Various (check config) | Check package.json scripts |

## Linter & Formatter Detection

| Indicator | Tool | Run Command |
|-----------|------|-------------|
| `.eslintrc.*` / `eslint.config.*` | ESLint | `npx eslint .` |
| `.prettierrc*` / `prettier.config.*` | Prettier | `npx prettier --check .` |
| `biome.json` / `biome.jsonc` | Biome | `npx biome check .` |
| `ruff.toml` / `[tool.ruff]` in pyproject.toml | Ruff | `ruff check .` |
| `.flake8` / `[flake8]` in setup.cfg | Flake8 | `flake8 .` |
| `mypy.ini` / `[mypy]` in pyproject.toml | mypy | `mypy .` |
| `checkstyle.xml` | Checkstyle | (integrated in Gradle/Maven) |
| `spotless` in build.gradle | Spotless | `./gradlew spotlessCheck` |
| `.golangci.yml` | golangci-lint | `golangci-lint run` |
| `clippy` in Cargo config | Clippy | `cargo clippy` |
| `rustfmt.toml` | rustfmt | `cargo fmt --check` |
| `.rubocop.yml` | RuboCop | `bundle exec rubocop` |

## CI System Detection

| Indicator | CI System | Config Location |
|-----------|-----------|-----------------|
| `.github/workflows/` | GitHub Actions | `.github/workflows/*.yml` |
| `.gitlab-ci.yml` | GitLab CI | `.gitlab-ci.yml` |
| `Jenkinsfile` | Jenkins | `Jenkinsfile` |
| `.circleci/config.yml` | CircleCI | `.circleci/config.yml` |
| `.travis.yml` | Travis CI | `.travis.yml` |
| `azure-pipelines.yml` | Azure DevOps | `azure-pipelines.yml` |
| `bitbucket-pipelines.yml` | Bitbucket Pipelines | `bitbucket-pipelines.yml` |
| `.buildkite/pipeline.yml` | Buildkite | `.buildkite/pipeline.yml` |

Read the CI configuration to extract:
- Build steps and their commands
- Test steps and their commands
- Lint/check steps
- Environment variables and required secrets (names only, not values)
- Deploy targets (staging, production)

## Monorepo Detection

A repository is likely a monorepo if:

1. It has a `workspaces` field in root `package.json`
2. It has a `pnpm-workspace.yaml` file
3. It has a `lerna.json` file
4. It has multiple `package.json` / `pom.xml` / `Cargo.toml` / `go.mod` files in subdirectories
5. It has a `packages/`, `apps/`, or `modules/` directory with multiple sub-projects
6. It uses Nx (`nx.json`) or Turborepo (`turbo.json`)

For monorepos, the reconnaissance should:
- List all packages/modules with their names and paths
- Identify shared/common packages vs application packages
- Map inter-package dependencies
- Note which packages have their own test suites

## Container & Infrastructure Detection

| Indicator | Technology |
|-----------|-----------|
| `Dockerfile` | Docker |
| `docker-compose.yml` / `docker-compose.yaml` / `compose.yml` | Docker Compose |
| `k8s/` or `kubernetes/` or `*.k8s.yml` | Kubernetes |
| `terraform/` or `*.tf` | Terraform |
| `serverless.yml` | Serverless Framework |
| `cdk.json` | AWS CDK |
| `pulumi.*` | Pulumi |
| `fly.toml` | Fly.io |
| `vercel.json` | Vercel |
| `netlify.toml` | Netlify |
| `railway.json` / `railway.toml` | Railway |

## Heuristic Priority

When multiple indicators exist, prioritize in this order:

1. **Lock files** for package manager (most reliable)
2. **CI configuration** for build/test commands (captures actual workflow)
3. **Framework config files** for framework identification
4. **Root build files** for language identification
5. **Directory conventions** as fallback

When the CI config specifies different commands from what the build file implies, prefer the CI config — it represents the team's actual workflow.
