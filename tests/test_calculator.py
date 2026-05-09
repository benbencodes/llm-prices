"""Tests for llm_prices.calculator"""
import json
import subprocess
import sys
import unittest

from llm_prices.calculator import calculate_cost, search_models, format_usd
from llm_prices.data import MODELS, PROVIDERS


class TestCalculateCost(unittest.TestCase):
    def test_exact_match(self):
        r = calculate_cost("gpt-4o", 1_000_000, 1_000_000)
        self.assertEqual(r["model"], "gpt-4o")
        self.assertEqual(r["provider"], "OpenAI")
        self.assertAlmostEqual(r["input_cost_usd"], 2.50, places=6)
        self.assertAlmostEqual(r["output_cost_usd"], 10.00, places=6)
        self.assertAlmostEqual(r["total_cost_usd"], 12.50, places=6)

    def test_zero_tokens(self):
        r = calculate_cost("gpt-4o-mini", 0, 0)
        self.assertEqual(r["total_cost_usd"], 0.0)

    def test_fuzzy_match_hyphens(self):
        r = calculate_cost("claude3haiku", 1000, 500)
        self.assertEqual(r["model"], "claude-3-haiku")

    def test_unknown_model_raises(self):
        with self.assertRaises(ValueError) as ctx:
            calculate_cost("nonexistent-model-xyz", 1000, 500)
        self.assertIn("Unknown model", str(ctx.exception))

    def test_ambiguous_model_raises(self):
        # "gpt4" matches gpt-4, gpt-4o, gpt-4o-mini, gpt-4-turbo
        with self.assertRaises(ValueError) as ctx:
            calculate_cost("gpt4", 1000, 500)
        self.assertIn("Ambiguous", str(ctx.exception))

    def test_case_insensitive(self):
        r = calculate_cost("GPT-4O", 1000, 1000)
        self.assertEqual(r["model"], "gpt-4o")

    def test_small_cost_precision(self):
        # gemini-1.5-flash-8b: $0.0375/Mtok in, $0.15/Mtok out
        r = calculate_cost("gemini-1.5-flash-8b", 1000, 500)
        self.assertAlmostEqual(r["input_cost_usd"], 0.0375 / 1000, places=10)

    def test_all_models_have_required_fields(self):
        for name, info in MODELS.items():
            self.assertIn("provider", info, f"{name} missing provider")
            self.assertIn("input_per_mtok", info, f"{name} missing input_per_mtok")
            self.assertIn("output_per_mtok", info, f"{name} missing output_per_mtok")
            self.assertIn("context_window", info, f"{name} missing context_window")
            self.assertIsInstance(info["input_per_mtok"], (int, float), f"{name} bad input price")
            self.assertIsInstance(info["output_per_mtok"], (int, float), f"{name} bad output price")
            self.assertGreater(info["input_per_mtok"], 0, f"{name} input price must be positive")
            self.assertGreater(info["output_per_mtok"], 0, f"{name} output price must be positive")
            self.assertGreater(info["context_window"], 0, f"{name} context window must be positive")


class TestSearchModels(unittest.TestCase):
    def test_filter_by_provider(self):
        results = search_models(provider="anthropic")
        for name, info in results:
            self.assertEqual(info["provider"], "Anthropic")
        self.assertGreater(len(results), 0)

    def test_filter_by_query(self):
        results = search_models(query="gpt-4o")
        names = [n for n, _ in results]
        self.assertIn("gpt-4o", names)

    def test_empty_query_returns_all(self):
        all_results = search_models()
        self.assertEqual(len(all_results), len(MODELS))

    def test_no_match_returns_empty(self):
        results = search_models(query="nonexistent-model-xyz-abc")
        self.assertEqual(results, [])


