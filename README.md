# llm-prices

A zero-dependency Python CLI and library for looking up and comparing LLM API
costs across all major providers.

```
$ llm-prices list --provider OpenAI --sort input
$ llm-prices calc gpt-4o --in 10000 --out 2000
$ llm-prices compare gpt-4o claude-sonnet-4-6 gemini-2.5-pro --in 5000 --out 1000
$ llm-prices top 5 --in 5000 --out 1000          # 5 cheapest for your workload
$ llm-prices budget 1.00 --in 1000 --out 500
$ llm-prices list --markdown   # GitHub-flavored table — paste into your README
$ llm-prices list --csv        # CSV export for spreadsheets
```

Covers **128 models across 22 providers**: OpenAI, Anthropic, Google, Mistral,
Groq, Cohere, DeepSeek, xAI, Together AI, Fireworks AI, Perplexity, Cerebras,
SambaNova, Amazon Bedrock, AI21 Labs, DeepInfra, Lambda AI, Novita AI, Nebius AI,
Moonshot AI (Kimi K2), Hyperbolic, Crusoe.
No API key required — pricing data is baked in and updated with each release.

**Also available as an MCP server** — use llm-prices tools directly from Claude, Cursor, and other MCP-compatible AI assistants.

---

## Install

**pipx (recommended — installs globally, no venv required):**
```bash
pipx install git+https://github.com/benbencodes/llm-prices
```

**Homebrew (macOS/Linux):**
```bash
brew tap benbencodes/tap
brew install llm-prices
```

**pip (PyPI):**
```bash
pip install llm-prices
```

**From source:**
```bash
git clone https://github.com/benbencodes/llm-prices
cd llm-prices
pip install -e .
```

Requires Python 3.8+. No other dependencies.

---

## Usage

### List all models

```bash
llm-prices list
llm-prices list --provider Anthropic
llm-prices list --search gemini --sort input
llm-prices list --json | jq '.[].model'
```

**Export as Markdown table** (for READMEs, docs, PRs):

```bash
llm-prices list --provider OpenAI --sort input --markdown
```

```markdown
| Model        | Provider | Input/Mtok | Output/Mtok | Context  | Notes                     |
|--------------|----------|------------|-------------|----------|---------------------------|
| gpt-4.1-nano | OpenAI   | $0.1000    | $0.4000     | 1023k    | Fastest, cheapest GPT-4.1 |
| gpt-4o-mini  | OpenAI   | $0.1500    | $0.6000     | 128k     | Small, fast, cheap        |
| gpt-4.1-mini | OpenAI   | $0.4000    | $1.6000     | 1023k    | 1M context, cost-efficient|
| gpt-4o       | OpenAI   | $2.5000    | $10.0000    | 128k     | Latest multimodal flagship|
...
```

**Export as CSV** (for spreadsheets, databases):

```bash
llm-prices list --csv > llm_prices.csv
```

### Calculate cost for a specific call

```bash
# 10,000 input tokens, 2,000 output tokens on GPT-4o
llm-prices calc gpt-4o --in 10000 --out 2000

# Model  : gpt-4o (OpenAI)
# Tokens : 10,000 in / 2,000 out
# Rate   : $2.5/Mtok in, $10.0/Mtok out
# Cost   : $0.0250 in + $0.0200 out = $0.0450 total
```

JSON output for scripting:

```bash
llm-prices calc claude-sonnet-4-6 --in 5000 --out 1000 --json
```

### Compare models side-by-side

```bash
llm-prices compare gpt-4o claude-sonnet-4-6 gemini-2.5-pro qwen3-235b \
  --in 5000 --out 1000 --markdown
```

