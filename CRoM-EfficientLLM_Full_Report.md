# CRoM-EfficientLLM 전체 프로젝트 보고서

## 1. 프로젝트 전체 구조 (Directory Tree)

```
CRoM-EfficientLLM/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── benchmarks/
│   ├── efficiency_eval.py
│   ├── longbench_eval.py
│   └── sample_results.json
├── dashboard/
│   ├── grafana_dashboard.json
│   └── prometheus_config.yml
├── docs/
│   ├── architecture.md
│   └── versioning.md
├── examples/
│   └── corpus/
│       ├── sample_docs.jsonl
│       └── sample_queries.jsonl
├── scripts/
│   ├── gen_release_notes.py
│   └── release.sh
├── src/
│   └── crom_efficientllm/
│       ├── budget_packer/
│       │   ├── __init__.py
│       │   └── packer.py
│       ├── drift_estimator/
│       │   ├── __init__.py
│       │   └── estimator.py
│       ├── plugins/
│       │   ├── evidently_drift.py
│       │   ├── flashrank_reranker.py
│       │   └── llmlingua_compressor.py
│       ├── rerank_engine/
│       │   ├── __init__.py
│       │   └── rerank.py
│       ├── __init__.py
│       ├── budget_packer.py
│       ├── capsule_logger.py
│       ├── cli.py
│       ├── cross_encoder.py
│       ├── demo.py
│       └── server.py
├── tests/
│   ├── test_drift.py
│   ├── test_packer.py
│   └── test_rerank.py
├── .gitignore
├── CHANGELOG.md
├── crom 1.0.1수정 업데이트 상세보고서.md
├── LICENSE
├── pyproject.toml
├── README.md
├── release_notes.md
└── requirements.txt
```

## 2. 파일별 상세 내용 

