# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Changed test to just test for sbml generation (not Matlab generation).

## [0.2.0] - 2022-06-21

### Added

- Add `CHANGELOG.md`.
- Add a `Makefile` to streamline using `poetry`.
- The `NOTICE` file is included in the build.
- Add test for exporting from onemodel into matlab.
- Add `noxfile.py`.

### Changed

- The subpackage `sbml2dae` is removed from the source code of `onemodel` and it is now installed from its repository.

### Removed

- Removed `MANIFEST.in` and `setup.py`, we use poetry instead.

## [0.1.0] - 2022-06-14

### Changed

- Use `poetry` for managing the project.

[unreleased]: https://github.com/sb2cl/onemodel/compare/v0.2.0...develop
[0.2.0]: https://github.com/sb2cl/onemodel/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/sb2cl/onemodel/releases/tag/v0.1.0
