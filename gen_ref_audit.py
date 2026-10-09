#!/usr/bin/env python3
"""Generate verify/REFERENCE_AUDIT.md -- a per-reference verification record.

Every entry in paper/refs.js must appear here with a status and the route by
which it was checked. audit.py enforces that: a reference with no recorded
status fails the build-time audit, so none can be left unverified.

ROUTES
  direct   fetched and compared against the entry in this session, by me
  deleg    fetched by a delegated verification pass; every item it flagged was
           then re-fetched and adjudicated directly, and the unflagged remainder
           rests on that pass
"""
import re, pathlib, datetime

R = pathlib.Path("/home/claude/review")
refs = dict(re.findall(r"^([A-Za-z0-9_]+):\s*`(.+?)`,\s*$",
                       (R/"paper"/"refs.js").read_text(), re.M))

# key -> (route, authority consulted, note)
S = {
 # ---- corrected this session ------------------------------------------------
 "awq":      ("direct","arxiv.org/abs/2306.00978","CORRECTED: title carried 'on-device', which is not in the paper's title"),
 "zahl":     ("direct","arxiv.org/abs/2608.00008","CORRECTED: four authors (Zahl, Dalipaj, Hennig, Bayer), not two; Hennig is third"),
 "lmeval":   ("direct","github.com/EleutherAI/lm-evaluation-harness","CORRECTED: title and year came from two different Zenodo records; now matches the repo's own BibTeX (v0.4.3)"),
 "marlin":   ("direct","arxiv.org/abs/2408.11743","CORRECTED: was cited as a GitHub repo with two authors; now the paper, five authors. Figure changed to the paper's own ~3.9x"),
 "nvidiaoss":("direct","blogs.nvidia.com H1","CORRECTED: headline had been paraphrased. HTML <title> and on-page H1 differ; the H1 is cited"),
 "techradar":("direct","techradar.com H1","CORRECTED: title had been invented; real headline and date (Oct. 20, 2025) substituted"),
 "hwcorner": ("direct","hardware-corner.net H1","CORRECTED: title paraphrased, byline and date missing; now A. Witt, Dec. 9, 2025"),
 "exllama":  ("direct","github.com/turboderp-org/exllamav2","CORRECTED: title paraphrased the repo description; archival note verified against the README"),
 "hqq":      ("direct","mobiusml.github.io/hqq_blog","CORRECTED: a blog post, not a technical report; month added"),
 "gdpr":     ("direct","eur-lex.europa.eu/eli/reg/2016/679","CORRECTED: official title restored the 'repealing Directive 95/46/EC' clause. OJ L 119, 4 May 2016, pp. 1-88 confirmed"),
 "llamacppbench":("direct","github.com discussion 15013","CORRECTED: thread opener attributed; 'Nvidia' capitalised as the thread titles it"),
 "powerinfer":("direct","Crossref 10.1145/3694715.3695964 + arxiv.org/html/2312.12456v2","page range 590-606 added; SOSP '24, four authors confirmed. SEPARATELY: the OPT-30B throughput this paper once took from Fig. 10 is NOT verifiable — the figure is a raster image in both the HTML render and the PDF, and no tokens-per-second value for OPT-30B appears as text anywhere in the source. The measurement was withdrawn from the corpus; see Sec. VII-C"),
 "roofline": ("direct","Crossref 10.1145/1498765.1498785","DOI added; Commun. ACM 52(4), 65-76, 2009 confirmed"),
 "langiants":("direct","ScienceDirect S1383762126000081","DOI added; J. Syst. Archit. 172, art. 103690, 2026 and all seven authors confirmed"),
 "edgesurvey":("direct","sciopen.com 10.26599/TST.2025.9010166","DOI added; vol. 31 no. 3, 1365-1380, 2026 confirmed"),
 "tokenpower":("direct","ojs.aaai.org article 40535","DOI added; vol. 40 no. 38, 32582-32590, 2026 confirmed"),
 # ---- verified first-hand, no change needed ---------------------------------
 "menlo":    ("direct","menlo.ai blog","every figure used in the paper confirmed: 170.63 / 100.43 / 144.19 / 88.70, batch_size 1, input_len 2048, output_len 512, AWQ int4 vs Q4_K_M"),
 "knoop":    ("direct","arxiv.org/abs/2601.09527 + HTML","ISL 8192 / OSL 512, concurrency 8, and the 'total output tokens per second (global TPS)' metric definition confirmed"),
 "unifiedquant":("direct","arxiv.org/abs/2601.14277 + HTML","sole author U. Kurt, 11 Jan 2026; lm_eval v0.4.9.2 and the five task metrics confirmed from the methodology section"),
 "kquantpr": ("direct","github.com/ggml-org/llama.cpp/pull/1684","title 'k-quants', opened by ikawrakow, merged Jun. 2023"),
 "puget":    ("direct","pugetsystems.com","J. Allman, 22 Aug 2024; Phi-3-mini-4k-instruct 4-bit GGUF, pp512 / tg128, 25 repetitions"),
 "vllm":     ("direct","Crossref 10.1145/3600006.3613165","29th SOSP 2023, pp. 611-626, nine authors in order"),
 "smoothquant":("direct","proceedings.mlr.press/v202/xiao23c","40th ICML, PMLR 202, pp. 38087-38099, six authors"),
 "sparsegpt":("direct","proceedings.mlr.press/v202/frantar23a","PMLR 202, pp. 10323-10337"),
 "flexgen":  ("direct","proceedings.mlr.press/v202/sheng23a","PMLR 202, pp. 31094-31116; full title includes 'with a Single GPU'"),
 "specdec":  ("direct","proceedings.mlr.press/v202/leviathan23a","PMLR 202, pp. 19274-19286"),
 "anyprecision":("direct","proceedings.mlr.press/v235/park24e","41st ICML, PMLR 235, pp. 39682-39701"),
 "medusa":   ("direct","proceedings.mlr.press/v235/cai24b","PMLR 235, pp. 5209-5235, seven authors"),
 "eagle":    ("direct","proceedings.mlr.press/v235/li24bt","PMLR 235, pp. 28935-28948"),
 "specsurvey":("direct","aclanthology.org/2024.findings-acl.456","Findings of ACL 2024, pp. 7655-7671, nine authors"),
 "nvfp4":    ("direct","developer.nvidia.com blog","headline, seven authors in order, 24 Jun 2025"),
 "nvidiablog":("direct","developer.nvidia.com blog","headline and date confirmed; the ~150 tok/s figure, ISL/OSL 100/100 and the absence of batch and phase confirmed"),
 "llamacpp": ("direct","api.github.com/repos/ggml-org/llama.cpp","description verbatim 'LLM inference in C/C++', created 2023-03-10"),
 "trtllm":   ("direct","api.github.com/repos/NVIDIA/TensorRT-LLM","path and owner confirmed, created 2023-08-16"),
 "ocpmx":    ("direct","opencompute.org","title and version 1.0, September 2023"),
 "localscore":("direct","localscore.ai/blog","C. J. Pais, 3 Apr 2025, 'A Mozilla Builders Project'"),
 "gemma3":   ("direct","arxiv.org/abs/2503.19786 + config.json","'Gemma Team' heads the author field; sliding_window 1024 and pattern 6 read from the published config"),
 "gptoss":   ("direct","arxiv.org/abs/2508.10925 + model card","'OpenAI' is the author field; 21B/3.6B and 117B/5.1B read from the card; MXFP4 scope read from config.json"),
 "qwen3moe": ("direct","huggingface.co/Qwen/Qwen3-30B-A3B","config.json dimensions confirm 30.5B total / 3.3B active"),
 "qwen3":    ("direct","arxiv.org/html/2505.09388v1","'Qwen Team' is the byline the paper prints on its own title page; arXiv metadata instead lists 62 individuals"),
 "webllm":   ("direct","arxiv.org/html/2412.15803v1","title and 13 authors confirmed; year established from the render stamp 'Generated on Fri Dec 20 ... 2024'"),
 # ---- delegated pass, nothing flagged ---------------------------------------
 "gptq":("deleg","arxiv.org/abs/2210.17323",""), "llmint8":("deleg","arxiv.org/abs/2208.07339",""),
 "moqe":("deleg","arxiv.org/abs/2310.02410",""), "flashattn2":("deleg","arxiv.org/abs/2307.08691",""),
 "sglang":("deleg","arxiv.org/abs/2312.07104","12 authors confirmed in order"),
 "moeoffload":("deleg","arxiv.org/abs/2312.17238",""), "moeinfinity":("deleg","arxiv.org/abs/2401.14361","title double-fetched"),
 "fiddler":("deleg","arxiv.org/abs/2402.07033",""), "dali":("deleg","arxiv.org/abs/2602.03495","eight authors confirmed in order"),
 "zeroinfinity":("deleg","arxiv.org/abs/2104.07857",""), "scalinginf":("deleg","arxiv.org/abs/2211.05102","10 authors confirmed"),
 "eagle3":("deleg","arxiv.org/abs/2503.01840",""), "zeus":("deleg","arxiv.org/abs/2208.06102",""),
 "mlenergy":("deleg","arxiv.org/abs/2505.06371","eight authors confirmed"),
 "joules":("deleg","arxiv.org/abs/2601.22076",""), "reqenergy":("deleg","arxiv.org/abs/2608.28044",""),
 "ondeviceeval":("deleg","arxiv.org/abs/2505.15030","14 authors confirmed"),
 "ondevicereview":("deleg","arxiv.org/abs/2409.00088","submitted 26 Aug 2024; identifier prefix is 2409"),
 "hwperspective":("deleg","arxiv.org/abs/2410.04466","12 authors confirmed"),
 "rooflinebench":("deleg","arxiv.org/html/2602.11506v1","abs page unreadable; title, seven authors and date from the HTML render"),
 "mlperf":("deleg","arxiv.org/abs/1911.02549","47 authors; cited prefix of 10 plus et al. is correct and in order"),
 "nondeterminism":("deleg","arxiv.org/abs/2506.09501","10 authors confirmed"),
 "metametrics":("deleg","arxiv.org/html/2508.10251v1","title and three authors confirmed from the HTML render. The abs page returns no submission-history line through this environment's fetch path and arxiv.org/bibtex/2508.10251 was refused by the proxy (HTTP 429, no retry), so the year rests on the arXiv identifier scheme, in which 2508 denotes August 2025"),
 "llama3":("deleg","arxiv.org/abs/2407.21783","'Llama Team, AI @ Meta' is the paper's own byline; arXiv metadata lists individuals"),
 "mixtral":("deleg","arxiv.org/abs/2401.04088","26 authors; cited prefix of seven plus et al. is correct"),
 "hybrimoe":("deleg","Crossref 10.1109/DAC63849.2025.11132676","62nd ACM/IEEE DAC 2025, six authors"),
 "adapmoe":("deleg","OpenAlex / ICCAD 2024","43rd IEEE/ACM ICCAD 2024, six authors"),
 "mlperfclient":("deleg","mlcommons.org/benchmarks/client","v1.0 released Jul 2025"),
 "mobilesurvey":("deleg","ScienceOpen 10.14293/PR2199.003569.v1","sole author S. Katakam, 16 May 2026"),
}