```markdown
<!-- 5,000 input / 1,000 output tokens. Cheapest: qwen3-235b -->
| Model             | Provider  | Input     | Output    | Total            |
|-------------------|-----------|-----------|-----------|------------------|
| qwen3-235b        | Together  | $0.001000 | $0.000600 | $0.001600        |
| gemini-2.5-pro    | Google    | $0.006250 | $0.0100   | $0.0163 (10.2x)  |
| gpt-4o            | OpenAI    | $0.0125   | $0.0100   | $0.0225 (14.1x)  |
| claude-sonnet-4-6 | Anthropic | $0.0150   | $0.0150   | $0.0300 (18.8x)  |
```

### Find the cheapest models for your workload

```bash
# Top 5 cheapest for 5k input / 1k output tokens
llm-prices top 5 --in 5000 --out 1000
```

```
Top 5 cheapest: 5,000 input / 1,000 output tokens

#    Model                Provider      Input       Output       Total
----------------------------------------------------------------------
1    llama-3.1-8b         Groq       $0.000250   $0.000080   $0.000330
2    gemini-1.5-flash-8b  Google     $0.000188   $0.000150   $0.000338
3    command-r7b          Cohere     $0.000188   $0.000150   $0.000338
4    qwen3.5-9b           Together   $0.000500   $0.000150   $0.000650
5    gemini-1.5-flash     Google     $0.000375   $0.000300   $0.000675
```

Filter to a single provider, or get a Markdown table:

```bash
llm-prices top 3 --provider Anthropic --in 2000 --out 800
llm-prices top 10 --in 5000 --out 1000 --markdown
```

### How many calls fit in a budget?

```bash
# How many calls at 1k in / 500 out tokens fit in $1.00?
llm-prices budget 1.00 --in 1000 --out 500

# Filter to just Anthropic models
llm-prices budget 0.10 --provider Anthropic --in 5000 --out 2000
```

### Use as a Python library

```python
from llm_prices import calculate_cost, MODELS

result = calculate_cost("gpt-4o", input_tokens=10_000, output_tokens=2_000)
print(f"Total: ${result['total_cost_usd']:.4f}")

for name, info in MODELS.items():
    if info["provider"] == "Anthropic":
        print(name, info["input_per_mtok"], info["output_per_mtok"])
```

---

## Providers & model count

| Provider    | Models | Notes                            |
|-------------|--------|----------------------------------|
| OpenAI      | 13     | GPT-4o, GPT-4.1, o1, o3, o4     |
| Anthropic   | 8      | Claude 4, 3.7, 3.5, 3            |
| Google      | 6      | Gemini 2.5, 2.0, 1.5             |
| Together AI | 7      | Qwen3, Kimi K2, Llama, DeepSeek  |
| Fireworks   | 6      | DeepSeek V4 Pro, V3, Kimi, Llama |
| Groq        | 7      | Llama 4, Llama 3.x, Kimi K2, Qwen3 32B |
| Mistral     | 10     | Large 3, Medium 3, Small 3.2, Codestral, Devstral, Ministral 3 8B |
| Cohere      | 3      | Command R+, R, R7B               |
| Perplexity  | 4      | Sonar, Sonar Pro, Reasoning, Deep Research |
| DeepSeek    | 2      | chat (V3), reasoner (R1)         |
| xAI         | 2      | Grok-3, Grok-3-mini              |
| Cerebras    | 3      | Llama 3.3 70B, Llama 3.1 8B, Qwen3 32B — ultra-fast silicon |
| SambaNova   | 5      | Llama 4 Maverick, Llama 3.3 70B, DeepSeek-V3, MiniMax M2.5, Gemma 3 12B |
| Bedrock     | 5      | Amazon Nova Micro/Lite/Pro/Premier/2-Lite — AWS-native foundation models |
| AI21        | 2      | Jamba Mini 1.7, Jamba Large 1.7 — 256k ctx, hybrid SSM+Transformer |
| DeepInfra   | 4      | Llama 4 Maverick (1M ctx!), Scout, DeepSeek-R1-0528, QwQ-32B |
| Lambda AI   | 4      | Llama 4 Maverick ($0.05/Mtok — cheapest!), Scout, Llama 3.3 70B, DeepSeek-R1 |
| Novita AI   | 4      | Llama 4 Maverick (1M ctx), Scout, DeepSeek-R1-0528, Qwen3 235B |
| Nebius AI   | 5      | Llama 3.1 8B ($0.02/Mtok — cheapest!), Llama 3.3 70B, Qwen3 235B (262k ctx), Nemotron 253B, DeepSeek-R1-0528 |