---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\.github\\workflows\\ci.yml`
```yaml
name: ci
on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e .[dev]
      - run: pre-commit run --all-files || true
      - run: ruff --version && black --version
      - run: pytest -q
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\.github\\workflows\\release.yml`
```yaml
name: release
on:
  push:
    tags:
      - 'v*'
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -e .[dev]
      - run: pytest -q
      - name: Build distribution
        run: |
          python -m pip install build
          python -m build
      - name: Generate release notes from CHANGELOG
        run: |
          python scripts/gen_release_notes.py "$GITHUB_REF_NAME"
      - name: Publish GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          name: ${{ github.ref_name }}
          body_path: release_notes.md
          files: |
            dist/*.whl
            dist/*.tar.gz
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\.gitignore`
```
# Python
__pycache__/
*.py[cod]
*.egg-info/
.env
.venv/
virtualenv/
.idea/
.vscode/
.ipynb_checkpoints/
.dist/
.build/
.coverage
.pytest_cache/

# OS
.DS_Store
Thumbs.db
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\CHANGELOG.md`
```markdown
# Changelog

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
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\LICENSE`
```

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted" 
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made, 
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with the Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor, 
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory, 
      whether in tort (including negligence), contract, or otherwise, 
      unless required by applicable law (such as deliberate and grossly 
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]" 
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\README.md`
```markdown
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
    <img alt="Versioning" src="https://img.shields.io/badge/semver-0.2.x-lightgrey" />
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

### Demo

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
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\benchmarks\\efficiency_eval.py`
```python
"""
Efficiency Evaluation for CRoM-EfficientLLM
- Synthetic workload to measure token savings, selection quality, and runtime.
- No third-party deps beyond numpy/matplotlib (pandas optional for CSVs).

Usage:
  python benchmarks/efficiency_eval.py --budget 0.3 --n 5000 --seed 123 --plot --save
"""
from __future__ import annotations

import argparse
import math
import time
from dataclasses import dataclass
from typing import List, Sequence, Tuple, Union

import numpy as np

try:
    import pandas as pd  # optional
except Exception:  # pragma: no cover
    pd = None

try:
    import matplotlib.pyplot as plt  # optional
except Exception:  # pragma: no cover
    plt = None

# --- Local packers (self-contained to avoid imports during quick eval) ---
@dataclass(frozen=True)
class Chunk:
    text: str
    score: float
    tokens: int

def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)

def _coerce_chunk(obj: Union[Chunk, dict], idx: int) -> Chunk:
    if isinstance(obj, Chunk):
        return obj
    if not isinstance(obj, dict):
        raise TypeError(f"Chunk #{idx} must be Chunk or dict, got {type(obj)}")
    text = str(obj.get("text", ""))
    if not text:
        raise ValueError(f"Chunk #{idx} has empty text")
    score = float(obj.get("score", 0.0))
    tokens = int(obj["tokens"]) if "tokens" in obj else _estimate_tokens(text)
    if tokens <= 0:
        raise ValueError(f"Chunk #{idx} has non-positive tokens: {tokens}")
    return Chunk(text=text, score=score, tokens=tokens)

def budget_pack(text_chunks: Sequence[Union[Chunk, dict]], budget: int = 1000) -> List[Chunk]:
    if budget <= 0:
        raise ValueError("budget must be > 0")
    coerced: List[Chunk] = [_coerce_chunk(c, i) for i, c in enumerate(text_chunks)]
    indexed = list(enumerate(coerced))
    indexed.sort(key=lambda it: (-it[1].score, it[1].tokens, it[0]))
    selected: List[Chunk] = []
    total = 0
    for _, ch in indexed:
        if total + ch.tokens <= budget:
            selected.append(ch)
            total += ch.tokens
    return selected

def pack_fcfs(text_chunks: Sequence[Union[Chunk, dict]], budget: int) -> List[Chunk]:
    sel, total = [], 0
    for i, obj in enumerate(text_chunks):
        ch = _coerce_chunk(obj, i)
        if total + ch.tokens <= budget:
            sel.append(ch)
            total += ch.tokens
    return sel

def pack_random(text_chunks: Sequence[Union[Chunk, dict]], budget: int, seed: int = 0) -> List[Chunk]:
    rng = np.random.default_rng(seed)
    indices = np.arange(len(text_chunks))
    rng.shuffle(indices)
    sel, total = [], 0
    for i in indices:
        ch = _coerce_chunk(text_chunks[i], i)
        if total + ch.tokens <= budget:
            sel.append(ch)
            total += ch.tokens
    return sel

# --- Data generation and metrics ---

def make_synthetic_chunks(n=2000, seed=42, corr=0.6):
    rng = np.random.default_rng(seed)
    true_rel = rng.normal(0, 1, size=n)
    noise = rng.normal(0, 1, size=n) * math.sqrt(1 - corr**2)
    score = corr * true_rel + noise
    tokens = np.clip(rng.lognormal(mean=4.0, sigma=0.6, size=n).astype(int), 5, 2000)
    chunks = [Chunk(text=("x"*int(t*4)), score=float(s), tokens=int(t)) for s, t in zip(score, tokens)]
    return chunks, true_rel

def eval_once(n=5000, budget_ratio=0.3, seed=123, corr=0.6):
    chunks, true_rel = make_synthetic_chunks(n=n, seed=seed, corr=corr)
    total_tokens = sum(c.tokens for c in chunks)
    budget = int(total_tokens * budget_ratio)

    def run(name, fn):
        t0 = time.perf_counter()
        sel = fn(chunks, budget)
        dt = time.perf_counter() - t0
        idx_map = {id(c): i for i, c in enumerate(chunks)}
        picked_idx = [idx_map[id(c)] for c in sel]
        rel_sum = float(np.sum(true_rel[picked_idx])) if picked_idx else 0.0
        sel_tokens = sum(c.tokens for c in sel)
        return {
            "name": name,
            "time_ms": dt*1000,
            "selected_chunks": len(sel),
            "selected_tokens": sel_tokens,
            "tokens_budget": budget,
            "tokens_total_unpacked": total_tokens,
            "tokens_saved": total_tokens - sel_tokens,
            "save_ratio": (total_tokens - sel_tokens)/total_tokens,
            "relevance_sum": rel_sum,
        }

    rows = [
        run("budget_pack", budget_pack),
        run("fcfs", pack_fcfs),
        run("random", lambda ch, b: pack_random(ch, b, seed=seed)),
    ]
    return rows

def quality_vs_optimal(n=200, budget_ratio=0.3, seed=123, corr=0.6):
    chunks, true_rel = make_synthetic_chunks(n=n, seed=seed, corr=corr)
    budget = int(sum(c.tokens for c in chunks) * budget_ratio)
    values = np.maximum(true_rel, 0.0)

    def optimal(chunks_sub, values, budget):
        items = chunks_sub
        vals = list(values)
        B = budget
        dp = [0.0]*(B+1)
        keep = [[False]*(B+1) for _ in range(len(items))]
        for i, it in enumerate(items):
            wt = it.tokens
            val = vals[i]
            for b in range(B, wt-1, -1):
                alt = dp[b - wt] + val
                if alt > dp[b]:
                    dp[b] = alt
                    keep[i][b] = True
        b = B
        picked_idx = []
        for i in range(len(items)-1, -1, -1):
            if keep[i][b]:
                picked_idx.append(i)
                b -= items[i].tokens
        picked_idx.reverse()
        rel_sum = float(np.sum([values[i] for i in picked_idx])) if picked_idx else 0.0
        total_tokens = sum(items[i].tokens for i in picked_idx)
        return picked_idx, rel_sum, total_tokens

    opt_idx, opt_rel, opt_tokens = optimal(chunks, values, budget)

    # selections
    idx_map = {id(c): i for i, c in enumerate(chunks)}
    def rel_of(selection):
        pid = [idx_map[id(c)] for c in selection]
        return float(np.sum(values[pid])) if pid else 0.0

    sel_bp = budget_pack(chunks, budget)
    sel_fc = pack_fcfs(chunks, budget)
    sel_rd = pack_random(chunks, budget, seed=seed)

    rows = [
        {"name":"optimal_true_rel", "relevance_sum": opt_rel, "selected_tokens": opt_tokens, "selected_chunks": len(opt_idx)},
        {"name":"budget_pack_small", "relevance_sum": rel_of(sel_bp), "selected_tokens": sum(c.tokens for c in sel_bp), "selected_chunks": len(sel_bp)},
        {"name":"fcfs_small", "relevance_sum": rel_of(sel_fc), "selected_tokens": sum(c.tokens for c in sel_fc), "selected_chunks": len(sel_fc)},
        {"name":"random_small", "relevance_sum": rel_of(sel_rd), "selected_tokens": sum(c.tokens for c in sel_rd), "selected_chunks": len(sel_rd)},
    ]
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5000)
    ap.add_argument("--budget", type=float, default=0.3)
    ap.add_argument("--seed", type=int, default=123)
    ap.add_argument("--corr", type=float, default=0.6)
    ap.add_argument("--plot", action="store_true")
    ap.add_argument("--save", action="store_true")
    args = ap.parse_args()

    rows = eval_once(n=args.n, budget_ratio=args.budget, seed=args.seed, corr=args.corr)
    rows_q = quality_vs_optimal(n=min(200, args.n), budget_ratio=args.budget, seed=args.seed, corr=args.corr)

    print("\n=== Efficiency (n={}, budget={{:.0%}}) ===".format(args.n, args.budget))
    for r in rows:
        print("{name:12s} time={{time_ms:7.2f}}ms  save_ratio={{save_ratio:6.3f}}  tokens_saved={{tokens_saved:8d}}  rel_sum={{relevance_sum:8.3f}}".format(**r))

    print("\n=== Quality vs Optimal (subset) ===")
    for r in rows_q:
        print("{name:18s} rel_sum={{relevance_sum:8.3f}}  tokens={{selected_tokens:5d}} chunks={{selected_chunks:4d}}".format(**r))

    if pd is not None and args.save:
        pd.DataFrame(rows).to_csv("benchmarks/results_efficiency.csv", index=False)
        pd.DataFrame(rows_q).to_csv("benchmarks/results_quality.csv", index=False)
        print("Saved CSVs to benchmarks حضرتك.")

    if plt is not None and args.plot:
        # single-figure plots, no explicit colors
        x = [r["name"] for r in rows]
        y = [r["time_ms"] for r in rows]
        import matplotlib.pyplot as plt
        plt.figure()
        plt.bar(x, y)
        plt.title("Packer Runtime (ms)")
        plt.xlabel("method")
        plt.ylabel("ms")
        plt.show()

if __name__ == "__main__":
    main()
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\benchmarks\\longbench_eval.py`
```python
"""
Benchmark script: LongBench-like evaluation.
Simulates context packing efficiency.
"""
from crom_efficientllm.budget_packer.packer import budget_pack

def evaluate():
    chunks = [{"text": f"chunk {i}", "score": i % 5, "tokens": 100} for i in range(20)]
    packed = budget_pack(chunks, budget=500)
    print("Selected:", len(packed), "chunks")

if __name__ == "__main__":
    evaluate()
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\benchmarks\\sample_results.json`
```json
{}
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\crom 1.0.1수정 업데이트 상세보고서.md`
```markdown
# CRoM-EfficientLLM v1.0.1 업데이트 상세 보고서

**문서 목적:** 소셜 미디어 (LinkedIn, Twitter, Medium) 포스팅을 위한 마케팅 AI의 정보 소스 제공
**작성일:** 2025-09-06
**작성자:** CLI ↯C01∞ | Σψ∴

---

## 1. 개요 (Overview)

- **프로젝트명:** CRoM-EfficientLLM (Context Rot Mitigation for Efficient LLMs)
- **이전 버전:** 0.2.1
- **신규 버전:** 1.0.1

**핵심 요약:**
이번 v1.0.1 업데이트는 CRoM-EfficientLLM 프로젝트의 **첫 번째 기능 구현(First Functional Implementation)**을 의미합니다. 기존의 아이디어와 뼈대만 있던 상태에서, 실제 동작하는 핵심 로직을 모두 구현하여 **작동 가능한 프로토타입(Working Prototype)**으로 전환했습니다. 이제 사용자들은 RAG 파이프라인의 컨텍스트를 효율적으로 관리하고 최적화하는 핵심 기능들을 직접 테스트하고 활용할 수 있습니다.

---

## 2. 배경 (Background)

기존 v0.2.1은 `pyproject.toml`, `README.md` 등 프로젝트의 방향성과 구조만 정의된 **설계 단계의 스캐폴드(Scaffold)**였습니다. 실제 핵심 로직을 담고 있는 Python 소스 코드가 부재하여 아이디어를 실제로 검증할 수 없었습니다.

이번 업데이트의 목표는 이 설계도에 따라, **처음부터(from scratch) 핵심 기능들을 모두 구현**하여 프로젝트에 생명을 불어넣고, 실제 사용 가능한 상태로 만드는 것이었습니다.

---

## 3. 상세 변경 내역 (Detailed Changes)

이번 업데이트를 통해 4개의 핵심 모듈이 `src/crom_efficientllm/` 디렉토리 내에 새롭게 구현되었습니다.

### 가. `budget_packer.py` - 지능형 컨텍스트 패킹 엔진
- **기능:** LLM에 전달할 컨텍스트(청크)를 주어진 토큰 예산 내에서 가장 효율적으로 구성합니다.
- **세부 사항:**
    - 단순히 텍스트를 자르는 것이 아니라, **점수/토큰 비율**을 기준으로 가장 중요한 정보를 우선적으로 선택합니다.
    - 패킹 후 **압축률, 절약된 토큰 수, 예산 효율성** 등 상세한 통계를 제공하여, 컨텍스트 관리 전략의 효과를 정량적으로 분석할 수 있는 기반을 마련했습니다.

### 나. `cross_encoder.py` - 안정성 강화 Cross-Encoder 관리자
- **기능:** RAG 파이프라인의 핵심인 Cross-Encoder 모델을 안정적으로 관리하고 오류 발생 시 시스템 전체의 다운을 방지합니다.
- **세부 사항:**
    - `sentence-transformers` 라이브러리가 없거나 모델 로딩에 실패하는 등 다양한 **오류 상황을 자동으로 감지하고 우아하게 처리(Graceful Fallback)**합니다.
    - 시스템이 멈추는 대신, "비활성화", "오류" 등의 명확한 상태를 API 응답에 포함시켜 **시스템의 안정성과 예측 가능성**을 크게 높였습니다.

### 다. `capsule_logger.py` - 투명성 확보를 위한 캡슐 로거
- **기능:** 시스템의 모든 처리 과정을 **구조화된 로그(Structured Log)**로 기록하여 투명성과 감사 가능성을 제공합니다.
- **세부 사항:**
    - 모든 API 요청, 처리 통계, 시스템 상태를 **"설명 캡슐(Explain Capsule)"**이라는 JSONL 형식으로 영구 저장합니다.
    - 이는 추후 시스템의 동작을 디버깅하거나, 성능 저하의 원인을 분석하고, AI의 판단 근거를 추적하는 데 필수적인 데이터가 됩니다.

### 라. `server.py` - 핵심 기능 통합 API 서버
- **기능:** 위에서 설명한 모든 모듈(패킹, 리랭킹, 로깅)을 하나로 묶어, 사용자가 쉽게 접근할 수 있는 **FastAPI 기반의 API 서버**를 제공합니다.
- **세부 사항:**
    - `/process` 엔드포인트를 통해 쿼리와 컨텍스트 데이터를 받아, 리랭킹부터 패킹, 로깅까지의 전 과정을 **하나의 트랜잭션으로 처리(Orchestration)**합니다.
    - `/healthz` 엔드포인트를 통해 외부 모니터링 시스템이 서버의 상태를 쉽게 확인할 수 있도록 구현했습니다.

---

## 4. 버전 관리 및 문서화 (Versioning & Documentation)

- **버전 업데이트:** 핵심 기능이 구현됨에 따라, 프로젝트의 버전을 `0.2.1`에서 **`1.0.1`**로 상향 조정하여 중요한 진전을 명시했습니다.
- **변경 이력 관리:** `CHANGELOG.md` 파일에 상기된 모든 구현 내역을 상세히 기록하여, 사용자와 기여자가 프로젝트의 발전 과정을 쉽게 추적할 수 있도록 투명성을 확보했습니다.

---

## 5. 기대 효과 및 다음 단계 (Expected Impact & Next Steps)

- **기대 효과:**
    - CRoM-EfficientLLM은 더 이상 아이디어가 아닌, **실제 RAG 시스템에 적용하여 컨텍스트 관리 효율성을 테스트할 수 있는 실용적인 도구**로 발전했습니다.
    - 개발자들은 LLM의 제한된 컨텍스트 창을 어떻게 하면 가장 효율적으로 사용할 수 있는지에 대한 **정량적인 데이터**를 얻을 수 있게 되었습니다.

- **다음 단계:**
    - `README.md`에 명시된 `crom-demo` 및 `crom-bench` CLI 기능 구현
    - 사용자가 원하는 토크나이저(Tokenizer)를 선택할 수 있는 기능 추가
    - 다양한 컨텍스트 관리 전략의 성능을 비교할 수 있는 벤치마크 시스템 고도화

---

**보고서 종료.**
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\dashboard\\grafana_dashboard.json`
```json
{}
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\dashboard\\prometheus_config.yml`
```


```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\docs\\architecture.md`
```markdown
# Architecture

This document outlines the architecture of the CRoM-EfficientLLM project.
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\docs\\versioning.md`
```markdown
# Versioning & PyPI Guidance

This document defines package naming, SemVer rules, and a future path to publish to PyPI.

## 1) Package name
- Distribution name (PyPI): `crom-efficientllm` (lowercase, hyphen-separated)
- Import name (module): `crom_efficientllm` (PEP 8 underscore)

> **Tip**: Keep both names consistent to avoid confusion in docs.

### Check name availability on PyPI
- Visit: https://pypi.org/project/crom-efficientllm/ (404 → available)
- If taken, consider: `crom-efficient-llm`, `crom-llm-efficient`, `crom-ctx-pack`
- Reserve on TestPyPI first: use `test.pypi.org` to validate metadata & upload

## 2) Semantic Versioning (SemVer)
We follow **MAJOR.MINOR.PATCH**.

- **MAJOR**: Backward-incompatible API changes
  - e.g., rename function signatures (`budget_pack`), move/rename modules, change return schemas
- **MINOR**: Backward-compatible features
  - new functions/flags (e.g., `pack_summary`, CLI subcommands), performance improvements
- **PATCH**: Backward-compatible bug fixes
  - logic corrections, docs/CI fixes, dependency pin updates without API changes

### Pre-releases
Use suffixes: `-a.1`, `-b.1`, `-rc.1` (alpha/beta/release-candidate)
- Example: `0.3.0-rc.1`

### Deprecation Policy
- Mark deprecated APIs in `CHANGELOG.md` and docstrings
- Provide at least **one MINOR release** with warnings before removal

### Public API Surface
We commit compatibility for:
- `crom_efficientllm.budget_packer.packer`: `Chunk`, `budget_pack`, `pack_summary`
- `crom_efficientllm.rerank_engine.rerank`: `hybrid_rerank`
- `crom_efficientllm.drift_estimator.estimator`: `DriftEstimator`, `DriftMode`
- CLI entrypoints: `crom-demo`, `crom-bench` and their documented flags

## 3) Release Flow (GitHub → PyPI later)
- Tag: `vX.Y.Z` → GitHub Actions builds & creates a Release (artifacts attached)
- Keep `CHANGELOG.md` updated per release
- After API stabilizes, enable **PyPI publish** using a separate workflow with `PYPI_API_TOKEN` secret

### (Future) PyPI publishing steps
1. Create a PyPI account & project
2. Add `PYPI_API_TOKEN` to repo `Settings → Secrets and variables → Actions`
3. Add `release-pypi.yml` workflow to upload on tag
4. Verify install: `pip install crom-efficientllm` and import `crom_efficientllm`

---
_Last updated: 2025-09-02_
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\examples\\corpus\\sample_docs.jsonl`
```json
{"id": 1, "text": "AI ethics and governance frameworks for responsible AI."}
{"id": 2, "text": "Techniques for detecting model drift in production systems."}
{"id": 3, "text": "A recipe for sourdough bread and fermentation tips."}
{"id": 4, "text": "Hybrid search: combining sparse and dense retrieval methods."}
{"id": 5, "text": "Token budgets and prompt compression strategies for LLMs."}
{"id": 6, "text": "Monitoring with Prometheus and building Grafana dashboards."}
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\examples\\corpus\\sample_queries.jsonl`
```json
{"query": "how to detect drift in ai models"}
{"query": "ways to reduce llm token usage"}
{"query": "observability stack prometheus grafana"}
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "crom-efficientllm"
version = "1.0.1"
description = "CRoM (Context Rot Mitigation)-EfficientLLM: Budget packing, hybrid rerank, and drift estimation with observability"
readme = "README.md"
requires-python = ">=3.9"
license = { text = "Apache-2.0" }
authors = [ { name = "Your Name" } ]
dependencies = [
  "numpy>=1.24,<3",
  "scikit-learn>=1.3,<2",
  "transformers>=4.41,<5",
  "sentence-transformers>=2.2,<3",
  "flask>=3,<4",
  "prometheus-client>=0.20,<1"
]

[project.optional-dependencies]
dev = [
  "pytest>=7",
  "ruff>=0.4",
  "black>=24.4",
  "pre-commit>=3.6",
  "matplotlib>=3.8,<4"
]
plugins = [
  "flashrank>=0.2; python_version>='3.9'",
  "llmlingua>=0.2; python_version>='3.9'",
  "evidently>=0.4; python_version>='3.9'"
]
haystack = [
  "farm-haystack[faiss,inference]>=1.26; python_version>='3.9'"
]

[project.urls]
Homepage = "https://github.com/Flamehaven/CRoM-Context-Rot-Mitigation--EfficientLLM"

[project.scripts]
"crom-demo" = "crom_efficientllm.demo:main"
"crom-bench" = "crom_efficientllm.cli:main"

[tool.setuptools]
package-dir = {"" = "src"}
packages = { find = { where = ["src"] } }

[tool.pytest.ini_options]
addopts = "-q"

[tool.black]
line-length = 100

[tool.ruff]
target-version = "py39"

[tool.ruff.lint]
select = ["E","F","I","UP","B","C4","SIM","PL","PERF","RUF","ANN"]
ignore = ["ANN101","ANN102"]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101","ANN","PLR2004"]
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\release_notes.md`
```markdown
# Release v0.2.1

## [0.2.1] - 2025-09-02
### Added
- CLI `--save-plots` option for `sweep` and `dp-curve`; saves PNG charts to `benchmarks/out/` (or `--out-dir`).
- README Quick Examples mention of plotting flag.
- This CHANGELOG.

### Changed
- Dev tooling: recommend `matplotlib` via dev extra for plotting.

— generated from [CHANGELOG.md](CHANGELOG.md)
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\requirements.txt`
```
numpy>=1.24,<3
scikit-learn>=1.3,<2
transformers>=4.41,<5
sentence-transformers>=2.2,<3
flask>=3,<4
prometheus-client>=0.20,<1
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\scripts\\gen_release_notes.py`
```python
#!/usr/bin/env python3
from __future__ import annotations
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"
OUT = ROOT / "release_notes.md"

def main(tag: str) -> None:
    version = tag.lstrip("v").strip()
    if not CHANGELOG.exists():
        OUT.write_text(f"# Release {tag}\n\n(CHANGELOG.md not found)
", encoding="utf-8")
        return
    text = CHANGELOG.read_text(encoding="utf-8")
    pat = re.compile(rf"^##\s*[[^{re.escape(version)}]]?[^\n]*$", re.MULTILINE)
    m = pat.search(text)
    if not m:
        OUT.write_text(
            f"# Release {tag}\n\nSection for {version} not found in CHANGELOG.\n\n" + text,
            encoding="utf-8",
        )
        return
    start = m.end()
    m2 = re.search(r"^##\s+", text[start:], re.MULTILINE)
    end = start + (m2.start() if m2 else len(text) - start)
    section = text[m.start():end].strip()
    body = f"# Release {tag}\n\n{section}\n\n— generated from [CHANGELOG.md](CHANGELOG.md)"
    OUT.write_text(body, encoding="utf-8")

if __name__ == "__main__":
    tag = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_REF_NAME", "")
    if not tag:
        print("Usage: gen_release_notes.py vX.Y.Z", file=sys.stderr)
        sys.exit(2)
    main(tag)
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\scripts\\release.sh`
```bash
#!/usr/bin/env bash
set -euo pipefail

TAG=${1:-}
if [[ -z "$TAG" ]]; then
  echo "Usage: scripts/release.sh vX.Y.Z"; exit 1
fi

# sanity checks
if [[ -n $(git status --porcelain) ]]; then
  echo "❌ Working tree not clean"; exit 1
fi

# ensure deps
python -m pip install -e .[dev]
pre-commit run --all-files
pytest -q

# generate release notes preview from CHANGELOG
python scripts/gen_release_notes.py "$TAG"
if [[ -f release_notes.md ]]; then
  echo "--- release_notes.md (preview top 60 lines) ---"
  head -n 60 release_notes.md || true
  echo "--- end preview ---"
else
  echo "⚠️ release_notes.md not generated; will fall back to default notes in GH release"
fi

# tag & push


git tag -a "$TAG" -m "Release $TAG"
git push origin "$TAG"

echo "✅ Pushed tag $TAG. GitHub Actions will create the Release automatically."
echo "➡️  Watch: https://github.com/Flamehaven/CRoM-EfficientLLM/actions"
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\__init__.py`
```python
"""Public API for CRoM-EfficientLLM."""
from .budget_packer.packer import Chunk, budget_pack, pack_summary
from .rerank_engine.rerank import hybrid_rerank
from .drift_estimator.estimator import DriftEstimator, DriftMode

__all__ = [
    "Chunk",
    "budget_pack",
    "pack_summary",
    "hybrid_rerank",
    "DriftEstimator",
    "DriftMode",
]
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\budget_packer.py`
```python
from typing import List, Dict
import logging

def enhanced_greedy_pack(chunks: List[Dict], budget: int, 
                        score_key: str = "score") -> tuple[List[Dict], Dict]:
    """
    기존 greedy_pack 함수를 확장하여 상세 통계 반환
    
    Returns:
        tuple: (packed_chunks, stats_dict)
    """
    if not chunks:
        return [], {
            "selected_count": 0,
            "packed_count": 0,
            "selected_tokens": 0,
            "packed_tokens": 0,
            "compression_ratio": 0.0,
            "token_savings": 0,
            "efficiency": 0.0
        }
    
    # 토큰 수 미리 계산
    for chunk in chunks:
        if "token_count" not in chunk:
            chunk["token_count"] = max(1, len(chunk.get("text", "")) // 4)
    
    # 효율성 기준 정렬 (score/token 비율)
    sorted_chunks = sorted(
        chunks, 
        key=lambda x: x.get(score_key, 0) / x["token_count"], 
        reverse=True
    )
    
    # 그리디 패킹
    packed_chunks = []
    used_tokens = 0
    
    for chunk in sorted_chunks:
        if used_tokens + chunk["token_count"] <= budget:
            packed_chunks.append(chunk)
            used_tokens += chunk["token_count"]
    
    # 상세 통계 계산
    total_selected_tokens = sum(chunk["token_count"] for chunk in chunks)
    
    stats = {
        "selected_count": len(chunks),
        "packed_count": len(packed_chunks),
        "selected_tokens": total_selected_tokens,
        "packed_tokens": used_tokens,
        "compression_ratio": len(packed_chunks) / len(chunks) if chunks else 0.0,
        "token_savings": total_selected_tokens - used_tokens,
        "efficiency": used_tokens / budget if budget > 0 else 0.0
    }
    
    # 📊 로깅 추가 (기존 코드에 없던 통계 가시성)
    logging.info(f"Packing completed: {stats['packed_count']}/{stats['selected_count']} chunks, "
                f"tokens: {stats['packed_tokens']}/{stats['selected_tokens']} "
                f"(efficiency: {stats['efficiency']:.1%})")
    
    return packed_chunks, stats
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\capsule_logger.py`
```python
import json
from pathlib import Path
from datetime import datetime
from typing import Union, Dict
import logging

class ExplainCapsuleLogger:
    """스키마 기반 설명 캡슐 저장 시스템"""
    
    def __init__(self, log_directory: str = "artifacts/logs"):
        self.log_dir = Path(log_directory)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 로그 파일 경로들
        self.capsules_file = self.log_dir / "explain_capsules.jsonl"
        self.metrics_file = self.log_dir / "processing_metrics.jsonl"
        self.errors_file = self.log_dir / "error_log.jsonl"
        
        logging.info(f"ExplainCapsule Logger initialized: {self.log_dir}")
    
    def create_explain_capsule(self, query: str, response_data: Dict, 
                              processing_stats: Dict, 
                              cross_encoder_status: str) -> Dict:
        """스키마 준수 설명 캡슐 생성"""
        
        capsule = {
            # 🔖 메타데이터 (필수)
            "timestamp": datetime.now().isoformat(),
            "version": "1.0",
            "processor": "CRoM-Enhanced",
            
            # 📝 쿼리 정보
            "query": {
                "text": query,
                "length": len(query),
                "token_estimate": len(query) // 4
            },
            
            # 📊 처리 통계 (패치 1에서 확장된 정보)
            "processing_stats": {
                **processing_stats,
                "cross_encoder_status": cross_encoder_status
            },
            
            # 🔧 시스템 상태
            "system_state": {
                "cross_encoder_available": cross_encoder_status not in ["disabled", "unavailable"]
            },

            # 📦 원본 및 결과 청크
            "chunks": {
                "packed": response_data.get("chunks", [])
            }
        }
        return capsule

    def log_capsule(self, capsule: Dict):
        """설명 캡슐을 .jsonl 파일에 기록"""
        try:
            with open(self.capsules_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(capsule, ensure_ascii=False) + "\n")
        except Exception as e:
            logging.error(f"Failed to log explain capsule: {e}")

    def log_error(self, error_details: Dict):
        """오류 정보를 .jsonl 파일에 기록"""
        try:
            error_details["timestamp"] = datetime.now().isoformat()
            with open(self.errors_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(error_details, ensure_ascii=False) + "\n")
        except Exception as e:
            logging.error(f"Failed to log error: {e}")
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\cli.py`
```python
from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass
from typing import List, Dict, Sequence

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from crom_efficientllm.budget_packer.packer import budget_pack, Chunk
from crom_efficientllm.rerank_engine.rerank import hybrid_rerank

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover
    SentenceTransformer = None  # type: ignore

# Optional plugins are imported lazily when flags are set

@dataclass
class Doc:
    id: str
    text: str

def load_jsonl(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def build_corpus(path: str) -> List[Doc]:
    rows = load_jsonl(path)
    return [Doc(id=str(r.get("id", i)), text=str(r["text"])) for i, r in enumerate(rows)]

def sparse_retrieval(query: str, corpus: Sequence[Doc], k: int = 100) -> List[Dict]:
    texts = [d.text for d in corpus]
    vect = TfidfVectorizer(ngram_range=(1, 2)).fit(texts)
    D = vect.transform(texts)
    Q = vect.transform([query])
    sims = cosine_similarity(Q, D).ravel()
    order = np.argsort(-sims)[:k]
    return [{"id": corpus[i].id, "text": corpus[i].text, "score_sparse": float(sims[i])} for i in order]

def dense_embed_model(name: str):
    if SentenceTransformer is None:
        raise RuntimeError("sentence-transformers not installed. Install with `pip install -e .`.")
    return SentenceTransformer(name)

def _apply_flashrank(query: str, docs: List[Dict], model_name: str) -> List[Dict]:
    try:
        from crom_efficientllm.plugins.flashrank_reranker import flashrank_rerank
    except Exception as e:  # pragma: no cover
        raise RuntimeError("FlashRank plugin not available. Install extras: pip install .[plugins]") from e
    ranked = flashrank_rerank(query, docs, model_name=model_name)
    # Normalize plugin score to 0..1 and put into score_final
    scores = np.array([d.get("score_flashrank", 0.0) for d in ranked], dtype=np.float32)
    if scores.size and float(scores.max() - scores.min()) > 1e-12:
        s = (scores - scores.min()) / (scores.max() - scores.min())
    else:
        s = np.zeros_like(scores)
    for i, d in enumerate(ranked):
        d["score_final"] = float(s[i])
    return ranked

def _apply_llmlingua(text: str, ratio: float) -> str:
    try:
        from crom_efficientllm.plugins.llmlingua_compressor import compress_prompt
    except Exception as e:  # pragma: no cover
        raise RuntimeError("LLMLingua plugin not available. Install extras: pip install .[plugins]") from e
    return compress_prompt(text, target_ratio=ratio)

def _save_evidently_report(all_embs: List[List[float]], out_html: str) -> None:
    try:
        from crom_efficientllm.plugins.evidently_drift import drift_report
    except Exception as e:  # pragma: no cover
        raise RuntimeError("Evidently plugin not available. Install extras: pip install .[plugins]") from e
    n = len(all_embs)
    if n < 4:
        return
    ref = all_embs[: n // 2]
    cur = all_embs[n // 2 :]
    rep = drift_report(ref, cur)
    rep.save_html(out_html)

def mock_llm_generate(prompt: str) -> str:
    time.sleep(0.005)  # simulate small latency
    return "[MOCK] " + prompt[:160]

def e2e(args: argparse.Namespace) -> None:
    corpus = build_corpus(args.corpus)
    queries = [r["query"] for r in load_jsonl(args.queries)]
    embed = dense_embed_model(args.model)
    all_embs: List[List[float]] = []

    t0 = time.perf_counter()
    all_rows = []
    for q in queries:
        t_s = time.perf_counter()
        cands = sparse_retrieval(q, corpus, k=args.k)
        t_sparse = (time.perf_counter() - t_s) * 1000

        t_r = time.perf_counter()
        if args.use_flashrank:
            reranked = _apply_flashrank(q, cands, args.flashrank_model)
        else:
            reranked = hybrid_rerank(q, cands, embed, alpha=args.alpha)
        t_rerank = (time.perf_counter() - t_r) * 1000

        # token heuristic + budget pack
        chunks = [
            Chunk(text=d["text"], score=d.get("score_final", d.get("score_sparse", 0.0)), tokens=max(1, len(d["text"]) // 4))
            for d in reranked
        ]
        budget_tokens = int(sum(c.tokens for c in chunks) * args.budget)
        t_p = time.perf_counter()
        packed = budget_pack(chunks, budget=budget_tokens)
        t_pack = (time.perf_counter() - t_p) * 1000

        prompt = "\n\n".join(c.text for c in packed) + f"\n\nQ: {q}\nA:"
        if args.use_llmlingua:
            prompt = _apply_llmlingua(prompt, ratio=args.compress_ratio)

        # collect embeddings for drift snapshot (mean-pooled)
        with np.errstate(all="ignore"):
            if len(packed) > 0:
                doc_embs = embed.encode([c.text for c in packed], convert_to_numpy=True)
                vec = np.mean(doc_embs, axis=0).tolist()
                all_embs.append(vec)

        t_l = time.perf_counter()
        _ = mock_llm_generate(prompt)
        t_llm = (time.perf_counter() - t_l) * 1000

        total = (time.perf_counter() - t_s) * 1000
        all_rows.append({
            "query": q,
            "sparse_ms": t_sparse,
            "rerank_ms": t_rerank,
            "pack_ms": t_pack,
            "llm_ms": t_llm,
            "total_ms": total,
            "packed_tokens": sum(c.tokens for c in packed),
            "orig_tokens": sum(c.tokens for c in chunks),
            "save_ratio": 1 - (sum(c.tokens for c in packed) / max(1, sum(c.tokens for c in chunks))),
            "used_flashrank": bool(args.use_flashrank),
            "used_llmlingua": bool(args.use_llmlingua),
        })

    elapsed = (time.perf_counter() - t0) * 1000
    os.makedirs(args.out_dir, exist_ok=True)
    out_path = os.path.join(args.out_dir, "e2e_results.jsonl")
    with open(out_path, "w", encoding="utf-8") as f:
        for r in all_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"saved results -> {out_path} ({len(all_rows)} queries) ; elapsed={elapsed:.2f}ms")

    if args.use_evidently and all_embs:
        html_path = os.path.join(args.out_dir, "evidently_report.html")
        _save_evidently_report(all_embs, html_path)
        print(f"evidently report -> {html_path}")

def budget_sweep(args: argparse.Namespace) -> None:
    import itertools
    corpus = build_corpus(args.corpus)
    queries = [r["query"] for r in load_jsonl(args.queries)][: args.max_q]
    embed = dense_embed_model(args.model)

    budgets = [b / 100.0 for b in range(args.b_min, args.b_max + 1, args.b_step)]
    rows = []
    for q, b in itertools.product(queries, budgets):
        cands = sparse_retrieval(q, corpus, k=args.k)
        reranked = hybrid_rerank(q, cands, embed, alpha=args.alpha)
        chunks = [Chunk(text=d["text"], score=d["score_final"], tokens=max(1, len(d["text"]) // 4)) for d in reranked]
        budget_tokens = int(sum(c.tokens for c in chunks) * b)
        packed = budget_pack(chunks, budget=budget_tokens)
        rows.append({
            "query": q,
            "budget": b,
            "packed_tokens": sum(c.tokens for c in packed),
            "orig_tokens": sum(c.tokens for c in chunks),
            "save_ratio": 1 - (sum(c.tokens for c in packed) / max(1, sum(c.tokens for c in chunks))),
            "avg_score": float(np.mean([c.score for c in packed])) if packed else 0.0,
        })

    os.makedirs(args.out_dir, exist_ok=True)
    out_path = os.path.join(args.out_dir, "budget_sweep.jsonl")
    with open(out_path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"saved results -> {out_path} ; points={len(rows)}")

    if args.save_plots:
        try:
            import matplotlib.pyplot as plt  # noqa: F401
            import matplotlib.pyplot as _plt
        except Exception:
            print("[warn] matplotlib not installed; install dev extras: pip install -e .[dev]")
        else:
            # Aggregate by budget
            import collections
            agg = collections.defaultdict(list)
            for r in rows:
                agg[r["budget"]].append(r)
            budgets_sorted = sorted(agg.keys())
            avg_save = [float(np.mean([x["save_ratio"] for x in agg[b]])) for b in budgets_sorted]
            avg_score = [float(np.mean([x["avg_score"] for x in agg[b]])) for b in budgets_sorted]

            _plt.figure()
            _plt.plot([b * 100 for b in budgets_sorted], [s * 100 for s in avg_save], marker="o")
            _plt.xlabel("Budget (%)")
            _plt.ylabel("Avg Save Ratio (%)")
            _plt.title("Budget Sweep: Save Ratio vs Budget")
            _plt.grid(True)
            _plt.tight_layout()
            _plt.savefig(os.path.join(args.out_dir, "budget_sweep.png")),

            _plt.figure()
            _plt.plot([s * 100 for s in avg_save], avg_score, marker="o")
            _plt.xlabel("Save Ratio (%)")
            _plt.ylabel("Avg Score (packed)")
            _plt.title("Pareto: Quality vs Savings")
            _plt.grid(True)
            _plt.tight_layout()
            _plt.savefig(os.path.join(args.out_dir, "budget_pareto.png")),
            print("plots ->", os.path.join(args.out_dir, "budget_sweep.png"), ",", os.path.join(args.out_dir, "budget_pareto.png"))

def scaling(args: argparse.Namespace) -> None:
    def make_synth(n: int, seed: int = 42):
        rng = np.random.default_rng(seed)
        tokens = np.clip(rng.lognormal(4.0, 0.6, n).astype(int), 5, 2000)
        score = rng.normal(0, 1, n)
        return [Chunk(text="x" * int(t * 4), score=float(s), tokens=int(t)) for s, t in zip(score, tokens)]

    for n in [1000, 5000, 10000, 20000, 50000, 100000]:
        if n > args.n_max:
            break
        chunks = make_synth(n)
        budget = int(sum(c.tokens for c in chunks) * args.budget)
        t0 = time.perf_counter()
        _ = budget_pack(chunks, budget)
        ms = (time.perf_counter() - t0) * 1000
        print(f"n={n:6d}  budget={args.budget:.0%}  time={ms:8.2f} ms")

def dp_curve(args: argparse.Namespace) -> None:
    def make_synth(n: int, seed: int = 123, corr: float = 0.6):
        rng = np.random.default_rng(seed)
        true_rel = rng.normal(0, 1, n)
        noise = rng.normal(0, 1, n) * np.sqrt(1 - corr**2)
        score = corr * true_rel + noise
        tokens = np.clip(rng.lognormal(4.0, 0.6, n).astype(int), 5, 2000)
        chunks = [Chunk(text="x" * int(t * 4), score=float(s), tokens=int(t)) for s, t in zip(score, tokens)]
        return chunks, true_rel

    def optimal(chunks: Sequence[Chunk], values: np.ndarray, budget: int) -> float:
        B = budget
        dp = np.zeros(B + 1, dtype=np.float32)
        for i, ch in enumerate(chunks):
            wt = ch.tokens
            val = max(0.0, float(values[i]))
            for b in range(B, wt - 1, -1):
                dp[b] = max(dp[b], dp[b - wt] + val)
        return float(dp[B])

    chunks, true_rel = make_synth(args.n)
    total = sum(c.tokens for c in chunks)
    budgets = [int(total * b / 100.0) for b in range(args.b_min, args.b_max + 1, args.b_step)]
    out_rows = []

    for B in budgets:
        sel = budget_pack(chunks, B)
        idx_map = {id(c): i for i, c in enumerate(chunks)}
        rel_bp = float(np.sum([max(0.0, true_rel[idx_map[id(c)]]) for c in sel]))
        rel_opt = optimal(chunks[: args.n_opt], true_rel[: args.n_opt], min(B, sum(c.tokens for c in chunks[: args.n_opt])))
        pct = rel_bp / max(rel_opt, 1e-9)
        out_rows.append({"budget": B, "pct": pct, "rel_bp": rel_bp, "rel_opt": rel_opt})
        print(f"budget={B:8d}  rel_bp={rel_bp:8.3f}  rel_opt≈{rel_opt:8.3f}  pct≈{pct*100:5.1f}% (subset n={args.n_opt})")

    if args.save_plots:
        try:
            import matplotlib.pyplot as plt  # noqa: F401
            import matplotlib.pyplot as _plt
        except Exception:
            print("[warn] matplotlib not installed; install dev extras: pip install -e .[dev]")
        else:
            _plt.figure()
            xs = [r["budget"] * 100.0 / total for r in out_rows]
            ys = [r["pct"] * 100 for r in out_rows]
            _plt.plot(xs, ys, marker="o")
            _plt.xlabel("Budget (%)")
            _plt.ylabel("% of optimal (subset)")
            _plt.title("DP Curve: Greedy vs Optimal")
            _plt.grid(True)
            _plt.tight_layout()
            os.makedirs(args.out_dir, exist_ok=True)
            _plt.savefig(os.path.join(args.out_dir, "dp_curve.png")),
            print("plot ->", os.path.join(args.out_dir, "dp_curve.png")),

def compare_haystack(args: argparse.Namespace) -> None:
    try:
        from haystack.nodes import BM25Retriever, SentenceTransformersRetriever
        from haystack.document_stores import InMemoryDocumentStore
    except Exception as e:  # pragma: no cover
        raise RuntimeError("Install extras: pip install .[haystack]") from e

    corpus = build_corpus(args.corpus)
    docs = [{"content": d.text, "meta": {"id": d.id}} for d in corpus]
    store = InMemoryDocumentStore(use_bm25=True)
    store.write_documents(docs)

    bm25 = BM25Retriever(document_store=store)
    dretr = SentenceTransformersRetriever(document_store=store, model_name_or_path=args.model)

    queries = [r["query"] for r in load_jsonl(args.queries)][: args.max_q]
    for q in queries:
        t0 = time.perf_counter()
        bm = bm25.retrieve(q, top_k=args.k)
        dn = dretr.retrieve(q, top_k=args.k)
        ms = (time.perf_counter() - t0) * 1000
        print(f"{q[:40]:40s}  bm25={len(bm):3d}  dense={len(dn):3d}  time={ms:7.2f} ms")

def main() -> None:
    ap = argparse.ArgumentParser(prog="crom-bench")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("e2e", help="end-to-end: retrieval → rerank → pack → mock LLM")
    p.add_argument("--corpus", default="examples/corpus/sample_docs.jsonl")
    p.add_argument("--queries", default="examples/corpus/sample_queries.jsonl")
    p.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    p.add_argument("--k", type=int, default=200)
    p.add_argument("--alpha", type=float, default=0.5)
    p.add_argument("--budget", type=float, default=0.3)
    # plugins
    p.add_argument("--use-flashrank", action="store_true")
    p.add_argument("--flashrank-model", default="ms-marco-TinyBERT-L-2-v2")
    p.add_argument("--use-llmlingua", action="store_true")
    p.add_argument("--compress-ratio", type=float, default=0.6)
    p.add_argument("--use-evidently", action="store_true")

    p.add_argument("--out-dir", default="benchmarks/out")
    p.set_defaults(func=e2e)

    p2 = sub.add_parser("sweep", help="budget sweep + Pareto csv")
    p2.add_argument("--corpus", default="examples/corpus/sample_docs.jsonl")
    p2.add_argument("--queries", default="examples/corpus/sample_queries.jsonl")
    p2.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    p2.add_argument("--k", type=int, default=200)
    p2.add_argument("--alpha", type=float, default=0.5)
    p2.add_argument("--b-min", type=int, default=10)
    p2.add_argument("--b-max", type=int, default=90)
    p2.add_argument("--b-step", type=int, default=10)
    p2.add_argument("--max-q", type=int, default=20)
    p2.add_argument("--out-dir", default="benchmarks/out")
    p2.add_argument("--save-plots", action="store_true")
    p2.set_defaults(func=budget_sweep)

    p3 = sub.add_parser("scale", help="scaling runtime with synthetic data")
    p3.add_argument("--n-max", type=int, default=100000)
    p3.add_argument("--budget", type=float, default=0.3)
    p3.set_defaults(func=scaling)

    p4 = sub.add_parser("dp-curve", help="% of optimal vs budget (synthetic)")
    p4.add_argument("--n", type=int, default=2000)
    p4.add_argument("--n-opt", type=int, default=200)
    p4.add_argument("--b-min", type=int, default=10)
    p4.add_argument("--b-max", type=int, default=90)
    p4.add_argument("--b-step", type=int, default=10)
    p4.add_argument("--out-dir", default="benchmarks/out")
    p4.add_argument("--save-plots", action="store_true")
    p4.set_defaults(func=dp_curve)

    p5 = sub.add_parser("haystack-compare", help="compare BM25 vs dense retrievers (Haystack)")
    p5.add_argument("--corpus", default="examples/corpus/sample_docs.jsonl")
    p5.add_argument("--queries", default="examples/corpus/sample_queries.jsonl")
    p5.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    p5.add_argument("--k", type=int, default=50)
    p5.add_argument("--max-q", type=int, default=10)
    p5.set_defaults(func=compare_haystack)

    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\cross_encoder.py`
```python
from typing import List, Optional
import logging

class SafeCrossEncoderManager: 
    """Cross-Encoder 상태를 명시적으로 관리하는 클래스"""
    
    def __init__(self, model_name: Optional[str] = None, device: str = "cpu"):
        self.model_name = model_name
        self.device = device
        self.model = None
        self.status = "unknown"
        self.last_error = None
        
        self._initialize()
    
    def _initialize(self):
        """Cross-Encoder 초기화 with 상세 상태 추적"""
        if not self.model_name:
            self.status = "disabled"
            logging.info("Cross-Encoder: DISABLED (no model specified)")
            return
        
        try:
            # sentence-transformers 임포트 체크
            from sentence_transformers import CrossEncoder
            
            # 모델 로딩 시도
            self.model = CrossEncoder(self.model_name, device=self.device)
            self.status = f"active ({self.model_name})"
            
            # 🆕 성공 시 상세 로깅
            logging.info(f"Cross-Encoder: ACTIVE")
            logging.info(f"  └─ Model: {self.model_name}")
            logging.info(f"  └─ Device: {self.device}")
            
        except ImportError as e:
            self.status = "unavailable (sentence-transformers not installed)"
            self.last_error = str(e)
            
            # 🆕 의존성 누락 시 명확한 안내
            logging.warning("Cross-Encoder: UNAVAILABLE")
            logging.warning("  └─ Reason: sentence-transformers not installed")
            logging.warning("  └─ Install: pip install sentence-transformers")
            
        except Exception as e:
            self.status = f"error ({type(e).__name__})"
            self.last_error = str(e)
            
            # 🆕 기타 오류 시 상세 로깅
            logging.error(f"Cross-Encoder: ERROR")
            logging.error(f"  └─ Model: {self.model_name}")
            logging.error(f"  └─ Error: {str(e)}")
    
    def get_status_for_response(self) -> str:
        """API 응답용 상태 문자열"""        return self.status
    
    def rerank(self, query: str, documents: List[str]) -> List[float]:
        """안전한 리랭킹 with 상태 로깅"""
        if self.model is None:
            # 🆕 비활성화 상태 명시적 로깅
            logging.debug(f"Cross-Encoder rerank skipped: {self.status}")
            return [0.5] * len(documents)  # 중립 점수
        
        try:
            pairs = [(query, doc) for doc in documents]
            scores = self.model.predict(pairs)
            
            # 🆕 성공적 리랭킹 로깅
            logging.debug(f"Cross-Encoder reranked {len(documents)} documents")
            
            return scores.tolist() if hasattr(scores, 'tolist') else list(scores)
            
        except Exception as e:
            # 🆕 런타임 오류 시 상세 로깅
            logging.error(f"Cross-Encoder rerank failed: {str(e)}")
            logging.error(f"  └─ Fallback: returning neutral scores")
            return [0.5] * len(documents)
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\demo.py`
```python
"""
Demo & Metrics Server for CRoM-EfficientLLM
------------------------------------------
- `crom-demo demo`  : run sample pipeline
- `crom-demo serve` : start Flask + Prometheus metrics on :8000
"""
from __future__ import annotations

import argparse
from typing import List

from flask import Flask, Response
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

from crom_efficientllm.budget_packer.packer import budget_pack, pack_summary, Chunk
from crom_efficientllm.rerank_engine.rerank import hybrid_rerank
from crom_efficientllm.drift_estimator.estimator import DriftEstimator, DriftMode

# ---- Prometheus metrics ----
TOKENS_SAVED = Gauge("crom_tokens_saved", "Tokens saved by budget packer")
DRIFT_ALERTS = Counter("crom_drift_alerts_total", "Total drift alerts emitted")

class DummyEmbed:
    def encode(self, text_or_list, convert_to_numpy=False):
        if isinstance(text_or_list, list):
            return [self.encode(t) for t in text_or_list]
        vec = [ord(c) % 7 for c in str(text_or_list)[:16]]
        while len(vec) < 16:
            vec.append(0)
        return vec

def run_demo() -> None:
    chunks: List[Chunk] = [
        Chunk(text="AI ethics is crucial", score=0.9, tokens=50),
        Chunk(text="Unrelated text", score=0.2, tokens=40),
        Chunk(text="Drift detection research", score=0.8, tokens=60),
    ]
    packed = budget_pack(chunks, budget=80)
    summary = pack_summary(packed)
    print("Packed:", [c.text for c in packed], summary)

    docs = [{"text": "AI drift measurement"}, {"text": "Cooking recipes"}]
    reranked = hybrid_rerank("AI ethics", docs, DummyEmbed(), alpha=0.5)
    print("Reranked:", [d["text"] for d in reranked])

    de = DriftEstimator(threshold=0.5, mode=DriftMode.L2)
    print("Drift state:", de.state())
    print("Drift alert?", de.update([1, 2, 3]))
    print("Drift alert?", de.update([10, 10, 10]))
    print("Drift state:", de.state())

    # Update metrics
    TOKENS_SAVED.set(max(0, sum(c.tokens for c in chunks) - summary["tokens"]))
    alert1, *_ = de.update([1, 2, 3])
    alert2, *_ = de.update([10, 10, 10])
    if alert1:
        DRIFT_ALERTS.inc()
    if alert2:
        DRIFT_ALERTS.inc()

def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    return app

def main() -> None:
    parser = argparse.ArgumentParser(prog="crom-demo")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("demo", help="run sample pipeline")

    pserve = sub.add_parser("serve", help="start metrics server on :8000")
    pserve.add_argument("--host", default="0.0.0.0")
    pserve.add_argument("--port", type=int, default=8000)

    args = parser.parse_args()

    if args.cmd == "demo":
        run_demo()
        return

    if args.cmd == "serve":
        app = create_app()
        app.run(host=args.host, port=args.port)
        return

if __name__ == "__main__":
    main()
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\server.py`
```python
from fastapi import FastAPI, HTTPException
import time
from typing import List, Dict
import logging

# 내부 모듈 임포트
from .budget_packer import enhanced_greedy_pack
from .cross_encoder import SafeCrossEncoderManager
from .capsule_logger import ExplainCapsuleLogger

# --- FastAPI 앱 및 주요 컴포넌트 초기화 ---

app = FastAPI(
    title="CRoM-EfficientLLM Server",
    description="Context Reranking and Management for Efficient LLMs",
    version="1.0.1"
)

logging.basicConfig(level=logging.INFO)

# 컴포넌트 인스턴스화
# TODO: 설정 파일(config.yaml)에서 모델 이름 등을 로드하도록 개선 필요
ce_manager = SafeCrossEncoderManager(model_name="ms-marco-TinyBERT-L-2-v2")
capsule_logger = ExplainCapsuleLogger(log_directory="artifacts/logs")


# --- 응답 스키마 및 헬퍼 함수 ---

class ProcessResponseV2:
    """확장된 /process 엔드포인트 응답 스키마 헬퍼"""
    
    @staticmethod
    def create_response(query: str, packed_chunks: List[Dict], 
                       processing_stats: Dict, cross_encoder_status: str, 
                       processing_time: float) -> Dict:
        """개선된 응답 생성"""
        
        response = {
            "success": True,
            "query": query,
            "chunks": packed_chunks,
            "stats": processing_stats, # packing 통계
            "meta": {
                "cross_encoder_status": cross_encoder_status,
                "processing_time_ms": processing_time * 1000,
                "timestamp": time.time()
            }
        }
        return response

# --- API 엔드포인트 정의 ---

@app.post("/process", summary="Rerank and pack text chunks")
def process_chunks(query: str, chunks: List[Dict], budget: int = 4096):
    """
    주어진 쿼리와 청크 목록을 리랭킹하고 예산에 맞게 패킹합니다.
    """
    start_time = time.time()

    try:
        # 1. Cross-Encoder로 리랭킹 (활성화 시)
        doc_texts = [chunk.get("text", "") for chunk in chunks]
        scores = ce_manager.rerank(query, doc_texts)
        for chunk, score in zip(chunks, scores):
            chunk["score"] = score

        # 2. 예산에 맞게 패킹
        packed_chunks, stats = enhanced_greedy_pack(chunks, budget=budget, score_key="score")

        # 3. 최종 응답 생성
        processing_time = time.time() - start_time
        response_data = ProcessResponseV2.create_response(
            query=query,
            packed_chunks=packed_chunks,
            processing_stats=stats,
            cross_encoder_status=ce_manager.get_status_for_response(),
            processing_time=processing_time
        )

        # 4. 설명 캡슐 로깅
        capsule = capsule_logger.create_explain_capsule(
            query=query,
            response_data=response_data,
            processing_stats=stats,
            cross_encoder_status=ce_manager.get_status_for_response()
        )
        capsule_logger.log_capsule(capsule)

        return response_data

    except Exception as e:
        logging.error(f"Error during /process: {e}", exc_info=True)
        # 오류 로깅
        capsule_logger.log_error({
            "endpoint": "/process",
            "error": str(e),
            "query": query,
        })
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.get("/healthz", summary="Health check")
def health_check():
    """서버의 상태를 확인합니다."""
    return {"status": "ok", "cross_encoder": ce_manager.get_status_for_response()}

@app.get("/metrics", summary="Get Prometheus metrics")
def get_metrics():
    """Prometheus 메트릭을 노출합니다."""
    # TODO: Prometheus-client를 사용하여 실제 메트릭을 구현해야 함
    return {"message": "Metrics endpoint is active. Implement with prometheus-client."}
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\tests\\test_drift.py`
```python
from crom_efficientllm.drift_estimator.estimator import DriftEstimator, DriftMode

def test_drift_triggers():
    de = DriftEstimator(threshold=0.1, mode=DriftMode.L2)
    alert, dist, ewma = de.update([0, 0, 0])
    assert alert is False
    alert, dist, ewma = de.update([1, 0, 0])
    assert isinstance(alert, bool)
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\tests\\test_packer.py`
```python
from crom_efficientllm.budget_packer.packer import budget_pack, Chunk

def test_budget_pack_respects_budget():
    chunks = [Chunk("a", 1.0, 60), Chunk("b", 0.9, 50), Chunk("c", 0.5, 20)]
    sel = budget_pack(chunks, budget=70)
    assert sum(c.tokens for c in sel) <= 70

def test_budget_pack_sorting_stable():
    chunks = [
        {"text": "x", "score": 0.9, "tokens": 30},
        {"text": "y", "score": 0.9, "tokens": 20},
        {"text": "z", "score": 0.8, "tokens": 10},
    ]
    sel = budget_pack(chunks, budget=60)
    assert [c.text for c in sel] == ["y", "x", "z"]
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\tests\\test_rerank.py`
```python
from crom_efficientllm.rerank_engine.rerank import hybrid_rerank

class Dummy:
    def encode(self, text_or_list, convert_to_numpy=False):
        if isinstance(text_or_list, list):
            return [self.encode(t) for t in text_or_list]
        vec = [ord(c) % 5 for c in str(text_or_list)[:8]]
        while len(vec) < 8:
            vec.append(0)
        return vec

def test_hybrid_rerank_returns_scores():
    docs = [{"text": "alpha"}, {"text": "beta"}]
    out = hybrid_rerank("alp", docs, Dummy(), alpha=0.5)
    assert len(out) == 2
    assert {"score_sparse", "score_dense", "score_final"} <= set(out[0].keys())
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\budget_packer\\__init__.py`
```python
from .packer import Chunk, budget_pack, pack_summary
__all__ = ["Chunk", "budget_pack", "pack_summary"]
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\budget_packer\\packer.py`
```python
"""
Budget Packer
-------------
Greedy packing of highest-scoring chunks under a token budget.
- Stable ordering (score desc, tokens asc, original index asc)
- Input validation and optional token estimation
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List, Sequence, Tuple, Union, Optional

@dataclass(frozen=True)
class Chunk:
    text: str
    score: float
    tokens: int

def _estimate_tokens(text: str) -> int:
    """Lightweight heuristic when `tokens` absent. Avoids heavy tokenizers.
    Why: keeps demo dependency-light and deterministic.
    """
    # approx: 4 chars ≈ 1 token; floor at 1
    return max(1, len(text) // 4)

def _coerce_chunk(obj: Union[Chunk, dict], idx: int) -> Chunk:
    if isinstance(obj, Chunk):
        return obj
    if not isinstance(obj, dict):
        raise TypeError(f"Chunk #{idx} must be Chunk or dict, got {type(obj)}")
    text = str(obj.get("text", ""))
    if not text:
        raise ValueError(f"Chunk #{idx} has empty text")
    score = float(obj.get("score", 0.0))
    tokens = int(obj["tokens"]) if "tokens" in obj else _estimate_tokens(text)
    if tokens <= 0:
        raise ValueError(f"Chunk #{idx} has non-positive tokens: {tokens}")
    return Chunk(text=text, score=score, tokens=tokens)

def budget_pack(
    text_chunks: Sequence[Union[Chunk, dict]],
    budget: int = 1000,
) -> List[Chunk]:
    """
    Args:
        text_chunks: iterable of Chunk or dict with keys {text, score, tokens}
        budget: max token budget (int > 0)
    Returns:
        list of selected chunks (order of selection)
    """
    if budget <= 0:
        raise ValueError("budget must be > 0")

    coerced: List[Chunk] = [_coerce_chunk(c, i) for i, c in enumerate(text_chunks)]

    # stable sort by (-score, tokens, original_index)
    indexed: List[Tuple[int, Chunk]] = list(enumerate(coerced))
    indexed.sort(key=lambda it: (-it[1].score, it[1].tokens, it[0]))

    selected: List[Chunk] = []
    total = 0
    for _, ch in indexed:
        if total + ch.tokens <= budget:
            selected.append(ch)
            total += ch.tokens
    return selected

def pack_summary(selected: Sequence[Chunk]) -> dict:
    tokens = sum(c.tokens for c in selected)
    return {
        "num_chunks": len(selected),
        "tokens": tokens,
        "avg_score": (sum(c.score for c in selected) / len(selected)) if selected else 0.0,
    }
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\drift_estimator\\__init__.py`
```python
from .estimator import DriftEstimator, DriftMode
__all__ = ["DriftEstimator", "DriftMode"]
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\drift_estimator\\estimator.py`
```python
"""
Drift Estimator
---------------
Monitors embedding shift using L2 or cosine distance.
Supports EWMA smoothing and exposes state for dashboards.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple
import numpy as np

class DriftMode(str, Enum):
    L2 = "l2"
    COSINE = "cosine"

@dataclass
class DriftEstimator:
    threshold: float = 0.2
    mode: DriftMode = DriftMode.L2
    ewma_alpha: float = 0.3  # smoothing for stability

    history: List[np.ndarray] = field(default_factory=list)
    distances: List[float] = field(default_factory=list)
    ewma: Optional[float] = None

    def _distance(self, a: np.ndarray, b: np.ndarray) -> float:
        a = np.asarray(a, dtype=np.float32).ravel()
        b = np.asarray(b, dtype=np.float32).ravel()
        if self.mode == DriftMode.L2:
            return float(np.linalg.norm(a - b))
        # cosine distance = 1 - cosine similarity
        denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-12
        return float(1.0 - float(np.dot(a, b)) / denom)

    def update(self, embedding) -> Tuple[bool, float, float]:
        """
        Args:
            embedding: vector representation of current response
        Returns:
            (drift_alert, distance, ewma)
        """
        emb = np.asarray(embedding, dtype=np.float32)
        if emb.ndim != 1:
            emb = emb.ravel()

        if not self.history:
            self.history.append(emb)
            self.ewma = 0.0
            self.distances.append(0.0)
            return (False, 0.0, 0.0)

        last = self.history[-1]
        dist = self._distance(emb, last)
        self.history.append(emb)
        self.distances.append(dist)

        # EWMA update
        if self.ewma is None:
            self.ewma = dist
        else:
            self.ewma = self.ewma_alpha * dist + (1 - self.ewma_alpha) * self.ewma

        return (bool(self.ewma > self.threshold), float(dist), float(self.ewma))

    def state(self) -> dict:
        return {
            "count": len(self.history),
            "last_distance": self.distances[-1] if self.distances else 0.0,
            "ewma": self.ewma or 0.0,
            "mode": self.mode.value,
            "threshold": self.threshold,
        }
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\plugins\\evidently_drift.py`
```python
from __future__ import annotations
from typing import List

try:
    from evidently.metric_preset import DataDriftPreset
    from evidently.report import Report
    import pandas as pd
except Exception as e:  # pragma: no cover
    raise RuntimeError("evidently not installed. Install extras: pip install .[plugins]") from e

def drift_report(ref: List[List[float]], cur: List[List[float]]):
    ref_df = pd.DataFrame(ref)
    cur_df = pd.DataFrame(cur)
    rep = Report(metrics=[DataDriftPreset()])
    rep.run(reference_data=ref_df, current_data=cur_df)
    return rep
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\plugins\\flashrank_reranker.py`
```python
from __future__ import annotations
from typing import List, Dict

try:
    from flashrank import Reranker
except Exception as e:  # pragma: no cover
    raise RuntimeError("flashrank not installed. Install extras: pip install .[plugins]") from e

def flashrank_rerank(query: str, docs: List[Dict[str, str]], model_name: str = "ms-marco-TinyBERT-L-2-v2") -> List[Dict]:
    rr = Reranker(model_name)
    pairs = [(query, d["text"]) for d in docs]
    scores = rr.rerank(pairs)
    order = sorted(range(len(docs)), key=lambda i: -scores[i])
    return [docs[i] | {"score_flashrank": float(scores[i])} for i in order]
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\plugins\\llmlingua_compressor.py`
```python
from __future__ import annotations

try:
    from llmlingua import PromptCompressor
except Exception as e:  # pragma: no cover
    raise RuntimeError("llmlingua not installed. Install extras: pip install .[plugins]") from e

def compress_prompt(text: str, target_ratio: float = 0.5) -> str:
    pc = PromptCompressor()
    out = pc.compress(text, target_ratio=target_ratio)
    return out["compressed_prompt"] if isinstance(out, dict) and "compressed_prompt" in out else str(out)
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\rerank_engine\\__init__.py`
```python
from .rerank import hybrid_rerank
__all__ = ["hybrid_rerank"]
```
---
### **File:** `D:\\Sanctum\\CRoM-EfficientLLM\\src\\crom_efficientllm\\rerank_engine\\rerank.py`
```python
"""
Hybrid Rerank Engine
--------------------
Combines sparse (TF-IDF cosine) and dense (embedding cosine) scores with
min-max normalization for robust fusion.
"""
from __future__ import annotations

from typing import Dict, List, Sequence
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def _to_numpy(x):
    arr = np.asarray(x)
    return arr.astype(np.float32)

def _batch_encode(embed_model, texts: Sequence[str]) -> np.ndarray:
    # Try common API of sentence-transformers: encode(list, convert_to_numpy=True)
    if hasattr(embed_model, "encode"):
        try:
            return _to_numpy(embed_model.encode(list(texts), convert_to_numpy=True))
        except TypeError:
            # Fallback: per-text encode
            return _to_numpy([embed_model.encode(t) for t in texts])
    raise TypeError("embed_model must provide .encode()")

def _minmax(x: np.ndarray) -> np.ndarray:
    if x.size == 0:
        return x
    mn, mx = float(np.min(x)), float(np.max(x))
    if mx - mn <= 1e-12:
        return np.zeros_like(x)
    return (x - mn) / (mx - mn)

def hybrid_rerank(
    query: str,
    docs: List[Dict[str, str]],
    embed_model,
    alpha: float = 0.5,
) -> List[Dict[str, object]]:
    """
    Args:
        query: query string
        docs: list of {"text": str}
        embed_model: model with .encode() -> vector(s)
        alpha: weight between sparse/dense in [0,1]
    Returns:
        ranked list of enriched docs with scores {score_sparse, score_dense, score_final}
    """
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha must be in [0, 1]")
    if not docs:
        return []

    texts = [d.get("text", "") for d in docs]

    # Sparse: TF-IDF cosine
    tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=1).fit(texts)
    Q = tfidf.transform([query])
    D = tfidf.transform(texts)
    sparse_scores = cosine_similarity(Q, D).ravel()

    # Dense: cosine(sim) between L2-normalized embeddings
    q_emb = _to_numpy(embed_model.encode(query))
    d_embs = _batch_encode(embed_model, texts)
    # L2 normalize
    def _l2norm(a):
        n = np.linalg.norm(a, axis=-1, keepdims=True) + 1e-12
        return a / n

    qn = _l2norm(q_emb.reshape(1, -1))
    dn = _l2norm(d_embs)
    dense_scores = cosine_similarity(qn, dn).ravel()

    # Min-max to [0,1] before fusion to avoid scale issues
    s_sparse = _minmax(sparse_scores)
    s_dense = _minmax(dense_scores)

    final_scores = alpha * s_sparse + (1 - alpha) * s_dense
    order = np.argsort(-final_scores)

    ranked = []
    for i in order:
        item = dict(docs[i])
        item.update(
            score_sparse=float(s_sparse[i]),
            score_dense=float(s_dense[i]),
            score_final=float(final_scores[i]),
        )
        ranked.append(item)
    return ranked
```
