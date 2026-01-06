# Daily AI4Science & Perturbation Prediction Papers

This repository automatically tracks daily arXiv papers related to **AI4Science** and **Perturbation Prediction** using DeepSeek AI.

## How it works
1. **Fetch**: Every day, it crawls arXiv for new papers in categories like `cs.AI`, `cs.LG`, `stat.ML`, `q-bio.QM`, etc.
2. **Filter**: It use DeepSeek API to analyze abstracts and filter for:
   - **AI4Science**: Applications of AI in biology, chemistry, physics, etc.
   - **Perturbation Prediction**: Specifically predicting cell responses to perturbations.
3. **Notify**: Results are appended to this README.

## Setup
1. Fork this repository.
2. Add your DeepSeek API key to GitHub Secrets:
   - Go to `Settings` -> `Secrets and variables` -> `Actions`.
   - Create a new secret named `DEEPSEEK_API_KEY`.
3. The workflow runs daily at 02:00 UTC. You can also trigger it manually in the `Actions` tab.

---
<!-- Generated Papers Below -->


## 2026-01-06

### [Meta-Learning Guided Pruning for Few-Shot Plant Pathology on Edge Devices](http://arxiv.org/abs/2601.02353v1)
- **Authors**: Shahnawaz Alam, Mohammed Mudassir Uddin, Mohammed Kaif Pasha
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文属于AI4Science领域，因为它将人工智能技术（元学习和神经网络剪枝）应用于植物病理学的科学发现和数据分类任务，帮助农民通过图像识别诊断植物疾病。但它不属于扰动预测领域，因为论文关注的是静态图像分类而非预测细胞对化学或遗传扰动的动态响应。

### [Hunting for "Oddballs" with Machine Learning: Detecting Anomalous Exoplanets Using a Deep-Learned Low-Dimensional Representation of Transit Spectra with Autoencoders](http://arxiv.org/abs/2601.02324v1)
- **Authors**: Alexander Roman, Emilie Panek, Roy T. Forestano, Eyup B. Unlu, Katia Matcheva, Konstantin T. Matchev
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文使用自编码器进行异常检测，识别具有非常规化学特征的外行星大气，属于AI在科学发现（天文学）中的应用，符合AI4Science范畴。但研究聚焦于异常检测而非预测细胞对化学或遗传扰动的响应，与扰动预测领域无关。

### [Environment-Adaptive Covariate Selection: Learning When to Use Spurious Correlations for Out-of-Distribution Prediction](http://arxiv.org/abs/2601.02322v1)
- **Authors**: Shuozhi Zuo, Yixin Wang
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文提出了一种环境自适应协变量选择算法，用于改进分布外预测，这属于AI在科学数据分析中的应用，符合AI4Science范畴。虽然论文涉及生物或化学数据集的应用，但其核心是通用的机器学习方法，而非专门针对细胞扰动响应的预测，因此不属于Perturbation Prediction领域。

### [TopoLoRA-SAM: Topology-Aware Parameter-Efficient Adaptation of Foundation Segmenters for Thin-Structure and Cross-Domain Binary Semantic Segmentation](http://arxiv.org/abs/2601.02273v1)
- **Authors**: Salim Khazem
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文属于AI4Science领域，因为它开发了一种参数高效的AI方法（TopoLoRA-SAM）用于生物医学图像分割（如视网膜血管、息肉）和遥感图像分析（SAR海陆分割），这些是AI在科学发现和数据分析中的应用。但论文不涉及扰动预测，因为它专注于图像分割技术改进，而非预测细胞对化学或遗传扰动的响应。

### [Predicting Early and Complete Drug Release from Long-Acting Injectables Using Explainable Machine Learning](http://arxiv.org/abs/2601.02265v1)
- **Authors**: Karla N. Robles, Manar D. Samad
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文使用可解释机器学习方法预测药物释放曲线，属于AI在生物医学科学（具体为药物递送系统优化）中的应用，符合AI4Science定义。但论文关注的是聚合物材料特性对药物释放的影响，而非细胞对化学或遗传扰动的响应预测，因此不属于扰动预测范畴。

### [POSEIDON: Physics-Optimized Seismic Energy Inference and Detection Operating Network](http://arxiv.org/abs/2601.02264v1)
- **Authors**: Boris Kriuk, Fedor Kriuk
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文属于AI4Science领域，因为它将物理定律（古登堡-里特定律、大森-宇津余震衰减定律）作为可学习约束嵌入基于能量的建模框架，用于地震事件预测、海啸生成潜力评估等多任务科学发现。但该研究不涉及扰动预测，因为它专注于地震学中的自然物理过程预测，而非细胞对化学或遗传扰动的响应预测。

### [Neuro-Channel Networks: A Multiplication-Free Architecture by Biological Signal Transmission](http://arxiv.org/abs/2601.02253v1)
- **Authors**: Emrah Mete, Emin Erkan Korkmaz
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文提出受生物神经系统启发的无乘法神经网络架构，属于AI4Science中利用AI模拟生物机制进行科学发现和硬件优化的范畴；但论文未涉及细胞对化学或遗传扰动的响应预测，因此与扰动预测领域无关。