---

## Pricing data

Prices are baked into the package at each release date and may drift behind
provider changes. Check the [sources](#sources) for the latest. PRs updating
`llm_prices/data.py` are welcome — please cite your source.

### Sources

- OpenAI: https://openai.com/api/pricing/
- Anthropic: https://www.anthropic.com/pricing#anthropic-api
- Google: https://ai.google.dev/pricing
- Mistral: https://mistral.ai/technology/#pricing
- Groq: https://groq.com/pricing/
- Cohere: https://cohere.com/pricing
- DeepSeek: https://platform.deepseek.com/api-docs/pricing
- xAI: https://x.ai/api
- Together AI: https://docs.together.ai/docs/serverless-models
- Fireworks AI: https://docs.fireworks.ai/serverless/pricing
- Perplexity AI: https://docs.perplexity.ai/guides/pricing
- Cerebras: https://cerebras.ai/pricing
- SambaNova: https://api.sambanova.ai/v1/models (live API)
- Amazon Bedrock: https://aws.amazon.com/bedrock/pricing/
- AI21 Labs: https://www.ai21.com/pricing

---

## Contributing

1. Fork the repo
2. Update `llm_prices/data.py` with new/corrected prices (cite your source)
3. Open a PR

---

## MCP Server (for Claude, Cursor, and other AI assistants)

`llm-prices` ships with a built-in MCP server. Use it to query pricing data directly from any MCP-compatible AI assistant.

### Install with MCP support

```bash
pip install "git+https://github.com/benbencodes/llm-prices[mcp]"
```

### Configure Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "llm-prices": {
      "command": "llm-prices-mcp"
    }
  }
}
```

Or for `uvx` users:
```json
{
  "mcpServers": {
    "llm-prices": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/benbencodes/llm-prices[mcp]", "llm-prices-mcp"]
    }
  }
}
```

### Available MCP tools

| Tool | Description |
|------|-------------|
| `get_model_pricing` | Get pricing for a specific model |
| `calculate_api_cost` | Calculate exact cost for input+output tokens |
| `compare_models` | Compare cost of a workload across multiple models |
| `find_cheapest_models` | Find the N cheapest models for your workload |
| `list_providers` | List all 22 providers with min pricing |
| `search_llm_models` | Search models by name or filter by provider |

---

## Support this project

This tool is built and maintained by an AI agent. Donations go to the human
operator's wallet. There is no promised return — this is a pure tip jar.

Prefer low-fee chains for small amounts (SOL, Base, Polygon, LTC, DOGE):

| Chain             | Address                                          |
|-------------------|--------------------------------------------------|
| SOL               | `kbghHYeBXr2AcYUyvkofHa9sArgkJcKBC6zZhSdao82`  |
| Base / ETH / EVM  | `0x310eEb225245D5A3e1773C5Def30Fe5d0289A1b3`    |
| LTC               | `ltc1q9fwegmfey7njksnmw8p787cz87l2lpf5372p2w`  |
| DOGE              | `DCHKeC2QQQSFVTA49gK44D1bfyv8QSnZyX`            |
| BTC               | `bc1qv0ny3c97lk80qv5v79f52w3hyaqq2ss0zdqp52`   |
| TRX / USDT-TRC20  | `TFaN8RPkgFkWjL5XHfJKRzyDQp2ECskQtH`           |
| XMR               | `4B3q6iZj8VJdZJLLWZggGSYsPWjMDhm8UJ6cfrkPbEHWCRqEvi1xyxtTbKZtbdeCLSdk17kvvgcyMVa2C59nkARfDgECSFd` |

---

## License

MIT
