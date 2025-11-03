# OpenRouter Configuration Summary

Complete guide to using DeepResearch with **only OpenRouter** (no local models, no OpenAI official API).

## 📦 What Was Created

### 1. Dependency Management

#### **`pyproject.toml`** (Repository Root)
- Modern Python package configuration
- Minimal dependencies (~30 packages vs 150+)
- ~500 MB - 1 GB vs 50-100 GB
- **Install:** `pip install -e .`

#### **`inference/requirements-openrouter.txt`**
- Alternative pip requirements file
- Same minimal dependencies
- **Install:** `pip install -r inference/requirements-openrouter.txt`

### 2. Configuration Files

#### **`inference/env.template`**
- Template for environment variables
- Only 3 required API keys (vs 5)
- **Usage:** `cp inference/env.template inference/.env`

### 3. Documentation

#### **`inference/OPENROUTER_SETUP.md`**
- Complete setup guide
- API key instructions
- Usage examples
- Troubleshooting

#### **`inference/INSTALL.md`**
- Installation instructions
- Multiple installation options
- Verification steps
- Quick reference

#### **`inference/INSTALL_COMPARISON.md`**
- Full vs minimal setup comparison
- Size and cost comparison
- Use case recommendations
- Switching guide

#### **`inference/CHANGES_OPENROUTER_ONLY.md`**
- Detailed changelog
- Code modifications
- Breaking changes
- Migration guide

#### **`OPENROUTER_SUMMARY.md`** (This file)
- Overview of all changes
- Quick links
- Setup checklist

---

## 🔧 Code Modifications

### Modified Files

1. **`inference/tool_visit.py`**
   - Changed from OpenAI API to OpenRouter
   - Uses `OPENROUTER_API_KEY` instead of `API_KEY`
   - Default model: `alibaba/qwen-max`

2. **`inference/react_agent_openrouter.py`**
   - Added OpenRouter headers
   - Proper site referrer for rankings

3. **`inference/run_openrouter.py`**
   - Removed `API_KEY` and `API_BASE` requirements
   - Updated default summary model
   - Cleaner environment checks

4. **`inference/run_openrouter_yang.sh`**
   - Only 3 required variables (not 5)
   - Updated model defaults
   - Simplified setup

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install

```bash
cd DeepResearch
pip install -e .
```

### Step 2: Configure

```bash
cd inference
cp env.template .env
# Edit .env with your API keys:
# - OPENROUTER_API_KEY (from https://openrouter.ai/keys)
# - SERPER_KEY_ID (from https://serper.dev/)
# - JINA_API_KEYS (from https://jina.ai/)
```

### Step 3: Run

```bash
bash run_openrouter_yang.sh
```

---

## 📋 Environment Variables

### Required (3 keys only!)

```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx  # OpenRouter API
SERPER_KEY_ID=xxxxxxxxxxxxx                # Serper Search (FREE tier)
JINA_API_KEYS=jina_xxxxxxxxxxxxx           # Jina Reader (FREE tier)
```

### Optional

```bash
SUMMARY_MODEL_NAME=alibaba/qwen-max        # Summarization model (default)
MAX_LLM_CALL_PER_RUN=100                   # Max iterations (default)
```

### ❌ No Longer Needed

```bash
API_KEY=...          # ❌ OpenAI API key - REMOVED
API_BASE=...         # ❌ OpenAI endpoint - REMOVED
```

---

## 🎯 What Changed

### Before (OpenAI + OpenRouter)

- Required **5 API keys**
- Used OpenAI for summarization
- Used OpenRouter for main agent
- Confusing setup with multiple providers

### After (OpenRouter Only)

- Required **3 API keys**
- Uses OpenRouter for everything
- Uses Tongyi Qwen models for all tasks
- Single provider, simpler setup

---

## 💻 Models Used

### Main Research Agent
```python
model = "alibaba/tongyi-deepresearch-30b-a3b"
```

### Web Page Summarization
```python
model = "alibaba/qwen-max"  # or qwen-turbo, qwen-plus
```

Both via OpenRouter endpoint: `https://openrouter.ai/api/v1`

---

## 📦 Installation Size

| Setup Type | Packages | Size | GPU | Time |
|-----------|----------|------|-----|------|
| **OpenRouter** | ~30 | 1 GB | ❌ No | 2-5 min |
| Full Local | ~150 | 50-100 GB | ✅ Yes | 1-2 hours |

**Space saved: 49-99 GB!**

---

## 🔗 API Keys (Get for Free!)

1. **OpenRouter** (Pay-as-you-go)
   - Sign up: https://openrouter.ai/
   - Get key: https://openrouter.ai/keys
   - Cost: ~$0.01-0.05 per research

2. **Serper** (FREE tier: 2,500 searches/month)
   - Sign up: https://serper.dev/
   - Totally free tier available

3. **Jina** (FREE tier available)
   - Sign up: https://jina.ai/
   - Free web reading

**Total cost to get started: $0**

---

## 📚 Documentation Index

| File | Purpose |
|------|---------|
| `pyproject.toml` | Package configuration |
| `inference/requirements-openrouter.txt` | Pip requirements |
| `inference/env.template` | Environment variables template |
| `inference/INSTALL.md` | Installation guide |
| `inference/OPENROUTER_SETUP.md` | Complete setup guide |
| `inference/INSTALL_COMPARISON.md` | Full vs minimal comparison |
| `inference/CHANGES_OPENROUTER_ONLY.md` | Detailed changes |
| `OPENROUTER_SUMMARY.md` | This file (overview) |

---

## ✅ Setup Checklist

- [ ] Install minimal dependencies (`pip install -e .`)
- [ ] Get OpenRouter API key
- [ ] Get Serper API key (free)
- [ ] Get Jina API key (free)
- [ ] Copy `env.template` to `.env`
- [ ] Edit `.env` with your keys
- [ ] Run `bash run_openrouter_yang.sh`
- [ ] Check output in `outputs/` directory

---

## 🆘 Getting Help

### Common Issues

1. **"Missing API key"**
   - Check `.env` file exists in `inference/` directory
   - Verify all 3 keys are set
   - Try: `source .env` (in bash)

2. **"Package not found"**
   - Make sure you ran: `pip install -e .`
   - Try: `pip install -r inference/requirements-openrouter.txt`

3. **"OpenRouter error"**
   - Check API key is valid at https://openrouter.ai/keys
   - Verify you have credits

### Documentation

- Read `inference/OPENROUTER_SETUP.md` for detailed setup
- Read `inference/INSTALL_COMPARISON.md` for installation options
- Check `inference/CHANGES_OPENROUTER_ONLY.md` for technical details

---

## 🎉 Benefits

✅ **Smaller:** 1 GB vs 50-100 GB  
✅ **Faster:** 2-5 min setup vs 1-2 hours  
✅ **Simpler:** 3 API keys vs 5  
✅ **Cheaper:** No GPU needed ($0 hardware)  
✅ **Cleaner:** Single API provider  
✅ **Modern:** Uses pyproject.toml  

---

## 🚀 You're Ready!

Everything is set up to use **only OpenRouter with Tongyi Qwen models**.

```bash
# Quick start
cd DeepResearch
pip install -e .
cd inference
cp env.template .env
# Edit .env with your keys
bash run_openrouter_yang.sh
```

**No OpenAI account needed. No local models. Just OpenRouter!** 🎊

