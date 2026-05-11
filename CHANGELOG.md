# Changelog

All notable changes to llm-prices will be documented here.

## [0.1.18] - 2026-05-11

### Added
- Nebius AI (19th provider) — 5 models:
  - llama-3.1-8b-nb: $0.02/$0.06 per Mtok, 128k ctx — **cheapest Llama 3.1 8B available**
  - llama-3.3-70b-nb: $0.13/$0.40, 128k ctx
  - qwen3-235b-nb: $0.20/$0.60, 262k ctx — 262k context window
  - nemotron-ultra-253b-nb: $0.60/$1.80, 128k ctx — Nvidia 253B research model
  - deepseek-r1-0528-nb: $0.80/$2.40, 164k ctx
- Total: 108 → 113 models, 18 → 19 providers
- 2 new tests for Nebius provider

## [0.1.17] - 2026-05-11

### Changed
- `providers` command enhanced: now shows min input/output price and max context window per provider
- `providers` command adds `--markdown` flag (GitHub-flavored table) and `--json` flag with structured data

### Added
- Novita AI (18th provider) — 4 models:
  - llama-4-maverick-no: $0.27/$0.85 per Mtok, 1M context
  - llama-4-scout-no: $0.18/$0.59, 131k ctx
  - deepseek-r1-0528-no: $0.70/$2.50, 163k ctx
  - qwen3-235b-no: $0.20/$0.80, 40k ctx
- Mistral new models (3 additions):
  - devstral-small: $0.10/$0.30, 128k ctx — coding agent model
  - devstral: $0.40/$2.00, 256k ctx — full coding agent, 256k context
  - ministral-3-8b: $0.15/$0.15, 262k ctx — ultra-cheap, huge context, same in/out price
- Total: 101 → 108 models, 17 → 18 providers
- Homebrew tap updated to v0.1.16 (SHA256 verified)

## [0.1.16] - 2026-05-11

### Added
- DeepInfra (16th provider) — 4 models:
  - llama-4-maverick-di: $0.15/$0.60 per Mtok, **1M token context** — largest Llama 4 context available
  - llama-4-scout-di: $0.08/$0.30, 327k ctx
  - deepseek-r1-0528-di: $0.50/$2.15, 163k ctx
  - qwq-32b-di: $0.15/$0.40, 131k ctx (Qwen QwQ reasoning model)
- Lambda AI (17th provider) — 4 models:
  - llama-4-maverick-la: $0.05/$0.10 per Mtok — tied with gpt-5-nano as cheapest capable model!
  - llama-4-scout-la: $0.05/$0.10, 16k ctx
  - llama3.3-70b-la: $0.12/$0.30, 131k ctx
  - deepseek-r1-0528-la: $0.20/$0.60, 131k ctx (very cheap reasoning)
- Total: 93 → 101 models, 15 → 17 providers
- 3 new tests for DeepInfra and Lambda providers

### Fixed
- pyproject.toml now uses dynamic versioning from `llm_prices.__version__` — fixes PyPI publish

## [0.1.15] - 2026-05-11

### Fixed
- Tests no longer hardcode `/workspace/projects/llm-prices` as `cwd` — they now
  work correctly in CI (GitHub Actions) and any other environment.

## [0.1.14] - 2026-05-09

### Added
- gpt-5-nano: $0.05/$0.40 per Mtok, 272k ctx — ultra-cheap GPT-5
- gpt-5-mini: $0.25/$2.00 per Mtok, 272k ctx — base GPT-5 mini tier
- o3-pro: $20.00/$80.00 per Mtok, 200k ctx — professional-grade reasoning
- o1-pro: $150.00/$600.00 per Mtok, 200k ctx — most expensive model in dataset
- Total: 89 → 93 models (same 15 providers)

### Changed
- Blog post rewritten: new headline/story focused on GPT-5, Grok 4.3, o3 repricing.
  Updated all model counts (80 → 93), terminal examples, provider highlights, and
  real-world cost calculations to reflect the current model landscape.

## [0.1.13] - 2026-05-09

