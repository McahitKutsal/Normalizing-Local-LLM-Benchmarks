// VERIFIED reference list, keyed. Numbers are assigned by build.js in order of
// first citation, so the list below is in no particular order and no entry can
// silently lose its number. Every entry was checked against a primary source in
// September-October 2026; see verify/VERIFICATION_LOG.md.
// Page ranges appear ONLY where the publisher's record was read directly.
module.exports = {

// --- quantization methods and formats ---
gptq: `E. Frantar, S. Ashkboos, T. Hoefler, and D. Alistarh, "GPTQ: Accurate post-training quantization for generative pre-trained transformers," in Proc. Int. Conf. Learn. Represent. (ICLR), 2023. arXiv:2210.17323.`,
awq: `J. Lin, J. Tang, H. Tang, S. Yang, W.-M. Chen, W.-C. Wang, G. Xiao, X. Dang, C. Gan, and S. Han, "AWQ: Activation-aware weight quantization for LLM compression and acceleration," in Proc. Mach. Learn. Syst. (MLSys), vol. 6, 2024. arXiv:2306.00978.`,
smoothquant: `G. Xiao, J. Lin, M. Seznec, H. Wu, J. Demouth, and S. Han, "SmoothQuant: Accurate and efficient post-training quantization for large language models," in Proc. 40th Int. Conf. Mach. Learn. (ICML), PMLR vol. 202, 2023, pp. 38087-38099.`,
llmint8: `T. Dettmers, M. Lewis, Y. Belkada, and L. Zettlemoyer, "LLM.int8(): 8-bit matrix multiplication for transformers at scale," in Adv. Neural Inf. Process. Syst. (NeurIPS), 2022. arXiv:2208.07339.`,
hqq: `H. Badri and A. Shaji, "Half-quadratic quantization of large machine learning models," Mobius Labs GmbH, blog post, Nov. 2023. [Online]. Available: https://mobiusml.github.io/hqq_blog/`,
kquantpr: `I. Kawrakow and llama.cpp contributors, "k-quants," pull request #1684, ggml-org/llama.cpp, Jun. 2023. [Online]. Available: https://github.com/ggml-org/llama.cpp/pull/1684`,
unifiedquant: `U. Kurt, "Which quantization should I use? A unified evaluation of llama.cpp quantization on Llama-3.1-8B-Instruct," arXiv:2601.14277, 2026.`,
nvfp4: `E. Alvarez, O. Almog, E. Chung, S. Layton, D. Stosic, R. Krashinsky, and K. Aubrey, "Introducing NVFP4 for efficient and accurate low-precision inference," NVIDIA Technical Blog, Jun. 24, 2025.`,
ocpmx: `Open Compute Project, "OCP microscaling formats (MX) specification, version 1.0," 2023. [Online]. Available: https://www.opencompute.org/documents/ocp-microscaling-formats-mx-v1-0-spec-final-pdf`,
sparsegpt: `E. Frantar and D. Alistarh, "SparseGPT: Massive language models can be accurately pruned in one-shot," in Proc. 40th Int. Conf. Mach. Learn. (ICML), PMLR vol. 202, 2023, pp. 10323-10337.`,
moqe: `Y. J. Kim, R. Fahim, and H. H. Awadalla, "Mixture of quantized experts (MoQE): Complementary effect of low-bit quantization and robustness," arXiv:2310.02410, 2023.`,
anyprecision: `Y. Park, J. Hyun, S. Cho, B. Sim, and J. W. Lee, "Any-precision LLM: Low-cost deployment of multiple, different-sized LLMs," in Proc. 41st Int. Conf. Mach. Learn. (ICML), PMLR vol. 235, 2024, pp. 39682-39701.`,

// --- engines, kernels, runtimes ---
llamacpp: `G. Gerganov and llama.cpp contributors, "llama.cpp: LLM inference in C/C++," GitHub repository, ggml-org/llama.cpp, 2023-2026.`,
vllm: `W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E. Gonzalez, H. Zhang, and I. Stoica, "Efficient memory management for large language model serving with PagedAttention," in Proc. 29th ACM Symp. Oper. Syst. Princ. (SOSP), 2023, pp. 611-626.`,
flashattn2: `T. Dao, "FlashAttention-2: Faster attention with better parallelism and work partitioning," in Proc. Int. Conf. Learn. Represent. (ICLR), 2024. arXiv:2307.08691.`,
trtllm: `NVIDIA Corporation, "TensorRT-LLM," GitHub repository, NVIDIA/TensorRT-LLM, 2023-2026.`,
exllama: `Turboderp and contributors, "ExLlamaV2: A fast inference library for running LLMs locally on modern consumer-class GPUs," GitHub repository, turboderp-org/exllamav2, 2023-2026. The README states the project is archived and development continues on ExLlamaV3.`,
sglang: `L. Zheng, L. Yin, Z. Xie, C. Sun, J. Huang, C. H. Yu, S. Cao, C. Kozyrakis, I. Stoica, J. E. Gonzalez, C. Barrett, and Y. Sheng, "SGLang: Efficient execution of structured language model programs," in Adv. Neural Inf. Process. Syst. (NeurIPS), 2024. arXiv:2312.07104.`,
webllm: `C. F. Ruan, Y. Qin, X. Zhou, R. Lai, H. Jin, Y. Dong, B. Hou, M.-S. Yu, Y. Zhai, S. Agarwal, H. Cao, S. Feng, and T. Chen, "WebLLM: A high-performance in-browser LLM inference engine," arXiv:2412.15803, 2024.`,
marlin: `E. Frantar, R. L. Castro, J. Chen, T. Hoefler, and D. Alistarh, "MARLIN: Mixed-precision auto-regressive parallel inference on large language models," arXiv:2408.11743, 2024.`,

// --- placement, offloading, mixture-of-experts ---
flexgen: `Y. Sheng, L. Zheng, B. Yuan, Z. Li, M. Ryabinin, B. Chen, P. Liang, C. Re, I. Stoica, and C. Zhang, "FlexGen: High-throughput generative inference of large language models with a single GPU," in Proc. 40th Int. Conf. Mach. Learn. (ICML), PMLR vol. 202, 2023, pp. 31094-31116.`,
powerinfer: `Y. Song, Z. Mi, H. Xie, and H. Chen, "PowerInfer: Fast large language model serving with a consumer-grade GPU," in Proc. ACM SIGOPS 30th Symp. Oper. Syst. Princ. (SOSP), 2024, pp. 590-606. doi:10.1145/3694715.3695964.`,
moeoffload: `A. Eliseev and D. Mazur, "Fast inference of mixture-of-experts language models with offloading," arXiv:2312.17238, 2023.`,
moeinfinity: `L. Xue, Y. Fu, Z. Lu, L. Mai, and M. Marina, "MoE-Infinity: Efficient MoE inference on personal machines with sparsity-aware expert cache," arXiv:2401.14361, 2024.`,
fiddler: `K. Kamahori, T. Tang, Y. Gu, K. Zhu, and B. Kasikci, "Fiddler: CPU-GPU orchestration for fast inference of mixture-of-experts models," in Proc. Int. Conf. Learn. Represent. (ICLR), 2025. arXiv:2402.07033.`,
hybrimoe: `S. Zhong, Y. Sun, L. Liang, R. Wang, R. Huang, and M. Li, "HybriMoE: Hybrid CPU-GPU scheduling and cache management for efficient MoE inference," in Proc. 62nd ACM/IEEE Des. Autom. Conf. (DAC), 2025. doi:10.1109/DAC63849.2025.11133274.`,
adapmoe: `S. Zhong, L. Liang, Y. Wang, R. Wang, R. Huang, and M. Li, "AdapMoE: Adaptive sensitivity-based expert gating and management for efficient MoE inference," in Proc. 43rd IEEE/ACM Int. Conf. Comput.-Aided Des. (ICCAD), 2024. doi:10.1145/3676536.3676741.`,
dali: `Z. Zhu, G. Li, P. Wang, Z. Mo, M. Pei, Z. Song, X. Liang, and J. Cheng, "DALI: A workload-aware offloading framework for efficient MoE inference on local PCs," arXiv:2602.03495, 2026.`,
zeroinfinity: `S. Rajbhandari, O. Ruwase, J. Rasley, S. Smith, and Y. He, "ZeRO-Infinity: Breaking the GPU memory wall for extreme scale deep learning," in Proc. Int. Conf. High Perform. Comput. Netw. Storage Anal. (SC), 2021. arXiv:2104.07857.`,

// --- performance models and speculative decoding ---
roofline: `S. Williams, A. Waterman, and D. Patterson, "Roofline: An insightful visual performance model for multicore architectures," Commun. ACM, vol. 52, no. 4, pp. 65-76, 2009. doi:10.1145/1498765.1498785.`,
scalinginf: `R. Pope, S. Douglas, A. Chowdhery, J. Devlin, J. Bradbury, A. Levskaya, J. Heek, K. Xiao, S. Agrawal, and J. Dean, "Efficiently scaling transformer inference," in Proc. Mach. Learn. Syst. (MLSys), vol. 5, 2023. arXiv:2211.05102.`,
specdec: `Y. Leviathan, M. Kalman, and Y. Matias, "Fast inference from transformers via speculative decoding," in Proc. 40th Int. Conf. Mach. Learn. (ICML), PMLR vol. 202, 2023, pp. 19274-19286.`,
medusa: `T. Cai, Y. Li, Z. Geng, H. Peng, J. D. Lee, D. Chen, and T. Dao, "Medusa: Simple LLM inference acceleration framework with multiple decoding heads," in Proc. 41st Int. Conf. Mach. Learn. (ICML), PMLR vol. 235, 2024, pp. 5209-5235.`,
eagle: `Y. Li, F. Wei, C. Zhang, and H. Zhang, "EAGLE: Speculative sampling requires rethinking feature uncertainty," in Proc. 41st Int. Conf. Mach. Learn. (ICML), PMLR vol. 235, 2024, pp. 28935-28948.`,
eagle3: `Y. Li, F. Wei, C. Zhang, and H. Zhang, "EAGLE-3: Scaling up inference acceleration of large language models via training-time test," arXiv:2503.01840, 2025.`,
specsurvey: `H. Xia, Z. Yang, Q. Dong, P. Wang, Y. Li, T. Ge, T. Liu, W. Li, and Z. Sui, "Unlocking efficiency in large language model inference: A comprehensive survey of speculative decoding," in Findings Assoc. Comput. Linguistics: ACL 2024, 2024, pp. 7655-7671.`,

// --- measurement sources in the corpus ---
knoop: `J. Knoop and H. Holtmann, "Private LLM inference on consumer Blackwell GPUs: A practical guide for cost-effective local deployment in SMEs," arXiv:2601.09527, 2026.`,
puget: `J. Allman, "LLM inference - consumer GPU performance," Puget Systems Labs technical report, Aug. 22, 2024. [Online]. Available: https://www.pugetsystems.com/labs/articles/llm-inference-consumer-gpu-performance/`,
menlo: `Menlo Research, "Benchmarking NVIDIA TensorRT-LLM," technical report, Apr. 29, 2024. [Online]. Available: https://menlo.ai/blog/benchmarking-nvidia-tensorrt-llm`,
nvidiablog: `A. Chockalingam, "Accelerating LLMs with llama.cpp on NVIDIA RTX systems," NVIDIA Technical Blog, Oct. 2, 2024.`,
nvidiaoss: `A. Chockalingam, "OpenAI's new open models accelerated locally on NVIDIA GeForce RTX and RTX PRO GPUs," NVIDIA Blog, Aug. 5, 2025. [Online]. Available: https://blogs.nvidia.com/blog/rtx-ai-garage-openai-oss/`,
techradar: `TechRadar, "NVIDIA RTX AI PCs pair with OpenAI's open-weight gpt-oss-20b for a huge performance boost," sponsor content created with NVIDIA, Oct. 20, 2025. [Online]. Available: https://www.techradar.com/ai-platforms-assistants/gpt-oss-20b-performance-faster-pc-rtx-nvidia`,
hwcorner: `A. Witt, "The definitive GPU ranking for LLMs: Token generation & prompt processing performance," Hardware Corner, Dec. 9, 2025. [Online]. Available: https://www.hardware-corner.net/gpu-ranking-local-llm/`,
llamacppbench: `O. Shulyakov and llama.cpp contributors, "Performance of llama.cpp on Nvidia CUDA," GitHub discussion 15013, ggml-org/llama.cpp, 2025. [Online]. Available: https://github.com/ggml-org/llama.cpp/discussions/15013`,
qwen3moe: `Qwen Team, "Qwen3-30B-A3B," model configuration, 2025. [Online]. Available: https://huggingface.co/Qwen/Qwen3-30B-A3B`,
zahl: `P. M. Zähl, E. Dalipaj, A. Hennig, and T. Bayer, "Energy efficiency of locally deployed LLMs: A preliminary quantitative GPU power benchmark on consumer hardware," arXiv:2608.00008, 2026.`,

// --- energy measurement ---
tokenpower: `C. Niu, W. Zhang, J. Li, Y. Zhao, T. Wang, X. Wang, and Y. Chen, "TokenPowerBench: Benchmarking the power consumption of LLM inference," in Proc. AAAI Conf. Artif. Intell., vol. 40, no. 38, 2026, pp. 32582-32590. doi:10.1609/aaai.v40i38.40535.`,
zeus: `J. You, J.-W. Chung, and M. Chowdhury, "Zeus: Understanding and optimizing GPU energy consumption of DNN training," in Proc. 20th USENIX Symp. Netw. Syst. Des. Implement. (NSDI), 2023. arXiv:2208.06102.`,
mlenergy: `J.-W. Chung, J. J. Ma, R. Wu, J. Liu, O. J. Kweon, Y. Xia, Z. Wu, and M. Chowdhury, "The ML.ENERGY benchmark: Toward automated inference energy measurement and optimization," arXiv:2505.06371, 2025.`,
joules: `J.-W. Chung, R. Wu, J. J. Ma, and M. Chowdhury, "Where do the joules go? Diagnosing inference energy consumption," arXiv:2601.22076, 2026.`,
reqenergy: `P. Vellaisamy, V. Lam, S. Blanton, and J. P. Shen, "Characterization of request and token energy costs for LLM inference workloads on GPU platforms," arXiv:2608.28044, 2026.`,

// --- surveys and benchmarking methodology ---
ondeviceeval: `Q. Song, R. Liu, W. Lin, P. Liao, W. Zhao, Y. Wang, S. Hu, Y. Jiang, M. Long, H.-L. Zhen, N. Jiang, M. Yuan, Q. Xiang, and H. Xu, "A systematic evaluation of on-device LLMs: Quantization, performance, and resources," arXiv:2505.15030, 2025.`,
ondevicereview: `J. Xu, Z. Li, W. Chen, Q. Wang, X. Gao, Q. Cai, and Z. Ling, "On-device language models: A comprehensive review," arXiv:2409.00088, 2024.`,
edgesurvey: `G. Cai, R. Tian, L. Yang, Y. Jia, L. Li, and J. Wang, "Efficient inference for edge large language models: A survey," Tsinghua Sci. Technol., vol. 31, no. 3, pp. 1365-1380, 2026. doi:10.26599/TST.2025.9010166.`,
hwperspective: `J. Li, J. Xu, S. Huang, Y. Chen, W. Li, J. Liu, Y. Lian, J. Pan, L. Ding, H. Zhou, Y. Wang, and G. Dai, "Large language model inference acceleration: A comprehensive hardware perspective," arXiv:2410.04466, 2024.`,
langiants: `Y. C. Kim, S. K. Yoon, S. S. Han, C. W. Park, J. O. Park, J. H. Ko, and H. Kim, "Accelerating language giants: A survey of optimization strategies for LLM inference on hardware platforms," J. Syst. Archit., vol. 172, art. 103690, 2026. doi:10.1016/j.sysarc.2026.103690.`,
gdpr: `Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation), Chapter V, Arts. 44-50, Official Journal of the European Union, L 119, pp. 1-88, May 4, 2016.`,
mobilesurvey: `S. Katakam, "On-device large language models for mobile applications: A systematic survey of optimization strategies, deployment challenges, and privacy implications," ScienceOpen Preprints, 2026. doi:10.14293/PR2199.003569.v1.`,
rooflinebench: `Z. Bi, X. Chen, L. Sun, Y. Yao, Q. Shen, J. Lou, and C. Deng, "RooflineBench: A benchmarking framework for on-device LLMs via roofline analysis," arXiv:2602.11506, 2026.`,
mlperf: `V. J. Reddi, C. Cheng, D. Kanter, P. Mattson, G. Schmuelling, C.-J. Wu, B. Anderson, M. Breughe, M. Charlebois, W. Chou, et al., "MLPerf inference benchmark," in Proc. 47th ACM/IEEE Annu. Int. Symp. Comput. Archit. (ISCA), 2020. arXiv:1911.02549.`,
mlperfclient: `MLCommons Association, "MLPerf Client benchmark," 2025. [Online]. Available: https://mlcommons.org/benchmarks/client/`,
localscore: `C. J. Pais, "Introducing LocalScore: A local LLM benchmark," Mozilla Builders, 2025. [Online]. Available: https://www.localscore.ai/blog`,
lmeval: `L. Gao, J. Tow, B. Abbasi, S. Biderman, S. Black, A. DiPofi, C. Foster, L. Golding, J. Hsu, A. Le Noac'h, et al., "The Language Model Evaluation Harness," Zenodo, v0.4.3, Jul. 2024. doi:10.5281/zenodo.12608602.`,
nondeterminism: `J. Yuan, H. Li, X. Ding, W. Xie, Y.-J. Li, W. Zhao, K. Wan, J. Shi, X. Hu, and Z. Liu, "Understanding and mitigating numerical sources of nondeterminism in LLM inference," arXiv:2506.09501, 2025.`,
metametrics: `S. Salaria, Z. Liu, and N. M. Gonzalez, "Meta-metrics and best practices for system-level inference performance benchmarking," arXiv:2508.10251, 2025.`,

// --- models ---
llama3: `Llama Team, AI @ Meta, "The Llama 3 herd of models," arXiv:2407.21783, 2024.`,
qwen3: `Qwen Team, "Qwen3 technical report," arXiv:2505.09388, 2025.`,
gemma3: `Gemma Team, "Gemma 3 technical report," arXiv:2503.19786, 2025.`,
mixtral: `A. Q. Jiang, A. Sablayrolles, A. Roux, A. Mensch, B. Savary, C. Bamford, D. S. Chaplot, et al., "Mixtral of experts," arXiv:2401.04088, 2024.`,
gptoss: `OpenAI, "gpt-oss-120b & gpt-oss-20b model card," arXiv:2508.10925, 2025.`,
};
