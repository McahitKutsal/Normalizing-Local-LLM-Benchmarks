// Manuscript part B: Sections VI and VII (quantization, engines)
module.exports = [
{
h: "VI. QUANTIZATION AND ACCURACY",
intro: [
`Quantization acts directly on the dominant term of equation (4), which makes it the primary lever in local inference and the first place to apply the framework. This section establishes effective bits per weight from published artifact sizes, then locates the point at which the accuracy trade stops being worth making.`
],
sub: [
{h: "A. Effective Bits per Weight, Derived",
 p: [
`Equation (1) needs b, and assuming it is the most common way to get the traffic calculation wrong. We derive it instead, from two independent sources.`,

`The first is a unified evaluation of every llama.cpp container on Llama-3.1-8B-Instruct [[unifiedquant]], which reports each container's size reduction against the FP16 baseline; b follows as 16·(1 − reduction). The second is the pull request that introduced the k-quant family [[kquantpr]], which publishes file sizes for LLaMA-7B and LLaMA-13B; b follows as 16·size/size_FP16, computed independently at each model scale.`,

`The derivations agree closely. The 7B and 13B derivations in [[kquantpr]] differ by at most 0.03 bits across nine containers, and the containers present in both sources correlate at r = 1.0000. This is a stronger footing than any assumed constant, and it exposes real spread: Q4_K_M measures 4.89 bits per weight while Q4_0, also nominally four-bit, measures 4.64, and Q5_K_M measures 5.70 against a nominal five.`,

`Effective bits per weight is a property of a model-container pair rather than of a container alone, because the share of parameters a container leaves in full precision (embeddings and the output projection above all) varies with vocabulary size. Where the exact pair has a published artifact we therefore measure that pair. For the engine comparison of Section VII-A, which runs Mistral-7B-Instruct-v0.2 under two containers, both artifacts are public: the AWQ int4 build measures 4.15 GB and the Q4_K_M GGUF 4.37 GB, giving 4.59 and 4.83 bits per weight against the model's 7.24 billion parameters. Both sides of that comparison are therefore measured on the same model, and no assumed constant enters it.`,

`The AWQ figure is worth one further remark because it is checkable from the container specification as well. The AutoAWQ packing used for this artifact stores 4-bit weights at group size 128 with fp16 group scales and 4-bit group zero points, which is 4 + 16/128 + 4/128 = 4.16 bits across the quantized tensors. That is a property of the released implementation rather than of the method as described in [[awq]], which is the point: the container is defined by what was packed, not by what was proposed. Subtracting Mistral's 262 million embedding and output-projection parameters, which AWQ leaves in fp16, from the measured artifact gives 4.16 bits for the quantized remainder, agreeing with the specification to three significant figures. The 4.59 figure used in equation (1) is the whole-model average, which is the quantity equation (1) requires.`
]},
{h: "B. The Accuracy Cost Is Smaller Than Its Reputation",
 p: [
`Table 4 and Fig. 3 give the trade on a common basis: derived bits per weight, compression ratio, WikiText-2 perplexity and its increase, the mean of five downstream tasks [[lmeval]] and its drop, and the traffic-implied ceiling ratio on a reference RTX 4090 at 4k context.`,

`Down to roughly 4.6 bits per weight, the accuracy cost is close to nothing. Q8_0 loses 0.06 percentage points on the five-task mean and 0.01 in perplexity. Q6_K loses 0.24 points. Q5_K_M loses 0.11 points and 0.08 perplexity while delivering a 2.65x traffic reduction. Q4_K_M, the practitioner default, loses 0.32 points and 0.24 perplexity for a 3.05x reduction. Several containers in the five- and six-bit range score marginally above the FP16 baseline on the task mean, which is best read as evaluation noise and as a caution against over-interpreting differences of a few tenths of a point.`,

`Below four bits the picture changes sharply. Q3_K_M loses 1.40 points, and Q3_K_S loses 3.98 points and 1.64 perplexity. The knee therefore sits near four bits per weight, lower than the five-to-six-bit band that practitioner guidance often recommends, and the common preference for Q4_K_M is on this evidence conservative rather than aggressive. Methods that push below four bits by other means, such as sub-1-bit expert compression [[moqe]] or structured pruning before quantization [[sparsegpt]], are addressing a regime this knee says is already expensive.`,

`A caution on reading the per-task columns too finely. GSM8K is scored on 1319 problems, so its granularity is 0.076 points and two containers landing on an identical score simply solved the same number of problems; Q5_K_S and Q4_0 do exactly this in [[unifiedquant]]. Differences below a few tenths of a point on any single task in Table 4 should not be interpreted.`
]},
{h: "C. Container Design Outweighs Nominal Bit Width",
 p: [
`Two containers in Table 4 make the point that nominal precision is the wrong unit. Q4_0 measures 4.64 bits per weight and loses 1.49 points. Q4_K_M measures 4.89 bits, only 0.25 bits more, and loses 0.32 points, a quarter of the degradation. Q4_K_S measures 4.67 bits, almost exactly Q4_0's width, and loses 0.30 points.`,

`At effectively equal bit width, therefore, the k-quant containers lose roughly a fifth of what the legacy Q4_0 container loses. We state that comparison with its uncertainty attached, because it is a 1.19-point difference and the noise floor established in Section VI-E is 0.90 points on this metric: the gap is 1.3 times the floor, which makes it suggestive rather than established. What is established is the sign and that nominal width does not predict it. The difference is where the bits go: per-block scales and minima, and selective promotion of the tensors most sensitive to rounding [[kquantpr]]. The same principle animates the calibration-based methods, which spend their budget protecting the weights that matter most to downstream activations [[awq]] or minimizing layer-wise reconstruction error [[gptq]], and the outlier-handling schemes that preceded them [[llmint8+smoothquant]]. Data-free approaches [[hqq]] and multi-precision packings [[anyprecision]] occupy the same design space.`,

`For the framework this matters twice over, because such containers are simultaneously harder to characterize by name and more accurate than their nominal width suggests. It also qualifies the engine comparison in Section VII-A, as we note there.`
]},
{h: "D. Reasoning Degrades First, and Fastest",
 p: [
`Averaging across tasks conceals the most decision-relevant fact in this section. At Q3_K_S the five-task mean falls 3.98 points, but GSM8K alone falls 9.32 points, more than twice as far. The asymmetry persists one container up: at Q3_K_M the mean falls 1.40 points against 4.47 on GSM8K, and at Q3_K_L 0.69 against 3.56.`,

`We restrict the claim to those three rows, and the restriction is deliberate. Section VI-E sets two floors on the GSM8K column: a paired sampling bound of 0.62 to 1.07 points, and a stricter attribution floor of 3.42 points taken from the table's own content. Only Q3_K_L, Q3_K_M and Q3_K_S clear both. Above four and a third bits the GSM8K differences, including the 1.97-point gap at Q4_0 that an earlier version of this paper cited as early evidence of the same effect, are not separable from noise, and three containers in that range score above the baseline, which is what noise looks like. Citing them would have repeated the error Section VI-B warns against.`,

`So the asymmetry is real but it is not gradual: it appears at and below roughly four and a third effective bits per weight and is absent above. That is a sharper statement than the one we set out to make, and it agrees with the knee in Section VI-B rather than cutting across it: the bit width at which aggregate accuracy begins to fall is the bit width at which reasoning begins to fall faster than the aggregate. Mathematical reasoning is thus the first capability to go once degradation begins at all. The practical consequence is that a container acceptable for summarization or dialogue may be unacceptable for code or mathematics at the same bit width, and that a single aggregate accuracy number is not sufficient to characterize a container for deployment.`,

`One scope limitation deserves emphasis. The evaluation underlying Table 4 covers llama.cpp containers on one model with one harness, which is what makes its rows internally comparable. We found no evaluation placing the calibrated integer containers [[gptq+awq]] and the 4-bit floating-point formats [[nvfp4+ocpmx]] on the same footing as the k-quants, and we therefore do not tabulate cross-family accuracy comparisons. That absence is itself a gap, and Section XIII returns to it.`
]},
{h: "E. What Counts as a Difference",
 p: [
`Sections VI-C and VI-D compare numbers that differ by one or two points, so they need a floor. Two are available and they disagree by a factor of three, which is itself the finding.`,

`The first is sampling. GSM8K is scored on its 1,319-item test split, and for a paired comparison (the same questions under two containers), the McNemar standard deviation of the accuracy difference is the square root of the discordance rate over the item count. The source reports point estimates without discordance counts, so we bound rather than know it: at 5 to 15 percent discordance the standard deviation is 0.62 to 1.07 points. The unpaired binomial bound, which pairing can only improve on, is 1.62 points.`,

`The second comes from the table itself and is stricter. Q5_0 and Q5_K_S are indistinguishable on both quantities the framework can check: identical effective width at 5.57 bits, identical perplexity at 7.43. Yet they differ by 3.42 points on GSM8K and 0.90 on the five-task mean. That difference cannot be attributed to bit width, because bit width is held fixed. It is an empirical floor on how large a gap must be before "the bit width caused it" is a defensible reading, and at 3.2 times the most conservative sampling bound it says plainly that sampling is not the dominant source of variation in this column. Container construction is.`,

`We therefore use the attribution floor, not the sampling bound, wherever the claim is about bit width. Applying it leaves three of thirteen containers with a GSM8K difference worth interpreting, all at or below 4.30 effective bits. The practical lesson for readers of such tables is the one Section VI-B states in another form: two containers can agree on width and on perplexity and still differ on a downstream task by more than the entire span this literature usually argues about.`
]},
{h: "F. Mixture-of-Experts and the Activated-Parameter Discount",
 p: [
`Sparsely activated architectures [[mixtral+gptoss]] change the calculus because equation (1) uses P_act rather than P. The discount can be large, and it is what makes models with large nominal parameter counts tractable on consumer hardware at all.`,

`The discount is conditional on residency, and the condition is strict. If all experts fit in VRAM, the model moves the traffic of a much smaller one while retaining the capability associated with its total parameter count. If they do not, each token may require fetching cold experts across the interconnect, and effective traffic is governed by that link rather than by VRAM bandwidth. The substantial literature on expert offloading, caching and prefetching is largely an effort to preserve the discount under memory pressure: activation-aware expert caching [[moeinfinity]], CPU-GPU co-execution [[fiddler]], hybrid scheduling [[hybrimoe]], sensitivity-based gating [[adapmoe]], workload-aware placement for local machines [[dali]], and mixed-precision expert allocation [[moeoffload]]. Section VII-C shows a closely related mechanism working in the dense case.`
]}
]},

{
h: "VII. ENGINES, KERNELS AND PLACEMENT",
intro: [
`This is where the comparability gap is widest, because engines are the variable practitioners most often believe they are choosing between, and the one for which published comparisons are least controlled.`
],
sub: [
{h: "A. A Controlled Engine Comparison",
 p: [
`One source in our corpus [[menlo]] permits a genuinely controlled comparison: the same model, the same batch size, the same prompt and generation lengths, two engines, on two consumer GPUs. It reports Mistral-7B at batch one with a 2048-token prompt and 512-token generation. On the RTX 4090, TensorRT-LLM [[trtllm]] reaches 170.63 tokens per second and llama.cpp [[llamacpp]] 100.43. On the RTX 3090, 144.19 and 88.70.`,

`Raw, that is a 1.70x and a 1.63x advantage, pooling to 1.66x. But the two engines were not running the same weights: TensorRT-LLM used an AWQ int4 container and llama.cpp a Q4_K_M container, measuring 4.59 and 4.83 effective bits per weight on this model by the artifact derivation of Section VI-A. Normalizing by equation (6) gives MBU 0.754 against 0.465 on the 4090 and 0.686 against 0.443 on the 3090, pooling to 1.58x.`,

`Measuring the gap as the margin above parity, normalization accounts for 12% of it and 88% survives. The modest size of that correction is itself informative, and it is a consequence of the two containers being close: 4.59 against 4.83 bits per weight is a 5% difference in traffic, so there was little for normalization to remove. The correction is not always small. A comparison of an FP16 build against a four-bit one, which several circulating comparisons are, carries a traffic ratio near 3.4x before any kernel runs, and there essentially the whole reported gap is artifact. What the framework supplies is not a universal discount but the ability to compute, from the containers alone and before trusting any number, which of those two situations a given comparison is in.`,

`On this particular comparison, then, the engine difference is largely real: a compiled architecture-specific engine extracts materially more of the available bandwidth than a portable one on the same hardware.`,

`The source's throughput figures span prefill and decode together, so the MBU values above are not pure decode utilizations, and the obvious worry is that a compiled engine wins disproportionately on prefill, which is compute-bound and where kernel quality tells most, and that the win is then misread as decode bandwidth efficiency. The token counts seem to support the worry: at 2048 prompt and 512 generated tokens, 80% of the tokens processed are prompt tokens. We think the worry is misplaced, and the reason is worth stating because the intuition behind it is natural.`,

`A throughput figure divides by time, not by tokens, and prefill is far faster per token than decode. llama.cpp's own CUDA scoreboard reports, for a 7B model at Q4_0 on an RTX 4090, 11,992.70 tokens per second of prompt processing against 186.21 of generation [[llamacppbench]], a ratio of 64. At that ratio a 2048-token prompt occupies 5.9% of the wall clock on this workload while supplying 80% of the tokens. Amdahl's law then caps what prefill can contribute to the overall ratio at 1.06x. For prefill alone to account for the measured 1.58x, it would have to occupy at least 36.9% of the run, six times its actual share.`,

`Bounding it properly: if the two engines are equally efficient at prefill, the decode-only ratio implied by the measurement is 1.65x; if the compiled engine's prefill advantage is unbounded, it is 1.49x. The decode-only engine ratio therefore lies in [1.49, 1.65], the mixed-phase value sits inside that interval and the worst-case displacement is 5.9%. The conclusion survives a wrong anchor: even at a prefill share five times the measured one the decode-only ratio stays above 1.11x. We therefore report the figure as the mixed-phase measurement it is, with that interval as its phase-attribution uncertainty.`,

`Two further limitations bound the reading, and neither is resolved here. With two GPUs and one model, the 1.58x residual is an estimate from a single controlled contrast, not a population parameter. And normalizing by effective bits per weight equalizes traffic but not quality: Section VI-C shows that containers of equal width can differ several-fold in accuracy loss, so part of the residual may reflect an uncontrolled quality difference rather than engine efficiency. An iso-quality comparison, matching containers by measured accuracy rather than by width, would be the stronger design, and we were unable to construct one from verified sources.`
]},
{h: "B. What a Kernel Speedup Actually Claims",
 p: [
`Table 5 collects the principal kernel and algorithmic multipliers in circulation, traced to their primary sources. Tracing them corrects one figure substantially and clarifies what the others mean.`,

`A tenfold kernel speedup is sometimes attributed to the Marlin W4A16 kernel. Marlin's authors claim something different and more interesting: a speedup of approximately 3.9x against FP16 on an inference-optimized A10, against a theoretical optimum of 4x for four-bit weights [[marlin]]. That is near-ideal by construction: it is almost exactly the memory-traffic bound for a four-bit container with group scales. Their contribution is not exceeding that bound but sustaining it, holding near-ideal speedup out to batch sizes of 16 to 32 where prior kernels degrade. Read through the framework, Marlin does not raise the ceiling; it keeps the achieved fraction of the ceiling near unity as batching erodes it for others. The tenfold figure appears to originate in a comparison against a particular poorly-performing baseline kernel and is not a claim its authors make.`,

`FlashAttention-2 reports roughly 2x over its predecessor and 50-73% of theoretical peak FLOPs on an A100 [[flashattn2]], with gains concentrated in long-context prefill, the compute-bound phase. PagedAttention's contribution is different in kind again: capacity and concurrency rather than single-stream latency [[vllm]]. It lets more sequences share a fixed cache budget without fragmentation, which is decisive for serving and close to neutral for one interactive user. Conflating the two is common, since both are described as cache optimizations, but one raises throughput per user and the other raises users per device. Structured-program execution engines [[sglang]] and browser-targeted runtimes [[webllm]] occupy adjacent positions, as does the ExLlama line [[exllama]] for consumer NVIDIA hardware specifically.`
]},
{h: "C. Placement, and a Result We Could Not Normalize",
 p: [
`The framework predicts that when a working set exceeds VRAM, throughput falls to the interconnect bound: weights must cross PCIe each sweep, so BW in equation (5) becomes the link's rather than the card's. For a 30-billion-parameter model at FP16, 60 GB of weights over a 64 GB/s PCIe 4.0 link, that bound is 1.06 tokens per second. The most-cited counterexample is PowerInfer [[powerinfer]], which runs OPT-30B at FP16 on a 24 GB RTX 4090 and reports, in its abstract, reaching 82 percent of an A100's token generation rate on that card, with an average across its models of 8.32 tokens per second for non-quantized models. Both figures are far above 1.06, so the naive bound plainly does not govern that system.`,

`We cannot say by how much, and the reason is the subject of this paper. PowerInfer's per-model throughput appears only inside Fig. 10, whose caption states that the number above each bar gives the end-to-end generation speed; the figure is a raster image in both the HTML rendering and the PDF, and no tokens-per-second value for OPT-30B appears as text anywhere in the paper. The measurement therefore fails the inclusion rule of Section V-A for exactly the reason the Puget benchmark fails it, and we exclude it on the same ground. An earlier version of this manuscript did not: it carried a figure of 16.06 tokens per second in the corpus, traceable to no readable text in the source, and derived from it both a multiple of the naive bound and a percentage of the resident ceiling. Those numbers are withdrawn.`,

`What survives does not depend on them. The mechanism is the lever the framework identifies: PowerInfer exploits activation sparsity, keeping frequently activated neurons resident and streaming only the remainder, so the bytes that actually cross the bus are a small fraction of the weight set. The interconnect bound is therefore a property of naive offloading, not of offloading as such, and what governs offloaded throughput is not whether the model fits but how much of it must move, the same quantity equation (4) measures in the resident case. Throughput-oriented offloading makes the opposite trade: FlexGen reaches roughly one token per second aggregate for a 175B model on a single 16 GB device at an effective batch of 144 [[flexgen]], transformative for batch processing and unusable interactively, and ZeRO-Infinity [[zeroinfinity]] established much of the staging machinery both rely on.`,

`Two limits bound the reading. The mechanism depends on ReLU-family activations, which the evaluated models provide and which the SwiGLU-based models dominating current local deployment, including every model elsewhere in this paper, do not; whether comparable placement gains are available for dense SwiGLU models is open, and Section XIII lists it accordingly. And because no offloaded measurement survives verification, this section states a mechanism and a direction rather than a magnitude. That is a weaker claim than we set out to make, and it is the honest one: a reader cannot place this result against a ceiling without information its source publishes only as a picture.`,

`It still reframes the practical question. A practitioner asking whether a model "fits" is asking the wrong one; the right question is what fraction of the weights a given placement strategy must stream per token. Section XI's reporting standard would have made the magnitude recoverable here, from a source that plainly measured it.`
]},
{h: "D. Speculative Decoding",
 p: [
`Speculative decoding is the one widely deployed technique that legitimately breaks the roofline of Section IV-B. A lightweight draft mechanism proposes several candidate tokens; the target model verifies them in a single forward pass and accepts the longest matching prefix [[specdec]]. Because verification costs one weight sweep, accepted tokens beyond the first are effectively free in bandwidth terms.`,

`The primary sources report 2-3x on T5-XXL for the original draft-model formulation [[specdec]], over 2.2x for Medusa-1 with multiple decoding heads and 2.3-2.8x for Medusa-2 [[medusa]], and 2.7-3.5x for EAGLE on a 70B chat model [[eagle]], with subsequent work extending the approach [[eagle3]]; the survey literature places these in a common taxonomy [[specsurvey]]. These are not consumer-GPU measurements, which is the gap worth naming: the technique's benefit is inversely related to batch size, because above roughly 32 concurrent sequences the target model is no longer memory-bound and verification is no longer free. Local single-user inference is therefore precisely the regime where speculation pays best.`,

`A technique offering two- to threefold gains in the exact setting under study, now shipping in the major engines, and largely absent from published local-inference benchmarks, is the most conspicuous measurement gap we encountered. Section XIII returns to it.`
]}
]}
];
