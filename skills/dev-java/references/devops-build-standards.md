# DevOps and Build Standards

> **Scope**: Maven/Gradle conventions, multi-module project structure, dependency management (BOM, version catalogs), Docker image optimization, CI/CD pipeline stages, environment configuration, health checks.

## Table of Contents

1. Maven Conventions
2. Gradle Conventions
3. Multi-Module Project Structure
4. Dependency Management
5. Docker Image Optimization
6. CI/CD Pipeline Standards
7. Environment Configuration

---

## 1. Maven Conventions

Use Maven Wrapper (`mvnw`) in every project. Commit the `.mvn/wrapper/` directory to version control. This ensures all developers and CI pipelines use the same Maven version regardless of local installation.

**POM structure**: Inherit from `spring-boot-starter-parent` (for Spring Boot projects) or use `spring-boot-dependencies` BOM as a dependency import. Define all property versions in a `<properties>` block. Group dependencies logically with XML comments.

```xml
<properties>
    <java.version>21</java.version>
    <mapstruct.version>1.5.5.Final</mapstruct.version>
    <springdoc.version>2.3.0</springdoc.version>
</properties>
```

**Plugin configuration**: Configure `maven-compiler-plugin` to use the project's Java version. Configure `maven-surefire-plugin` for unit tests and `maven-failsafe-plugin` for integration tests (tests ending in `IT`). Use `maven-enforcer-plugin` to enforce minimum Maven/Java versions and ban duplicate dependencies.

**Repository policy**: Use only the central Maven repository and your company's internal Nexus/Artifactory. Never add public snapshot repositories. Pin all dependency versions — no version ranges, no `LATEST`, no `RELEASE`.

---

## 2. Gradle Conventions

Use Gradle Wrapper (`gradlew`). Commit the `gradle/wrapper/` directory. Use Kotlin DSL (`build.gradle.kts`) over Groovy DSL (`build.gradle`) for new projects — Kotlin DSL provides type safety and IDE auto-completion.

Use the `java-library` plugin for library modules and the `application` plugin for executable modules. Configure source compatibility and target compatibility to the project's Java version.

Use `implementation` for dependencies needed at compile and runtime. Use `api` (in library modules only) for dependencies that are part of the module's public API. Use `testImplementation` for test-only dependencies. Never use the deprecated `compile` and `testCompile` configurations.

---

## 3. Multi-Module Project Structure

For projects with shared code or multiple deployment units, use a multi-module build.

```
project-root/
├── pom.xml                          # Parent POM (packaging: pom)
├── project-common/                  # Shared utilities, DTOs, constants
│   └── pom.xml
├── project-api/                     # API interfaces, shared contracts
│   └── pom.xml
├── project-service/                 # Business logic (Spring Boot application)
│   └── pom.xml
├── project-web/                     # Web layer (optional, if separated from service)
│   └── pom.xml
└── project-infrastructure/          # External integrations (DB, MQ, external APIs)
    └── pom.xml
```

**For microservices**, each service is its own top-level project with its own build. Shared code is published as a library artifact to the internal Maven repository — not shared via multi-module builds across services. This prevents coupling between services through shared build dependencies.

---

## 4. Dependency Management

**BOM (Bill of Materials)**: Use BOMs to manage dependency versions centrally. Spring Boot provides `spring-boot-dependencies`. For non-Spring libraries, create a project-level BOM or use `dependencyManagement` imports. In Gradle, use the `platform()` dependency type.

**Version catalogs (Gradle 7.0+)**: Define all dependency versions in `gradle/libs.versions.toml`. Reference them in build scripts as `libs.spring.boot.starter.web`. This centralizes version management and enables dependency update tools (Renovate, Dependabot) to find all versions in one file.

**Dependency hygiene**: Run `mvn dependency:analyze` (Maven) or `gradle dependencies` regularly to detect unused declared dependencies and used undeclared dependencies. Exclude transitive dependencies that conflict or are unnecessary. Use `<exclusions>` in Maven or `exclude` in Gradle.

