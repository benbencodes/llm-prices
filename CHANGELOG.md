# Changelog

All notable changes to llm-prices will be documented here.

## [0.1.31] - 2026-05-12

### Added
- **New provider: Inflection AI**
  - Inflection-3 Pi (`inflection-3-pi`): $2.50/$10.00 per Mtok, 8k ctx — conversational AI (Pi)
  - Inflection-3 Productivity (`inflection-3-productivity`): $2.50/$10.00, 8k ctx — enterprise tasks
- **Qwen3 model expansion** (4 new models):
  - Qwen3-8B (`qwen3-8b`): $0.05/$0.40 per Mtok, 40k ctx — smallest Qwen3 dense model
  - Qwen3-30B-A3B MoE (`qwen3-30b-moe`): $0.09/$0.45, 40k ctx — 3B active params, very cheap
  - Qwen3 Max (`qwen3-max`): $0.78/$3.90, 262k ctx — Alibaba's Qwen3 flagship with thinking mode
  - Qwen3 Coder (`qwen3-coder`): $0.22/$1.80, 262k ctx — coding specialist, 262k context
- **Google Gemma 4** (2 new models):
  - Gemma 3 4B (`gemma-3-4b`): $0.04/$0.08, 131k ctx — ultra-compact Gemma 3
  - Gemma 4 27B Dense (`gemma-4-27b`): $0.12/$0.37, 262k ctx — Google's 2026 open-weights flagship
  - Gemma 4 27B MoE (`gemma-4-27b-moe`): $0.06/$0.33, 262k ctx — cheaper MoE variant
- **Mistral additions** (3 new models):
  - Mistral Saba (`mistral-saba`): $0.20/$0.60, 32k ctx — Arabic & multilingual specialist (24B)
  - Ministral 3B (`ministral-3b`): $0.10/$0.10, 131k ctx — smallest Mistral model, flat rate
  - Voxtral Small (`voxtral-small`): $0.10/$0.30, 32k ctx — Mistral's speech/voice processing model
- Total: 173 → 185 models; 24 → 25 providers

## [0.1.30] - 2026-05-12

### Added
- **New provider: Microsoft Azure AI Foundry**
  - Phi-4 14B (`phi-4`): $0.065/$0.140 per Mtok, 16k ctx — SOTA SLM for reasoning/coding
  - Phi-4 Mini (`phi-4-mini-instruct`): $0.080/$0.350 per Mtok, 131k ctx — 3.8B compact model
  - Phi-4 Reasoning (`phi-4-reasoning`): $1.50/$6.00 per Mtok, 32k ctx — chain-of-thought model
- DeepSeek-R1-0528 (`deepseek-r1-0528`): $0.55/$2.19 per Mtok, 163k ctx
  — May 2026 R1 checkpoint; improved agentic + STEM reasoning; available on DeepSeek native API
- Qwen3-32B (`qwen3-32b`): $0.20/$0.60 per Mtok, 131k ctx — dense model, strong coding/math
- Qwen3-14B (`qwen3-14b`): $0.10/$0.30 per Mtok, 131k ctx — compact with excellent efficiency
- Total: 167 → 173 models; 23 → 24 providers

## [0.1.29] - 2026-05-12

### Added
- DeepSeek V4 Flash (`deepseek-v4-flash`): $0.14/$0.28 per Mtok, 1M ctx
  — Cheapest DeepSeek model with massive 1M context window
- DeepSeek-R1 Distill Qwen-32B (`deepseek-r1-distill-qwen-32b`): $0.29/$0.29 per Mtok, 32k ctx
  — R1 reasoning distilled into Qwen2.5-32B; flat-rate pricing
- DeepSeek-R1 Distill Llama-70B (`deepseek-r1-distill-llama-70b`): $0.70/$0.80 per Mtok, 131k ctx
  — R1 reasoning on Llama-3.3-70B open-weights backbone
- Ministral 14B (`ministral-14b`): $0.20/$0.20 per Mtok, 262k ctx
  — Ministral 14B (Dec 2025); 262k ctx; step up from 8B at same flat-rate pricing
- Mistral Small 2603 (`mistral-small-2603`): $0.15/$0.60 per Mtok, 262k ctx
  — Mistral Small March 2026; 262k ctx; asymmetric pricing with cheap input
- Gemma 3 27B (`gemma-3-27b`): $0.08/$0.16 per Mtok, 131k ctx
  — Google's flagship open-weights Gemma 3 model; runs via Google AI Studio
- Gemma 3 12B (`gemma-3-12b`): $0.04/$0.13 per Mtok, 131k ctx
  — Compact Gemma 3; strong multilingual + coding capability
- **New provider: Qwen / Alibaba Cloud** (direct dashscope API)
  - Qwen Turbo (`qwen-turbo`): $0.03/$0.13 per Mtok, 131k ctx — fastest/cheapest
  - Qwen Plus (`qwen-plus`): $0.26/$0.78 per Mtok, 1M ctx — 1M context window
  - Qwen Max (`qwen-max`): $1.04/$4.16 per Mtok, 32k ctx — Alibaba flagship
  - Qwen3-235B (`qwen3-235b`): $0.45/$1.82 per Mtok, 131k ctx — 235B MoE open-weights
- Total: 157 → 167 models; 22 → 23 providers

## [0.1.28] - 2026-05-12

### Added
- Mistral Pixtral Large (`pixtral-large`): $2.00/$6.00 per Mtok, 131k ctx
  — Mistral's multimodal vision flagship (Nov 2024); same price tier as Mistral Large 2
- Mistral Mixtral 8×22B (`mixtral-8x22b`): $2.00/$6.00 per Mtok, 65k ctx
  — Mistral's largest open-weights MoE (141B total params); 141B total params
