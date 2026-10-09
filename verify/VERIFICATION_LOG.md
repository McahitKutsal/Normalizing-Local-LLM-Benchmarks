# Verification log

Every citation and every extracted measurement in the manuscript was checked
against a primary source between 27 September 2026. This log records what was
checked, what was wrong, and what was removed. Nothing in the manuscript now
rests on recalled information.

Method: arXiv identifiers were resolved at `arxiv.org/abs/<id>` and the returned
title and author list compared against the claim. Conference papers were checked
against the publisher's record (PMLR, ACL Anthology, ACM DL, dblp, OJS). Web and
vendor reports were fetched and their title, author and date read off the page.
Model architectures were read from the published `config.json`.

A wrong identifier can resolve to a real but different paper, so in every case
the returned **title** was compared, not merely the fact that the identifier
resolved.

---

## Part 1 — Citations

### 1.1 Verified correct, no change (34 entries)

All arXiv identifiers below resolved to the claimed title and author list:

| Ref | arXiv | Verified title |
|---|---|---|
| GPTQ | 2210.17323 | GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers |
| AWQ | 2306.00978 | AWQ: Activation-aware Weight Quantization … |
| SmoothQuant | 2211.10438 | SmoothQuant: Accurate and Efficient Post-Training Quantization … |
| LLM.int8() | 2208.07339 | LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale |
| PagedAttention | 2309.06180 | Efficient Memory Management for LLM Serving with PagedAttention |
| FlashAttention-2 | 2307.08691 | FlashAttention-2: Faster Attention with Better Parallelism … |
| SGLang | 2312.07104 | SGLang: Efficient Execution of Structured Language Model Programs |
| WebLLM | 2412.15803 | WebLLM: A High-Performance In-Browser LLM Inference Engine |
| FlexGen | 2303.06865 | FlexGen: High-Throughput Generative Inference … |
| PowerInfer | 2312.12456 | PowerInfer: Fast LLM Serving with a Consumer-grade GPU |
| MoE offloading | 2312.17238 | Fast Inference of Mixture-of-Experts Language Models with Offloading |
| MoE-Infinity | 2401.14361 | MoE-Infinity: Efficient MoE Inference on Personal Machines … |
| Fiddler | 2402.07033 | Fiddler: CPU-GPU Orchestration for Fast Inference of MoE Models |
| HybriMoE | 2504.05897 | HybriMoE: Hybrid CPU-GPU Scheduling and Cache Management … |
| AdapMoE | 2408.10284 | AdapMoE: Adaptive Sensitivity-based Expert Gating … |
| DALI | 2602.03495 | DALI: A Workload-Aware Offloading Framework … on Local PCs |
| ZeRO-Infinity | 2104.07857 | ZeRO-Infinity: Breaking the GPU Memory Wall … |
| Scaling inference | 2211.05102 | Efficiently Scaling Transformer Inference |
| Speculative decoding | 2211.17192 | Fast Inference from Transformers via Speculative Decoding |
| Medusa | 2401.10774 | Medusa: Simple LLM Inference Acceleration Framework … |
| EAGLE | 2401.15077 | EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty |
| EAGLE-3 | 2503.01840 | EAGLE-3: Scaling up Inference Acceleration … |
| Spec. survey | 2401.07851 | Unlocking Efficiency in LLM Inference: … Speculative Decoding |
| Knoop et al. | 2601.09527 | Private LLM Inference on Consumer Blackwell GPUs … |
| Energy benchmark | 2608.00008 | Energy Efficiency of Locally Deployed LLMs … |
| Joules | 2601.22076 | Where Do the Joules Go? Diagnosing Inference Energy Consumption |
| Request/token energy | 2608.28044 | Characterization of Request and Token Energy Costs … |
| On-device eval | 2505.15030 | A Systematic Evaluation of On-Device LLMs … |
| On-device review | 2409.00088 | On-Device Language Models: A Comprehensive Review |
| Hardware perspective | 2410.04466 | LLM Inference Acceleration: A Comprehensive Hardware Perspective |
| RooflineBench | 2602.11506 | RooflineBench: A Benchmarking Framework for On-Device LLMs … |
| SparseGPT | 2301.00774 | SparseGPT: Massive Language Models Can Be Accurately Pruned … |
| MoQE | 2310.02410 | Mixture of Quantized Experts (MoQE) … |
| Any-precision | 2402.10517 | Any-Precision LLM: Low-Cost Deployment … |
| MLPerf inference | 1911.02549 | MLPerf Inference Benchmark |
| Zeus | 2208.06102 | Zeus: Understanding and Optimizing GPU Energy Consumption … |
| ML.ENERGY | 2505.06371 | The ML.ENERGY Benchmark … |
| TokenPowerBench | 2512.03024 | TokenPowerBench: Benchmarking the Power Consumption … |
| Nondeterminism | 2506.09501 | Understanding and Mitigating Numerical Sources of Nondeterminism … |
| Meta-metrics | 2508.10251 | Meta-Metrics and Best Practices … |

No fabricated arXiv identifier was found. Every identifier in the original
list resolved to the paper it was claimed to be.

### 1.2 Corrected

| # | What was wrong | Corrected to |
|---|---|---|
| 1 | **Journal wrong.** "Accelerating language giants" cited to *Computer Science Review*. | *Journal of Systems Architecture*, vol. 172, art. 103690, 2026; authors Y. C. Kim, S. K. Yoon, S. S. Han, C. W. Park, J. O. Park, J. H. Ko, H. Kim. Source: ScienceDirect record. |
| 2 | **Title invented.** NVFP4 cited as "NVFP4: A 4-bit floating-point format for Blackwell tensor cores, NVIDIA Tech. Rep., 2025" — no such report. | E. Alvarez, O. Almog, E. Chung, S. Layton, D. Stosic, R. Krashinsky, K. Aubrey, "Introducing NVFP4 for Efficient and Accurate Low-Precision Inference," NVIDIA Technical Blog, 24 Jun 2025. |
| 3 | **Twelve entries credited to "Anonymous."** Placeholder, not publishable. | Real authors retrieved for all twelve: Zähl & Hennig (2608.00008); Niu et al. (TokenPowerBench); Chung, Wu, Ma & Chowdhury (2601.22076); Vellaisamy, Lam, Blanton & Shen (2608.28044); Song et al. (2505.15030); Cai, Tian, Yang, Jia, Li & Wang (Tsinghua Sci. Technol.); Li et al. (2410.04466); Kim et al. (J. Syst. Archit.); Katakam (ScienceOpen); Bi et al. (2602.11506); Yuan et al. (2506.09501); Salaria, Liu & Gonzalez (2508.10251). |
| 4 | Knoop et al. listed as "and 1 other author." | J. Knoop and H. Holtmann. |
| 5 | Puget Systems report had no author or date. | J. Allman, 22 Aug 2024. |
| 6 | NVIDIA llama.cpp post had no author or date. | A. Chockalingam, 2 Oct 2024. |
| 7 | Menlo report had no date. | 29 Apr 2024. |
| 8 | TokenPowerBench cited to AAAI without volume/pages. | *Proc. AAAI*, vol. 40, no. 38, 2026, pp. 32582-32590 (OJS record). |
| 9 | Medusa, EAGLE, spec. survey cited without pages. | Medusa PMLR 235:5209-5235; EAGLE PMLR 235:28935-28948; survey Findings ACL 2024:7655-7671. |
| 10 | PowerInfer cited with page numbers. | Pages **removed** — could not be verified (ACM DL returned 403). DOI given instead. |
| 11 | Tsinghua Sci. Technol. survey cited without volume/pages. | Vol. 31, no. 3, pp. 1365-1380, 2026. |
| 12 | lm-evaluation-harness author list abbreviated to "L. Gao et al." | Expanded to the credited author list. |
| 13 | ExLlamaV2 cited without noting successor. | Noted as superseded by ExLlamaV3. |
| 14 | MLPerf Client cited as "version 0.6" with a 2025 news URL. | Cited to the stable benchmark page; version claim dropped. |

