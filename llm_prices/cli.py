"""llm-prices CLI — look up and compare LLM API costs."""

import argparse
import csv
import io
import json
import signal
import sys

from .data import MODELS, PROVIDERS, DATA_DATE
from .calculator import calculate_cost, format_usd, search_models

# Suppress BrokenPipeError when output is piped to head/less/etc.
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

DONATION_NOTE = """
Built by an AI agent. If this tool saves you time, consider a tip:
  SOL : kbghHYeBXr2AcYUyvkofHa9sArgkJcKBC6zZhSdao82
  ETH : 0x310eEb225245D5A3e1773C5Def30Fe5d0289A1b3
  BTC : bc1qv0ny3c97lk80qv5v79f52w3hyaqq2ss0zdqp52
  https://github.com/benbencodes/llm-prices
"""


def _to_markdown_table(headers, rows):
    widths = [max(len(str(r[i])) for r in ([headers] + rows)) for i in range(len(headers))]
    sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
    def fmt_row(r):
        return "|" + "|".join(f" {str(r[i]):<{widths[i]}} " for i in range(len(headers))) + "|"
    return "\n".join([fmt_row(headers), sep] + [fmt_row(r) for r in rows])


def _to_csv(headers, rows):
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(headers)
    w.writerows(rows)
    return buf.getvalue().rstrip()


def cmd_list(args):
    results = search_models(query=args.search or "", provider=args.provider or "")

    if args.sort == "input":
        results.sort(key=lambda x: x[1]["input_per_mtok"])
    elif args.sort == "output":
        results.sort(key=lambda x: x[1]["output_per_mtok"])
    elif args.sort == "total":
        results.sort(key=lambda x: x[1]["input_per_mtok"] + x[1]["output_per_mtok"])
    else:
        results.sort(key=lambda x: (x[1]["provider"], x[0]))

    if args.json:
        output = [
            {
                "model": name,
                "provider": info["provider"],
                "input_per_mtok_usd": info["input_per_mtok"],
                "output_per_mtok_usd": info["output_per_mtok"],
                "context_window": info["context_window"],
                "notes": info.get("notes", ""),
            }
            for name, info in results
        ]
        print(json.dumps(output, indent=2))
        return

    if not results:
        print("No models found matching your filters.")
        return

    headers = ["Model", "Provider", "Input/Mtok", "Output/Mtok", "Context", "Notes"]
    rows = [
        [
            name,
            info["provider"],
            f"${info['input_per_mtok']:.4f}",
            f"${info['output_per_mtok']:.4f}",
            f"{info['context_window'] // 1000}k",
            info.get("notes", ""),
        ]
        for name, info in results
    ]

    if args.markdown:
        print(f"<!-- Prices as of {DATA_DATE}. Verify at provider's pricing page. -->")
        print(_to_markdown_table(headers, rows))
        return

    if args.csv:
        print(_to_csv(
            ["model", "provider", "input_per_mtok_usd", "output_per_mtok_usd", "context_window", "notes"],
            [
                [name, info["provider"], info["input_per_mtok"], info["output_per_mtok"],
                 info["context_window"], info.get("notes", "")]
                for name, info in results
            ],
        ))
        return

    # Plain table
    col_model = max(len(r[0]) for r in rows) + 2
    col_model = max(col_model, 26)
    header = (
        f"{'Model':<{col_model}} {'Provider':<12} "
        f"{'Input/Mtok':>12} {'Output/Mtok':>12} {'Context':>10}  Notes"
    )
    print(f"Prices as of {DATA_DATE}. Verify at provider's pricing page.")
    print()
    print(header)
    print("-" * len(header))

    for name, info in results:
        ctx = f"{info['context_window'] // 1000}k"
        notes = info.get("notes", "")
        print(
            f"{name:<{col_model}} {info['provider']:<12} "
            f"${info['input_per_mtok']:>10.4f}  ${info['output_per_mtok']:>10.4f} "
            f"{ctx:>10}  {notes}"
        )

    print()
    print(f"{len(results)} model(s) shown.")


def cmd_calc(args):
    try:
        result = calculate_cost(args.model, args.input_tokens, args.output_tokens)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print(f"Model  : {result['model']} ({result['provider']})")
    print(f"Tokens : {result['input_tokens']:,} in / {result['output_tokens']:,} out")
    print(f"Rate   : ${result['input_per_mtok']}/Mtok in, ${result['output_per_mtok']}/Mtok out")
    print(f"Cost   : {format_usd(result['input_cost_usd'])} in + "
          f"{format_usd(result['output_cost_usd'])} out = "
          f"{format_usd(result['total_cost_usd'])} total")


