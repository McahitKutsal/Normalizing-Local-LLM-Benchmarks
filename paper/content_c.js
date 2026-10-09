// Manuscript part C: Sections VIII-XIV
module.exports = [
{
h: "VIII. CAPACITY AND CONTEXT",
intro: [
`Every other application in this paper operates inside a constraint this one defines. Section VII-C showed that exceeding VRAM need not be catastrophic, but it remains the boundary that decides which strategies are available at all. This section computes that boundary from verified architectures.`
],
sub: [
{h: "A. The Capacity Ceiling",
 p: [
`Consumer VRAM has grown slowly against model sizes. From 24 GB at the top of Ampere, to 24 GB on Ada's flagship, to 32 GB on Blackwell's, capacity rose a third across two generations while model releases spanned three orders of magnitude in parameter count. The volume segment has been flatter still: 12 and 16 GB parts dominate across all three generations.`,

`Table 6 gives total VRAM demand for six models across containers at 32k context, with the smallest consumer tier that admits each configuration. A 24 GB card admits an 8B model [[llama3+qwen3]] at full FP16 precision, Gemma-3-27B [[gemma3]] at Q5_K_M, and Qwen2.5-32B only at IQ3_M, where Section VI-B shows accuracy has begun to degrade materially. Llama-3.3-70B fits no single consumer card at any container considered, needing 50.7 GiB even at Q4_K_M.`,

`The ceiling for high-quality single-card local inference therefore sits between 27B and 32B parameters, and it is a capacity fact rather than a software limitation. What Section VII-C adds is that this ceiling bounds resident execution, not inference as such: beyond it, throughput depends on how well a placement strategy exploits sparsity, not on the capacity shortfall alone.`
]},
{h: "B. The Context Wall, and the Architecture That Removes It",
 p: [
`Weight footprint is the constraint practitioners plan around. Cache footprint is the one that surprises them, and the common way of estimating it is wrong for a growing class of models.`,

`Applying the naive formula, in which every layer holds the full context, to Gemma-3-12B at 32k context gives a cache of 12.0 GiB. Applying equation (2), which honours the model's interleaved attention [[gemma3]], gives 2.3 GiB. The naive estimate overstates the cache itself by a factor of 5.2, and the total footprint by 1.95 at Q4_K_M. The footprint factor is container-dependent, since the cache competes with weights whose size the container sets: it runs from 1.37 at FP16 to 2.14 at IQ3_M, so the error is worst exactly where a practitioner is quantizing hardest to make a model fit. At Q4_K_M it would lead them to reject a configuration that sits comfortably on a 12 GB card.`,

`With the correction applied, Fig. 4 inverts the ranking that the naive calculation implies. At 32k context the full-attention models hold on average 33.9% of their footprint in cache against 18.9% for the interleaved ones, and the single worst case is not a large model but Qwen3-8B at 44.5%, followed by Llama-3.1-8B at 42.0%. At 128k the asymmetry becomes stark: Llama-3.1-8B reaches 74.4% while Gemma-3-27B, more than three times its size, reaches 38.8%.`,

`The finding is therefore not that long context is intractable but that the architectural answer already exists and is deployed. Interleaved sliding-window attention converts cache growth from linear in context to linear in the global-layer fraction, and models that adopt it pay a small fraction of the wall. What remains is a reporting problem: a benchmark that evaluates a sliding-window model at short context, or that estimates its footprint naively, will mischaracterize it in opposite directions.`,

`FP8 cache quantization is the orthogonal mitigation, and its benefit is proportional to the cache's share. It saves 21.0% of total footprint for Llama-3.1-8B at 32k but only 7.5% for Gemma-3-27B, where the interleaving has already done the work.`
]}
]},

{
h: "IX. ENERGY AND COST",
sub: [
{h: "A. Measured Energy, and Where Equation (6) Departs From It",
 p: [
`Instrumented energy measurement on consumer hardware remains scarce relative to throughput measurement, and our corpus reflects that: one study [[zahl]] supplies all nine measured energy figures, on an RTX 4060 Ti 16 GB with Ollama, decode-only throughput and measured board power at batch one.`,

`That source computes energy per token as mean board power integrated over the inference window, divided by the output tokens, while deriving throughput from the decode phase alone. The two denominators differ, and the gap is the prefill and call-overhead energy amortized across the output. Across the nine models it runs from 0.085 to 0.319 J, averaging 18% of the reported energy per token. Equation (6) recovers only the decode term and is therefore an approximation on this table rather than an identity. We use the measured figure, not (6), wherever cost is computed, because the measured figure is what a deployment actually pays.`,

`Table 7 and Fig. 5 give the measurements. Across models from 1B to 7B parameters, energy per token spans 0.556 to 2.485 joules, a 4.5-fold range. Throughput and energy per token correlate at r = −0.89, which is the expected signature of a bandwidth-bound workload: the board draws roughly constant power while waiting on memory, so joules per token is close to inversely proportional to tokens per second. The measured mean power supports this directly, rising only from 83 W to 123 W across a range in which throughput falls by a factor of 3.8.`,

`That relationship has a practical corollary. Because power varies much less than throughput, energy efficiency is almost entirely a function of how fast the model runs, which is in turn a function of how many bytes it moves. Energy efficiency in this workload is therefore not a separate optimization target from throughput; it is the same target measured in different units.`,

`Two methodological cautions carry over from the wider literature. Models that emit extended internal reasoning before their visible output can show anomalously high per-response energy while appearing ordinary per token, so metrics that do not distinguish generation modes will mislead [[zahl]]. And joules per token is itself an incomplete unit, because the hardware-visible cost is the inference window rather than the token, so request energy and token energy can move in opposite directions as output length and batch size vary [[reqenergy]]. Dedicated energy harnesses [[zeus+mlenergy+tokenpower]] and diagnostic studies of where inference energy goes [[joules]] address this more rigorously than our corpus can; we report joules per token because it is the unit the corpus supports, and we flag the limitation rather than resolve it.`
]},
{h: "B. The Amortization Gap",
 p: [
`Studies advocating self-hosting frequently report cost as electricity alone, yielding figures of a few cents per million tokens and supporting claims of being orders of magnitude cheaper than metered APIs. The arithmetic is correct and the accounting is incomplete: it holds volume fixed at a level most local deployments never reach.`,

`Applying equations (8) and (9) to the measured energy figures of Table 7, at 0.16 USD per kWh, a three-year horizon and a 25% duty cycle, gives totals from 0.13 to 0.49 USD per million tokens. Electricity accounts for 21% of that; hardware amortization accounts for 79%. Electricity-only accounting therefore understates the true cost by a factor of 4.7.`,

`The amortization base is the GPU's launch price alone. Including the host system (CPU, board, memory, power supply, chassis) would raise the hardware share further, so the 79% figure is a lower bound on the capital term rather than an estimate of it.`,

`The duty cycle decides the outcome and is almost never reported. At continuous operation the amortization term falls fourfold and the electricity-only approximation becomes defensible. At the 5 to 10% duty cycle typical of an individual developer's workstation it rises three- to fivefold, and local inference stops being cost-competitive with metered APIs on price alone.`,

`The honest conclusion is that local inference is justified by privacy, latency and control, and is cost-competitive above a volume threshold each deployment must compute for itself. We provide the calculation rather than the verdict.`
]},
{h: "C. Bandwidth per Dollar as a Purchasing Criterion",
 p: [
`Section III implies that a card intended for single-stream local inference should be judged on memory bandwidth per dollar, not compute per dollar. Table 1 reports both at launch pricing. The leaders are the RTX 5070 at 1.22 GB/s per dollar and the RTX 5070 Ti at 1.20, followed by the RTX 3060 12GB at 1.09 and the RTX 5060 Ti at 1.04. Flagship parts fare poorly: the RTX 5090 returns 0.90 and the RTX 4090 0.63.`,

`Generationally, Blackwell averages 1.06 GB/s per dollar against 0.66 for Ada and 0.86 for Ampere, reversing the regression Ada represented for this workload. Capacity per dollar tells a different story, with Ampere still leading, and the difference matters because capacity determines feasibility while bandwidth determines speed.`,

`The purchasing rule that follows is two-stage, and it is the practical summary of this paper. First select the smallest VRAM tier that admits the target model and context at a container above the four-bit knee, using Table 6. Then, within that tier, maximize bandwidth per dollar. Selecting on flagship status or advertised TFLOPS optimizes a quantity this workload does not use.`
]}
]},

{
h: "X. WHAT THE FRAMEWORK SHOWS",
intro: [
`Five applications, one framework. This section draws out what they have in common.`
],
sub: [
{h: "A. A Filter That Can Be Checked",
 p: [
`Three of eight measurements in the corpus imply memory traffic above their device's peak bandwidth, which is physically impossible for the batch-1 decoding their presentation implies. Fig. 6 plots every measurement against its computed ceiling; the three sit above the diagonal.`,

`What makes this more than an accusation is that the flagged rows can be checked independently. All three come from a study [[knoop]] that states it measured at concurrency eight, and that mostly reports concurrency four through 256. The filter recovered, from published architecture parameters and vendor bandwidth figures alone, a fact that is present in the source but absent from the number as it travels.`,

`We are careful about what this establishes, and about where it does not come from. Because the corpus admits only measurements whose batch level is stated, these three rows are a calibration against known ground truth: the filter was asked a question whose answer was already recorded, and it gave the right one. That shows the test is well-formed: it produced a falsifiable prediction, the prediction was checkable against the source, and it held. But a check is not a finding.`,

`The finding is in Table 3, where the filter is applied to nine measurements from four sources that the inclusion rule had to exclude. There the ground truth is genuinely absent, and the filter returns indeterminate on four: the traffic consistent with what each source states spans the bandwidth bound, so the published number is either unremarkable or impossible and the reader cannot tell which. That is a statement about reporting practice, not about hardware, and it is reproducible by anyone with the sources and equation (6). We still do not claim a rate of occurrence (four of the nine rows come from one site, and the two vendor items share an author), but it is no longer a single study with a single cause.`,

`Section IV-F bounds the other side. The filter detects a batch-B measurement presented as single-stream only above a true per-stream efficiency of roughly 1/B, so the eightfold mislabelling it caught here cleared the threshold by thirty-four to fifty percent, and a fourfold one would have been borderline. Passing the filter is therefore weak evidence; failing it is strong evidence.`,

`That is the useful property. Applying the filter requires no access to the original hardware and no re-execution of any benchmark; it follows from information any reader already has. A number that fails it is not necessarily wrong, but it is certainly not what it appears to be, and the reader now knows to go back to the source. We suggest it is worth applying, by reviewers of inference benchmarks and by authors to their own tables before submission.`
]},
{h: "B. Confounds Are Large but Not Total",
 p: [
`The controlled engine comparison of Section VII-A is the paper's cleanest estimate of how much of a published performance gap is artifact, and the answer there was 12% of the margin above parity. That figure is not a constant, and this instance sits at the low end by construction: the two containers differ by 5% in effective width, so there was little for normalization to remove. Had the comparison been FP16 against a four-bit container, as several circulating comparisons are, the traffic ratio alone would have been about 3.4x and essentially the whole reported gap would have been artifact.`,

`So the useful claim is not that confounds are small. It is that their size is computable in advance, from the containers alone, before any benchmark is trusted, and that a comparison which does not state them leaves the reader unable to tell which case they are in. The corollary is that engine choice deserves measured evidence, but the measurement must control the container: a comparison that omits effective bits per weight for both sides cannot distinguish a kernel from a file format.`
]},
{h: "C. The Binding Quantity Is Bytes Moved, Not Bytes Stored",
 p: [
`Three findings in this paper look unrelated and are the same finding. Quantization helps because it reduces bytes moved per token, and its accuracy cost stays negligible until the container runs out of room for the metadata protecting sensitive tensors, at roughly four bits. Interleaved sliding-window attention helps because it caps what the cache contributes, converting growth in context into growth in only the global-layer fraction. And a sparsity-aware placement strategy beats the interconnect bound because it reduces the bytes that must cross the bus, not because it changes the bus.`,

`Equation (4) is the common denominator. Whether a technique narrows the weight representation, bounds the cache, exploits activation sparsity or amortizes a sweep across speculated tokens, it is lowering B_tok. Techniques that do not lower B_tok, including most compute-side advances, do not help single-stream local inference, and the framework says so in advance rather than discovering it per technique. That is why we present the framework as the contribution and the applications as demonstrations: a corpus of eight measurements will be superseded, and the reduction of a reported rate to a fraction of a computed physical bound will not.`
]}
]},

{
h: "XI. A MINIMUM REPORTING STANDARD",
p: [
`The findings above are, in one sense, a critique of reporting practice rather than of the systems themselves. That critique implies a remedy, and the remedy is cheap.`,

`We propose that any published local-inference benchmark report the following, each required for a third party to normalize the result: the model identifier and its activated parameter count; the container and its effective bits per weight, measured from artifact size rather than named nominally; the key-value cache precision, and the attention pattern where the model interleaves sliding windows; the context length, with prompt and generation lengths given separately; the batch size or concurrency level; the phase attribution of each throughput figure, prefill or decode or combined; the device and its peak memory bandwidth; whether the working set was fully VRAM-resident and, if not, what placement strategy was used; whether speculative decoding was enabled and at what acceptance rate; and, where energy is reported, the measurement method, the integration window and the sustained board power.`,

`The list is derived mechanically: it is what equations (1) through (11) consume. That is also how it differs from a reproducibility checklist such as [[metametrics]], which asks what another laboratory would need to obtain the same number on the same harness. These fields ask something weaker and more portable: what a reader with no access to the hardware needs to convert the published figure to their own device. That is why the list is short.`,

`None of these fields is burdensome. Most are already known to the experimenter at measurement time. Their absence is a convention, not a constraint, and Section V-B shows what it costs: most published measurements we examined could not be normalized, and the two we traced most carefully had each acquired an error in retelling that the original did not contain.`,

`To keep the standard from being only a list, the released code reads it. The CSV column names are the fields above, and the tool returns per-token traffic, the ceiling, MBU and the filter verdict for each row; a row missing a field is not given a default but reported, naming the field and the equation it blocks. It also prints two verdicts wherever the batch size exceeds one: what the filter says given the stated batch, and what it would say to a reader who met the same figure presented as single-stream. On the corpus of Table 2 the two verdicts differ for three rows, which is Section V-D's result stated as a command line rather than a table.`,

`We additionally suggest reporting MBU alongside tokens per second. It is computable from fields a study already possesses, it makes results portable to hardware the authors did not test, and it exposes the inconsistencies documented in Section X-A before a reviewer has to.`
]},

{
h: "XII. THREATS TO VALIDITY",
p: [
`Construct validity. MBU assumes decode traffic is dominated by weight and cache reads, ignoring activation traffic, embedding and output-projection reads, and imperfect cache reuse. These are second-order at the model scales considered and would bias MBU slightly and uniformly downward. The same direction applies to our use of vendor peak bandwidth rather than achievable bandwidth, which is typically 80 to 90 percent of peak: absolute MBU values are correspondingly low and the validity filter is made conservative, as Sections IV-E and IV-F describe. We do not assume the peak-to-achievable ratio is constant. It is not: it depends on the memory technology, and the cards here span GDDR6, GDDR6X and GDDR7. What makes this tolerable is narrower and checkable: no study in the corpus crosses a memory-technology boundary. Menlo's two cards are both GDDR6X, Knoop's three are all GDDR7, and the remaining two studies are single-card. Every within-study comparison the paper draws is therefore made at a constant ratio whatever its value, and the engine comparison of Section VII-A is immune outright, since both of its rows share a card and the bandwidth cancels in the MBU ratio. What the assumption does touch is the cross-generation per-dollar ranking of Table 1 and the absolute reading of any single MBU value. A measured achievable figure per card would settle both, and producing one is the first item in Section XIII's list of what this paper could not do without hardware`,

`Internal validity. The reported rates in Table 2 do not all measure the same thing, and the table's phase column separates two distinct departures from pure decode. Four of eight measurements are mixed: prefill and decode tokens share both the numerator and the denominator, which inflates the apparent MBU by an amount that depends on the prompt-to-generation ratio. Section VII-A bounds that inflation for the four rows that carry the engine result. Three further measurements are output-tokens-over-total-time: the numerator counts only generated tokens while the denominator includes prefill, so the rate understates decode speed and the MBU derived from it is a lower bound. All three are the flagged rows, which means the filter fires on them despite being handed a conservative input. Only one row is decode on both sides.`,

`Occupancy convention. Equations (3) and (4) evaluate the cache at mean occupancy C̄ = L_p + L_g/2. Two other conventions are defensible: charging every step the prompt length alone, or charging it the final context. Both bound the choice, and the bound is narrow. Across all eight rows with a known prompt and generation length, moving from the prompt-only convention to the final-length convention raises B_tok and therefore raises MBU, monotonically and with no exceptions, by at most 1.5 percent of the tabulated value. The engine comparison is more robust still: because the two containers differ in weight traffic but share a context, both rows shift together and the pooled ratio moves from 1.584 to 1.585 across the full span of conventions. No claim in this paper turns on which of the three is adopted; we report the middle one because it is the only one that corresponds to a quantity the hardware actually moves.`,

`The cost model's duty-cycle and horizon parameters are consequential, which is why Section IX-B reports the decomposition and its sensitivity rather than a single number. Every bits-per-weight value in the paper is measured from a published artifact; the two containers in the engine comparison are measured from artifacts of the same model, so the comparison does not inherit a cross-model difference in how much of each model a container leaves in full precision.`,

`External validity. The corpus is weighted toward NVIDIA hardware, reflecting both the literature and the consumer market. AMD RDNA and Intel Arc parts, and Apple Silicon unified memory, are absent, and their different memory architectures may not normalize as cleanly, though the underlying roofline argument applies to any bandwidth-bound decoder. The verified measurements concentrate between 7B and 30B parameters; conclusions may not extend to sub-1B models, where fixed overheads dominate. The accuracy analysis in Section VI rests on one model family evaluated with one harness, which is what makes its rows mutually comparable but also what limits their generality. The offloading result rests on a mechanism with an activation-function precondition that most current models do not meet, as Section VII-C states.`,

`Conclusion validity. Eight throughput measurements and nine energy measurements support the direction and rough magnitude of the effects reported here. They do not support precise population estimates, and no significance test in this paper would be meaningful at that sample size, which is why we report none. The engine result rests on a single controlled contrast across two GPUs; we present it as an existence proof that the confound is large and that a residual survives it, not as a measurement of the typical engine gap. The filter result rests on three rows from one study. We regard extending the corpus as the obvious next step, and we have released the framework so that extending it does not require rebuilding anything.`
]},

{
h: "XIII. OPEN PROBLEMS",
p: [
`Five directions follow from the gaps this work exposes.`,

`Normalizable benchmarking at scale. The field lacks a benchmark suite that fixes the confounds identified here: a common model-container matrix, mandatory phase separation, reported MBU, and a released harness. MLPerf Client [[mlperfclient]], the MLPerf line more generally [[mlperf]], community efforts such as LocalScore [[localscore]], and roofline-based on-device frameworks [[rooflinebench]] move in this direction but do not yet cover the quantization and placement dimensions that dominate local deployment. The framework in Section IV is intended as a specification such a suite could adopt directly.`,

`Cross-family accuracy evaluation. Section VI-D had to restrict its accuracy analysis to one container family because no evaluation places the calibrated integer containers, the k-quants and the 4-bit floating-point formats on a common model with a common harness. Producing one, with per-task rather than aggregate reporting given the reasoning asymmetry, would settle a question practitioners currently answer by folklore.`,

`Energy measurement at consumer scale. Instrumented energy studies on consumer GPUs number in the low single digits against hundreds of throughput studies, and our corpus draws all nine of its energy figures from one of them [[zahl]]. Given that Section IX shows energy tracking throughput almost deterministically, extending this would be inexpensive and immediately useful, and the harnesses to do it already exist [[zeus+mlenergy]].`,

`Placement strategies for dense SwiGLU models. Section VII-C showed one system beating the naive interconnect bound by a mechanism that requires ReLU-family activation sparsity, though it could not say by how much. Whether comparable gains are available for the SwiGLU-based models that dominate current local deployment is the open question, and it is the one that determines how far above the capacity ceiling consumer hardware can usefully reach. The mixture-of-experts offloading literature [[moeinfinity+fiddler+dali]] attacks a related problem but evaluates predominantly on datacenter hardware with large host memory.`,

`Speculative decoding on consumer hardware. Reported gains of two- to threefold fall exactly in the single-user regime that characterizes local inference, and the technique now ships in the major engines, yet we found no consumer-GPU benchmark reporting acceptance rates alongside throughput. Systematic characterization across model families, draft configurations and consumer devices would likely yield larger practical gains than any further round of engine comparison.`
]},

{
h: "XIV. CONCLUSION",
p: [
`We began with three published claims that cannot jointly guide a decision, and named the reason the comparability gap. This paper has shown that the gap is measurable, that it can be closed arithmetically, and that closing it changes what the evidence says.`,

`The framework reduces any reported figure to the fraction of its device's memory bandwidth that the configuration actually uses, computing per-token traffic from the model, the container's effective bits per weight measured rather than assumed, and a cache model that honours interleaved sliding-window attention. The roofline and MBU are borrowed; using them to falsify a measurement's stated conditions, the window-aware cache model, and the portability-oriented reporting standard are what this paper adds.`,

`Applied to a corpus in which every measurement was verified against its primary source, it establishes five things. The filter identifies three of eight measurements as incompatible with single-stream decoding, and all three prove, on checking, to have been taken at concurrency eight. Normalization removes 12% of the margin in a controlled engine gap and leaves 1.58x standing, bounded to [1.49, 1.65] once phase attribution is accounted for, the artifact being small here precisely because the two containers are close in effective bit width. Offloading is bounded by the interconnect only for systems that let it be, since one that streams only what sparsity requires plainly exceeds that bound, though by a mechanism current SwiGLU models do not supply, and by a margin its source publishes only as a picture, which is the fourth of these findings turning into an instance of the first. Quantization accuracy is near-free to roughly 4.6 bits per weight, degrading first and fastest on mathematical reasoning, with container design outweighing nominal bit width. And the true cost of a locally generated token is dominated by hardware amortization rather than electricity, which accounts for 21% of it at a realistic duty cycle.`,

`Underneath all five is one quantity. Bytes moved per token is what sets local inference throughput, what sets its energy, and what every effective technique in this literature reduces. The framework makes that quantity computable from information papers already publish, which is why we think it is the durable part of this contribution and the eight measurements are not.`,

`What the field needs is not more benchmarks but normalizable ones. The fields required are listed in Section XI, none of them is burdensome, and reporting them would let measurements accumulate rather than merely multiply. We release the framework, the verified corpus and the verification record so that the claims made here can be checked, extended, and in time superseded.`
]}
];
