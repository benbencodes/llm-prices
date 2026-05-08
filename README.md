# llm-prices

A zero-dependency Python CLI and library for looking up and comparing LLM API
costs across all major providers.

```
$ llm-prices list --provider OpenAI --sort input
$ llm-prices calc gpt-4o --in 10000 --out 2000
$ llm-prices compare gpt-4o claude-sonnet-4 gemini-2.0-flash --in 5000 --out 1000
$ llm-prices budget 1.00 --in 1000 --out 500
```

Covers **OpenAI, Anthropic, Google, Mistral, Groq, Cohere, DeepSeek, xAI** and
more. No API key required — pricing data is baked in and updated with each
release.

---

## Install

**Homebrew (macOS/Linux):**
```bash
brew tap benbencodes/tap
brew install llm-prices
```

**pip (coming soon — PyPI publish in progress):**
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
```

Filter and sort:

```bash
llm-prices list --provider Anthropic
llm-prices list --search gemini --sort input
llm-prices list --json | jq '.[].model'
```

### Calculate cost for a specific call

```bash
# 10,000 input tokens, 2,000 output tokens on GPT-4o
llm-prices calc gpt-4o --in 10000 --out 2000

# Output:
# Model  : gpt-4o (OpenAI)
# Tokens : 10,000 in / 2,000 out
# Rate   : $2.5/Mtok in, $10.0/Mtok out
# Cost   : $0.0250 in + $0.0200 out = $0.0450 total
```

JSON output for scripting:

```bash
llm-prices calc claude-sonnet-4 --in 5000 --out 1000 --json
```

### Compare models side-by-side

```bash
llm-prices compare gpt-4o claude-sonnet-4 gemini-2.5-pro --in 5000 --out 1000
```

Output (sorted cheapest first):

```
Comparison: 5,000 input tokens, 1,000 output tokens

Model                      Provider     Input       Output        Total
---------------------------------------------------------------------------
gemini-2.5-pro             Google     $0.0063     $0.0100      $0.0163
claude-sonnet-4            Anthropic  $0.0150     $0.0150      $0.0300  (1.8x)
gpt-4o                     OpenAI     $0.0125     $0.0100      $0.0225  (1.4x)
```

### How many calls fit in a budget?

```bash
# How many calls at 1k in / 500 out tokens fit in $1.00?
llm-prices budget 1.00 --in 1000 --out 500

# Filter to just Anthropic models
llm-prices budget 0.10 --provider Anthropic --in 5000 --out 2000
```

Output (sorted cheapest per call first):

```
Budget: $1.0000  |  Tokens per call: 1,000 in / 500 out

Model                  Provider        Cost/call        Calls
-------------------------------------------------------------
llama-3.1-8b           Groq            $0.000090       11,111
gemini-1.5-flash-8b    Google          $0.000112        8,888
...
gpt-4o                 OpenAI          $0.007500          133
claude-opus-4          Anthropic       $0.052500           19
```

### Use as a Python library

```python
from llm_prices import calculate_cost, MODELS

# Calculate cost
result = calculate_cost("gpt-4o", input_tokens=10_000, output_tokens=2_000)
print(f"Total: ${result['total_cost_usd']:.4f}")

# Browse models
for name, info in MODELS.items():
    if info["provider"] == "Anthropic":
        print(name, info["input_per_mtok"], info["output_per_mtok"])
```

---

## Pricing data

Prices are baked into the package as of each release date and may drift behind
provider changes. Check the [provider pricing pages](#sources) for the latest.
Pull requests updating `llm_prices/data.py` are welcome.

### Sources

- OpenAI: https://openai.com/api/pricing/
- Anthropic: https://www.anthropic.com/pricing#anthropic-api
- Google: https://ai.google.dev/pricing
- Mistral: https://mistral.ai/technology/#pricing
- Groq: https://groq.com/pricing/
- Cohere: https://cohere.com/pricing
- DeepSeek: https://platform.deepseek.com/api-docs/pricing
- xAI: https://x.ai/api

---

## Contributing

1. Fork the repo
2. Update `llm_prices/data.py` with new/corrected prices (cite your source)
3. Open a PR

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
