---
language: en
license: apache-2.0
library_name: crom-efficientllm
tags:
- rag
- llm
- retrieval
- rerank
- reranker
- context-management
- prompt-engineering
- observability
- python
---
# CRoM-Context-Rot-Mitigation--EfficientLLM: Context Reranking and Management for Efficient LLMs

<p align="left">
  <a href="https://github.com/Flamehaven/CRoM-Context-Rot-Mitigation--EfficientLLM/actions">
    <img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Flamehaven/CRoM-Context-Rot-Mitigation--EfficientLLM/ci.yml?branch=main" />
  </a>
  <a href="#-benchmarks">
    <img alt="Bench" src="https://img.shields.io/badge/benchmarks-ready-success" />
  </a>
  <a href="LICENSE">
    <img alt="License" src="https://img.shields.io/badge/license-Apache%202.0-blue" />
  </a>
  <a href="https://github.com/Flamehaven/CRoM-Context-Rot-Mitigation--EfficientLLM/releases">
    <img alt="Release" src="https://img.shields.io/github/v/release/Flamehaven/CRoM-Context-Rot-Mitigation--EfficientLLM?display_name=tag" />
  </a>
  <a href="CHANGELOG.md">
    <img alt="Versioning" src="https://img.shields.io/badge/semver-1.0.2-green" />
  </a>
  <a href="https://github.com/Flamehaven/CRoM-Context-Rot-Mitigation--EfficientLLM/releases/latest">
    <img alt="Wheel" src="https://img.shields.io/badge/wheel-available-success" />
  </a>
</p>

**CRoM (Context Rot Mitigation)-EfficientLLM** is a Python toolkit designed to optimize the context provided to Large Language Models (LLMs). It provides a suite of tools to intelligently select, re-rank, and manage text chunks to fit within a model\'s context budget while maximizing relevance and minimizing performance drift.

This project is ideal for developers building RAG (Retrieval-Augmented Generation) pipelines who need to make the most of limited context windows.

## Key Features

*   **Budget Packer:** Greedily packs the highest-scoring text chunks into a defined token budget using a stable sorting algorithm.
*   **Hybrid Reranker:** Combines sparse (TF-IDF) and dense (Sentence-Transformers) retrieval scores for robust and high-quality reranking of documents.
*   **Drift Estimator:** Monitors the semantic drift between sequential model responses using L2 or cosine distance with EWMA smoothing.
*   **Observability:** Exposes Prometheus metrics for monitoring token savings and drift alerts in production.
*   **Extensible Plugins:** Supports optional plugins for advanced reranking (`FlashRank`), compression (`LLMLingua`), and drift analysis (`Evidently`).
*   **Comprehensive Benchmarking:** Includes a CLI for end-to-end pipeline evaluation, budget sweeps, and quality-vs-optimal analysis.

## Installation

Install the package directly from source using pip. For development, it\'s recommended to install in editable mode with the `[dev]` extras.

```bash
# Clone the repository
git clone https://github.com/Flamehaven/CRoM-Context-Rot-Mitigation--EfficientLLM.git
cd CRoM-Context-Rot-Mitigation--EfficientLLM

# Install in editable mode with development and plugin dependencies
pip install -e .[dev,plugins]
```

## Quickstart

### 🚀 Interactive Demo

Try CRoM live in your browser without any installation:

**[🎯 Try CRoM Demo on Hugging Face Spaces](https://huggingface.co/spaces/Flamehaven/crom-demo)**

The interactive demo lets you:
- Experiment with budget packing algorithms
- Visualize context drift detection
- See real-time performance metrics
- Adjust token budgets and see immediate results

### Local Demo

Run a simple, self-contained demonstration of the core components:

```bash
# Run the demo script
crom-demo demo
```

### CLI Benchmarking Examples

The package includes a powerful `crom-bench` CLI for evaluation.

```bash
# Default E2E (Search→Rerank→Pack→Mock LLM)
crom-bench e2e --budget 0.3

# Optional: High-precision configuration with plugins
crom-bench e2e --budget 0.3 \
  --use-flashrank --flashrank-model ms-marco-TinyBERT-L-2-v2 \
  --use-llmlingua --compress-ratio=0.6 \
  --use-evidently
```

### Plotting

If `matplotlib` is installed (`pip install -e .[dev]`), you can save benchmark plots directly:

```bash
# Save budget sweep result plots
crom-bench sweep --save-plots

# Save DP-curve plots
crom-bench dp-curve --save-plots
```

## Release & Changelog

This project follows semantic versioning. For detailed changes, see the [**CHANGELOG.md**](CHANGELOG.md).

Releases are automated via GitHub Actions when a `v*` tag is pushed.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.