**Vulnerability scanning**: Integrate OWASP Dependency Check (`dependency-check-maven` plugin) or Snyk into the CI pipeline. Fail the build on critical/high severity vulnerabilities. Update vulnerable dependencies within the sprint.

---

## 5. Docker Image Optimization

Use multi-stage builds to keep the final image small. The build stage compiles the application; the runtime stage copies only the JAR and runs it.

```dockerfile
# Build stage
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app
COPY . .
RUN ./mvnw package -DskipTests -Dmaven.javadoc.skip=true

# Runtime stage
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar

# Non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Layered JARs** (Spring Boot 2.3+): Use `java -Djarmode=layertools -jar app.jar extract` to split the JAR into layers (dependencies, snapshot-dependencies, spring-boot-loader, application). Copy each layer separately in the Dockerfile — Docker caches unchanged layers, dramatically speeding up builds when only application code changes.

**Base image selection**: Use Eclipse Temurin (Adoptium) as the JDK/JRE distribution. Use `-alpine` variants for smaller images. Use `-jre` (not `-jdk`) for runtime images — JDK adds ~200MB of unnecessary tools.

**JVM configuration in containers**: Set `-XX:MaxRAMPercentage=75.0` instead of fixed `-Xmx` to let the JVM auto-size based on the container's memory limit. Set `-XX:+UseContainerSupport` (enabled by default since JDK 10) to ensure the JVM reads cgroup limits correctly.

---

## 6. CI/CD Pipeline Standards

A standard CI/CD pipeline for Java projects has these stages:

**Stage 1 — Compile**: `mvn compile` or `gradle compileJava`. Fast feedback on syntax errors.

**Stage 2 — Unit Test**: `mvn test` or `gradle test`. Run all unit tests. Fail fast on test failures.

**Stage 3 — Static Analysis**: Run SonarQube analysis, Checkstyle, SpotBugs, OWASP Dependency Check. Quality gates must pass. New code must meet the project's coverage threshold.

**Stage 4 — Integration Test**: `mvn verify` or `gradle integrationTest`. Run with Testcontainers for database and message broker tests. This stage requires Docker.

**Stage 5 — Build Artifact**: `mvn package` or `gradle bootJar`. Build the Docker image with the application. Tag with the Git commit hash and semantic version.

**Stage 6 — Deploy to Staging**: Deploy the Docker image to the staging environment. Run smoke tests (health check, critical path).

**Stage 7 — Deploy to Production**: Manual approval gate. Blue-green or canary deployment. Monitor error rates for 15 minutes post-deployment. Rollback automatically if error rate exceeds threshold.

Fail the pipeline early — do not proceed to integration tests if unit tests fail. Do not build a Docker image if static analysis fails.

---

## 7. Environment Configuration

Follow the twelve-factor app methodology for configuration. Store environment-specific configuration in the environment, not in the code.

**Configuration hierarchy (highest priority wins)**: Command-line arguments → environment variables → `application-{profile}.yml` → `application.yml` → default values in `@ConfigurationProperties`.

**Profiles**: Use `dev` for local development (embedded database, debug logging, mock external services). Use `test` for CI tests (Testcontainers, test data). Use `staging` for pre-production (real infrastructure, synthetic data). Use `prod` for production (real infrastructure, real data, minimal logging).

Never include production credentials in any profile file. Production secrets come exclusively from environment variables or a secrets manager.

**Health checks**: Every deployable service must expose health endpoints. For Kubernetes: `/actuator/health/liveness` (am I alive?) and `/actuator/health/readiness` (can I accept traffic?). Include custom health indicators for critical dependencies (database, cache, message broker, external APIs). A service that cannot reach its database should report "not ready" — the load balancer removes it from rotation until the connection recovers.