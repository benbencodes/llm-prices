# Changelog

All notable changes to llm-prices will be documented here.

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