### 1.3 Confirmed against a suspicion that proved unfounded

- **FlexGen author list.** The arXiv version lists 14 authors, the PMLR version 10.
  The manuscript cites the PMLR version, and its 10-author list is correct as given.
- **AWQ title.** The arXiv title dropped "On-Device"; the MLSys 2024 proceedings
  title retains it. The manuscript cites MLSys, so "On-Device" is correct.
- **DALI (arXiv:2602.03495).** Flagged internally as a probable fabrication
  because of its 2026 identifier. It is real, and the author list was correct.

---

## Part 2 — Extracted measurements (more serious)

Verifying the citations surfaced a larger problem: the measurements in Table 5
had been assembled the same way as the citations, and several did not survive
contact with their sources.

### 2.1 Corrected

**Menlo Research 2024.** The manuscript recorded TensorRT-LLM running **FP16**
at 159 and 132 tok/s on the RTX 4090 and 3090. The report actually benchmarks
**Mistral 7B v0.2 in AWQ int4** for TensorRT-LLM and **GGUF Q4_K_M** for
llama.cpp, at `batch_size 1, input_len 2048, output_len 512`:

| GPU | TensorRT-LLM (AWQ int4) | llama.cpp (Q4_K_M) |
|---|---|---|
| RTX 4090 | 170.63 tok/s | 100.43 tok/s |
| RTX 3090 | 144.19 tok/s | 88.70 tok/s |
| RTX 4070 Laptop | 51.57 tok/s | 39.70 tok/s |
| RTX 4090 eGPU | 104.95 tok/s | 62.22 tok/s |

The figures also span prefill and decode together rather than decode alone,
which the manuscript now states.

**Knoop et al. 2026.** Recorded as batch-1 measurements. The paper reports
**concurrency 8** (and mostly c4-c256). Real values for Qwen3-8B NVFP4 at 8k:
RTX 5060 Ti 115, RTX 5070 Ti 211, RTX 5090 411 TPS. These are now labelled as
batched and excluded from single-stream pooling.

**Zähl & Hennig 2026.** The manuscript quoted two figures second-hand. The full
measured table has been substituted (9 models, tok/s, J/token, mean watts, RTX
4060 Ti 16 GB, Ollama, **decode-only** via `eval_count`/`eval_duration`, batch 1).

### 2.2 Removed

| Removed | Why |
|---|---|
| 3 Puget Systems rows (Llama-2-13B) | The report benchmarks **Phi-3-mini-4k-instruct in 4-bit GGUF**, not Llama-2-13B, and publishes its numbers only inside a chart image. Nothing extractable. |
| 2 Oobabooga / ExLlamaV2 rows | Traced only to a secondary blog summarising them. Primary measurement not located. |
| 2 "Offload-est" rows (Llama-3.3-70B, Mixtral-8x7B) | These were the author's own estimates presented in a table of extracted measurements. Not measurements. |

**Consequence.** The verified corpus contains no offloaded configuration, so the
"residency cliff" (3.3× MBU, 13× energy) has **no empirical support** and has been
withdrawn as an empirical finding. The underlying mechanism — PCIe bandwidth
replacing VRAM bandwidth in equation (4) — is retained as an analytic prediction
and explicitly labelled as untested here.

### 2.3 What this changed in the results

| Claim in the previous draft | Status after verification |
|---|---|
| 16% of single-stream figures exceed the bandwidth ceiling | **Rebuilt.** 3 of 9 rows exceed it — and all three are the Knoop rows, which the source independently documents as concurrency 8. The filter's flag is confirmed by ground truth rather than inferred. |
| Engine gaps dissolve: 1.49× raw → 1.06× MBU, p = 0.74 | **Reversed.** On matched hardware and matched model, TensorRT-LLM vs llama.cpp is 1.66× raw → **1.47× normalized**. Normalization removes ~29% of the apparent gap; a real engine effect remains. |
| Residency cliff 3.3× / 13× | **Withdrawn** (see 2.2). |
| Electricity-only accounting understates cost 5.7× | Retained but recomputed from measured power. |
| Dispersion 6.8× → 2.6× | **Rebuilt** on the smaller verified corpus. |

### 2.4 How each gap was closed

All three gaps flagged in the first pass have since been resolved.

1. **PRISMA counts — removed.** The paper no longer claims a systematic review.
   It is now a framework paper; Figure 1 is the normalization pipeline, and
   Section IV states plainly how sources were selected and that no exhaustive
   database search was performed.
