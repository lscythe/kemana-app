# Contributing to Kemana

Thank you for contributing. Keep changes focused, tested and easy to review.

## Before you start

1. Search existing issues and pull requests.
2. For a new feature or an architectural change, open an issue first so the approach can be agreed.
3. Run `mise install`. [mise](https://mise.jdx.dev) installs every pinned tool (JDK, hk, kempt, Python, pkl, taplo, yamlfmt) from `mise.toml` and then installs the git hooks (`hk install --mise`), so there is nothing else to set up. The Gradle version is pinned by the wrapper, and the Android SDK is installed separately.

## Git hooks

| Hook | Runs |
|---|---|
| `pre-commit` | kempt formatting, final newline, trailing whitespace, merge conflict markers, taplo for TOML and yamlfmt for YAML, on staged files only |
| `commit-msg` | the Conventional Commits check in `.github/scripts/commit_scope.py` |
| `pre-push` | `mise run check` and `mise run test` |

Run `mise run format` to apply the formatters by hand, and `hk fix --all` to apply every pre-commit fixer to the whole repository.

## Branch flow

```text
feature/*, fix/*  ->  develop  ->  release/*  ->  main
hotfix/*          ->  main
```

| Branch | Created from | Merged into | Merge method |
|---|---|---|---|
| `feature/*` | `develop` | `develop` | Squash |
| `fix/*` | `develop` | `develop` | Squash |
| `release/*` | `develop` | `main`, then back into `develop` | Merge commit into `main` |
| `hotfix/*` | `main` | `main`, then back into `develop` | Merge commit into `main` |

`develop` and `main` are protected: changes go through pull requests, and force pushes and deletions are blocked. Merged branches are deleted automatically.

## Commit messages

Commits follow [Conventional Commits](https://www.conventionalcommits.org) and are checked by the `commit-msg` hook:

```text
type(scope): summary
```

- **Types:** `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, `revert`. Add `!` after the scope for a breaking change.
- **Scope:** a Gradle module path such as `shared` or `androidApp`, or one of the areas `build`, `build-logic`, `ci`, `deps`, `tooling`, `docs`, `release`. The scope is optional for `ci` and `docs`. Modules are read from `settings.gradle.kts`, so a new module becomes a valid scope as soon as it is included.
- **Summary:** imperative, starts with a lowercase letter, no trailing period. The whole header is at most 72 characters.

Examples:

```text
feat(shared): add greeting screen
fix(androidApp): keep the activity edge to edge
docs: describe the release flow
```

## Pull requests

- Use the pull request template.
- The pull request title must be a valid commit header: it becomes the squash commit on `develop`.
- One pull request is one complete change: logic, wiring and tests together. Keep unrelated refactors out.
- Explain architectural changes in the pull request description.
- Resolve all review conversations before merging.

## Code style

- Kotlin is formatted by kempt (ktfmt, Kotlin style) on commit. Run `mise run format` to format manually.
- Prefer clear names and small functions over comments. Comment only on a non-obvious reason.
- Write tests first.

## Local verification

```sh
mise run check
mise run test
mise run build
```

With Xcode and an iOS simulator runtime installed, also run `mise run test-ios` and `mise run build-ios`.

The `pre-push` hook runs `mise run check` and `mise run test`. On every pull request CI runs:

- **Android**: `mise run check`, `mise run test`, `mise run build` and Kover coverage uploaded to Codecov
- **CodeQL** for Kotlin and Java, and **Dependency review** for new dependencies

The Android job must pass before a pull request can merge. A pull request that only changes Markdown files or `docs/` skips the build jobs; the skipped Android job still satisfies the required check.

## Secrets

Never commit signing keys, tokens or personal data. Anything private belongs in `local.properties` or CI secrets.
