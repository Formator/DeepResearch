# Installation Guide - OpenRouter Setup

Quick installation guide for running DeepResearch with OpenRouter (no local models needed).

## Prerequisites

- Python 3.9 or higher
- pip
- Internet connection

## Installation Options

### Option 1: Using pyproject.toml (Recommended)

From the repository root:

```bash
# Clone the repository
git clone https://github.com/QwenLM/DeepResearch.git
cd DeepResearch

# Install in editable mode
pip install -e .
```

This installs minimal dependencies (~500 MB - 1 GB).

### Option 2: Using requirements file

From the inference directory:

```bash
cd inference
pip install -r requirements-openrouter.txt
```

### Option 3: Using virtual environment (Best Practice)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
cd DeepResearch
pip install -e .
```

## Verify Installation

Check that key packages are installed:

```bash
python -c "import openai; import qwen_agent; import rich; print('✓ All core packages installed!')"
```

Or run the verification script:

```bash
cd inference
python verify_openrouter_setup.py
```

## What Gets Installed

### Core Dependencies (~500 MB)

- **openai**: OpenRouter API client
- **qwen-agent**: Agent framework  
- **requests, httpx, aiohttp**: Web requests
- **rich**: Beautiful CLI output
- **tiktoken**: Token counting
- **pandas, pdfplumber, python-pptx**: File parsing
- **sandbox-fusion**: Python code execution

### What's NOT Installed

- ❌ PyTorch (~5 GB)
- ❌ vLLM (~3 GB)
- ❌ CUDA libraries (~4 GB)
- ❌ Model weights (30-80 GB)

**Total savings: ~40-90 GB!**

## Next Steps

After installation:

1. **Configure environment**:
   ```bash
   cd inference
   cp env.template .env
   # Edit .env with your API keys
   ```

2. **Get API keys**:
   - OpenRouter: https://openrouter.ai/keys
   - Serper (free): https://serper.dev/
   - Jina (free): https://jina.ai/

3. **Run your first research**:
   ```bash
   bash run_openrouter_yang.sh
   ```

## Troubleshooting

### Package conflicts

If you have issues, create a fresh environment:

```bash
python -m venv venv-clean
source venv-clean/bin/activate
pip install -e .
```

### "No module named 'qwen_agent'"

Update qwen-agent:

```bash
pip install -U qwen-agent
```

### "openai" package issues

Make sure you have the latest version:

```bash
pip install -U openai
```

### Import errors

Check your Python version:

```bash
python --version  # Should be 3.9+
```

## Documentation

- [OpenRouter Setup Guide](OPENROUTER_SETUP.md) - Complete setup instructions
- [Installation Comparison](INSTALL_COMPARISON.md) - Full vs minimal setup
- [Changes Documentation](CHANGES_OPENROUTER_ONLY.md) - What was modified

## Getting Help

If you encounter issues:

1. Check the [troubleshooting section](OPENROUTER_SETUP.md#troubleshooting)
2. Verify your API keys are set correctly
3. Make sure you have Python 3.9+
4. Try creating a fresh virtual environment

## Quick Reference

```bash
# Install
pip install -e .

# Set up
cp inference/env.template inference/.env
# Edit .env with keys

# Run
bash inference/run_openrouter_yang.sh
```

That's it! 🚀