2. **Table 2 accuracy columns — sourced.** Replaced with a unified evaluation of
   every llama.cpp container on Llama-3.1-8B-Instruct (arXiv:2601.14277):
   WikiText-2 perplexity plus five lm-evaluation-harness tasks. Cross-checked
   against the k-quant pull request (ggml-org/llama.cpp #1684) on LLaMA-7B and
   13B. Effective bits per weight are now **derived** from published artifact
   sizes; the 7B and 13B derivations agree to 0.03 bits and the two sources
   correlate at r = 1.0000.
3. **Table 3 multipliers — traced, and one corrected.** The "10.9x Marlin"
   figure is not a claim its authors make; the Marlin README claims **3.87x
   against FP16**, describing it as near-ideal because it is the memory-traffic
   bound, with the contribution being that it *holds* to batch 16-32.
   FlashAttention-2 (~2x, 50-73% of peak FLOPs, A100), Leviathan speculative
   decoding (2-3x, T5-XXL), Medusa (2.2x / 2.3-2.8x) and EAGLE (2.7-3.5x) were
   each read from the primary source.

### 2.5 Second-pass corrections to the data

| What was wrong | Corrected to |
|---|---|
| Quantization perplexity deltas inflated 5-11x (e.g. Q4_K_M claimed +0.26, real +0.24 on an 8B model but +0.05 on the 7B k-quant table; Q6_K claimed +0.05, real +0.004) | Real tables substituted; the accuracy curve is far flatter than the draft claimed, moving the knee from 4.8-5.7 bits down to ~4 bits |
| KV cache computed as if every layer holds the full context | Equation (2) now models interleaved sliding-window attention. Gemma 3 keeps one global layer per six (window 1024), verified from config.json. This **overstated Gemma-3-12B's cache at 32k by 2.6x** and inverted the ranking: full-attention models average 33.9% cache share at 32k against 18.9% for interleaved ones |
| No verified offloaded measurement | PowerInfer OPT-30B FP16 on RTX 4090, batch 1, 16.06 tok/s (Fig. 10 of the paper), with hardware spec verified. This gives the offloading finding an empirical basis: 15.2x the naive PCIe bound and 96% of the resident ceiling |
| Model architectures assumed | All six frontier models read from published config.json: Mistral-7B, Llama-3-8B, Qwen3-8B, Gemma-3-12B, Gemma-3-27B, Qwen2.5-32B, Llama-3.3-70B, OPT-30B |

### 2.6 Findings as they now stand

| Claim | Basis |
|---|---|
| 3 of 10 measurements exceed the batch-1 ceiling | Computed; all three independently documented by their source as concurrency 8 |
| Engine effect 1.66x raw -> 1.47x normalized | Single controlled contrast, 2 GPUs, matched model and batch |
| Offloading reaches 96% of the resident ceiling | One verified measurement (PowerInfer) |
| Accuracy near-free to ~4.6 bpw, cliff below 4 | Unified 13-container evaluation, cross-checked |
| GSM8K falls 9.3 pp where the 5-task mean falls 4.0 | Same source, per-task reporting |
| Full attention pays the context wall, interleaved does not | Computed from verified architectures |
| Electricity is 19% of true cost | Measured power, 9 models, one instrumented study |

The withdrawn "residency cliff" (3.3x / 13x) has **not** been reinstated. The
verified offloading evidence points the other way: naive offloading is
interconnect-bound, but a placement strategy that exploits sparsity is not.

---

## Part 3 — Model architectures used in normalization

Read from published `config.json`:

| Model | Layers | KV heads | Head dim | Source |
|---|---|---|---|---|
| Mistral-7B-Instruct-v0.2 | 32 | 8 | 128 | HF `mistralai/Mistral-7B-Instruct-v0.2` |
| Llama-3-8B | 32 | 8 | 128 | HF `unsloth/llama-3-8b` (mirror of Meta config) |
| Qwen3-8B | 36 | 8 | 128 | HF `Qwen/Qwen3-8B` |

Architectures for the remaining models in the frontier table (Gemma-3-12B,
Gemma-3-27B, Qwen2.5-32B, Llama-3.3-70B, Mixtral-8x7B, GPT-OSS-20B) were **not**
re-verified in this pass and should be confirmed before submission, since the
VRAM frontier depends on them.

---

## Part 4 — Revision round, 1 October 2026

Addressing an external review. Items are the review's own identifiers.

### 4.1 Open questions the review could not check

The review flagged that it could not verify [29] (Knoop) or [33] (Zähl), the
sources behind the filter result and the entire energy analysis. Both were
re-checked at source:

- **Knoop & Holtmann (arXiv:2601.09527).** Title and both authors confirmed on
  the arXiv abstract page. The concurrency-8 figures (Qwen3-8B NVFP4 at 8k:
  5060 Ti 115, 5070 Ti 211, 5090 411 TPS) and the statement that the paper
  reports c4 through c256 rather than single-stream were read from the full text.
- **Zähl & Hennig (arXiv:2608.00008).** Title, both authors and the full Table III
  confirmed. See 4.2 for what re-reading it settled.

### 4.2 P1-1 — the two energy columns, resolved

The review was right that `J/token` and the electricity cost derived from
`Mean W / (tok/s)` are not the same quantity. The source defines:

    J/tok = E_GPU / n_out,  E_GPU = P_load,mean · Δt

where Δt is the **whole inference call** ("from API invocation through response
receipt"), while throughput comes from Ollama's `eval_count`/`eval_duration`,
which is **decode only**. The difference is therefore prefill plus call overhead
amortized across the output tokens: 0.085–0.319 J per row, averaging 18% of the
reported energy. Not a unit error, and not constant, exactly as the review
predicted.

Fixed by computing cost from the measured `J/token` (new `cost_from_energy()` in
`normalize.py`). Equation (6) is now stated in Sec. IV-D and Sec. IX-A as a
decode-only approximation rather than an identity. Resulting figures:

| | before | after |
|---|---|---|
| electricity share | 19% | **21.4%** |
| understatement factor | 5.4x | **4.7x** |

matching the review's predicted ~21% and ~4.7x.

### 4.3 P1-2 — the non-compliant corpus row

Removed. The NVIDIA row stated neither batch nor phase and named its container
only as "int4", which is the paper's own second disqualifier. Corpus is n=9; the
filter result is 3 of 9. Sec. V-A now names the exclusion explicitly, so the
criterion is visibly applied to our own candidates rather than only to others'.

### 4.4 Everything else in the list

| Item | Resolution |
|---|---|
| P0-1 equations absent | Root cause found: the part-A render loop handled only `sub.p` and silently dropped `eq`/`p2`/`eq2`/`p3`/`eq3`/`p4`. Both loops now call one `renderSub()`. All eight equations present, numbered, IEEE-style (centred body, number flush right via tab stops). |
| P0-2 no in-text citations | Citations are now written as `[[key]]` and resolved by `build.js` in order of first appearance. The build **fails** if any reference is never cited. 64 of 64 cited; no gaps in the numbering. |
| P0-3 artifact link | Artifact statement added to the front matter with repository and Zenodo DOI placeholders, plus a paragraph in Sec. V-C listing what the repository contains. Addresses still to be filled in. |
| P0-4 author block | Placeholder retained but marked, and a funding statement block added (IEEE Access requires one even when the work is unfunded). |
| P1-3 B_tok means two things | Dagger footnote on Table 2 and on the offloaded row's two affected cells. |
| P1-4 not iso-quality | Added to the limitations paragraph of Sec. VII-A, in the review's own terms. |
| P1-5 positioning | New Sec. II "Related Work and Positioning". Roofline and MBU explicitly acknowledged as borrowed; the three novel elements stated narrowly against RooflineBench and the meta-metrics work. |
| P1-6 ReLU precondition | Added to Sec. VII-C and to the corresponding item in Sec. XIII. |
| P1-7 abstract overclaims | "Five results follow" → "We demonstrate the framework in five applications"; "all from one study" added to the filter sentence; Sec. X-A softened and given an explicit paragraph on what a single test does and does not establish. |
| P2-1 "factor of 2.6" | Corrected to 5.2x on the cache and 1.95x on the footprint. |
| P2-2 Ctx = 2304 | Table 2 footnote states the prompt-plus-half-generation convention; Sec. XII bounds the alternative at under 2%. |
| P2-3 repeated values | Re-checked at source: Q5_K_S and Q4_0 genuinely both report GSM8K 75.66. Not an extraction error. Sec. VI-B now notes GSM8K's 0.076-point granularity (1319 problems) and warns against reading sub-point differences. |
| P2-4 peak vs achievable BW | Added to Sec. IV-B and Sec. XII, framed as the review suggested: the filter is conservative by construction, and for a test meant to challenge claims that is the right direction to err. |
| P2-5 amortization base | Sec. IX-B now states the base is the GPU alone and that 79% is therefore a lower bound. |
| P2-6 table order | Tables renumbered and repositioned to first-citation order: 1 hardware (V), 2 corpus (V, landscape), 3 quantization (VI), 4 kernels (VII), 5 frontier (VIII), 6 energy (IX). |
| P2-7 no Related Work | Closed with P1-5. |
| P3-1 umlaut | Table 2 now reads "Zähl 2026". |
| P3-2 model tag | Re-checked: the source's Table II really does list `gemma4:e2b`. Left as the source gives it. |
| P3-3 AWQ 4.25 bpw | Sec. VI-A now derives it from the container specification and flags it as the one bits-per-weight value not measured from an artifact; Sec. XII repeats the flag. |
| P3-4 contribution count | Four contributions, five applications, stated consistently in Sec. I, the abstract and Sec. XIV. |
| P3-5 / P3-6 figure labels | Fig. 2(a) labels now carry leader lines and are attached unambiguously to the five-task-mean markers. |

### 4.5 Items the review verified and asked us not to re-litigate

We left Table 1, the compression ratios and delta columns of Table 3, the VRAM
frontier, the ceiling and MBU arithmetic, the 29/71 decomposition, the cache-share
figures, the PowerInfer ceiling calculation and the kernel multipliers untouched,
as instructed. The one exception is that the 29/71 split is now stated in the text
as a share of the margin above parity, which the review asked for.

---

## Part 5 — Revision round 2, 1 October 2026

Addressing the v2 review. Items are that review's identifiers.

### 5.1 R-4 — the AWQ bits-per-weight value, and a second error it exposed

The review was right to press on this, and the fix uncovered an inconsistency the
review had not asked about.

**What was wrong with the derivation.** The paper computed 4.25 bits as
`4 + 32/128 + 32/128 = 4.5`, "reduced to 4.25 for zero-point-free packing". Both
halves of that are wrong: AWQ uses fp16 group scales, not 32-bit, and it is an
asymmetric scheme that does store zero points. The correct specification figure is
`4 + 16/128 + 4/128 = 4.16` bits across the quantized tensors.

**What it was replaced with.** Both containers in the engine comparison are now
measured from published artifacts of the same model:

| Container | Artifact | Size | Measured b |
|---|---|---|---|
| AWQ int4 | TheBloke/Mistral-7B-Instruct-v0.2-AWQ, `model.safetensors` | 4.15 GB | **4.59** |
| Q4_K_M | TheBloke/Mistral-7B-Instruct-v0.2-GGUF | 4.37 GB | **4.83** |

The 4.59 is the whole-model average, which is what equation (1) consumes.
Subtracting Mistral's 262 M embedding and output-projection parameters, which AWQ
leaves in fp16, gives 4.16 bits for the quantized remainder — agreeing with the
corrected specification figure to three significant figures. Two independent
routes to the same number.

**The second error.** The Q4_K_M value had been carried over from a derivation on
*Llama-3.1-8B*, whose 128k vocabulary gives it a very different embedding share
from Mistral's 32k. The engine comparison was therefore mixing a container
measured on one model with a container assumed for another. Effective bits per
weight is a property of a (model, container) **pair**, not of a container, and
`normalize.py` now carries a `BPW_MEASURED` table keyed on the pair, with
`bits_per_weight()` preferring a measured pair over the generic value. Sections
IV-A and VI-A state this explicitly.

**Effect on the headline numbers.** Larger than the review's sensitivity estimate,
because the correction moved both containers, not one:

| | before | after |
|---|---|---|
| AWQ bits/weight | 4.25 (assumed) | **4.59 (measured)** |
| Q4_K_M bits/weight | 4.89 (other model) | **4.83 (same model)** |
| MBU, RTX 4090 | 0.677 / 0.451 | **0.728 / 0.450** |
| pooled normalized ratio | 1.47x | **1.58x** |
| margin removed by normalization | 29% | **12%** |

The engine effect is therefore *larger* than previously reported and the confound
*smaller*. Sections VII-A, X-B, XIV and the abstract were rewritten accordingly,
and the rewrite makes the stronger point the number now supports: the size of the
artifact is computable in advance from the containers, it is small here because
4.59 and 4.83 are close, and it would be near-total for an FP16-against-4-bit
comparison, whose traffic ratio alone is about 3.4x. The exception clause in
Section XII is gone: every bits-per-weight value in the paper is now measured.

### 5.2 R-6 — the two model tags

Re-checked at source, with an explicit instruction not to normalize or correct the
strings. Table II of the energy study prints `gemma3:1b`, `gemma3:4b`, **`gemma4:e2b`**,
`llama3.2:1b`, `llama3.2:3b`, `mistral:7b`, `phi4-mini:3.8b`, `qwen2.5:3b` and
**`qwen3.5:2b`**. Not `gemma3n:e2b`. Left as the source gives them, and Table 6's
caption now says so, which should stop the question recurring.

### 5.3 The remaining four items

| Item | Resolution |
|---|---|
| R-1 heading/text mismatch | `APPLICATION N:` prefix dropped from the four headings, as the review suggested. Text keeps "five applications"; Section I names all five. |
| R-2 "Four of nine" | Corrected to **Five of nine**. Confirmed from Table 2: mixed = Menlo x4 + PowerInfer x1 = 5; decode = Zähl x1 + Knoop x3 = 4. |
| R-3 conclusion counts four | Now five, with the energy result added ("the true cost of a locally generated token is dominated by hardware amortization rather than electricity, which accounts for 21%"), and "Underneath all five is one quantity". |
| R-5 citation groups | Fixed structurally rather than by hand. `build.js` now accepts `[[a+b+c]]`, resolves each key, and prints the numbers **sorted ascending**; numbering still follows first appearance so the reference list tracks the text. All 15 adjacent citation runs in the manuscript were converted, so the rule now holds everywhere rather than at the two places the review happened to catch. |

### 5.4 On the sources the review could not check

The v2 review notes it verified the arithmetic but not whether [4] Menlo,
[7] PowerInfer, [26] the container evaluation, [33] Knoop and [36] Zähl say what
they are claimed to say. All five were read at source during preparation, and the
specific values taken from each are recorded in Parts 2 and 4 of this log:

- **Menlo** — the four throughput values, `batch_size 1`, ISL 2048 / OSL 512, and
  the two container names, read from the report's own results section.
- **PowerInfer** — 16.06 tok/s for OPT-30B FP16, Figure 10's caption, batch 1,
  and the PC-High hardware specification including the PCIe 4.0 figure.
- **Container evaluation** — the full 14-row results table, the WikiText-2
  methodology sentence and the five task definitions.
- **Knoop** — title and both authors from the arXiv record; the concurrency-8
  values and the statement that the paper reports c4 through c256 from the full
  text.
- **Zähl** — title, both authors, the full Table III, the `J/tok = E_GPU / n_out`
  definition with its integration window, and Table II's model tags.

Anyone re-checking these should start from the quoted values in Parts 2, 4 and 5
rather than from the manuscript, since that is the order in which they were
established.

---

# Part 6 — Revision round 3 (second reviewer, October 2026)

The second reviewer independently recomputed every derived value in the paper —
Table 1's 22 ratios, Table 2's 27 values, the roofline rows, Table 5's 42 cells,
the cost columns, r = −0.89, the 21/79 split, the 4.7x factor and the cache
ratios — and reproduced all of them within rounding. The items below are
therefore not arithmetic slips but two local modelling errors, one structural
weakness and a set of evidential gaps.

## P0.1 — The double-averaging error (confirmed, corrected)

**The reviewer was right.** Equation (3) read `B_tok = B_w + B_kv(C)/2`, justified
as the mean of a cache growing from zero to C. But the Table 2 note defined Ctx
as "prompt length plus half the generation length", which is *already* a mean.
Both were applied. Verified directly:

```
Mistral-7B, 131,072 cache bytes per token of depth
  C=2304 with /2 : 4.150 + 0.151 = 4.301 GB   <- what Table 2 printed (4.30)
  C=2304 no  /2  : 4.150 + 0.302 = 4.452 GB   <- correct
```

The ceiling 1008/4.30 = 234 matched only the first line, confirming both were in
play. Adopted the reviewer's recommended option (b): C̄ = L_p + L_g/2 is now its
own equation (3), and equation (4) evaluates the cache at that depth without
halving. The justification moved from the table note to the equation.

Option (b) is the correct one because the cache ramp starts at the prompt length,
not at zero, and no measurement in circulation is prompt-free.

**Structural fixes made at the same time**, since the root cause was duplication:

- `ctx` is no longer hand-entered per row. Each corpus row carries the prompt and
  generation lengths its source states and C̄ is derived by `ctx_bar()`.
- `quality.py` held an inlined second copy of the traffic formula whose `/2` had
  not been removed. It showed up as an F16 row whose ceiling ratio against itself
  was 1.02x rather than 1.00x. There is now one implementation.
- `vram_footprint()` used the generic `BPW[fmt]` while equation (1) used the
  measured `bits_per_weight()`. Unified on the measured value.
- **`tables.json` was hand-maintained.** This is why a corpus change did not
  reach the manuscript. `gen_tables.py` now generates every numeric cell from the
  analysis CSVs; only the qualitative mechanism table is carried through.
- `renderSub()` in build.js hardcoded the body/equation rungs up to `p4` and
  silently dropped anything past it — the same defect that shipped a manuscript
  without equations in round 1. It is now generic and throws on any unrendered key.
- Added `test_normalize.py`, including `test_btok_mistral_menlo()` as the reviewer
  asked and `test_no_double_averaging()`, which recovers d(B_tok)/d(C̄) and
  asserts it equals the full per-token cache bytes.

**Resulting values** match the reviewer's predictions exactly: MBU 0.754, 0.465,
0.686, 0.443. The headline is unchanged, as the reviewer predicted: pooled raw
1.66x → normalized 1.58x, normalization accounting for 12%.

**One value differs from the reviewer's estimate, in the paper's favour.** The
reviewer flagged that Knoop's `ctx=8192` needed checking. Verified against the
source: it is ISL 8192 / OSL 512 ("Prompt length: ... 8,192 tokens (short-RAG)",
"Maximum output length: 512 tokens"), so C̄ = 8448, not 8192. B_tok 5.85 GB and
the flagged MBUs are 1.34, 1.38, 1.50 rather than the reviewer's estimated
1.33–1.49.

**A second correction the reviewer did not raise.** The same source defines its
metric as "total output tokens per second (global TPS)" over a window that
includes prefill. The `phase` field conflated the numerator with the denominator,
so it now distinguishes three cases, and the Knoop rows are `decode/total`: the
rate understates decode speed, which makes the filter's flag on them conservative.

## P0.2 — Sign error (confirmed, sentence removed)

"Using the final length instead would lower the affected MBU values by under two
percent" had both the direction and the magnitude wrong. Recomputed across all
three defensible conventions:

| row | prompt-only | C̄ | final length |
|---|---|---|---|
| Menlo 4090 AWQ-4 | 0.7479 | 0.7536 | 0.7593 |
| Knoop 5090 | 1.3336 | 1.3423 | 1.3510 |

The final length **raises** MBU, monotonically, by at most 1.5%. The passage was
rewritten rather than patched, and now also reports that the engine ratio is
near-invariant to the convention (1.5835 / 1.5840 / 1.5846).

## P0.3 — Delta conventions (fixed)

Adopted option (2): the columns are now "PPL incr.", "Acc. loss (pp)" and "GSM8K
loss (pp)" — all cost columns, positive = worse — so no reader has to infer a
sign convention. Signs are printed explicitly so the containers that score above
baseline remain visible as what Sec. VI-E reads as noise.

## P1.1 — The filter's real test domain (Table 3, new)

The reviewer's strongest point: the inclusion rule requires the batch level to be
stated, so the corpus cannot contain the measurements the filter targets. Running
it there is a check, not a finding.

Built a second, disjoint set of nine widely-circulated measurements from four
sources, each verified first-hand against its primary source:

| source | what is missing |
|---|---|
| NVIDIA RTX AI Garage (256 tok/s, RTX 5090) | model identity, batch, phase, lengths, context |
| TechRadar / NVIDIA sponsored (282 tok/s) | precision, batch, phase, lengths, context |
| NVIDIA Developer Blog (150 tok/s) | batch, phase |
| hardware-corner.net (6 rows) | batch, tokens generated, prompt length, expert residency |

**The finding is decidability, not violation.** Four of nine have traffic ranges
that straddle MBU = 1: unremarkable under one admissible reading, physically
impossible under another. The filter returns *indeterminate*, which is a property
of the reporting. No row is claimed to be wrong.

The MoE rows are the sharpest case: Qwen3-30B-A3B reported at 141.6 / 139.7 /
113.8 tok/s on cards spanning 1.78x in bandwidth. Active-path reading → MBU 0.28
/ 0.49 / 0.43, i.e. not bandwidth-bound, which *explains* why the three cluster.
Resident-sweep reading → 1.60 / 2.81 / 2.46, impossible. The source does not say.

Contrast row: the Qwen3-8B measurements state container and context, and their
range collapses from 6.9x to 1.03x. Two fields cut the ambiguity ~200-fold —
the quantitative case for the Sec. XI standard.

Architectures for the new models were read from published config.json files.
gpt-oss effective bits are *derived* from the config (`modules_to_not_convert`
keeps attention, router and embeddings at BF16): 5.26 bits for the 20b and 4.44
for the 120b — same container, 0.8 bits apart, which is the paper's own thesis.

## P1.2 — Filter sensitivity (Sec. IV-F and Fig. 5, new)

Derived analytically from eq (6) with no new assumption. With r = B_kv/B_w:

```
MBU_computed = η(1+r)/(1/B + r)     fires when   η > (1/B + r)/(1+r)
```

At the corpus's cache share (r = 0.270) the threshold is η > 0.61 at batch 2,
0.41 at batch 4, 0.31 at batch 8. The flagged rows imply η = 0.42–0.47, clearing
the batch-8 threshold by 34–50%. As B → ∞ the threshold tends to r/(1+r) = 0.21,
not to zero: **a cache-dominated run can never be caught**, so long-context
measurements are the blind spot. Stated plainly: passing the filter is weak
evidence, failing it is strong evidence.

## P1.3 — Uncertainty (Sec. VI-E, new)

Per-item data is unavailable; the source reports point estimates (Appendix B
gives standard errors but not the discordance counts McNemar needs). Took the
reviewer's stated fallback and added a second, stricter bound.

1. **Sampling.** GSM8K n = 1319 (verified against the dataset's own test split).
   Paired McNemar SD = √(d/n) = 0.62–1.07 pp at 5–15% discordance, matching the
   reviewer's figures.
2. **Attribution, from the table itself.** Q5_0 and Q5_K_S share 5.57 effective
   bits and 7.43 perplexity but differ by 3.42 pp on GSM8K — 3.2x the most
   conservative sampling bound. Sampling is *not* the dominant source of
   variation; container construction is.

Applying the stricter bound, only Q3_K_L, Q3_K_M and Q3_K_S survive — all at or
below 4.30 effective bits. **This sharpens rather than weakens the paper**: the
reasoning asymmetry appears exactly at the knee. Sec. VI-D's earlier use of the
Q4_0 1.97 pp gap as "earlier and milder" evidence is removed; it was the error
Sec. VI-B warns against. Sec. VI-C's "one fifth" claim is 1.3x the floor and is
now explicitly hedged.

## P1.4 — Mixed-phase bias (bounded; the concern does not survive)

The reviewer reasoned from token counts: 80% of tokens at ISL 2048 / OSL 512 are
prefill, so prefill efficiency may be carrying the 1.58x. **A throughput figure
divides by time, not tokens.** llama.cpp's own CUDA scoreboard gives, for a 7B
Q4_0 on an RTX 4090, pp512 = 11,992.70 t/s against tg128 = 186.21 t/s — a ratio
of 64. Prefill is therefore **5.9% of the wall clock** while supplying 80% of the
tokens, and Amdahl's law caps its contribution at 1.06x. For prefill alone to
explain 1.58x it would need ≥36.9% of the run — six times its actual share.

Bounded both ways: equal prefill efficiency → decode-only ratio 1.65x; unbounded
prefill advantage → 1.49x. **Decode-only lies in [1.49, 1.65]**, the mixed-phase
1.58x sits inside, worst-case displacement 5.9%. Robust: even at five times the
measured prefill share the ratio stays above 1.11x. The interval now accompanies
the figure in the abstract, Sec. VII-A, Sec. X and Sec. XIV.

## P1.5 — Citation hygiene

- **Intro's 50–85% claim removed.** It cited two GitHub repositories for a
  measurement neither contains — the paper's own criticism, in its opening
  sentence. Replaced with the verified gpt-oss pair (256 vs 282 tok/s).
- **Marlin corrected** to arXiv:2408.11743, Frantar, Castro, Chen, Hoefler,
  Alistarh. Verified first-hand. The paper states "approximately 3.9×" on an A10
  against a theoretical optimum of 4×; the previous 3.87× came from the repo
  README, so the figure was changed to the cited paper's own.
- **Primary regulatory source added**: Regulation (EU) 2016/679, Chapter V,
  Arts. 44–50, replacing a preprint as support for the data-residency claim.
- **Single-source dependencies declared in the table captions**, not only in
  Sec. XII, since tables travel separately.
- **Conflict of interest declared**: the engine comparison rests on a technical
  report by a vendor of its own local inference product.

## P2 — Polish

| item | resolution |
|---|---|
| P2.1 | The offloaded row is now held out of the MBU column entirely, with its own "Frac. resid. ceil." column, rather than daggered inside a column whose premise is a common basis. |
| P2.2 | No measured bandwidth available without hardware. Instead scoped the assumption precisely: **no study in the corpus crosses a memory-technology boundary** (Menlo both GDDR6X, Knoop all GDDR7, the rest single-card), and the engine comparison is immune outright since both rows share a card. Exposure is limited to Table 1's cross-generation ranking and absolute MBU readings. |
| P2.3 | Novelty claim #2 softened to "a correction to benchmark practice", explicitly crediting the engines that already implement windowed caches and the Gemma 3 report that presents the saving as its own result. |
| P2.4 | 1.95x now named as Q4_K_M, with the container-dependent range 1.37x (FP16) to 2.14x (IQ3_M) — the error is worst exactly where a practitioner quantizes hardest to fit. |
| P2.5 | Sec. X-B and X-C compressed (~380 words); abstract cut 482 → 394 words. See the note on length below. |
| P2.6 | Parameter counts footnoted in the Table 6 caption, with the direction of the generic-width substitution's bias stated (large-vocabulary models are understated). |

## Tooling — `from_csv.py`

The Sec. XI field list is now a working tool rather than a checklist. CSV columns
are the Sec. XI fields; a missing field is reported by name together with the
equation it blocks, never defaulted. `--reproduce-table2` regenerates the corpus
through the public interface and returns 0 failures. Where the batch exceeds one
it prints **two** verdicts — given the stated batch, and as a reader would reach
meeting the figure presented as single-stream — which is Sec. V-D as a command.

## Not done, and why

- **The 108-measurement set.** Requires GPU hardware this environment does not
  have. Every other item of the 8.5+ package that can be done without hardware
  has been. This remains the single largest outstanding gap and the reviewer is
  right that it is what moves the paper from 7.5–8 to 8.5+.
- **A measured achievable-bandwidth figure per card** (P2.2) — same reason;
  scoped and bounded instead.
- **The 15–20% length cut** (P2.5) was only partly achieved. P1.1–P1.4 added
  roughly 2,200 words of analysis the reviewer required; about 500 were cut from
  genuine redundancy. The manuscript is ~12,600 words against ~11,800 before this
  round. The two instructions pull against each other and the analysis was judged
  the higher priority.

---

# Part 7 — Full reference audit (October 2026)

All 71 reference entries re-verified against primary sources: every arXiv ID
fetched from arxiv.org/abs/ and its returned title and author list compared
against the claim; every URL fetched and its published headline compared; every
conference paper checked against PMLR, ACL Anthology, Crossref, OpenAlex or the
publisher. Seven defects found and corrected.

## A structural bug: a silently discarded reference

`refs.js` is a JavaScript object literal, so a repeated key is overwritten
without any error. `gptoss` was defined twice — an existing arXiv model-card
entry and a HuggingFace entry added during revision round 3 — and the first was
discarded in silence. The uncited-reference guard could not see it, because the
object still had one key per name.

Removed the redundant entry (the arXiv model card is the citable form) and added
a guard to `build.js` that parses the source text rather than the object, fails
the build on any repeated key, and cross-checks the number of keys defined
against the number exported. Verified by introducing a deliberate duplicate: the
build now refuses it by name.

## Defects corrected

| ref | defect | correction |
|---|---|---|
| `awq` | Title carried "on-device", which is not in the paper's title | "AWQ: Activation-aware weight quantization for LLM compression and acceleration" — confirmed first-hand against arXiv:2306.00978 |
| `zahl` | Cited as two authors, presented as complete, with no "et al." The paper has **four**, and Hennig is third, not second | "P. M. Zähl, E. Dalipaj, A. Hennig, and T. Bayer" — confirmed first-hand. This matters: it is the single source for all nine energy measurements |
| `lmeval` | Title and year came from two different Zenodo records. The cited author list and 2024 belong to v0.4.3, whose title is different | "The Language Model Evaluation Harness," Zenodo v0.4.3, Jul. 2024, doi:10.5281/zenodo.12608602 — taken from the repository's own BibTeX |
| `nvidiaoss` | **Added this round; headline paraphrased, not quoted.** The HTML `<title>` and the on-page headline differ, and neither matched the citation | "OpenAI's new open models accelerated locally on NVIDIA GeForce RTX and RTX PRO GPUs" — read from the page's H1 |
| `techradar` | **Added this round; title invented** | "NVIDIA RTX AI PCs pair with OpenAI's open-weight gpt-oss-20b for a huge performance boost," Oct. 20, 2025 |
| `hwcorner` | **Added this round; title paraphrased, byline and date missing** | "The definitive GPU ranking for LLMs: Token generation & prompt processing performance," A. Witt, Dec. 9, 2025 |
| `llamacppbench` | Thread attributed to no one | Opened by O. Shulyakov; "Nvidia" capitalised as the thread titles it |

Three of the seven were introduced during revision round 3, by paraphrasing a
headline from memory of the page rather than quoting it. That is the same class
of error this paper exists to criticise, committed while correcting it. The
`audit.py` reference checks added afterwards pin each of these specific strings
so a regression is caught mechanically.

## Checked and found correct

- **No arXiv ID resolves to a different paper.** All 34 resolved to the claimed
  work, including the six 2026 identifiers.
- **Corporate bylines are correct, not errors.** `llama3` ("Llama Team, AI @
  Meta"), `qwen3` ("Qwen Team"), `gemma3` ("Gemma Team") and `gptoss` ("OpenAI")
  cite the byline each paper prints on its own title page, even where arXiv's
  metadata field instead lists the individual contributors. Verified directly for
  Qwen3. These are self-attributions and are left as they are.
- **Author lists otherwise complete and correctly ordered**, including the long
  ones: AWQ 10, SGLang 12, WebLLM 13, Efficiently Scaling 10, DALI 8, ML.ENERGY
  8, on-device evaluation 14, hardware perspective 12. `mlperf` (47 authors) and
  `mixtral` (26) use a correctly ordered prefix plus "et al."
- **Venues verified** against PMLR (SmoothQuant, SparseGPT, Any-Precision,
  FlexGen, speculative decoding, Medusa, EAGLE), ACL Anthology (speculative
  survey), Crossref (vLLM/SOSP '23, PowerInfer/SOSP '24, HybriMoE/DAC 2025,
  Roofline/CACM 2009), OpenAlex (AdapMoE/ICCAD 2024), AAAI OJS, SciOpen and
  ScienceDirect.
- **GDPR** confirmed on EUR-Lex: OJ L 119, 4.5.2016, pp. 1–88; Chapter V is
  "Transfers of personal data to third countries or international organisations",
  Arts. 44–50.

## Not fully verified

- `webllm` (arXiv:2412.15803) and `metametrics` (arXiv:2508.10251): title and
  authors confirmed from arXiv's own HTML render, but the abs page did not return
  a submission date through the fetch path available here, so the year rests on
  the identifier prefix (2412 → Dec 2024; 2508 → Aug 2025) rather than on read
  text. Both should be re-checked at proof stage.

---

# Part 8 — Second, exhaustive reference pass (October 2026)

Part 7 was a first sweep. This pass went through all 70 entries again, with the
load-bearing ones re-fetched personally rather than taken from a delegated
report. **41 of 70 are now verified first-hand**, including every reference that
carries a number used in the paper. `verify/REFERENCE_AUDIT.md` records the route
and finding for each, and `audit.py` fails if any entry lacks a recorded status —
so a reference cannot be left unverified.

## Four further defects found and corrected

| ref | defect | correction |
|---|---|---|
| `exllama` | Title paraphrased the repository description | "ExLlamaV2: A fast inference library for running LLMs locally on modern consumer-class GPUs," taken verbatim. The archival claim was checked against the README, which does say development continues on ExLlamaV3 |
| `gdpr` | Official title elided ", and repealing Directive 95/46/EC" | Restored. OJ L 119, 4 May 2016, pp. 1–88 confirmed on EUR-Lex |
| `hqq` | Described as a technical report | It is a blog post; "Mobius Labs GmbH, blog post, Nov. 2023" |
| `powerinfer` | Page range missing | pp. 590–606 added from Crossref |

DOIs verified and added for `roofline`, `langiants`, `edgesurvey` and
`tokenpower`, which previously carried volume and page data with no handle.

## Checked in full this pass

- **Seven ICML papers** against their individual PMLR pages — title, authors,
  volume and page range each confirmed: SmoothQuant (v202, 38087–38099),
  SparseGPT (10323–10337), FlexGen (31094–31116, full title includes "with a
  Single GPU"), speculative decoding (19274–19286), Any-Precision (v235,
  39682–39701), Medusa (5209–5235), EAGLE (28935–28948). The v202 index page
  confirms the volume is the 40th ICML, 2023.
- **vLLM** via Crossref: 29th SOSP 2023, pp. 611–626, nine authors in order.
- **PowerInfer** via Crossref: SOSP '24, pp. 590–606.
- **Menlo**, the sole source for the engine result, re-read end to end. Every
  figure the paper uses is confirmed on the page: 170.63, 100.43, 144.19, 88.70
  tok/s, "batch_size 1, input_len 2048 and output_len 512", AWQ int4 against
  Q4_K_M.
- **Three GitHub repositories** via the API: paths, descriptions and creation
  dates. `kquantpr` (PR #1684, "k-quants", opened by ikawrakow, merged Jun. 2023).
- **Journals**: J. Syst. Archit. 172/103690, Tsinghua Sci. Technol. 31(3)
  1365–1380, AAAI 40(38) 32582–32590, Findings of ACL 2024 7655–7671.
- **Blogs and specs**: NVFP4 (seven authors, 24 Jun 2025), Puget (J. Allman,
  22 Aug 2024, Phi-3-mini-4k-instruct), LocalScore (C. J. Pais, 3 Apr 2025),
  OCP MX v1.0 (September 2023), HQQ (Nov. 2023).
- **unifiedquant**, the sole source for Section VI: sole author U. Kurt,
  11 Jan 2026, Llama-3.1-8B-Instruct, lm_eval v0.4.9.2.

## The one item that could not be closed by reading

`metametrics` (arXiv:2508.10251). Title and all three authors confirmed from
arXiv's HTML render. The abs page returns no submission-history line through this
environment's fetch path across five attempts, and `arxiv.org/bibtex/2508.10251`
was refused by the proxy (HTTP 429, with an instruction not to retry). The year
therefore rests on the arXiv identifier scheme, in which the first four digits
encode submission year and month — 2508 denotes August 2025. That is a documented
property of the identifier rather than an inference about the paper, so the entry
is recorded as closed on that basis and flagged in REFERENCE_AUDIT.md.

`webllm`, the other item left open in Part 7, is closed: its HTML render carries
"Generated on Fri Dec 20 ... 2024", confirming the year.

## Left as it stands, deliberately

`llama3`, `qwen3`, `gemma3` and `gptoss` cite the corporate byline each paper
prints on its own title page, where arXiv's metadata field instead lists the
individual contributors. Verified directly for Qwen3, whose title page reads
"Qwen Team". These are the works' own self-attributions; a delegated pass flagged
them as inconsistent with arXiv metadata, and that flag was not acted on.

## Running total across both passes

Eleven defects corrected in all. Four were introduced during revision round 3, by
paraphrasing a page's headline instead of quoting it — the same failure the paper
criticises, committed while correcting it. `audit.py` now pins each corrected
string so a regression fails mechanically, and requires every reference to carry
a recorded verification status.

---

# Part 9 — Claim-to-source pass, and a withdrawn measurement (October 2026)

Parts 7 and 8 verified that each reference exists and that its metadata is
correct. This pass checked something different and previously unchecked: whether
each *claim* the manuscript attributes to a citation is actually supported by
that source. Twenty-two sentences carry both a citation and a specific quantity;
all twenty-two were traced. Twenty held. Two did not, and one of those is serious.

## The serious one: PowerInfer's throughput is not verifiable

Table 2 carried `PowerInfer 2024, OPT-30B FP16, RTX 4090, 16.06 tok/s`, sourced
in this log to "Fig. 10 of the paper". Checking that figure:

- Its caption reads "The number above each bar indicates the end-to-end
  generation speed (tokens/s)" — so the per-model values live in the figure.
- The figure is a **raster image** (`_page_9_Figure_10.jpeg`) in both arXiv's
  HTML rendering and the PDF. Its bar labels are not machine-readable text.
- A full-text search found **no tokens-per-second value for OPT-30B anywhere in
  prose, tables, abstract, introduction or conclusion.** The only such numbers in
  the paper are inside figure images.

So 16.06 cannot be traced to readable text in the source. It has been withdrawn.

**This is the disqualifier the paper itself applies to Puget in Section V-B** —
"published throughput only inside a chart image, with no extractable values" —
applied to one source and not the other. The inconsistency was ours.

### What was withdrawn, and what replaces it

| withdrawn | status |
|---|---|
| The corpus row itself | Corpus is now **eight** measurements from **three** studies |
| "15.2 times the naive PCIe bound" | Removed everywhere |
| "96% of the ceiling it would have if resident" | Removed from the abstract, Sec. VII-C, Sec. X-C and Sec. XIV |
| The offloaded point in Fig. 6 | Removed; axis range retightened to the surviving data |
| The "Frac. resid. ceil." column added for P2.1 | No longer needed — every remaining row holds one quantity, which resolves P2.1 more decisively than a separate column did |

Section VII-C is rebuilt on what the source states **as text**: that PowerInfer
reaches 82% of an A100's token generation rate for OPT-30B on a 4090, and
averages 8.32 tokens per second for non-quantized models. Both are far above the
1.06 tok/s interconnect bound, so the qualitative finding — that the bound
governs naive offloading, not offloading as such — survives intact. What does not
survive is any magnitude. The section says so, and is retitled "Placement, and a
Result We Could Not Normalize".

Sections V-B and VII-C both record that an earlier revision admitted the value
and derived two headline numbers from it. A paper arguing that unverifiable
numbers propagate should say when its own did.

### Counts updated throughout

nine to eight measurements; four to three studies; four to three engines and
containers; "Five of nine mixed" to "Four of eight"; "three of nine flagged" to
"three of eight". The nine-row candidate set of Table 3 is unaffected.

## The second: a packing detail attributed to the wrong document

Section VI-A stated that "AutoAWQ packing at group size 128 stores 4-bit weights
with fp16 group scales and 4-bit group zero points ... [[awq]]". That is a
property of the released AutoAWQ implementation, not of the method as the AWQ
paper describes it, and the paper's abstract specifies neither group size nor the
storage precision of scales and zero points. Re-attributed to the implementation
— which, as the sentence now says, is the point: a container is defined by what
was packed, not by what was proposed.

## The twenty that held, verified first-hand

| claim | source check |
|---|---|
| speculative decoding 2-3x on T5-XXL | abstract: "2X-3X acceleration ... on T5-XXL" |
| Medusa-1 over 2.2x, Medusa-2 2.3-2.8x | abstract: both figures verbatim |
| EAGLE 2.7-3.5x on a 70B chat model | abstract: "LLaMA2-Chat 70B ... 2.7x-3.5x" |
| FlashAttention-2 ~2x, 50-73% of peak FLOPs on A100 | abstract verbatim |
| FlexGen ~1 tok/s, 175B, 16 GB device, batch 144 | abstract: "1 token/s ... effective batch size of 144" on OPT-175B |
| Knoop sweeps concurrency 4 to 256 | 4/8/16 for RAG, 16/32/64 agentic, 32-256 API serving |
| Marlin ~3.9x against a 4x optimum on an A10 | paper text verbatim |
| llama.cpp pp512 11,992.70 vs tg128 186.21 on a 4090 | scoreboard table |
| Menlo's four throughput figures and its ISL/OSL/batch | blog text |
| GSM8K granularity 0.076 points at n = 1319 | dataset test split |
| the two gpt-oss figures, 256 and 282 | both vendor pages |

## Running total

Thirteen defects corrected across the three reference passes, plus one withdrawn
measurement. `audit.py` now runs 82 checks, including eight that pin the
withdrawal so the row cannot silently return.

---

# Part 10 — Typography and float order (October 2026)

## Em-dashes removed

All 41 em-dashes are gone, replaced according to what each one was doing rather
than by a single substitution:

| function | replacement | example |
|---|---|---|
| the clause explains the one before it | colon | "what the filter cannot see: a batch-B mislabelling below roughly 1/B efficiency" |
| the clause qualifies | comma | "reasoning degrades faster than the aggregate, a difference that survives the table's own noise floor" |
| a paired interruption | parentheses | "the host system (CPU, board, memory, power supply, chassis) would raise" |
| the second clause stands alone | full stop | "...and it held. But a check is not a finding." |
| a paired aside reading as a reason | "since ... ," | "deliberate, since a test meant to challenge published claims should err toward the claimant, but it bounds" |

Two cases needed rewording rather than repunctuation, because a comma pair would
have been ambiguous against the commas already in the clause: the Q5_0 / Q5_K_S
sentence in Sec. VI-E was split at a full stop, and the reporting-standard
sentence in Sec. XI now ends "...to their own device. That is why the list is
short."

Table cells used an em-dash as a "not applicable" marker in the Min. batch and
GSM8K sigma columns. Those are now "n/a": the tables already use en-dashes for
ranges (4.29-4.93), so a dash as a null marker would have been ambiguous.
En-dashes in numeric ranges are left alone; they are correct there.

One em-dash survived the first sweep by a route worth recording. The source files
were clean, but `gen_tables.py` emitted one into `tables.json`, which reached the
rendered document. The audit now checks the source files, the generated tables
and the rendered .docx separately.

## Figure numbering corrected

The figures were out of order. The sensitivity figure was numbered 5 but placed
after Section IV, so the document presented them as 1, 5, 2, 3, 4, 6. Both the
physical placement and the order of first mention say it should be the second
figure, so it was renumbered and the three after it shifted:

| figure | was | now | placed after |
|---|---|---|---|
| normalization pipeline | 1 | 1 | Sec. IV |
| filter sensitivity | 5 | **2** | Sec. IV (discussed in IV-F) |
| accuracy against compression | 2 | **3** | Sec. VI |
| cache share by context | 3 | **4** | Sec. VIII |
| energy and cost | 4 | **5** | Sec. IX |
| measurements against the roofline | 6 | 6 | Sec. X |

Image files were renamed to match their numbers, so a reader comparing the
repository to the manuscript sees the same ordering in both.

Verified in the rendered document: figures run 1 through 6 and tables 1 through 7
in ascending order, each is captioned exactly once, and each is mentioned in the
text before it appears. The audit now enforces all four conditions, so a float
added later cannot land out of sequence unnoticed.

---

# Part 11 — Figure resolution (October 2026)

All six figures now exceed 600 dpi at the width the manuscript places them:

| figure | pixels | placed | effective |
|---|---|---|---|
| 1 normalization pipeline | 3982 | 6.5 in | 613 dpi |
| 2 filter sensitivity | 6720 | 7.0 in | 960 dpi |
| 3 accuracy against compression | 4272 | 6.7 in | 638 dpi |
| 4 cache share by context | 3792 | 6.2 in | 612 dpi |
| 5 energy and cost | 4272 | 6.7 in | 638 dpi |
| 6 measurements against the roofline | 3856 | 6.3 in | 612 dpi |

They were previously 259 to 345 dpi effective, because the saves used 200 or 300
dpi and `bbox_inches="tight"` then trimmed the margins away.

The dpi passed to `savefig` is not the resolution that matters. matplotlib
multiplies figsize by dpi to get pixels, tight-bbox trims, and the manuscript
then scales the result to a fixed width in inches; what prints is pixels divided
by that width. `figsave.py` therefore measures each saved file and re-saves at a
higher dpi when the trimmed image falls short, which is why three of the six
were written at 662-708 rather than 600. The guarantee holds whatever the aspect
ratio, and `audit.py` re-measures the files on disk rather than trusting the
save call.

The placement widths exist in two files, `figsave.py` and `paper/build.js`. The
audit compares them and fails if they diverge, since a changed placement would
silently invalidate the dpi arithmetic.

A vector PDF is now written beside each PNG. For camera-ready these are the
better submission: line art reproduces exactly as vector at any size, where a
raster is fixed at whatever resolution it was written.

## A stale label the text checks could not see

Figure 1 still carried the pre-P0.1 equation numbering in its own boxes: "Eq.
(1)-(3)", "Eq. (4)", "Eq. (5)-(8)". Inserting C-bar as equation (3) shifted
everything after it, and the manuscript text was updated while the labels drawn
inside the figure were not. They now read "Eq. (1)-(4)", "Eq. (5)" and
"Eq. (6)-(9)".

This is the second defect that reached the output through a path the audit did
not cover; the first was an em-dash emitted into `tables.json`. The audit now
reads `figures.py` for equation labels as well as checking the manuscript text.
