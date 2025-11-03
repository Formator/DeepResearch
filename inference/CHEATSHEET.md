# 🚀 DeepResearch OpenRouter - One-Page Cheat Sheet

## ⚡ Setup (2 minutes)

```bash
cd inference
cp .env.openrouter.example .env
nano .env  # Add your API keys
python verify_openrouter_setup.py
```

## 🔑 Required API Keys

```bash
OPENROUTER_API_KEY=sk-or-v1-xxx     # openrouter.ai
SERPER_KEY_ID=xxx                   # serper.dev (FREE!)
JINA_API_KEYS=jina_xxx              # jina.ai (FREE!)
API_KEY=sk-xxx                      # platform.openai.com
API_BASE=https://api.openai.com/v1
```

## 🎯 Run Research

```bash
# Yang Zhenning (quick)
bash run_openrouter_yang.sh

# Custom topic
python run_openrouter.py --topic "Your question here"

# With options
python run_openrouter.py \
  --topic "Your question" \
  --output "./my_output" \
  --temperature 0.7
```

## 📋 Commands Reference

| Command | Purpose |
|---------|---------|
| `python verify_openrouter_setup.py` | Test setup |
| `bash run_openrouter_yang.sh` | Research Yang Zhenning |
| `python run_openrouter.py --topic "X"` | Research topic X |
| `python run_openrouter.py --help` | Show all options |

## 📁 Output Files

```
outputs/yang_zhenning/
├── *_full.json        # Complete data
└── *_readable.md      # Report (OPEN THIS!)
```

## 💰 Cost

~$0.35-1.15 per research (10-30 min)

## 🐛 Quick Fixes

```bash
# Missing packages
pip install -r requirements.txt

# Environment not loaded
source .env

# Permission denied
chmod +x run_openrouter_yang.sh

# Test APIs
python verify_openrouter_setup.py
```

## 💡 Best Practices

✅ **DO:**
- Use specific questions
- Check verify script first
- Read the markdown output
- Set MAX_LLM_CALL_PER_RUN if needed

❌ **DON'T:**
- Use vague questions
- Commit .env to git
- Interrupt mid-research
- Use on rate-limited accounts

## 📚 Full Docs

- Setup: `QUICKSTART_OPENROUTER.md`
- Detailed: `README_OPENROUTER.md`
- Summary: `SETUP_SUMMARY.md`

## 🎓 Example Topics

```bash
python run_openrouter.py --topic "Yang Zhenning Nobel Prize significance"
python run_openrouter.py --topic "Yang-Mills theory explanation"
python run_openrouter.py --topic "Comparison of Yang Zhenning and Tsung-Dao Lee"
python run_openrouter.py --topic "Latest quantum computing breakthroughs"
```

## 🔧 Configuration

Edit `.env`:

```bash
# Increase max iterations (default: 100)
MAX_LLM_CALL_PER_RUN=150

# Change summarization model
SUMMARY_MODEL_NAME=gpt-4o-mini

# Adjust timeouts
VISIT_SERVER_TIMEOUT=200
```

## 📞 Support

- Issues: github.com/Alibaba-NLP/DeepResearch/issues
- Email: yongjiang.jy@alibaba-inc.com

---

**Start now:**
```bash
bash run_openrouter_yang.sh
```

