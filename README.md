# Kemana

[![CI](https://github.com/lscythe/kemana-app/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/lscythe/kemana-app/actions/workflows/ci.yml)
[![CodeQL](https://github.com/lscythe/kemana-app/actions/workflows/codeql.yml/badge.svg?branch=develop)](https://github.com/lscythe/kemana-app/actions/workflows/codeql.yml)
[![codecov](https://codecov.io/gh/lscythe/kemana-app/branch/develop/graph/badge.svg)](https://codecov.io/gh/lscythe/kemana-app)
[![License](https://img.shields.io/github/license/lscythe/kemana-app)](LICENSE)

Kemana is a public transport companion app built with Kotlin and Compose Multiplatform for Android and iOS.

> Kemana is in early development. The project currently contains the multiplatform skeleton and repository tooling only.

## Layout

```text
shared/     Compose Multiplatform UI and logic for Android and iOS
androidApp/ Android application host
iosApp/     iOS application host (Xcode project)
```

## Requirements

- [mise](https://mise.jdx.dev): `mise install` provides the pinned JDK and the other tools listed in `mise.toml`, and installs the git hooks
- Android SDK; point Gradle at it with a `local.properties` file containing `sdk.dir=/path/to/sdk`
- Xcode, for the iOS targets

## Build and test

```sh
mise run check      # YAML and TOML lint, Android lint
mise run test       # Python script tests and Android host unit tests
mise run build      # Debug APK
./gradlew koverXmlReport   # Coverage report
```

With Xcode and an iOS simulator runtime installed:

```sh
mise run test-ios
mise run build-ios
```

You can also open `iosApp/iosApp.xcodeproj` in Xcode and run the `iosApp` scheme.

See [CONTRIBUTING](.github/CONTRIBUTING.md) for the branch flow and commit rules.

## License

Kemana is licensed under the [Apache License 2.0](LICENSE).
