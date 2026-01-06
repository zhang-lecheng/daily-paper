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