def cmd_compare(args):
    models = args.models
    if len(models) < 2:
        print("Error: provide at least 2 model names to compare.", file=sys.stderr)
        sys.exit(1)

    rows = []
    for m in models:
        try:
            result = calculate_cost(m, args.input_tokens, args.output_tokens)
            rows.append(result)
        except ValueError as e:
            print(f"Warning: {e}", file=sys.stderr)

    if not rows:
        return

    rows.sort(key=lambda r: r["total_cost_usd"])
    cheapest = rows[0]["total_cost_usd"] if rows else 1

    if args.json:
        print(json.dumps(rows, indent=2))
        return

    headers = ["Model", "Provider", "Input", "Output", "Total"]
    table_rows = []
    for r in rows:
        ratio = ""
        if r["total_cost_usd"] > cheapest and cheapest > 0:
            ratio = f" ({r['total_cost_usd'] / cheapest:.1f}x)"
        table_rows.append([
            r["model"], r["provider"],
            format_usd(r["input_cost_usd"]),
            format_usd(r["output_cost_usd"]),
            format_usd(r["total_cost_usd"]) + ratio,
        ])

    if args.markdown:
        caption = (
            f"<!-- {args.input_tokens:,} input / {args.output_tokens:,} output tokens. "
            f"Cheapest: {rows[0]['model']} -->"
        )
        print(caption)
        print(_to_markdown_table(headers, table_rows))
        return

    col = max(len(r["model"]) for r in rows) + 2
    col = max(col, 20)
    print(f"Comparison: {args.input_tokens:,} input tokens, {args.output_tokens:,} output tokens")
    print()
    hdr = f"{'Model':<{col}} {'Provider':<12} {'Input':>12} {'Output':>12} {'Total':>12}"
    print(hdr)
    print("-" * len(hdr))

    for r, tr in zip(rows, table_rows):
        print(
            f"{r['model']:<{col}} {r['provider']:<12} "
            f"{format_usd(r['input_cost_usd']):>12} "
            f"{format_usd(r['output_cost_usd']):>12} "
            f"{tr[4]:>12}"
        )

    print()
    print(f"Cheapest: {rows[0]['model']} at {format_usd(rows[0]['total_cost_usd'])}")


def cmd_budget(args):
    """How many calls can you make within a budget?"""
    budget = args.budget
    input_tokens = args.input_tokens
    output_tokens = args.output_tokens

    results = search_models(query=args.search or "", provider=args.provider or "")
    rows = []
    for name, info in results:
        try:
            r = calculate_cost(name, input_tokens, output_tokens)
            if r["total_cost_usd"] > 0:
                calls = int(budget / r["total_cost_usd"])
                rows.append((name, info["provider"], r["total_cost_usd"], calls))
        except ValueError:
            pass

    rows.sort(key=lambda x: -x[3])  # most calls first

    if args.json:
        output = [
            {"model": n, "provider": p, "cost_per_call_usd": c, "calls_within_budget": k}
            for n, p, c, k in rows
        ]
        print(json.dumps(output, indent=2))
        return

    if not rows:
        print("No models found.")
        return

    col = max(len(r[0]) for r in rows) + 2
    col = max(col, 22)
    print(
        f"Budget: ${budget:.4f}  |  "
        f"Tokens per call: {input_tokens:,} in / {output_tokens:,} out"
    )
    print()
    hdr = f"{'Model':<{col}} {'Provider':<12} {'Cost/call':>12} {'Calls':>12}"
    print(hdr)
    print("-" * len(hdr))
    for name, provider, cost, calls in rows:
        calls_str = f"{calls:,}" if calls < 1_000_000_000 else ">1B"
        print(f"{name:<{col}} {provider:<12} {format_usd(cost):>12} {calls_str:>12}")


def cmd_top(args):
    """Show the N cheapest models for a given token workload."""
    n = args.n
    input_tokens = args.input_tokens
    output_tokens = args.output_tokens

    results = search_models(query=args.search or "", provider=args.provider or "")
    rows = []
    for name, info in results:
        try:
            r = calculate_cost(name, input_tokens, output_tokens)
            if r["total_cost_usd"] >= 0:
                rows.append(r)
        except ValueError:
            pass

    rows.sort(key=lambda r: r["total_cost_usd"])
    rows = rows[:n]

    if not rows:
        print("No models found.")
        return

    if args.json:
        print(json.dumps(rows, indent=2))
        return

    headers = ["Rank", "Model", "Provider", "Input", "Output", "Total"]
    table_rows = [
        [
            f"#{i+1}",
            r["model"],
            r["provider"],
            format_usd(r["input_cost_usd"]),
            format_usd(r["output_cost_usd"]),
            format_usd(r["total_cost_usd"]),
        ]
        for i, r in enumerate(rows)
    ]

    if args.markdown:
        caption = (
            f"<!-- Top {n} cheapest: {input_tokens:,} input / {output_tokens:,} output tokens -->"
        )
        print(caption)
        print(_to_markdown_table(headers, table_rows))
        return

    col = max(len(r["model"]) for r in rows) + 2
    col = max(col, 22)
    print(f"Top {n} cheapest: {input_tokens:,} input / {output_tokens:,} output tokens")
    print()
    hdr = f"{'#':<4} {'Model':<{col}} {'Provider':<12} {'Input':>12} {'Output':>12} {'Total':>12}"
    print(hdr)
    print("-" * len(hdr))
    for i, r in enumerate(rows):
        print(
            f"{i+1:<4} {r['model']:<{col}} {r['provider']:<12} "
            f"{format_usd(r['input_cost_usd']):>12} "
            f"{format_usd(r['output_cost_usd']):>12} "
            f"{format_usd(r['total_cost_usd']):>12}"
        )


