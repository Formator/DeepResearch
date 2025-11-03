# DeepResearch with OpenRouter - No Local Deployment Needed! 🚀

This guide shows you how to run Tongyi DeepResearch using OpenRouter API without any local model deployment. Perfect for users who want the best results without managing GPU infrastructure.

## ✨ Features

- **🌐 Fully Cloud-Based**: No local GPU or model deployment required
- **🔥 Best Performance**: Uses Tongyi-DeepResearch-30B-A3B via OpenRouter
- **💰 Cost-Effective**: Pay-per-use pricing, no infrastructure costs
- **⚡ Quick Setup**: Get started in minutes
- **📊 Rich Output**: Beautiful console output and detailed reports

## 🎯 Quick Start

### 1. Install Dependencies

```bash
cd inference
pip install -r requirements.txt
```

### 2. Get API Keys

You'll need the following API keys:

| Service | Purpose | Get Key From | Cost |
|---------|---------|--------------|------|
| **OpenRouter** | Main LLM (DeepResearch model) | [openrouter.ai](https://openrouter.ai/) | ~$0.30-1 per research |
| **Serper** | Google Search | [serper.dev](https://serper.dev/) | Free tier: 2,500 queries/month |
| **Jina AI** | Web Content Reading | [jina.ai](https://jina.ai/) | Free tier available |
| **OpenAI** | Page Summarization | [platform.openai.com](https://platform.openai.com/) | ~$0.10 per research |

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.openrouter.example .env

# Edit .env and add your API keys
nano .env  # or use your favorite editor
```

Or export them directly:

```bash
export OPENROUTER_API_KEY='your-openrouter-key'
export SERPER_KEY_ID='your-serper-key'
export JINA_API_KEYS='your-jina-key'
export API_KEY='your-openai-key'
export API_BASE='https://api.openai.com/v1'
```

### 4. Run Research!

```bash
# Research on Yang Zhenning (杨振宁)
python run_openrouter.py --topic "Yang Zhenning"

# Research on any other topic
python run_openrouter.py --topic "What are the latest developments in quantum computing?"

# With custom output directory
python run_openrouter.py --topic "Climate change solutions" --output "./my_research"
```

## 📝 Example Output

The script will:

1. **Show progress** with a beautiful console interface
2. **Display the final answer** in formatted markdown
3. **Save two files**:
   - `*_full.json` - Complete research data with all intermediate steps
   - `*_readable.md` - Human-readable markdown report

Example output structure:
```
outputs/openrouter/
├── Yang_Zhenning_20250122_143022_full.json
└── Yang_Zhenning_20250122_143022_readable.md
```

## 🎨 Advanced Usage

### Custom Model or Parameters

```bash
python run_openrouter.py \
  --topic "Artificial General Intelligence" \
  --model "alibaba/tongyi-deepresearch-30b-a3b" \
  --temperature 0.7 \
  --top_p 0.95 \
  --output "./agi_research"
```

### Programmatic Usage

```python
from react_agent_openrouter import MultiTurnReactAgent
import os

# Set environment variables
os.environ["OPENROUTER_API_KEY"] = "your-key"
os.environ["SERPER_KEY_ID"] = "your-key"
os.environ["JINA_API_KEYS"] = "your-key"
os.environ["API_KEY"] = "your-key"
os.environ["API_BASE"] = "https://api.openai.com/v1"

# Configure agent
llm_cfg = {
    'model': 'alibaba/tongyi-deepresearch-30b-a3b',
    'generate_cfg': {
        'temperature': 0.6,
        'top_p': 0.95,
    },
}

# Run research
agent = MultiTurnReactAgent(
    llm=llm_cfg,
    function_list=["search", "visit", "google_scholar", "PythonInterpreter"]
)

result = agent._run(
    question="What are the key contributions of Yang Zhenning to physics?",
    answer=""
)

print(result['prediction'])
```

## 🔧 Configuration Options

### Command Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--topic` | "Yang Zhenning" | Research topic or question |
| `--output` | "./outputs/openrouter" | Output directory |
| `--model` | "alibaba/tongyi-deepresearch-30b-a3b" | OpenRouter model name |
| `--temperature` | 0.6 | Generation temperature |
| `--top_p` | 0.95 | Top-p sampling parameter |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | Yes | OpenRouter API key |
| `SERPER_KEY_ID` | Yes | Serper API key for search |
| `JINA_API_KEYS` | Yes | Jina AI API key for web reading |
| `API_KEY` | Yes | OpenAI-compatible API key |
| `API_BASE` | Yes | OpenAI-compatible API base URL |
| `SUMMARY_MODEL_NAME` | No | Model for summarization (default: gpt-4o-mini) |
| `MAX_LLM_CALL_PER_RUN` | No | Max iterations (default: 100) |

## 💡 Tips for Best Results

1. **Be Specific**: More specific questions get better answers
   - ❌ "Tell me about AI"
   - ✅ "What are the key breakthroughs in transformer architectures since 2020?"

2. **Use for Complex Topics**: DeepResearch excels at multi-hop reasoning
   - Research questions requiring multiple sources
   - Topics needing academic references
   - Complex analysis requiring data processing

3. **Monitor API Usage**: 
   - Each research session makes multiple API calls
   - Expect 20-50 rounds for thorough research
   - Cost: typically $0.30-$2.00 per research topic

4. **Check the Process**: 
   - The `*_readable.md` file shows all research steps
   - Review tool calls to understand the reasoning process
   - Use logs to debug if results aren't as expected

## 🐛 Troubleshooting

### "Missing required environment variables"
- Ensure all API keys are set in `.env` or exported
- Check that `.env` file is in the `inference/` directory

### "OpenRouter API error"
- Verify your OpenRouter API key is valid
- Check your OpenRouter account has sufficient credits
- Ensure the model name is correct

### "No results found" for search
- Check SERPER_KEY_ID is valid
- Verify your Serper account has remaining quota
- Try a different search query

### Rate Limits
- OpenRouter: Depends on your plan
- Serper: 2,500 free queries/month, then paid
- Jina: Check your plan limits
- OpenAI: Depends on your tier

## 📊 Example Topics to Try

- **Biography**: "Yang Zhenning's contributions to physics"
- **Technology**: "Latest developments in quantum computing"
- **Science**: "Current state of fusion energy research"
- **Business**: "Analysis of AI chip market trends"
- **History**: "The impact of the Silk Road on global trade"

## 🆚 Comparison: OpenRouter vs Local Deployment

| Aspect | OpenRouter | Local Deployment |
|--------|------------|------------------|
| **Setup Time** | 5 minutes | 2-4 hours |
| **GPU Required** | No | Yes (40GB+ VRAM) |
| **Cost** | ~$0.50-2 per research | GPU rental/purchase |
| **Maintenance** | None | Regular updates |
| **Performance** | Best (optimized) | Depends on hardware |
| **Scalability** | Unlimited | Limited by GPU |

## 📚 Additional Resources

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [DeepResearch GitHub](https://github.com/Alibaba-NLP/DeepResearch)
- [DeepResearch Blog Post](https://tongyi-agent.github.io/blog/introducing-tongyi-deep-research/)
- [Model on HuggingFace](https://huggingface.co/Alibaba-NLP/Tongyi-DeepResearch-30B-A3B)

## 🤝 Support

- GitHub Issues: [DeepResearch Issues](https://github.com/Alibaba-NLP/DeepResearch/issues)
- Contact: yongjiang.jy@alibaba-inc.com

## 📄 License

Same as the main DeepResearch project. See [LICENSE](../LICENSE).

---

**Happy Researching! 🎉**