- Mistral NeMo 12B (`mistral-nemo`): $0.02/$0.03 per Mtok, 131k ctx
  — Ultra-cheap Mistral+NVIDIA collaboration (Jul 2024); open-weights; among cheapest per-token
- Llama 3.2 11B Vision (`llama-3.2-11b-vision`): $0.18/$0.18 per Mtok, 128k ctx
  — Meta's multimodal vision model via Groq; compact image+text at flat rate
- Llama 3.2 90B Vision (`llama-3.2-90b-vision`): $0.90/$0.90 per Mtok, 128k ctx
  — Meta's large multimodal vision model via Groq; highest accuracy Llama 3.2 vision
- Total: 152 → 157 models

## [0.1.27] - 2026-05-12

### Added
- Mistral Magistral Medium (`magistral-medium`): $2.00/$5.00 per Mtok, 40k ctx
  — Mistral's first reasoning flagship (Jun 2025); extended thinking, 40k output window
- Mistral Magistral Small (`magistral-small`): $0.50/$1.50 per Mtok, 40k ctx
  — Compact reasoning model; same price tier as Mistral Large 3 but with chain-of-thought
- xAI Grok-3 Mini Fast (`grok-3-mini-fast`): $0.60/$4.00 per Mtok, 131k ctx
  — High-speed reasoning tier; premium compute for latency-sensitive reasoning workloads
- Total: 149 → 152 models

## [0.1.26] - 2026-05-12

### Added
- Claude Opus 4.6 (`claude-opus-4-6`): $5.00/$25.00 per Mtok, 128k ctx
  — Feb 2026 Opus 4 revision; expanded context at same price as 4.7
- Claude Opus 4.5 (`claude-opus-4-5`): $5.00/$25.00 per Mtok, 64k ctx
  — Nov 2025 mid-cycle Opus 4 revision
- Claude Opus 4.1 (`claude-opus-4-1`): $15.00/$75.00 per Mtok, 32k ctx
  — Original Opus 4 launch (Aug 2025); expensive legacy tier
- Claude Sonnet 4.5 (`claude-sonnet-4-5`): $3.00/$15.00 per Mtok, 64k ctx
  — Sep 2025 first Sonnet 4 release; 64k context window
- Cohere Command A (`command-a`): $2.50/$10.00 per Mtok, 256k ctx
  — Mar 2025 enterprise instruction-following model; 256k context; replaces Command R+
- Total: 144 → 149 models

## [0.1.25] - 2026-05-12

### Added
- GPT-5 base (`gpt-5`): $1.25/$10.00 per Mtok, 128k ctx
  — Original GPT-5 release (Aug 2025); foundation of the GPT-5 family
- GPT-5.1 (`gpt-5.1`): $1.25/$10.00 per Mtok, 128k ctx
  — Nov 2025 GPT-5 update; improved quality at same price as base GPT-5
- GPT-5.2 (`gpt-5.2`): $1.75/$14.00 per Mtok, 128k ctx
  — Dec 2025 GPT-5 update; improved performance at moderate price premium
- GPT-5 Pro (`gpt-5-pro`): $15.00/$120.00 per Mtok, 272k ctx
  — Premium GPT-5 tier; ultra-high capability for most demanding tasks
- Grok-4 standard (`grok-4`): $3.00/$15.00 per Mtok, 256k ctx
  — xAI's Grok-4 (Jul 2025); predecessor to 4.3 and 4.20-reasoning variants
- Grok Code Fast (`grok-code-fast`): $0.20/$1.50 per Mtok, 256k ctx
  — xAI coding specialist; ultra-low cost for code generation and review tasks
- Total: 138 → 144 models

## [0.1.24] - 2026-05-11

### Added
- DeepSeek V3.2 (`deepseek-v3.2`): $0.28/$0.40 per Mtok, 163k ctx
  — DeepSeek's latest V3 revision with reasoning support and flat-rate output pricing
- OpenAI open-source 120B on Groq (`gpt-oss-120b-gq`): $0.15/$0.60 per Mtok, 131k ctx
  — OpenAI's open-weight 120B model hosted on Groq's fast inference
- OpenAI open-source 20B on Groq (`gpt-oss-20b-gq`): $0.075/$0.30 per Mtok, 131k ctx
  — Cheaper 20B tier of the OpenAI open-source family on Groq
- Google Deep Research Pro (`gemini-deep-research-pro`): $2.00/$12.00 per Mtok, 65k ctx
  — Multi-step web research with grounding; Google's dedicated research model
- Total: 134 → 138 models

## [0.1.23] - 2026-05-11

### Added
- OpenAI o3 Deep Research (`o3-deep-research`): $10.00/$40.00 per Mtok, 200k ctx
  — Multi-step web + document research model using o3 reasoning
- OpenAI o4-mini Deep Research (`o4-mini-deep-research`): $2.00/$8.00 per Mtok, 200k ctx
  — Affordable deep research for agentic research loops
- OpenAI GPT-5 Codex (`gpt-5-codex`): $1.25/$10.00 per Mtok, 272k ctx
  — GPT-5 coding-focused model with 272k context
- OpenAI Codex Mini Latest (`codex-mini-latest`): $1.50/$6.00 per Mtok, 200k ctx
  — Compact, cost-efficient coding model
- Total: 130 → 134 models

## [0.1.22] - 2026-05-11

### Added
- Gemini 3 Flash Preview (`gemini-3-flash-preview`): $0.50/$3.00 per Mtok, 1M ctx
  — Google's latest speed+intelligence model with search/grounding
- xAI Grok 4.1 Fast (`grok-4-1-fast`): $0.20/$0.50 per Mtok, 2M ctx
  — New cheaper xAI tier; 6× less expensive than grok-4.3 for both reasoning and non-reasoning
- Total: 128 → 130 models

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
