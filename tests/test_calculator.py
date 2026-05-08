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
        r = self.run_cli("list", "--csv")
        self.assertEqual(r.returncode, 0)
        lines = r.stdout.strip().splitlines()
        # First line is header
        self.assertEqual(lines[0], "model,provider,input_per_mtok_usd,output_per_mtok_usd,context_window,notes")
        # At least one data row
        self.assertGreater(len(lines), 1)
        # Columns are comma-separated
        self.assertEqual(len(lines[1].split(",")), 6)

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
        """Together, Fireworks, Perplexity should all be queryable."""
        for provider in ["Together", "Fireworks", "Perplexity"]:
            r = self.run_cli("list", "--provider", provider)
            self.assertEqual(r.returncode, 0, f"Provider {provider} failed")
            self.assertIn(provider, r.stdout)

    def test_perplexity_models_present(self):
        r = self.run_cli("list", "--provider", "Perplexity")
        self.assertEqual(r.returncode, 0)
        for model in ["sonar", "sonar-pro", "sonar-reasoning-pro", "sonar-deep-research"]:
            self.assertIn(model, r.stdout)

    def test_total_model_count(self):
        """Sanity check: at least 60 models across at least 11 providers."""
        r = self.run_cli("list", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertGreaterEqual(len(data), 60)
        providers = {m["provider"] for m in data}
        self.assertGreaterEqual(len(providers), 11)

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


if __name__ == "__main__":
    unittest.main()
