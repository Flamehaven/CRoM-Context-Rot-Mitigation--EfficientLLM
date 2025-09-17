# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-09-17
### Fixed
- **Critical SyntaxError** in `SafeCrossEncoderManager.get_status_for_response` method
  - Separated docstring and return statement that were incorrectly on the same line
  - Resolves import failures preventing `crom_efficientllm.cross_encoder` module loading
- **FastAPI Server ImportError** for `enhanced_greedy_pack` function
  - Implemented lazy loading with `importlib` to resolve circular import dependency
  - Fixed module structure allowing `enhanced_greedy_pack` to be properly exported from `budget_packer` package
  - Resolves FastAPI server startup failures

### Improved
- Enhanced error handling and import resilience across core modules
- Better module architecture preventing circular dependency issues
- Improved debugging output for Cross-Encoder initialization failures

### Testing
- All core module imports now function correctly
- FastAPI server starts without import errors
- Cross-encoder manager operates with proper error handling

## [1.0.1] - 2025-09-06
### Added
- Implemented core modules from scratch based on design documents.
- Implemented FastAPI server with `/process` endpoint (`src/crom_efficientllm/server.py`).
- Added `enhanced_greedy_pack` with detailed statistics for budget packing (`src/crom_efficientllm/budget_packer.py`).
- Implemented `SafeCrossEncoderManager` for robust and observable Cross-Encoder handling (`src/crom_efficientllm/cross_encoder.py`).
- Added `ExplainCapsuleLogger` for structured JSONL logging of all processing events (`src/crom_efficientllm/capsule_logger.py`).

### Changed
- Major version bump to reflect the first functional implementation of core logic.


## [0.2.1] - 2025-09-02
### Added
- CLI `--save-plots` option for `sweep` and `dp-curve`; saves PNG charts to `benchmarks/out/` (or `--out-dir`).
- README Quick Examples mention of plotting flag.
- This CHANGELOG.

### Changed
- Dev tooling: recommend `matplotlib` via dev extra for plotting.

## [0.2.0] - 2025-09-02
### Added
- GitHub Actions CI (3.9–3.12), pre-commit(ruff/black).
- `crom-bench` CLI: `e2e`, `sweep`, `scale`, `dp-curve`, `haystack-compare`.
- Plugins: FlashRank/LLMLingua/Evidently (optional extras).
- Example corpus & queries (JSONL).

## [0.1.0] - 2025-09-02
- Initial packaging; budget packer, hybrid rerank, drift estimator, demo & metrics.