missing = sorted(set(refs) - set(S))
extra   = sorted(set(S) - set(refs))
if missing: raise SystemExit(f"references with no recorded verification status: {missing}")
if extra:   raise SystemExit(f"status recorded for references that no longer exist: {extra}")

corrected = [k for k,(r,a,n) in S.items() if n.startswith("CORRECTED")]
direct    = [k for k,(r,a,n) in S.items() if r=="direct"]

out = [f"# Reference audit\n",
 f"Generated by `gen_ref_audit.py` on {datetime.date.today().isoformat()}. "
 f"Every one of the **{len(refs)}** entries in `paper/refs.js` appears below with a "
 f"verification status; `audit.py` fails if any entry is missing from this record, "
 f"so no reference can be left unverified.\n",
 f"- **{len(direct)}** verified first-hand against the primary source in this session",
 f"- **{len(refs)-len(direct)}** verified by a delegated fetch pass; every item it "
 f"flagged was then re-fetched and adjudicated directly",
 f"- **{len(corrected)}** carried a defect and were corrected: "
 f"{', '.join('`'+k+'`' for k in sorted(corrected))}\n",
 "No arXiv identifier resolves to a different paper. No entry is uncited, and no "
 "citation refers to an undefined entry; `build.js` enforces both, and also refuses "
 "a duplicated key after one was found silently overwriting another.\n",
 "| key | route | authority consulted | finding |", "|---|---|---|---|"]
for k in sorted(refs):
    route, auth, note = S[k]
    out.append(f"| `{k}` | {route} | {auth} | {note or 'matches the entry'} |")
out += ["", "## Entries whose year rests on the arXiv identifier scheme", "",
 "arXiv identifiers encode submission year and month in their first four digits. "
 "Where a submission-history line could not be read through this environment's fetch "
 "path, that scheme is the basis for the year, and it is noted in the table above. "
 "This affects `metametrics` only; `webllm` was closed from its render stamp.",
 "", "## Convention retained deliberately", "",
 "`llama3`, `qwen3`, `gemma3` and `gptoss` are cited by the corporate byline each "
 "paper prints on its own title page, even where arXiv's author metadata instead "
 "lists the individual contributors. Verified directly for Qwen3. These are the "
 "works' own self-attributions and are left as they stand."]
(R/"verify"/"REFERENCE_AUDIT.md").write_text("\n".join(out)+"\n")
print(f"wrote verify/REFERENCE_AUDIT.md -- {len(refs)} entries, "
      f"{len(direct)} first-hand, {len(corrected)} corrected")
