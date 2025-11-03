#!/bin/bash
# Quick start script for researching Yang Zhenning using OpenRouter API
# No local model deployment needed!

echo "=================================================="
echo "🚀 DeepResearch with OpenRouter - Yang Zhenning"
echo "=================================================="
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo ""
    echo "Please create a .env file with your API keys:"
    echo "  cp .env.openrouter.example .env"
    echo "  # Then edit .env and add your API keys"
    echo ""
    echo "Or set environment variables:"
    echo "  export OPENROUTER_API_KEY='your-key'"
    echo "  export SERPER_KEY_ID='your-key'"
    echo "  export JINA_API_KEYS='your-key'"
    echo ""
    exit 1
fi

# Load environment variables
source .env
echo "✓ Environment variables loaded from .env"

# Check required variables (only OpenRouter keys, no OpenAI needed)
REQUIRED_VARS=("OPENROUTER_API_KEY" "SERPER_KEY_ID" "JINA_API_KEYS")
MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -ne 0 ]; then
    echo "❌ Missing required environment variables:"
    for var in "${MISSING_VARS[@]}"; do
        echo "  - $var"
    done
    echo ""
    echo "Please set them in your .env file"
    exit 1
fi

echo "✓ All required API keys are set"
echo ""

# Set defaults if not set (using OpenRouter Qwen model for summarization)
export SUMMARY_MODEL_NAME=${SUMMARY_MODEL_NAME:-"alibaba/qwen-max"}
export MAX_LLM_CALL_PER_RUN=${MAX_LLM_CALL_PER_RUN:-100}

# Run the research
echo "🔍 Starting research on Yang Zhenning..."
echo "   Model: alibaba/tongyi-deepresearch-30b-a3b"
echo "   This may take 10-30 minutes depending on the complexity"
echo ""

python run_openrouter.py \
    --topic "Yang Zhenning" \
    --output "./outputs/yang_zhenning" \
    --model "alibaba/tongyi-deepresearch-30b-a3b" \
    --temperature 0.6 \
    --top_p 0.95

echo ""
echo "=================================================="
echo "✅ Research complete!"
echo "=================================================="

