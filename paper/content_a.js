// Manuscript part A: front matter, Sections I-V
module.exports = {
title: "Local LLM Inference on Consumer GPUs: A Memory-Traffic Normalization Framework for Comparable Benchmarks",

// TODO before submission: replace with real names, affiliations and e-mail.
// IEEE Access also requires a funding statement; if the work was unfunded, say
// so explicitly rather than omitting the block.
authors: "First Author, Second Author",
affil: "Department of Computer Engineering, University Name, City, Country",
corresponding: "Corresponding author: First Author (e-mail: author@university.edu).",
funding: "This work received no specific grant from any funding agency. [Replace or confirm before submission.]",
artifact: "The framework, the verified corpus, the table-generating scripts and the per-measurement verification record are available at https://github.com/ORG/REPO and archived at doi:10.5281/zenodo.XXXXXXX. [Replace both before submission.]",

abstract: `Large language model inference has moved onto consumer graphics cards, but the figures published about it are not comparable. Throughput is reported against undocumented batch sizes, context lengths, quantization containers and power states, so a claim that one engine is faster than another cannot be separated from the fact that it was measured on a different card at a different bit width. We call this the comparability gap and present a framework that closes it arithmetically: it computes the per-token memory traffic a configuration implies, honouring interleaved sliding-window attention and deriving each container's effective bits per weight from published artifacts rather than its name, then re-expresses any reported figure as Model Bandwidth Utilization, energy per token and amortized cost. Neither the roofline nor MBU is ours; what is new is using them to falsify the conditions a measurement claims, and a reporting standard that makes third-party normalization possible.

We separate what the resulting validity filter checks from what it finds. On a corpus of eight measurements verified against their primary sources it is a calibration: three imply traffic above their device's peak bandwidth, and the source documents all three as batched. Its findings come from the measurements that corpus had to exclude. Applied to nine widely circulated figures from four sources that omit a field the arithmetic needs, it returns no verdict at all on four: their admissible traffic ranges straddle the bandwidth bound, so the same published number is either unremarkable or physically impossible depending on information the source withholds. We also bound what the filter cannot see: a batch-B mislabelling below roughly 1/B efficiency.

Four further results follow from the same arithmetic. Normalization removes 12% of a controlled engine gap, leaving 1.58x (bounded to [1.49, 1.65] on decode alone), a correction small here only because the two containers measure 4.59 and 4.83 bits per weight. Offloading is bounded by the interconnect only when a system lets it be, but we report that result without a magnitude: the most-cited counterexample publishes its throughput only inside a figure image, so it fails our own inclusion rule and we withdraw the numbers an earlier revision derived from it. Quantization accuracy is near-free to roughly 4.6 bits and collapses below four, where reasoning degrades faster than the aggregate, a difference that survives the table's own noise floor only below 4.3 bits. And electricity is 21% of the true cost of a local token once hardware amortization at a realistic duty cycle is counted.`,

indexTerms: "Large language models, GPU inference, quantization, memory bandwidth, model bandwidth utilization, benchmarking methodology, energy efficiency.",

sections: [
{
h: "I. INTRODUCTION",
p: [
`Three claims about local large language model inference, each published and each defensible on its own terms. The same open model on the same RTX 5090 is reported at 256 tokens per second by one vendor-affiliated page [[nvidiaoss]] and at 282 by another [[techradar]]. A compiled engine [[trtllm]] is roughly 70 percent faster than a portable one [[llamacpp]] on an RTX 4090 [[menlo]]. A specialized kernel [[marlin]] delivers a tenfold speedup over a baseline on identical weights. Together they tell a practitioner choosing a stack almost nothing.`,

`They tell nothing because each is entangled with variables the reader cannot factor out. The first pair states neither batch size, nor sequence lengths, nor, on one of the two pages, which of two models of very different size produced the figure, and the traffic consistent with what they do state spans a factor of nearly seven, which is wider than the ten percent between them. The second compares builds at different precisions on different cards. The third, traced to its origin in Section VII-B, turns out to be a comparison against an unusually poor baseline kernel, while the kernel's own authors claim approximately 3.9x, which is precisely the memory-traffic bound. The numbers are correct. The comparisons are not.`,

`This is not a story about careless authors. It is structural. Tokens per second is not a property of an engine; it is a property of a tuple comprising the model architecture, the quantization container and its metadata overhead, the context length and cache precision, the batch size, the device's memory bandwidth, the sustained power state, and only then the engine and its kernels. Report the last element while silently varying the others and you produce a literature in which every system outperforms every other system, and in which no published figure transfers to anyone else's hardware. We call this the comparability gap.`,

`The gap matters because the migration it obscures has become consequential. Post-training quantization now reduces weight storage three- to fourfold at accuracy costs that, as Section VI shows with verified data, fall inside benchmark noise for most containers. Engines written for single-device execution have displaced general-purpose frameworks. Offloading systems stage weights across GPU memory, host memory and storage [[flexgen+powerinfer]]. A consumer card costing under a thousand dollars now sustains interactive generation from models that required a server two years ago, and practitioners make real commitments on the strength of published benchmarks.`,

`Those stakes extend beyond cost. Local inference keeps prompt content on the user's own hardware, which is decisive wherever data residency is a regulatory requirement rather than a preference. Chapter V of the General Data Protection Regulation conditions any transfer of personal data outside the European Economic Area on an adequacy decision or equivalent safeguards [[gdpr]], and sending a prompt to a third-party endpoint is such a transfer when the prompt contains personal data [[mobilesurvey]]. It removes per-token metering, network latency, and dependence on a third party's pricing and terms. A literature that cannot support comparison is therefore failing an audience that is both large and acting on its evidence.`,

`This paper makes four contributions.`,

`First, a normalization framework. Given a reported figure and the parameters that accompany it, the framework computes the per-token memory traffic the configuration implies, derives the device's bandwidth-bound ceiling, and re-expresses the figure as Model Bandwidth Utilization, bandwidth-normalized throughput, energy per token and amortized cost. Section IV specifies it. Its treatment of the key-value cache honours interleaved sliding-window attention [[gemma3]], which Section VIII shows changes long-context conclusions substantially.`,

`Second, a validity filter that falls out of the framework. Because MBU is bounded by unity for single-stream decoding, a computed MBU above one falsifies the conditions a measurement claims. Section V-C reports what it found.`,

`Third, five worked applications of the framework, each confined to measurements verified against their primary sources, and one of them, offloaded placement, reports what that confinement costs: the accuracy cost of quantization containers, the size of engine effects once containers are controlled, the behaviour of offloaded placement against two different ceilings, the capacity and context limits of consumer hardware, and the true energy and cost of a locally generated token.`,

`Fourth, a minimum reporting standard: the specific fields a benchmark must publish for a third party to normalize it.`,

`A note on scope. This is a framework paper with a worked demonstration, not an exhaustive survey. Section V states exactly how sources were selected and verified, and why we preferred a corpus small enough to verify completely over one large enough to look authoritative. That choice is itself a response to the problem the paper describes.`
]},

{
h: "II. RELATED WORK AND POSITIONING",
intro: [
`Two of the three ingredients in this paper are borrowed, and saying so precisely is the only way to make the third legible.`
],
sub: [
{h: "A. What Is Not New Here",
 p: [
`The roofline model is Williams, Waterman and Patterson's [[roofline]], and its application to transformer inference is well established: the observation that decoding is bandwidth-bound at low batch size, and that arithmetic intensity scales with batch size over bytes per parameter, is developed in [[scalinginf]] and is now standard. Model Bandwidth Utilization is likewise not ours. It has circulated as a serving metric since the industry benchmarking work that introduced it, and it is used in production inference tooling. We adopt both unchanged.`,

`Nor is the general project of benchmarking on-device inference new. RooflineBench [[rooflinebench]] is a benchmarking framework for on-device LLMs built explicitly on roofline analysis, and it is the closest prior work to this paper. Systematic evaluations of on-device quantization and resource use exist [[ondeviceeval]], as do surveys of edge inference [[edgesurvey]], hardware-perspective surveys of acceleration strategies [[hwperspective+langiants]], a comprehensive review of on-device language models [[ondevicereview]], and a survey of speculative decoding [[specsurvey]]. On the methodology side, [[metametrics]] sets out meta-metrics and best practices for system-level inference benchmarking, and the MLPerf line [[mlperf+mlperfclient]] and community efforts such as LocalScore [[localscore]] supply standardized harnesses.`
]},
{h: "B. What Is New Here",
 p: [
`Three things distinguish this work from that body, and we state them narrowly.`,

`First, the use of the roofline as a falsifier rather than a predictor. RooflineBench [[rooflinebench]] and the surveys above use roofline analysis to characterize achievable performance: given a device and a workload, what throughput should be expected. We invert the direction. Given a published figure and the conditions its authors state, we ask whether those conditions are consistent with the device's physical bound, and treat a computed utilization above unity as a falsification of the stated conditions rather than as a performance result. Section V-C shows this recovering, from public information alone, a measurement condition that the source records but the circulating number does not. We are not aware of prior work that uses the roofline this way, and we regard it as the most defensible novel element of the paper.`,

`Second, a correction to benchmark practice on the key-value cache. The arithmetic of equation (2) is not new: llama.cpp, vLLM and HuggingFace Transformers all allocate windowed caches correctly, and the Gemma 3 technical report presents the saving as a headline result of its own [[gemma3]]. What is not done is carrying it into the cache term of a published memory or throughput estimate, where the full-attention formula remains the default. Gemma 3 interleaves one global layer per five local layers with a 1024-token window, and equation (2) accounts for this. Section VIII-B shows that applying the standard formula to Gemma-3-12B at 32k context overstates its cache by a factor of 5.2 and its total footprint by 1.95 at Q4_K_M, and inverts the ranking of models by long-context memory demand. This is a concrete, checkable correction rather than a framing.`,

`Third, a reporting standard aimed specifically at third-party normalizability. Here the overlap with [[metametrics]] is real and we do not claim otherwise: that work also argues for disciplined reporting. The difference is the criterion. Their fields serve reproducibility, meaning that another laboratory running the same harness should obtain the same number. Ours serve portability: a reader with no access to the hardware should be able to convert the published figure to their own device. The field list in Section XI is derived from exactly what equations (1) through (8) consume, which is why it includes effective bits per weight measured from artifact size and the attention pattern, and why it is shorter than a reproducibility checklist.`
]}
]},

{
h: "III. WHY DECODING IS MEMORY-BOUND",
p: [
`One physical fact underlies everything that follows: autoregressive decoding is memory-bandwidth-bound at low batch sizes [[roofline+scalinginf]]. Emitting a single token requires a forward pass that reads every weight the computation touches and performs roughly two floating-point operations per weight read. Arithmetic intensity is therefore approximately batch size divided by bytes per parameter, about 0.5 FLOPs per byte at batch one in BF16. Modern accelerators have ridge points two to three orders of magnitude higher. During single-stream decoding the matrix engines idle through the overwhelming majority of cycles, waiting on weights.`,

`Two consequences structure this paper. Decode throughput scales with memory bandwidth rather than compute, so consumer GPUs should be compared on bandwidth rather than on the TFLOPS figures their marketing foregrounds. And any technique that reduces bytes read per token, whether by narrowing the weight representation, activating fewer parameters, capping what the cache must hold, or producing more than one token per weight sweep, translates almost linearly into throughput, while techniques that accelerate arithmetic do not.`,

`Prefill inverts this. Processing a prompt of several hundred tokens amortizes one weight sweep across all of them, raising arithmetic intensity by the prompt length and pushing prefill into the compute-bound region. A study that reports a single throughput number without separating the phases has therefore averaged two regimes with opposite bottlenecks. Section V-B shows that this ambiguity is present in sources that are otherwise carefully documented.`,

`The framework in Section IV is the arithmetic consequence of this fact. If decode throughput is set by how many bytes must move, then computing those bytes converts any reported rate into a fraction of what the hardware can physically deliver, and that fraction is comparable where the rate is not.`
]},

{
h: "IV. THE NORMALIZATION FRAMEWORK",
intro: [
`Fig. 1 shows the pipeline. A reported figure enters with whatever parameters its source provides; three computed stages convert it to a device-independent basis; a validity filter tests whether the stated conditions can be true.`
],
sub: [
{h: "A. Per-Token Memory Traffic",
 p: [
`Let a model have P total parameters, of which P_act are activated per token; for dense models P_act equals P, while for sparsely activated mixture-of-experts models [[mixtral+gptoss]] it sums the always-active parameters and the routed experts selected for that token. Let b denote the effective bits per weight of the container. Weight traffic per decoded token is then`
],
eq: ["B_w  =  P_act  ×  b / 8      (1)"],
p2: [
`Effective, not nominal. A container described as "4-bit" is never 4.00 bits in practice. We derive b from published artifact sizes rather than assuming it: Section VI-A reports values obtained from two independent sources [[kquantpr+unifiedquant]] that agree to 0.03 bits. On that basis Q4_K_M measures 4.89 bits per weight on Llama-3.1-8B and Q4_0 measures 4.64, while the AWQ build of Mistral-7B used in Section VII-A measures 4.59. Treating all three as "4-bit" introduces errors above 15% in the traffic calculation, which is larger than several of the inter-engine differences the literature reports. The same container also measures differently on different models, for reasons Section VI-A sets out, which is why we measure the exact model-container pair wherever its artifact is published.`,

`Key-value cache traffic must be added, and here the common formula is wrong for an increasingly important class of models. A model with L layers, H_kv key-value heads and head dimension d, at cache precision b_kv bits, adds 2·H_kv·d·(b_kv/8) bytes per layer per token. If every layer attends over the whole context, the cache after t tokens is that quantity times L·t. But Gemma 3 [[gemma3]] and similar architectures interleave attention: one full-attention layer every p layers, with the remaining layers capping their cache at a sliding window w. The cache held at context C is then`
],
eq2: ["B_kv(C)  =  2·H_kv·d·(b_kv/8) · [ n_full·C  +  n_local·min(C, w) ]      (2)"],
p3: [
`with n_full = L/p and n_local = L − n_full. Past the window, only the full-attention layers keep growing, so the cache grows at a fraction n_full/L of the naive rate. Section VIII-B quantifies what the naive formula costs.`,

`Equation (2) gives the cache held at a given depth. What a decode step actually pays is the cache at its own depth, because attention re-reads the whole live cache every step. A run is therefore not characterised by its final context but by its mean cache occupancy. Writing L_p for the prompt length and L_g for the number of tokens generated, the cache is already L_p deep when the first token is decoded and grows to L_p + L_g by the last, so its mean depth over the run is`
],
eq3: ["C̄  =  L_p  +  L_g / 2      (3)"],
p4: [
`and total memory traffic per decoded token is the cache evaluated at that depth, added to the weight traffic:`
],
eq4: ["B_tok  =  B_w  +  B_kv(C̄)      (4)"],
p5: [
`The averaging over the generation happens once, in equation (3). Equation (4) must not halve again. We note this because the arithmetic invites the error: the familiar statement that a cache growing from zero to C has mean size C/2 is true only of a prompt-free generation, and no measurement in circulation is prompt-free. On a prompt-heavy workload the ramp starts at L_p rather than at zero, and halving a quantity that is already a mean understates cache traffic by a factor approaching two. An earlier version of this manuscript made exactly that mistake; Section V-C records how the regression test that now guards equation (4) is constructed.`,

`Equations (3) and (4) together expose a dependency the literature routinely suppresses: per-token traffic is a function of how full the cache is, not of the context the model was configured to allow. A figure measured with a 512-token prompt and one measured with a 32,768-token prompt describe different workloads on the same model, and a figure reported against a configured maximum context describes neither.`
]},
{h: "B. Ceiling and Model Bandwidth Utilization",
 p: [
`Given a device with peak memory bandwidth BW, the bandwidth-bound ceiling on decode throughput at batch one is`
],
eq: ["T_max  =  BW / B_tok      (5)"],
p2: [
`and the Model Bandwidth Utilization achieved by a reported throughput T is`
],
eq2: ["MBU  =  T / T_max  =  T · B_tok / BW      (6)"],
p3: [
`MBU is dimensionless, bounded above by unity for true batch-1 decoding, and directly interpretable: the fraction of the device's memory system that the software stack manages to keep busy. Two configurations with equal MBU extract equal efficiency from their respective hardware, whatever their absolute token rates.`,

`We use the vendor's peak bandwidth for BW throughout. Achievable bandwidth is typically 80 to 90 percent of peak, so every MBU here is systematically low by roughly that margin. The effect is one-directional and nearly constant, so comparisons between rows are unaffected; Section XII returns to what it means for the filter.`,

`Which BW applies depends on residency. If the working set fits in VRAM, BW is the card's memory bandwidth. If it does not, the naive expectation is that BW becomes the interconnect's, since weights must cross PCIe each sweep. Section VII-C shows that this naive bound is not destiny, which is why both ceilings are worth computing.`
]},
{h: "C. Bandwidth-Normalized Throughput",
 p: [
`MBU normalizes away both device and container, which for some purposes is too much. A reader choosing hardware wants to know how many tokens per second a card delivers for a given model, controlling only for the card. We therefore also report bandwidth-normalized throughput, T divided by bandwidth in terabytes per second, which removes the device's bandwidth advantage while preserving the effect of container and stack. Reporting both separates the two questions practitioners actually ask: which stack is more efficient, and which card is the better purchase.`
]},
{h: "D. Energy and Cost",
 p: [
`Energy per token follows from throughput and sustained board power:`
],
eq: ["E_tok  =  P_sustained / T      (7)"],
p2: [
`Equation (7) is an approximation, not an identity, and Section IX-A shows where it departs from measurement: it recovers decode energy only, while a source that integrates power over the whole inference window also captures prefill. We use measured energy in preference to (7) wherever a source reports it. Cost per million tokens is the quantity this literature reports most misleadingly. Studies advocating local deployment frequently compute cost as electricity alone, producing figures of a few cents per million tokens. The arithmetic is correct; the accounting is not. It omits the capital cost of the hardware, which for an intermittently used consumer card is the dominant term. We therefore decompose:`
],
eq2: ["C_elec  =  (E_tok · 10⁶ / 3.6·10⁶) · p_kWh      (8)",
      "C_cap   =  M / (T · 3.156·10⁷ · y · u / 10⁶)      (9)"],
p3: [
`where p_kWh is the electricity price, M the acquisition cost, y the amortization horizon in years and u the duty cycle, the fraction of wall-clock time the card actually spends generating tokens. We adopt p_kWh = 0.16 USD, y = 3 years and u = 0.25 as a base case. The duty cycle is both the parameter that matters most and the one this literature almost never states.`
]},
{h: "E. The Validity Filter",
 p: [
`Equation (6) yields a falsifiable prediction. If a study reports single-stream decode throughput T for a configuration whose per-token traffic is B_tok on a device with bandwidth BW, then T·B_tok must not exceed BW. A measurement violating that bound is not evidence of an exceptional kernel. It is evidence that the measurement does not describe what its label claims.`,

`Three mechanisms produce such violations. Aggregate throughput across concurrent requests may be reported as single-stream. Prefill throughput may be reported as generation throughput, or the two averaged. Or speculative decoding [[specdec]] may be enabled, which emits several tokens per weight sweep and legitimately exceeds the batch-1 ceiling while no longer being batch-1 decoding in the sense the ceiling assumes.`,

`We apply the bound as a filter: measurements at or below unity enter pooled single-stream statistics; measurements above it are flagged, excluded, and reported separately with the minimum batch size that would reconcile them. Because BW is the vendor peak rather than the achievable bandwidth, the filter is conservative by construction: it will not raise a false alarm, but it can miss a violation that a stricter bandwidth figure would catch. For a test whose purpose is to challenge published claims, erring toward the claimant is the defensible direction. Section IV-F quantifies how much it misses.`
]},
{h: "F. How Much the Filter Can See",
 p: [
`A filter that is conservative by construction invites an obvious question the previous subsection does not answer: how large does a mislabelling have to be before it is noticed? The answer follows from (6) without any new assumption, and it is less flattering than the qualitative claim of conservatism suggests.`,

`Suppose a measurement was really taken at batch B with true per-stream efficiency \u03b7, the fraction of the batch-B aggregate ceiling actually achieved, and is then presented as single-stream. At batch B the weights are read once per sweep and shared across B streams while each stream keeps its own cache, so per-token traffic is B_w/B + B_kv. Writing r = B_kv/B_w for the cache share, a reader who normalizes the reported rate as batch one obtains`
],
eq: ["MBU_computed  =  \u03b7 \u00b7 (1 + r) / (1/B + r)      (10)"],
p2: [
`and the filter fires when that exceeds one, which happens when`
],
eq2: ["\u03b7  >  (1/B + r) / (1 + r).      (11)"],
p3: [
`Two consequences follow. With a negligible cache the threshold is \u03b7 > 1/B: a batch-two measurement is caught only if the run was better than fifty percent efficient, and a batch-four measurement only above twenty-five percent. Ordinary efficiencies at small batch sizes pass unnoticed. And as B grows the threshold does not fall to zero but to r/(1 + r), so a workload whose cache dominates its traffic can be batched arbitrarily and still escape. Long-context measurements are the filter's blind spot, and they are the ones becoming most common.`,

`Fig. 2 maps this plane for the cache share of the corpus's flagged configuration, r = 0.270, under both vendor peak and eighty-five percent achievable bandwidth. At that cache share the detection threshold is \u03b7 > 0.61 at batch two, \u03b7 > 0.41 at batch four and \u03b7 > 0.31 at batch eight. The three flagged rows imply true per-stream efficiencies of 0.42 to 0.47, which clears the batch-eight threshold by thirty-four to fifty percent. An eightfold mislabelling was therefore caught, but not by a wide margin, and the same measurements at batch four would have been borderline.`,

`We state the consequence plainly rather than leave it implicit. This filter is a test for gross misattribution, not an audit. A measurement that passes it has not been shown to be single-stream; it has only been shown not to be impossible. The asymmetry is deliberate, since a test meant to challenge published claims should err toward the claimant, but it bounds what Section V-D's verdicts can mean, and it is why the reporting standard of Section XI asks for the batch size to be stated rather than inferred.`
]},
{h: "G. What the Framework Does Not Capture",
 p: [
`Kernel-level improvements raise achieved MBU rather than lowering B_tok. A better GEMM kernel [[marlin]] moves the same bytes with less overhead, appearing as higher utilization of the same ceiling, which is the correct treatment and the one Section VII exploits.`,

`Speculative decoding and multi-token prediction [[specdec+medusa]] break the one-sweep-one-token assumption behind (4), amortizing a weight sweep across several accepted tokens. We treat speculation as a multiplier applied atop a normalized baseline rather than folding it into the baseline.`,

`Batching breaks the same assumption for the same reason: at batch n the weight traffic amortizes across n tokens, raising the effective ceiling by roughly n until the workload crosses the ridge point. Because the motivating use case for local inference is predominantly single-user, we normalize to batch one and treat batched serving separately. Numerical nondeterminism across batch shapes [[nondeterminism]] is a further reason not to pool the two regimes.`
]}
]},

{
h: "V. SOURCES AND VERIFICATION PROTOCOL",
intro: [
`The framework is only as useful as the numbers fed into it. This section states how sources were selected, how every value was verified, and what was discarded.`
],
sub: [
{h: "A. Selection",
 p: [
`We did not attempt an exhaustive database search, and this paper makes no systematic-review claim. We searched the 2023-2026 literature and the engineering reports of hardware vendors and inference-engine maintainers for measurements of local LLM inference on consumer-class GPUs, defined as GeForce RTX or equivalent commodity parts with 8 to 32 GB of on-board memory. From the candidates, we retained only measurements that could be verified in full against a primary source: the throughput value itself, the quantization container, the batch size or concurrency level, the context length and the phase attribution.`,

`That criterion is strict, and it is the point. A measurement missing any one of these cannot be normalized by equation (4), and including it under assumed defaults would reproduce at one remove exactly the problem this paper describes. We preferred a corpus small enough to verify completely over one large enough to look authoritative. We applied the criterion to our own candidates without exception: one otherwise attractive measurement [[nvidiablog]], widely cited and on exactly the hardware of interest, was dropped because its source states neither batch size nor phase and names its container only as "int4".`,

`The criterion has a consequence we must state before any result is read. Because admission requires the batch or concurrency level to appear in the source, the corpus cannot, by construction, contain a measurement whose batch level is unstated or mislabelled, which is precisely the class the validity filter of Section IV-E exists to catch. Running the filter on the corpus therefore tests whether it agrees with a ground truth already in hand. That is a useful check and we report it as one, but it is not a finding, and an earlier version of this paper did not draw the distinction sharply enough.`,

`We therefore keep a second, disjoint set: the measurements this criterion eliminated. Those are the ones that circulate without the fields equation (4) needs, and they are the filter's actual test domain. Section V-D applies the filter to them and Table 3 reports the result. The two sets answer different questions and are never pooled: the first supports the quantitative comparisons in Sections VI through IX, the second tests the method itself.`
]},
{h: "B. What Verification Removed",
 p: [
`Applying the criterion eliminated most candidates, and the pattern of elimination is itself a finding. The most common disqualifier was that a report published throughput only inside a chart image, with no extractable values [[puget+powerinfer]], and the second of those two is a peer-reviewed systems paper, not a blog post, which is worth stating plainly because the practice is not confined to informal venues. The second was that the container was named nominally without the information needed to establish its effective bits per weight [[nvidiablog]]. The third was phase ambiguity: throughput reported without stating whether it covered decode alone or prefill and decode together.`,

`We applied that disqualifier late and at cost. An earlier revision of this paper admitted the PowerInfer measurement to the corpus on the strength of a value no reader can extract from the source, and derived two headline numbers from it; Section VII-C sets out what was withdrawn. We record it here rather than quietly dropping it, because a paper arguing that unverifiable numbers propagate should say when its own did.`,

`Two further cases are worth naming because they are easy to miss. One widely cited consumer benchmark [[puget]] reports throughput for a model different from the one commonly attributed to it in secondary discussion. Another [[knoop]] reports values that secondary summaries present as single-stream but that the source documents as concurrent. In both cases the error enters not at the original measurement but in its retelling, which is the mechanism by which the comparability gap propagates.`,

`We also verified every model architecture used in the framework by reading the published configuration file rather than relying on recalled parameters, because equations (2) and (4) depend on layer counts, key-value head counts, head dimensions and sliding-window configuration. One such check materially changed a conclusion: Gemma 3 [[gemma3]] interleaves sliding-window attention at a ratio of five local layers to one global, which Section VIII-B shows inverts the apparent ranking of models by long-context memory demand. Architectures for Llama [[llama3]] and Qwen [[qwen3]] models were verified the same way.`
]},
{h: "C. The Resulting Corpus",
 p: [
`Eight throughput measurements survived, drawn from three studies [[menlo+zahl+knoop]], spanning six consumer GPUs across three architecture generations, three engines and three containers. A fourth study [[powerinfer]] was admitted by an earlier revision and is withdrawn here: Section VII-C sets out why. Nine measured energy figures on a single device [[zahl]], with measured board power, support Section IX. Table 1 gives the hardware substrate and Table 2 the normalized corpus.`,

`Applying the validity filter of Section IV-E to these eight measurements flags three. All three come from one study [[knoop]], and that study documents them as having been taken at concurrency eight. The filter therefore recovers, from published architecture parameters and device bandwidths alone, a condition that the source records but that the number does not carry into secondary use. Because the batch level is stated in the source, this is a calibration against known ground truth, not a discovery: it establishes that the filter does not raise a false alarm on three measurements whose true batch level makes a violation expected. The filter is also handed a conservative input here, since all three rates are output tokens over a window that includes prefill and so understate decode speed. Section V-D applies the same filter where the ground truth is genuinely absent.`,

`All of this is released. The repository carries the code implementing equations (1) through (11), the machine-readable corpus behind Table 2, the source-mapped accuracy data behind Table 4, the script that generates Table 6, and a verification record resolving every measurement to its primary source. Addresses are given in the artifact statement on the first page.`,

`We note the other limitation plainly. Nine measurements support the direction and rough magnitude of the effects reported here; they do not support precise population estimates, and Section XII says so explicitly. The framework, the equations and the released code apply to any corpus; extending them is the natural next step and one we invite.`
]},
{h: "D. The Filter Where Ground Truth Is Absent",
 p: [
`Table 3 applies the validity filter to nine measurements that the inclusion criterion eliminated, drawn from four sources: two NVIDIA publications [[nvidiaoss+nvidiablog]], one vendor-sponsored article [[techradar]] and one independent benchmarking site [[hwcorner]]. All nine are visible, current and of the kind that propagates into secondary discussion. For each we computed the range of per-token traffic consistent with everything the source states, then the Model Bandwidth Utilization that range implies under the single-stream reading each presentation invites.`,

`The headline result is not that these measurements are wrong. It is that four of the nine cannot be adjudicated at all. Their traffic ranges straddle MBU = 1: under the most favourable admissible reading the reported rate sits comfortably below the bandwidth bound, and under the least favourable it is physically impossible on the stated device at batch one. A reader cannot tell which applies, because the distinguishing information is not published. The filter's output on these rows is neither pass nor fail but indeterminate, and that verdict is a property of the reporting rather than of the hardware.`,

`What drives the ambiguity is worth separating, because the two mechanisms have different remedies. The first is model identity. One vendor page reports "up to 256 tokens per second" for a paragraph that names both gpt-oss-20b and gpt-oss-120b and attributes the figure to neither [[nvidiaoss]]; a second page reports 282 tokens per second for gpt-oss-20b on the same card with no precision stated at all [[techradar]]. The two figures differ by ten percent and neither can be placed against a ceiling. The remedy is a sentence.`,

`The second is expert residency, and it is the more interesting case. For a mixture-of-experts model, per-token weight traffic depends on whether the reported rate reflects reading only the experts a token activates or sweeping the resident weight set. The three Qwen3-30B rows in Table 3 are reported at 141.6, 139.7 and 113.8 tokens per second on cards spanning a factor of 1.78 in memory bandwidth. Under the active-path reading the implied utilizations are 0.28, 0.49 and 0.43, which says these runs are not bandwidth-bound and that ranking the cards by bandwidth on this workload is therefore uninformative. Under the resident-sweep reading the same numbers imply 1.60, 2.81 and 2.46, which is impossible. The framework does not resolve which reading is correct, but it does explain why the three numbers cluster: a model activating 3.3 of 30.5 billion parameters [[qwen3moe]] moves too little per token for bandwidth to bind on any of these devices.`,

`Two rows in Table 3 show the other side of the result. The Qwen3-8B measurements state their container and their context, and their traffic range collapses to a factor of 1.03, against 6.9 for the gpt-oss rows. They still omit the batch level, so they remain outside the corpus, but the filter can at least place them: all three pass. Stating two fields reduced the ambiguity by a factor of roughly two hundred. This is the quantitative case for the reporting standard of Section XI, and it is the reason that standard asks for fields rather than for more measurements.`,

`One caution about what Table 3 does and does not establish. Four of its nine rows come from a single site and the two NVIDIA items share an author, so the table characterises a reporting culture rather than estimating a rate of occurrence in a population. Section IV-F quantifies the complementary limitation: how large a mislabelling has to be before this filter notices it at all.`
]}
]}
]
};