### [From Mice to Trains: Amortized Bayesian Inference on Graph Data](http://arxiv.org/abs/2601.02241v1)
- **Authors**: Svenja Jedhoff, Elizaveta Semenova, Aura Raulo, Anne Meyer, Paul-Christian Bürkner
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文开发了一种基于摊销贝叶斯推断的图数据推理方法，并在生物学领域进行了实际应用评估，符合AI4Science中利用AI进行科学数据分析和发现的要求。虽然涉及生物学领域，但论文主要关注图结构参数的推理而非细胞对化学或遗传扰动的响应预测，因此不属于扰动预测范畴。

### [Quantized SO(3)-Equivariant Graph Neural Networks for Efficient Molecular Property Prediction](http://arxiv.org/abs/2601.02213v1)
- **Authors**: Haoyu Zhou, Ping Xue, Tianfan Fu, Hao Zhang
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文属于AI4Science领域，因为它开发了用于分子性质预测的3D图神经网络（GNN），这是AI在化学科学中的应用。论文未涉及扰动预测，因为它专注于分子能量和力的预测，而不是细胞对化学或遗传扰动的响应。

### [Mind the Gap: Continuous Magnification Sampling for Pathology Foundation Models](http://arxiv.org/abs/2601.02198v1)
- **Authors**: Alexander Möllers, Julius Hense, Florian Schulz, Timo Milbich, Maximilian Alber, Lukas Ruff
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文属于AI4Science领域，因为它开发了用于组织病理学图像分析的病理学基础模型，涉及人工智能在生物医学科学（具体是组织病理学）中的应用，用于改进多尺度图像分析。它不属于扰动预测领域，因为论文关注的是图像放大采样策略和模型性能评估，而非预测细胞对化学或遗传扰动的响应。

### [FormationEval, an open multiple-choice benchmark for petroleum geoscience](http://arxiv.org/abs/2601.02158v1)
- **Authors**: Almaz Ermilov
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文涉及使用语言模型评估石油地球科学知识，属于AI在科学领域（地球科学）的应用，符合AI4Science的定义。但论文内容不涉及预测细胞对化学或遗传扰动的响应，因此与扰动预测无关。

### [Multi-fidelity graph-based neural networks architectures to learn Navier-Stokes solutions on non-parametrized 2D domains](http://arxiv.org/abs/2601.02157v1)
- **Authors**: Francesco Songia, Raoul Sallé de Chou, Hugues Talbot, Irene Vignon-Clementel
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文属于AI4Science领域，因为它使用图神经网络、Transformer和Mamba架构来预测Navier-Stokes方程在流体动力学中的解，将物理知识嵌入AI模型以指导科学发现过程。但该研究专注于流体力学模拟而非细胞扰动预测，不涉及化学或遗传扰动对细胞响应的预测。

### [AI-enhanced tuning of quantum dot Hamiltonians toward Majorana modes](http://arxiv.org/abs/2601.02149v1)
- **Authors**: Mateusz Krawczyk, Jarosław Pawłowski
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文使用神经网络模型分析量子点模拟器的物理数据并自动调整设备参数以实现Majorana模式，属于AI在物理学领域的科学发现应用。虽然涉及参数调整，但核心是设备优化而非预测细胞对化学或遗传扰动的响应。

### [BiPrompt: Bilateral Prompt Optimization for Visual and Textual Debiasing in Vision-Language Models](http://arxiv.org/abs/2601.02147v1)
- **Authors**: Sunny Gupta, Shounak Das, Amit Sethi
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文涉及AI模型优化（视觉语言模型去偏），属于AI4Science中AI工具开发范畴，但未涉及细胞扰动预测或生物化学实验数据。

### [Feature-based Inversion of 2.5D Controlled Source Electromagnetic Data using Generative Priors](http://arxiv.org/abs/2601.02145v1)
- **Authors**: Hongyu Zhou, Haoran Sun, Rui Guo, Maokun Li, Fan Yang, Shenheng Xu
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文使用变分自编码器（VAE）作为生成先验来约束地球物理反演过程，属于AI在科学数据分析和模拟中的应用（地球物理学领域），符合AI4Science范畴。但论文研究的是电磁数据反演中的电导率分布重建问题，而非预测细胞对化学或遗传扰动的响应，因此不属于扰动预测领域。

### [Edge-aware GAT-based protein binding site prediction](http://arxiv.org/abs/2601.02138v1)
- **Authors**: Weisen Yang, Hanqing Zhang, Wangren Qiu, Xuan Xiao, Weizhong Lin
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文使用图注意力网络（GAT）预测蛋白质结合位点，属于AI在生物分子结构分析中的应用，符合AI4Science范畴。但论文未涉及预测细胞对化学或遗传扰动的响应，因此不属于扰动预测领域。

### [Remote Sensing Change Detection via Weak Temporal Supervision](http://arxiv.org/abs/2601.02126v1)
- **Authors**: Xavier Bou, Elliot Vincent, Gabriele Facciolo, Rafael Grompone von Gioi, Jean-Michel Morel, Thibaud Ehret
- **Date**: 2026-01-05
- **Tags**: `AI4Science`
- **AI Reason**: 该论文涉及使用AI技术（弱监督学习和迭代优化）处理遥感数据，属于AI在科学数据分析（地球科学/环境监测）中的应用，符合AI4Science范畴。但论文关注的是土地覆盖变化检测，而非细胞对化学或遗传扰动的响应预测，因此不属于扰动预测领域。