### Added
- OpenAI GPT-5 series (4 models):
  - gpt-5.5: $5.00/$30.00 per Mtok, 1M context — current OpenAI flagship
  - gpt-5.4: $2.50/$15.00 per Mtok, 1M context
  - gpt-5.4-mini: $0.75/$4.50 per Mtok, 272k context
  - gpt-5.4-nano: $0.20/$1.25 per Mtok, 272k context
- xAI Grok 4 series (2 models):
  - grok-4.3: $1.25/$2.50 per Mtok, 1M context — current Grok flagship
  - grok-4.20-reasoning: $1.25/$2.50 per Mtok, **2M context**
- Total: 83 → 89 models (same 15 providers)
- Tests: 54 → 57 (test_gpt5_models_present, test_o3_repriced, test_grok4_present)

### Fixed
- o3: corrected from $10/$40 to **$2/$8** per Mtok (OpenAI repriced ~5× cheaper)

## [0.1.12] - 2026-05-09

### Added
- Google Gemini 3.1 Pro Preview ($2.00/$12.00, 1M ctx) — multimodal+agentic flagship preview
- Google Gemini 3.1 Flash-Lite ($0.25/$1.50, 1M ctx) — cost-efficient Gemini 3 model
- Google Gemini 2.5 Flash-Lite ($0.10/$0.40, 1M ctx) — smallest/cheapest Gemini 2.5
- Total: 80 → 83 models (same 15 providers)
- Tests: 51 → 54 (claude4_pricing_correct, gemini3_models_present, gemini_flash_pricing_updated)

### Fixed
- Claude Opus 4.7: corrected from $15/$75 to **$5/$25** per Mtok; context 200k → **1M tokens**
  (Anthropic official docs: claude-opus-4-7 is the affordable flagship, not legacy Opus 3 pricing)
- Claude Sonnet 4.6: context window 200k → **1M tokens**
- Claude Haiku 4.5: corrected from $0.80/$4.00 to **$1.00/$5.00** per Mtok
- Gemini 2.5 Flash: corrected from $0.15/$0.60 to **$0.30/$2.50** per Mtok
  (hybrid reasoning model with thinking budgets — output price reflects that)
- Gemini 2.5 Pro: updated notes (tiered pricing: $1.25/$10 ≤200k, $2.50/$15 >200k)

## [0.1.11] - 2026-05-09

### Added
- AI21 Labs (15th provider): Jamba Mini 1.7 ($0.20/$0.40, 256k ctx) and
  Jamba Large 1.7 ($2.00/$8.00, 256k ctx). Hybrid SSM+Transformer architecture.
- Total: 78 → 80 models, 14 → 15 providers
- Tests: 50 → 51 (test_ai21_models_present)

### Fixed
- test_list_csv: use csv.reader instead of naive split(",") to handle
  quoted fields that contain commas in the notes column

## [0.1.10] - 2026-05-09

### Added
- Groq: Kimi K2 (kimi-k2-gq, $1.00/$3.00, 262k ctx) and Qwen3 32B (qwen3-32b-gq, $0.29/$0.59)
- Mistral Large 3 (mistral-large-3): $0.50/$1.50 per Mtok, 262k context — 4× cheaper
  than Large 2 with 2× the context window. Major price cut for the flagship model.
- Mistral Medium 3 (mistral-medium-3): $0.40/$2.00 per Mtok, 131k context (new family)
- Mistral Small 3.2 (mistral-small-3-2): $0.06/$0.18 per Mtok, 131k context
  (cheaper and larger context than the older Small 3)
- Total: 73 → 78 models, same 14 providers
- Tests: 48 → 50 (test_mistral_large3_present, test_groq_new_models)

## [0.1.9] - 2026-05-09

### Added
- Amazon Bedrock provider: 5 models (nova-micro-br, nova-lite-br, nova-pro-br,
  nova-premier-br, nova-2-lite-br)
  Amazon's own Nova foundation models via Bedrock on-demand pricing (US East).
  Nova Micro has a 128k context at just $0.035/Mtok input — one of the cheapest options.
  Nova Premier offers a 1M token context window.
