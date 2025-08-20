---
project: Robust_Prover
tags:
---

Robust_Prover
├── [README.md](README.md)
├── [.git/](.git)
├── [.gitattributes](.gitattributes)
├── [.gitignore](.gitignore)
└── [Paper/](Paper)


# Proposal: Robust Mathematical Problem Solver
1. 关于robustness：以往研究显示在提示词中加入无关信息（比如猫猫）会让模型的推理能力大幅下降（Cats Confuse Reasoning LLM: Query Agnostic Adversarial Triggers for Reasoning Models），同时需要防范提示词注入等，增加模型的抗干扰能力
2. 关于数学：数学能力是衡量模型推理能力等重要指标，有专门的程序语言（如lean等）检查逻辑是否正确
3. 关于agent：现在数据集趋于完善，但模型处理不恰当输入和自我纠错的能力并不强，利用agent调用多种工具或许可以解决这个问题

MCP协议安全性: https://mp.weixin.qq.com/s/IH5esRD9mzwbq5TCYF9eHg

Concept Explanations
1. AI agent - 自主感知、决策与行动的人工智能系统
2. 自然语言推理 - 用人类语言表达的逻辑推理过程
3. 形式化证明 - 符合严格逻辑规则的计算机验证证明
4. 形式化语言（如lean） - 为逻辑证明设计的严密表达方式
5. 模型微调（fine-tune） - 针对特定任务的进一步训练

# Info
Programme Cohort: Large Language Models & Generative AI
Course Group: GEA-Group 2
Group Name: Robust Mathematical Problem Solver
Group Members: Liu Peixuan, Long Haobo, Cao Shuhan, Wu Jiayu, Wu Xuanyu, Wei Yanran, Jin Huiyan
slogan: Logic. Rigor. Automation.

# Proposed Workflow
1. 预处理去干扰
2. 生成自然语言推理
3. 转写成形式化语言（如lean）进行自动检验
4. 根据反馈调整

扩展方向:
1. 对模型进行微调(fine-tune)以使其更适合这个任务
2. 设计更适合根据已有论文形式化的工作流

**Development Team:**
1. Anti-interference implementation (Python) - Long Haobo
2. Natural language reasoning generation and transformation (LLM calling & Agent) - Cao Shuhan
3. Auto-correction implementation (Agent) - Wu Jiayu
**Data Team:**  
4. Math problem dataset collection and organization - Wu Xuanyu
**Evaluation Team:**  
5. Test framework setup/metric calculation - Wei Yanran  
6. Evaluation results analysis - Jin Huiyan
**Coordination Team:**  
7. Progress tracking/documentation - Liu Peixuan
没有必要死板, 可以互相学习帮助

我现在在改project proposal, 因为overleaf的限制只能一个人编辑, 其他人只能看, 大家看了有需要改的地方可以联系我
关于最终的目标, 其实只需要最终能提高准确率就可以了，方法没有必要死板, 可以互相学习帮助，现在提出的几种方法或者还找的其他方法有成功的就行了, 同时需要构建整体的框架，主要是题库和评估方法
大家可以再找一些自己任务对应的文献和资料, 现在用于project proposal的文献已经够了, 主要是用于后面完成项目, 可以分享到群里
# Key References
1. DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition
2. Cats Confuse Reasoning LLM: Query Agnostic Adversarial Triggers for Reasoning Models
3. A Language-Agent Approach to Formal Theorem-Proving
4. An In-Context Learning Agent for Formal Theorem-Proving
5. Prover Agent: An Agent-based Framework for Formal Mathematical Proofs

# Presentation Outline
1. **Introduction** 1min
	- Team overview
	- Problem: LLM vulnerability to interference in math reasoning
	- Goal: Build robust math problem solver with self-correction
2. **Approach**
	- workflow outline
	- 3-stage workflow: 
	   - Preprocessing龙浩博: 先用一个较小的模型预处理去干扰, 再用去干扰后的问题生成回答 1min
	   - Reasoning and transformation曹舒涵: 包括由自然语言到lean语言, lean语言到自然语言 1min
	   - Verification武家玉 1min
3. **Implementation**刘佩轩 1.5min
	- 最终成功构建工作流, 实现用工作流解决示例问题
	- 使用JSON schema, 保留分析的情况下标准化输出
	- 使用prompt engineering, 渐进地引导AI生成答案, 并且包含足够的依赖库和定义
	- 同时支持使用线上api和本地模型
4. **Results & Evaluation**
	- Demo of workflow (example problem)刘佩轩 1min
	- Evaluation Method & Demo金慧妍/卫嫣然 1.5min
	- Dataset & Github repository we have built吴炫谕 1min
5. **Future Work**
	- 完善项目:2min
		- 修复步奏中可能会出现死循环，比如ring_nf被AI改为ring, 在下一轮中ring被AI改为ring_nf
		- 更精细的和lean的交互
	- Fine-tuning potential
	- Generalization to other domains
	- Future of computer-assisted proof 1.5min
		- Category Theory, Type Theory