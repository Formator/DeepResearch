# OpenRouter Setup Guide - Using ONLY Tongyi Qwen Models

This guide shows how to use DeepResearch with **only OpenRouter and Tongyi Qwen models** - no OpenAI API needed!

## What Changed?

✅ **Main Model**: `alibaba/tongyi-deepresearch-30b-a3b` via OpenRouter  
✅ **Summarization Model**: `alibaba/qwen-max` via OpenRouter (configurable)  
❌ **No OpenAI API needed** - everything goes through OpenRouter

## Quick Setup

### 0. Install Dependencies

**Option A: Using pyproject.toml (Recommended)**

From the repository root:
```bash
pip install -e .
```

**Option B: Using minimal requirements file**

From the inference directory:
```bash
cd inference
pip install -r requirements-openrouter.txt
```

**What's NOT needed:**
- ❌ PyTorch (no local model training)
- ❌ vLLM (no local model serving)
- ❌ CUDA/GPU drivers (cloud-based only)
- ❌ Transformers heavy models
- ❌ 100+ GB model downloads

**What IS needed:**
- ✅ OpenAI SDK (for OpenRouter API)
- ✅ qwen-agent (agent framework)
- ✅ Basic web tools (requests, httpx)
- ✅ File parsers (PDF, Excel, PPT)
- ✅ ~500 MB of dependencies (vs 50+ GB for local setup)

### 1. Get Your API Keys

You need only **3 API keys**:

- **OpenRouter API Key** (Required)
  - Sign up at: https://openrouter.ai/
  - Get your API key from: https://openrouter.ai/keys
  - Format: `sk-or-v1-xxxxxxxxxxxxx`

- **Serper API Key** (Required, FREE tier available)
  - Sign up at: https://serper.dev/
  - Free tier: 2,500 searches/month
  - Format: `xxxxxxxxxxxxx`

- **Jina API Key** (Required, FREE tier available)
  - Sign up at: https://jina.ai/
  - Free tier available for web reading
  - Format: `jina_xxxxxxxxxxxxx`

### 2. Set Environment Variables

**Option A: Create a .env file** (Recommended)

```bash
cd inference
cp env.template .env
# Edit .env with your actual API keys
```

Your `.env` file should look like:

```bash
OPENROUTER_API_KEY=sk-or-v1-your-actual-key
SERPER_KEY_ID=your-actual-key
JINA_API_KEYS=jina_your-actual-key

# Optional: Use different Qwen model for summarization
SUMMARY_MODEL_NAME=alibaba/qwen-max
```

**Option B: Export directly**

```bash
export OPENROUTER_API_KEY='sk-or-v1-your-actual-key'
export SERPER_KEY_ID='your-actual-key'
export JINA_API_KEYS='jina_your-actual-key'
```

### 3. Run the Research

```bash
# Using the bash script (easiest)
bash run_openrouter_yang.sh

# Or directly with Python
python run_openrouter.py --topic "Yang Zhenning" --output "./outputs"

# Custom topic
python run_openrouter.py --topic "Quantum Computing" --output "./outputs/quantum"
```

## Models Used

### Main Agent Model
- **Default**: `alibaba/tongyi-deepresearch-30b-a3b`
- This is the primary reasoning model for the research agent
- Configured via `--model` parameter

### Summarization Model
- **Default**: `alibaba/qwen-max`
- Used for summarizing web pages during research
- Configured via `SUMMARY_MODEL_NAME` environment variable
- Other options:
  - `alibaba/qwen-turbo` (faster, cheaper)
  - `alibaba/qwen-plus` (balanced)
  - `alibaba/qwen-max` (best quality)

## Example Usage

```python
from openai import OpenAI

# This is how we're calling OpenRouter
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "https://github.com/QwenLM/DeepResearch",
    "X-Title": "DeepResearch",
  },
  model="alibaba/tongyi-deepresearch-30b-a3b",
  messages=[
    {"role": "user", "content": "Research Yang Zhenning"}
  ]
)
```

## Troubleshooting

### Missing API Keys Error

If you see:
```
❌ Missing required environment variables
```

Make sure you've:
1. Created the `.env` file in the `inference/` directory
2. Added all 3 required API keys
3. If using bash, run: `source .env` to load the variables

### OpenRouter API Error

If you see OpenRouter connection errors:
1. Check your API key is valid at https://openrouter.ai/keys
2. Verify you have credits in your OpenRouter account
3. The model `alibaba/tongyi-deepresearch-30b-a3b` is available on OpenRouter

### Model Not Found

If the model is unavailable:
- Try an alternative Qwen model: `alibaba/qwen-max` or `alibaba/qwen-turbo`
- Pass it via: `--model "alibaba/qwen-max"`

## Cost Estimation

OpenRouter pricing for Alibaba/Qwen models is very competitive:
- Check current pricing at: https://openrouter.ai/models
- Most Qwen models are significantly cheaper than GPT-4

## Notes

- **No OpenAI API needed**: Everything runs through OpenRouter
- **Both main and summarization models** use OpenRouter endpoints
- The code includes proper retry logic and error handling
- Results are saved in both JSON and Markdown formats