- Total: 68 → 73 models across 14 providers
- Test suite: 47 → 48 tests (test_bedrock_models_present)

## [0.1.8] - 2026-05-09

### Added
- SambaNova provider: 5 models (llama-4-maverick-sb, llama-3.3-70b-sb, deepseek-v3-sb,
  minimax-m2-5-sb, gemma-3-12b-sb)
  Ultra-fast inference on SambaNova RDU (Reconfigurable Dataflow Unit) silicon.
  Includes Llama 4 Maverick — the latest Meta flagship (17B MoE).
  Prices sourced from the live SambaNova API (api.sambanova.ai/v1/models).
- Total: 63 → 68 models across 13 providers
- Test suite: 46 → 47 tests (test_sambanova_models_present)

## [0.1.7] - 2026-05-08

### Added
- Cerebras provider: 3 models (llama-3.3-70b-cb, llama-3.1-8b-cb, qwen3-32b-cb)
  Ultra-fast inference on custom Cerebras silicon (wafer-scale chips)
- Total: 60 → 63 models across 12 providers

## [0.1.6] - 2026-05-08

### Added
- `top` command: show N cheapest models for a given token workload
  (`llm-prices top 5 --in 5000 --out 1000 --markdown`)
- Tests expanded from 39 → 45 (6 new tests for `top` command)

## [0.1.5] - 2026-05-08

### Changed
- Test suite expanded from 26 → 39 tests
- Added coverage for: --markdown output, --csv output, compare --markdown,
  budget command, new providers (Together/Fireworks/Perplexity), model count
  assertions, sort order verification

## [0.1.4] - 2026-05-08

### Added
- Perplexity AI provider: 4 models (sonar, sonar-pro, sonar-reasoning-pro,
  sonar-deep-research) with notes about per-request search fees
- Total: 56 → 60 models across 11 providers

## [0.1.3] - 2026-05-08

### Added
- Fireworks AI provider: 6 models (deepseek-v4-pro-fw, deepseek-v3-fw, kimi-k2-fw,
  llama-3.1-70b-fw, llama-3.1-8b-fw, mixtral-8x7b-fw)
- DeepSeek V4 Pro on Together AI (deepseek-v4-pro-together)
- Total: 49 → 56 models across 10 providers

## [0.1.2] - 2026-05-08

### Added
- Together AI provider: 6 models (qwen3-235b, kimi-k2, llama-3.3-70b-turbo,
  qwen3.5-9b, deepseek-r1-together, deepseek-v3-together)
- `list --markdown`: output as GitHub-flavored Markdown table (paste into READMEs/docs)
- `list --csv`: output as CSV (import into spreadsheets, databases)
- `compare --markdown`: output comparison as Markdown table
- Total: 43 → 49 models across 9 providers

## [0.1.1] - 2026-05-08

### Added
- OpenAI: gpt-4.1, gpt-4.1-mini, gpt-4.1-nano (up to 1M context window)
- Google: gemini-2.5-flash
- Anthropic: claude-3-7-sonnet; versioned model IDs (claude-opus-4-7,
  claude-sonnet-4-6, claude-haiku-4-5)
- Groq: llama-4-scout, llama-4-maverick
- Total: 36 → 43 models

### Fixed
- Corrected project URLs in pyproject.toml to point to actual GitHub repo

## [0.1.0] - 2026-05-08

### Added
- Initial release
- `list` command: show all models with pricing, filterable by provider/name, sortable
- `calc` command: calculate exact cost for a model + token count
- `compare` command: side-by-side cost comparison of multiple models
- `budget` command: how many API calls fit within a dollar budget
- `providers` command: list available providers
- JSON output mode (`--json`) for all commands
- Fuzzy model name matching (normalises hyphens, underscores, case)
- 36 models across 8 providers: OpenAI, Anthropic, Google, Mistral, Groq, Cohere, DeepSeek, xAI
- Zero runtime dependencies (Python stdlib only)
- Donation tip jar in `--help` output and README
- 26-test suite (100% passing)
- GitHub Actions CI + PyPI Trusted Publishing workflow
