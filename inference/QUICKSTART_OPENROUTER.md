# 🚀 Quickstart: Yang Zhenning Research with OpenRouter

Get deep research results on Yang Zhenning (杨振宁) in just 5 minutes - no local GPU needed!

## ⚡ Super Quick Start (TL;DR)

```bash
# 1. Navigate to inference directory
cd inference

# 2. Set up environment
cp .env.openrouter.example .env
# Edit .env and add your API keys

# 3. Verify setup
python verify_openrouter_setup.py

# 4. Run research on Yang Zhenning
bash run_openrouter_yang.sh
```

## 📋 Step-by-Step Guide

### Step 1: Get Your API Keys (5 minutes)

You need 4 API keys. Most have free tiers:

#### 1.1 OpenRouter (Main LLM) - **Required**
- Go to [openrouter.ai](https://openrouter.ai/)
- Sign up / Log in
- Go to "Keys" section
- Create a new API key
- Cost: ~$0.30-1.00 per research

#### 1.2 Serper (Search) - **Required**
- Go to [serper.dev](https://serper.dev/)
- Sign up with Google
- Copy your API key
- Free tier: 2,500 searches/month (more than enough!)

#### 1.3 Jina AI (Web Reading) - **Required**
- Go to [jina.ai](https://jina.ai/)
- Sign up
- Get your API key from dashboard
- Free tier available

#### 1.4 OpenAI (Summarization) - **Required**
- Go to [platform.openai.com](https://platform.openai.com/)
- Sign up / Log in
- Create API key
- Will use `gpt-4o-mini` (very cheap: ~$0.10 per research)
- Alternative: Use any OpenAI-compatible API (Groq, Deepseek, etc.)

### Step 2: Configure Environment (1 minute)

```bash
cd /Users/dingkwang/sci/DeepResearch/inference

# Copy the example configuration
cp .env.openrouter.example .env

# Edit the file and add your API keys
nano .env  # or use your favorite editor
```

Your `.env` file should look like:

```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
SERPER_KEY_ID=xxxxxxxxxxxxx
JINA_API_KEYS=jina_xxxxxxxxxxxxx
API_KEY=sk-xxxxxxxxxxxxx
API_BASE=https://api.openai.com/v1
SUMMARY_MODEL_NAME=gpt-4o-mini
```

### Step 3: Verify Setup (30 seconds)

```bash
python verify_openrouter_setup.py
```

This will:
- ✓ Check all environment variables are set
- ✓ Test each API connection
- ✓ Confirm everything is working

Expected output:
```
✅ Setup Complete!

All checks passed! You're ready to run DeepResearch.
```

### Step 4: Run Research on Yang Zhenning (10-30 minutes)

#### Option A: Using the Bash Script (Recommended)

```bash
bash run_openrouter_yang.sh
```

#### Option B: Using Python Directly

```bash
python run_openrouter.py --topic "Yang Zhenning"
```

#### Option C: Custom Question about Yang Zhenning

```bash
python run_openrouter.py --topic "What are Yang Zhenning's most significant contributions to particle physics and why did he win the Nobel Prize?"
```

### Step 5: View Results

Results will be saved in `outputs/yang_zhenning/`:

```
outputs/yang_zhenning/
├── Yang_Zhenning_20250122_143022_full.json      # Complete research data
└── Yang_Zhenning_20250122_143022_readable.md    # Human-readable report
```

**Open the markdown file** for a beautifully formatted research report!

## 🎯 What You'll Get

The research will provide:

1. **Biography**: Life history and background
2. **Scientific Contributions**: Key discoveries and theories
3. **Nobel Prize**: Why he won and the significance
4. **Legacy**: Impact on physics and science
5. **Citations**: Academic sources and references

Example sections:
- Early life and education
- Collaboration with Tsung-Dao Lee
- Parity violation discovery
- Yang-Mills theory
- Statistical mechanics contributions
- Awards and honors
- Current activities

## 💰 Cost Breakdown

Approximate costs per research:

| Service | Cost | Notes |
|---------|------|-------|
| OpenRouter | $0.30-1.00 | Depends on research depth |
| Serper | Free | 2,500 free searches/month |
| Jina | Free | Within free tier |
| OpenAI | $0.05-0.15 | Using gpt-4o-mini |
| **Total** | **$0.35-1.15** | Per research topic |

## 🔧 Troubleshooting

### "Missing required environment variables"
```bash
# Make sure you're in the inference directory
cd /Users/dingkwang/sci/DeepResearch/inference

# Check if .env exists
ls -la .env

# If not, copy the example
cp .env.openrouter.example .env

# Edit and add your keys
nano .env
```

### "OpenRouter API error"
- Check your API key is correct (starts with `sk-or-v1-`)
- Verify you have credits on OpenRouter
- Check [OpenRouter status](https://status.openrouter.ai/)

### "Serper API error"
- Verify your API key at [serper.dev/dashboard](https://serper.dev/dashboard)
- Check you haven't exceeded free tier (2,500/month)

### "Jina API error"
- Confirm API key at [jina.ai/dashboard](https://jina.ai/)
- Check API quota

### Script runs but produces poor results
- Increase `MAX_LLM_CALL_PER_RUN` in .env (default: 100)
- Try different temperature: `--temperature 0.7`
- Make your question more specific

## 📊 Example Research Topics

Try these after Yang Zhenning:

```bash
# Physics
python run_openrouter.py --topic "Explain Yang-Mills theory and its impact on physics"

# Biography
python run_openrouter.py --topic "Compare Yang Zhenning's and Tsung-Dao Lee's scientific contributions"

# History
python run_openrouter.py --topic "Why was the discovery of parity violation revolutionary?"

# Current events
python run_openrouter.py --topic "What is Yang Zhenning's current work and influence in China?"
```

## 🎓 Understanding the Research Process

The agent will:

1. **Plan**: Analyze the question and plan research strategy
2. **Search**: Use Google Scholar and web search for sources
3. **Read**: Visit and read relevant webpages
4. **Analyze**: Extract and synthesize information
5. **Verify**: Cross-reference multiple sources
6. **Synthesize**: Create comprehensive answer
7. **Cite**: Provide sources and references

You'll see each step in real-time in the console!

## 🔄 Next Steps

After getting results for Yang Zhenning:

1. **Review the markdown file** - It has the full research report
2. **Check the JSON file** - See all intermediate steps
3. **Try another topic** - Use what you learned
4. **Adjust parameters** - Experiment with temperature/top_p
5. **Share your findings** - Export and share the markdown

## 💡 Pro Tips

1. **Specific Questions Work Better**
   - Instead of: "Tell me about Yang Zhenning"
   - Try: "What are Yang Zhenning's contributions to gauge theory and why are they important?"

2. **Use the Markdown Output**
   - The `*_readable.md` file is perfect for sharing
   - Import it into Notion, Obsidian, or other note apps
   - Convert to PDF for presentations

3. **Monitor Progress**
   - Watch the console output to see what the agent is doing
   - Each round shows the thinking process
   - Typical research: 20-40 rounds

4. **Save Costs**
   - Use specific questions to avoid unnecessary searches
   - Set `MAX_LLM_CALL_PER_RUN` to limit iterations
   - Use the verification script to test without full research

5. **Batch Research**
   - Research multiple related topics
   - Compare and contrast in follow-up questions
   - Build a knowledge base over time

## 📚 Learn More

- [Full OpenRouter Guide](README_OPENROUTER.md)
- [DeepResearch Paper](https://tongyi-agent.github.io/blog/introducing-tongyi-deep-research/)
- [Model on OpenRouter](https://openrouter.ai/alibaba/tongyi-deepresearch-30b-a3b)

## ❓ Need Help?

- Run verification: `python verify_openrouter_setup.py`
- Check issues: [GitHub Issues](https://github.com/Alibaba-NLP/DeepResearch/issues)
- Read docs: [README_OPENROUTER.md](README_OPENROUTER.md)

---

**Ready? Let's start researching! 🎉**

```bash
bash run_openrouter_yang.sh
```

