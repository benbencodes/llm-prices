# Changelog

All notable changes to llm-prices will be documented here.

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
