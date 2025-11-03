# Installation Comparison: Full vs OpenRouter-Only

## 🆚 Size Comparison

### Full Installation (Local Model Deployment)
```bash
pip install -r requirements.txt
```

**Size:** ~50-100 GB total
- PyTorch: ~5 GB
- CUDA libraries: ~4 GB
- vLLM: ~3 GB
- Model weights: 30-80 GB (depending on model)
- Other dependencies: ~5 GB

**Use case:** Running models locally on your GPU

---

### OpenRouter-Only Installation (Cloud-Based)
```bash
# Option 1: Using pyproject.toml
pip install -e .

# Option 2: Using minimal requirements
pip install -r inference/requirements-openrouter.txt
```

**Size:** ~500 MB - 1 GB total
- Core dependencies only
- No PyTorch
- No CUDA
- No model downloads
- Just API clients and tools

**Use case:** Running everything via OpenRouter API

---

## 📦 What's Removed in OpenRouter-Only

### Heavy ML Libraries (Removed)
```python
# ❌ Not needed for OpenRouter
torch==2.7.1                    # ~5 GB
torchvision==0.22.1             # ~1 GB
torchaudio==2.7.1               # ~500 MB
vllm==0.10.1                    # ~3 GB
transformers==4.56.1            # Uses only tokenizer, much lighter
```

### CUDA Libraries (Removed)
```python
# ❌ Not needed for cloud-based
# nvidia-cuda-*
# nvidia-cudnn-*
# nvidia-cublas-*
# cupy-cuda12x
# triton
# xformers
```

### Local Model Tools (Removed)
```python
# ❌ Not needed for OpenRouter
dashscope==1.24.4              # Alibaba local models
modelscope==1.30.0             # Model downloads
```

### What Stays (Kept)

```python
# ✅ Essential for OpenRouter
openai>=1.0.0                  # OpenRouter API client
qwen-agent>=0.0.26             # Agent framework
requests>=2.32.0               # HTTP requests
rich>=14.0.0                   # CLI UI
tiktoken>=0.6.0                # Token counting
sandbox-fusion>=0.3.0          # Code execution
pandas>=2.0.0                  # File parsing
pdfplumber>=0.11.0             # PDF parsing
python-pptx>=1.0.0             # PPT parsing
```

---

## 🚀 Quick Start Commands

### For OpenRouter-Only Setup

```bash
# Clone the repo
git clone https://github.com/QwenLM/DeepResearch.git
cd DeepResearch

# Install minimal dependencies
pip install -e .

# Set up your environment
cd inference
cp env.template .env
# Edit .env with your API keys

# Run!
bash run_openrouter_yang.sh
```

**Time to start:** 2-5 minutes ⚡
**Disk space:** ~1 GB 💾
**No GPU needed:** ✅

---

### For Full Local Setup

```bash
# Clone the repo
git clone https://github.com/QwenLM/DeepResearch.git
cd DeepResearch

# Install full dependencies
pip install -r requirements.txt

# Download models (30-80 GB)
# Set up vLLM server
# Configure GPU...

# Run!
```

**Time to start:** 1-2 hours 🐌
**Disk space:** 50-100 GB 💾
**GPU required:** ✅ (24GB+ VRAM)

---

## 💰 Cost Comparison

### Local Deployment
- **Setup cost:** GPU hardware ($1,000 - $10,000)
- **Running cost:** Electricity (~$0.10-0.50 per hour)
- **Maintenance:** High (updates, CUDA, drivers)
- **Best for:** Heavy usage, privacy requirements

### OpenRouter API
- **Setup cost:** $0
- **Running cost:** Pay per token (~$0.01-0.05 per research)
- **Maintenance:** None
- **Best for:** Occasional use, testing, no GPU available

---

## 🎯 Which Should You Use?

### Use OpenRouter-Only If:
- ✅ You don't have a GPU
- ✅ You want to start quickly
- ✅ You're testing or developing
- ✅ You run research occasionally
- ✅ You don't want to maintain infrastructure

### Use Full Local If:
- ✅ You have a powerful GPU (24GB+ VRAM)
- ✅ You need privacy (data stays local)
- ✅ You run many research tasks daily
- ✅ You want full control over models
- ✅ You have technical expertise

---

## 📊 Dependency Count

| Setup | Total Packages | Size | GPU Required |
|-------|---------------|------|--------------|
| Full | ~150 packages | 50-100 GB | Yes (24GB+) |
| OpenRouter | ~30 packages | 500 MB - 1 GB | No |

---

## 🔄 Can I Switch?

Yes! You can:

1. **Start with OpenRouter** (fast setup, test everything)
2. **Switch to local later** if needed (install full requirements.txt)

The code is compatible with both setups. Just change:
- OpenRouter: Use `run_openrouter.py`
- Local: Use `run_react_infer.sh` or `run_multi_react.py`

---

## 📝 Installation Commands Reference

```bash
# OpenRouter-Only (Recommended for most users)
pip install -e .
# or
pip install -r inference/requirements-openrouter.txt

# Full Local Setup (For GPU users)
pip install -r requirements.txt

# Check what's installed
pip list | grep -E "torch|openai|qwen"
```

---

## 🆘 Troubleshooting

### "Too many dependencies" error
If you accidentally installed full requirements:
```bash
# Create a fresh virtual environment
python -m venv venv-openrouter
source venv-openrouter/bin/activate  # or .\venv-openrouter\Scripts\activate on Windows
pip install -e .
```

### "Package not found" error
Make sure you're in the right directory:
```bash
cd /path/to/DeepResearch
pip install -e .
```

### "qwen-agent" issues
Update to latest:
```bash
pip install -U qwen-agent
```