class TestFormatUsd(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(format_usd(0), "$0.000000")

    def test_small(self):
        s = format_usd(0.000001)
        self.assertTrue(s.startswith("$"))

    def test_normal(self):
        self.assertEqual(format_usd(1.5), "$1.5000")

    def test_large(self):
        s = format_usd(100.0)
        self.assertEqual(s, "$100.0000")


class TestProviders(unittest.TestCase):
    def test_providers_list_not_empty(self):
        self.assertGreater(len(PROVIDERS), 0)

    def test_known_providers_present(self):
        for p in ["OpenAI", "Anthropic", "Google", "Mistral"]:
            self.assertIn(p, PROVIDERS)


class TestCLI(unittest.TestCase):
    """Integration tests for the CLI via subprocess."""

    def run_cli(self, *args):
        result = subprocess.run(
            [sys.executable, "-m", "llm_prices.cli"] + list(args),
            capture_output=True, text=True,
            cwd="/workspace/projects/llm-prices"
        )
        return result

    def test_list_runs(self):
        r = self.run_cli("list")
        self.assertEqual(r.returncode, 0)
        self.assertIn("OpenAI", r.stdout)
        self.assertIn("Anthropic", r.stdout)

    def test_list_json(self):
        r = self.run_cli("list", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("model", data[0])

    def test_calc_basic(self):
        r = self.run_cli("calc", "gpt-4o", "--in", "10000", "--out", "2000")
        self.assertEqual(r.returncode, 0)
        self.assertIn("gpt-4o", r.stdout)
        self.assertIn("$0.0450", r.stdout)

    def test_calc_json(self):
        r = self.run_cli("calc", "gpt-4o-mini", "--in", "1000", "--out", "500", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(data["model"], "gpt-4o-mini")
        self.assertIn("total_cost_usd", data)

    def test_compare_runs(self):
        r = self.run_cli("compare", "gpt-4o", "claude-sonnet-4", "--in", "1000", "--out", "500")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Cheapest", r.stdout)

    def test_providers_runs(self):
        r = self.run_cli("providers")
        self.assertEqual(r.returncode, 0)
        self.assertIn("OpenAI", r.stdout)

    def test_unknown_model_exits_nonzero(self):
        r = self.run_cli("calc", "not-a-real-model-xyz", "--in", "1000", "--out", "500")
        self.assertNotEqual(r.returncode, 0)

    def test_filter_by_provider(self):
        r = self.run_cli("list", "--provider", "Google")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Google", r.stdout)
        self.assertNotIn("OpenAI", r.stdout)

    def test_list_markdown(self):
        r = self.run_cli("list", "--provider", "OpenAI", "--markdown")
        self.assertEqual(r.returncode, 0)
        # Must contain GFM table pipe characters
        self.assertIn("|", r.stdout)
        # Header row present
        self.assertIn("Model", r.stdout)
        self.assertIn("Provider", r.stdout)
        self.assertIn("Input/Mtok", r.stdout)
        # Separator row present
        self.assertIn("---", r.stdout)
        # Data row with dollar sign
        self.assertIn("$", r.stdout)
        # No stray plain-table lines
        self.assertNotIn("model(s) shown", r.stdout)

    def test_list_markdown_all_providers(self):
        r = self.run_cli("list", "--markdown")
        self.assertEqual(r.returncode, 0)
        lines = [l for l in r.stdout.splitlines() if l.startswith("|")]
        # header + separator + data rows
        self.assertGreater(len(lines), 10)

    def test_list_csv(self):
        import csv as csv_mod
        r = self.run_cli("list", "--csv")
        self.assertEqual(r.returncode, 0)
        lines = r.stdout.strip().splitlines()
        # First line is header
        self.assertEqual(lines[0], "model,provider,input_per_mtok_usd,output_per_mtok_usd,context_window,notes")
        # At least one data row
        self.assertGreater(len(lines), 1)
        # Parse via csv reader to handle quoted fields
        rows = list(csv_mod.reader(lines))
        self.assertEqual(len(rows[1]), 6)

    def test_list_csv_provider_filter(self):
        r = self.run_cli("list", "--provider", "Perplexity", "--csv")
        self.assertEqual(r.returncode, 0)
        lines = r.stdout.strip().splitlines()
        # header + 4 Perplexity models
        self.assertEqual(len(lines), 5)
        for line in lines[1:]:
            self.assertIn("Perplexity", line)

    def test_compare_markdown(self):
        r = self.run_cli("compare", "gpt-4o", "gemini-2.5-flash",
                         "--in", "1000", "--out", "500", "--markdown")
        self.assertEqual(r.returncode, 0)
        self.assertIn("|", r.stdout)
        self.assertIn("Model", r.stdout)
        self.assertIn("Total", r.stdout)
        # Should contain a comment line naming the cheapest
        self.assertIn("Cheapest", r.stdout)

    def test_compare_sorted_cheapest_first(self):
        r = self.run_cli("compare", "claude-opus-4-7", "gpt-4.1-nano",
                         "--in", "1000", "--out", "500")
        self.assertEqual(r.returncode, 0)
        # JSON mode gives deterministic order to test sorting
        r2 = self.run_cli("compare", "claude-opus-4-7", "gpt-4.1-nano",
                          "--in", "1000", "--out", "500", "--json")
        data = json.loads(r2.stdout)
        self.assertEqual(len(data), 2)
        # nano ($0.10/Mtok in) is cheaper than opus ($15/Mtok in)
        self.assertEqual(data[0]["model"], "gpt-4.1-nano")
        self.assertEqual(data[1]["model"], "claude-opus-4-7")
        self.assertLess(data[0]["total_cost_usd"], data[1]["total_cost_usd"])

    def test_budget_basic(self):
        r = self.run_cli("budget", "1.00", "--in", "1000", "--out", "500")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Budget", r.stdout)
        self.assertIn("Calls", r.stdout)

    def test_budget_json(self):
        r = self.run_cli("budget", "1.00", "--in", "1000", "--out", "500", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("calls_within_budget", data[0])
        self.assertIn("cost_per_call_usd", data[0])

    def test_new_providers_present(self):
        """Newer providers should all be queryable."""
        for provider in ["Together", "Fireworks", "Perplexity", "Cerebras", "SambaNova", "Bedrock", "AI21"]:
            r = self.run_cli("list", "--provider", provider)
            self.assertEqual(r.returncode, 0, f"Provider {provider} failed")
            self.assertIn(provider, r.stdout)

    def test_cerebras_models_present(self):
        r = self.run_cli("list", "--provider", "Cerebras")
        self.assertEqual(r.returncode, 0)
        for model in ["llama-3.3-70b-cb", "llama-3.1-8b-cb", "qwen3-32b-cb"]:
            self.assertIn(model, r.stdout)

    def test_perplexity_models_present(self):
        r = self.run_cli("list", "--provider", "Perplexity")
        self.assertEqual(r.returncode, 0)
        for model in ["sonar", "sonar-pro", "sonar-reasoning-pro", "sonar-deep-research"]:
            self.assertIn(model, r.stdout)

    def test_total_model_count(self):
        """Sanity check: at least 83 models across at least 15 providers."""
        r = self.run_cli("list", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertGreaterEqual(len(data), 83)
        providers = {m["provider"] for m in data}
        self.assertGreaterEqual(len(providers), 15)

    def test_claude4_pricing_correct(self):
        """Claude 4 family: Opus 4.7 at $5/$25 (not $15/$75), 1M context."""
        r = self.run_cli("list", "--provider", "Anthropic", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        by_id = {m["model"]: m for m in data}
        opus = by_id["claude-opus-4-7"]
        self.assertAlmostEqual(opus["input_per_mtok_usd"], 5.00)
        self.assertAlmostEqual(opus["output_per_mtok_usd"], 25.00)
        self.assertEqual(opus["context_window"], 1_000_000)
        # Sonnet and Haiku should have correct prices too
        sonnet = by_id["claude-sonnet-4-6"]
        self.assertEqual(sonnet["context_window"], 1_000_000)
        haiku = by_id["claude-haiku-4-5"]
        self.assertAlmostEqual(haiku["input_per_mtok_usd"], 1.00)

    def test_gemini3_models_present(self):
        """Gemini 3.1 Flash-Lite and Pro Preview should be in the dataset."""
        r = self.run_cli("list", "--provider", "Google")
        self.assertEqual(r.returncode, 0)
        for model in ["gemini-3.1-flash-lite", "gemini-3.1-pro-preview", "gemini-2.5-flash-lite"]:
            self.assertIn(model, r.stdout)

    def test_gemini_flash_pricing_updated(self):
        """Gemini 2.5 Flash output at $2.50 (hybrid reasoning model)."""
        r = self.run_cli("list", "--provider", "Google", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        by_id = {m["model"]: m for m in data}
        flash = by_id["gemini-2.5-flash"]
        self.assertAlmostEqual(flash["output_per_mtok_usd"], 2.50)

    def test_ai21_models_present(self):
        r = self.run_cli("list", "--provider", "AI21")
        self.assertEqual(r.returncode, 0)
        for model in ["jamba-mini-a21", "jamba-large-a21"]:
            self.assertIn(model, r.stdout)

    def test_mistral_large3_present(self):
        """Mistral Large 3 must be cheaper than Large 2 and have larger context."""
        r = self.run_cli("list", "--provider", "Mistral", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        by_id = {m["model"]: m for m in data}
        self.assertIn("mistral-large-3", by_id)
        self.assertIn("mistral-large-2", by_id)
        self.assertLess(
            by_id["mistral-large-3"]["input_per_mtok_usd"],
            by_id["mistral-large-2"]["input_per_mtok_usd"],
        )

    def test_groq_new_models(self):
        r = self.run_cli("list", "--provider", "Groq")
        self.assertEqual(r.returncode, 0)
        for model in ["kimi-k2-gq", "qwen3-32b-gq"]:
            self.assertIn(model, r.stdout)

    def test_bedrock_models_present(self):
        r = self.run_cli("list", "--provider", "Bedrock")
        self.assertEqual(r.returncode, 0)
        for model in ["nova-micro-br", "nova-lite-br", "nova-pro-br", "nova-premier-br"]:
            self.assertIn(model, r.stdout)

    def test_sambanova_models_present(self):
        r = self.run_cli("list", "--provider", "SambaNova")
        self.assertEqual(r.returncode, 0)
        for model in ["llama-4-maverick-sb", "llama-3.3-70b-sb", "deepseek-v3-sb"]:
            self.assertIn(model, r.stdout)

    def test_list_sort_input(self):
        r = self.run_cli("list", "--sort", "input", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        prices = [m["input_per_mtok_usd"] for m in data]
        self.assertEqual(prices, sorted(prices))

    def test_list_sort_total(self):
        r = self.run_cli("list", "--sort", "total", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        totals = [m["input_per_mtok_usd"] + m["output_per_mtok_usd"] for m in data]
        self.assertEqual(totals, sorted(totals))

    def test_top_default(self):
        r = self.run_cli("top")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Top 10", r.stdout)
        # Rank numbers appear at the start of data lines
        self.assertIn("1 ", r.stdout)

    def test_top_n(self):
        r = self.run_cli("top", "5", "--in", "5000", "--out", "1000", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(len(data), 5)

    def test_top_json(self):
        r = self.run_cli("top", "5", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(len(data), 5)
        # Must be sorted cheapest first
        totals = [d["total_cost_usd"] for d in data]
        self.assertEqual(totals, sorted(totals))

    def test_top_markdown(self):
        r = self.run_cli("top", "3", "--in", "1000", "--out", "500", "--markdown")
        self.assertEqual(r.returncode, 0)
        self.assertIn("|", r.stdout)
        self.assertIn("Rank", r.stdout)
        self.assertIn("#1", r.stdout)

    def test_top_provider_filter(self):
        r = self.run_cli("top", "3", "--provider", "Anthropic")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Anthropic", r.stdout)
        self.assertNotIn("OpenAI", r.stdout)

    def test_top_cheapest_is_actually_cheapest(self):
        """The #1 model in top should match the cheapest in budget list."""
        r_top = self.run_cli("top", "1", "--in", "1000", "--out", "500", "--json")
        r_budget = self.run_cli("budget", "1.00", "--in", "1000", "--out", "500", "--json")
        top_data = json.loads(r_top.stdout)
        budget_data = json.loads(r_budget.stdout)
        # Budget is sorted most-calls-first = cheapest first
        self.assertEqual(top_data[0]["model"], budget_data[0]["model"])


if __name__ == "__main__":
    unittest.main()
