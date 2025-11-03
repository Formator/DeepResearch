# Changes Made: OpenRouter Only Configuration

## Summary

Updated DeepResearch to use **ONLY OpenRouter** with Tongyi Qwen models. No OpenAI official API needed!

## Files Modified

### 1. `tool_visit.py`
**Changes**: Updated web page summarization to use OpenRouter instead of OpenAI API

```python
# Before (used OpenAI API):
api_key = os.environ.get("API_KEY")
url_llm = os.environ.get("API_BASE")
model_name = os.environ.get("SUMMARY_MODEL_NAME", "")

# After (uses OpenRouter):
api_key = os.environ.get("OPENROUTER_API_KEY")
url_llm = "https://openrouter.ai/api/v1"
model_name = os.environ.get("SUMMARY_MODEL_NAME", "alibaba/qwen-max")
```

**Added**: `extra_headers` for OpenRouter:
```python
extra_headers={
    "HTTP-Referer": "https://github.com/QwenLM/DeepResearch",
    "X-Title": "DeepResearch",
}
```

### 2. `react_agent_openrouter.py`
**Changes**: Added `extra_headers` to the main agent's OpenRouter calls

```python
extra_headers={
    "HTTP-Referer": "https://github.com/QwenLM/DeepResearch",
    "X-Title": "DeepResearch",
}
```

### 3. `run_openrouter.py`
**Changes**: 
- Removed `API_KEY` and `API_BASE` from required environment variables
- Changed default summary model from `gpt-4o-mini` to `alibaba/qwen-max`
- Updated documentation

```python
# Before:
required_vars = {
    "OPENROUTER_API_KEY": ...,
    "SERPER_KEY_ID": ...,
    "JINA_API_KEYS": ...,
    "API_KEY": ...,          # REMOVED
    "API_BASE": ...,         # REMOVED
}

# After:
required_vars = {
    "OPENROUTER_API_KEY": ...,
    "SERPER_KEY_ID": ...,
    "JINA_API_KEYS": ...,
}
```

### 4. `run_openrouter_yang.sh`
**Changes**:
- Removed `API_KEY` and `API_BASE` from required variables check
- Updated default summary model to `alibaba/qwen-max`
- Simplified environment variable instructions

```bash
# Before:
REQUIRED_VARS=("OPENROUTER_API_KEY" "SERPER_KEY_ID" "JINA_API_KEYS" "API_KEY" "API_BASE")

# After:
REQUIRED_VARS=("OPENROUTER_API_KEY" "SERPER_KEY_ID" "JINA_API_KEYS")
```

## New Files Created

### 1. `env.template`
A template file for users to copy and fill in their API keys.

### 2. `OPENROUTER_SETUP.md`
Complete setup guide for using OpenRouter only.

### 3. `CHANGES_OPENROUTER_ONLY.md`
This file - documenting all changes made.

## Required Environment Variables

### Before (5 variables):
- `OPENROUTER_API_KEY`
- `SERPER_KEY_ID`
- `JINA_API_KEYS`
- `API_KEY` ❌ (OpenAI API key)
- `API_BASE` ❌ (OpenAI API endpoint)

### After (3 variables):
- `OPENROUTER_API_KEY` ✅
- `SERPER_KEY_ID` ✅
- `JINA_API_KEYS` ✅

## Optional Variables

- `SUMMARY_MODEL_NAME`: Default changed from `gpt-4o-mini` to `alibaba/qwen-max`
- `MAX_LLM_CALL_PER_RUN`: Unchanged (default: 100)

## Models Used

1. **Main Agent**: `alibaba/tongyi-deepresearch-30b-a3b` (via OpenRouter)
2. **Summarization**: `alibaba/qwen-max` (via OpenRouter, configurable)

## How to Use

1. **Setup environment**:
   ```bash
   cd inference
   cp env.template .env
   # Edit .env with your API keys
   ```

2. **Run research**:
   ```bash
   bash run_openrouter_yang.sh
   ```

   Or:
   ```bash
   python run_openrouter.py --topic "Your Topic"
   ```

## Testing

To verify your setup:
```bash
# Set your environment variables
export OPENROUTER_API_KEY='sk-or-v1-your-key'
export SERPER_KEY_ID='your-key'
export JINA_API_KEYS='jina_your-key'

# Run the verification script (if available)
python verify_openrouter_setup.py
```

## Benefits

✅ **Single API provider**: Only need OpenRouter account  
✅ **Consistent pricing**: All LLM costs through one provider  
✅ **Simpler setup**: Fewer API keys to manage  
✅ **Cost-effective**: Qwen models are cheaper than OpenAI GPT models  
✅ **No OpenAI dependency**: Works without OpenAI account  

## Backward Compatibility

⚠️ **Breaking Change**: If you were using OpenAI's official API for summarization, you'll need to:
1. Get an OpenRouter API key
2. Update your environment variables
3. Remove `API_KEY` and `API_BASE` from your `.env` file

## Notes

- All API calls now go through OpenRouter's endpoint: `https://openrouter.ai/api/v1`
- The OpenAI Python SDK is still used, but pointing to OpenRouter
- Extra headers are added for OpenRouter ranking/statistics
- Default models use Alibaba/Qwen family through OpenRouter