def cmd_providers(args):
    if args.json:
        print(json.dumps(PROVIDERS))
        return
    print("Available providers:")
    for p in PROVIDERS:
        count = sum(1 for m in MODELS.values() if m["provider"] == p)
        print(f"  {p:<16} ({count} model{'s' if count != 1 else ''})")


def main():
    parser = argparse.ArgumentParser(
        prog="llm-prices",
        description="Look up and compare LLM API pricing across providers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=DONATION_NOTE,
    )
    from . import __version__
    parser.add_argument("--version", action="version", version=f"llm-prices {__version__}")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    # list
    p_list = sub.add_parser("list", help="List models and their pricing")
    p_list.add_argument("--provider", "-p", help="Filter by provider name")
    p_list.add_argument("--search", "-s", help="Filter by model name substring")
    p_list.add_argument(
        "--sort",
        choices=["provider", "input", "output", "total"],
        default="provider",
        help="Sort order (default: provider)",
    )
    p_list.add_argument("--json", action="store_true", help="Output as JSON")
    p_list.add_argument("--markdown", action="store_true", help="Output as Markdown table")
    p_list.add_argument("--csv", action="store_true", help="Output as CSV")

    # calc
    p_calc = sub.add_parser("calc", help="Calculate cost for a specific model and token count")
    p_calc.add_argument("model", help="Model name (e.g. gpt-4o, claude-sonnet-4)")
    p_calc.add_argument("--in", dest="input_tokens", type=int, required=True,
                        help="Number of input (prompt) tokens")
    p_calc.add_argument("--out", dest="output_tokens", type=int, required=True,
                        help="Number of output (completion) tokens")
    p_calc.add_argument("--json", action="store_true", help="Output as JSON")

    # compare
    p_cmp = sub.add_parser("compare", help="Compare costs across multiple models")
    p_cmp.add_argument("models", nargs="+", help="Two or more model names")
    p_cmp.add_argument("--in", dest="input_tokens", type=int, default=1000,
                       help="Input tokens (default: 1000)")
    p_cmp.add_argument("--out", dest="output_tokens", type=int, default=500,
                       help="Output tokens (default: 500)")
    p_cmp.add_argument("--json", action="store_true", help="Output as JSON")
    p_cmp.add_argument("--markdown", action="store_true", help="Output as Markdown table")

    # providers
    p_prov = sub.add_parser("providers", help="List available providers")
    p_prov.add_argument("--json", action="store_true", help="Output as JSON")

    # budget
    p_bud = sub.add_parser("budget", help="How many API calls fit within a dollar budget?")
    p_bud.add_argument("budget", type=float, help="Budget in USD (e.g. 1.00, 10.00)")
    p_bud.add_argument("--in", dest="input_tokens", type=int, default=1000,
                       help="Input tokens per call (default: 1000)")
    p_bud.add_argument("--out", dest="output_tokens", type=int, default=500,
                       help="Output tokens per call (default: 500)")
    p_bud.add_argument("--provider", "-p", help="Filter by provider")
    p_bud.add_argument("--search", "-s", help="Filter by model name")
    p_bud.add_argument("--json", action="store_true", help="Output as JSON")

    # top
    p_top = sub.add_parser("top", help="Show the N cheapest models for a given workload")
    p_top.add_argument("n", type=int, nargs="?", default=10,
                       help="Number of models to show (default: 10)")
    p_top.add_argument("--in", dest="input_tokens", type=int, default=1000,
                       help="Input tokens per call (default: 1000)")
    p_top.add_argument("--out", dest="output_tokens", type=int, default=500,
                       help="Output tokens per call (default: 500)")
    p_top.add_argument("--provider", "-p", help="Filter by provider")
    p_top.add_argument("--search", "-s", help="Filter by model name")
    p_top.add_argument("--json", action="store_true", help="Output as JSON")
    p_top.add_argument("--markdown", action="store_true", help="Output as Markdown table")

    args = parser.parse_args()

    dispatch = {
        "list": cmd_list,
        "calc": cmd_calc,
        "compare": cmd_compare,
        "providers": cmd_providers,
        "budget": cmd_budget,
        "top": cmd_top,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
