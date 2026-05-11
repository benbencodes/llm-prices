"""MCP server for llm-prices — exposes LLM pricing tools via the Model Context Protocol."""

from mcp.server.fastmcp import FastMCP
from .calculator import calculate_cost, search_models
from .data import MODELS, PROVIDERS

mcp = FastMCP(
    name="llm-prices",
    instructions=(
        "Query LLM API pricing across 128+ models and 22+ providers. "
        "Use these tools to compare costs, find the cheapest option for a workload, "
        "or calculate the exact cost of an API call before making it."
    ),
)


@mcp.tool()
def get_model_pricing(model_id: str) -> dict:
    """Get pricing details for a specific LLM model.

    Args:
        model_id: The model identifier (e.g. 'gpt-4o', 'claude-sonnet-4-6',
                  'gemini-2.5-flash'). Fuzzy matching is supported.
    """
    if model_id not in MODELS:
        results = search_models(query=model_id)
        if not results:
            return {"error": f"Model '{model_id}' not found. Use list_models to see available models."}
        if len(results) > 1:
            matches = [r[0] for r in results[:10]]
            return {"error": f"Ambiguous query '{model_id}'. Did you mean one of: {matches}?"}
        model_id = results[0][0]

    info = MODELS[model_id]
    return {
        "model": model_id,
        "provider": info["provider"],
        "input_per_mtok_usd": info["input_per_mtok"],
        "output_per_mtok_usd": info["output_per_mtok"],
        "context_window": info["context_window"],
        "notes": info.get("notes", ""),
    }


@mcp.tool()
def calculate_api_cost(model_id: str, input_tokens: int, output_tokens: int) -> dict:
    """Calculate the exact cost of an LLM API call.

    Args:
        model_id: The model identifier (e.g. 'gpt-4o', 'claude-sonnet-4-6').
        input_tokens: Number of input/prompt tokens.
        output_tokens: Number of output/completion tokens.
    """
    try:
        result = calculate_cost(model_id, input_tokens, output_tokens)
        return {
            "model": result["model"],
            "provider": result["provider"],
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost_usd": round(result["input_cost_usd"], 8),
            "output_cost_usd": round(result["output_cost_usd"], 8),
            "total_cost_usd": round(result["total_cost_usd"], 8),
            "input_per_mtok_usd": result["input_per_mtok_usd"],
            "output_per_mtok_usd": result["output_per_mtok_usd"],
        }
    except ValueError as e:
        return {"error": str(e)}


@mcp.tool()
def compare_models(model_ids: list[str], input_tokens: int, output_tokens: int) -> dict:
    """Compare the cost of the same workload across multiple models.

    Args:
        model_ids: List of model identifiers to compare (e.g. ['gpt-4o', 'claude-sonnet-4-6']).
        input_tokens: Number of input tokens.
        output_tokens: Number of output tokens.
    """
    results = []
    errors = []
    for model_id in model_ids:
        try:
            r = calculate_cost(model_id, input_tokens, output_tokens)
            results.append({
                "model": r["model"],
                "provider": r["provider"],
                "total_cost_usd": round(r["total_cost_usd"], 8),
                "input_cost_usd": round(r["input_cost_usd"], 8),
                "output_cost_usd": round(r["output_cost_usd"], 8),
            })
        except ValueError as e:
            errors.append({"model": model_id, "error": str(e)})

    results.sort(key=lambda x: x["total_cost_usd"])
    if results:
        cheapest_cost = results[0]["total_cost_usd"]
        for r in results:
            r["ratio_vs_cheapest"] = (
                round(r["total_cost_usd"] / cheapest_cost, 2) if cheapest_cost > 0 else 1.0
            )

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "results": results,
        "errors": errors,
        "cheapest": results[0]["model"] if results else None,
    }


@mcp.tool()
def find_cheapest_models(input_tokens: int, output_tokens: int, limit: int = 5) -> dict:
    """Find the cheapest models for a given token workload.

    Args:
        input_tokens: Number of input tokens.
        output_tokens: Number of output tokens.
        limit: How many results to return (default 5, max 20).
    """
    limit = min(limit, 20)
    costs = []
    for model_id, info in MODELS.items():
        total = (input_tokens / 1_000_000) * info["input_per_mtok"] + \
                (output_tokens / 1_000_000) * info["output_per_mtok"]
        costs.append({
            "model": model_id,
            "provider": info["provider"],
            "total_cost_usd": round(total, 8),
            "input_per_mtok_usd": info["input_per_mtok"],
            "output_per_mtok_usd": info["output_per_mtok"],
            "context_window": info["context_window"],
        })
    costs.sort(key=lambda x: x["total_cost_usd"])
    top = costs[:limit]
    if top:
        cheapest = top[0]["total_cost_usd"]
        for r in top:
            r["ratio_vs_cheapest"] = round(r["total_cost_usd"] / cheapest, 2) if cheapest > 0 else 1.0
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "results": top,
    }


@mcp.tool()
def list_providers() -> dict:
    """List all supported LLM providers with their model counts and cheapest pricing."""
    summary = {}
    for model_id, info in MODELS.items():
        p = info["provider"]
        if p not in summary:
            summary[p] = {
                "provider": p,
                "model_count": 0,
                "cheapest_input_per_mtok": float("inf"),
                "cheapest_output_per_mtok": float("inf"),
                "max_context_window": 0,
            }
        summary[p]["model_count"] += 1
        summary[p]["cheapest_input_per_mtok"] = min(
            summary[p]["cheapest_input_per_mtok"], info["input_per_mtok"]
        )
        summary[p]["cheapest_output_per_mtok"] = min(
            summary[p]["cheapest_output_per_mtok"], info["output_per_mtok"]
        )
        summary[p]["max_context_window"] = max(
            summary[p]["max_context_window"], info["context_window"]
        )
    providers = sorted(summary.values(), key=lambda x: x["cheapest_input_per_mtok"])
    return {"providers": providers, "total_providers": len(providers)}


@mcp.tool()
def search_llm_models(query: str = "", provider: str = "") -> dict:
    """Search for LLM models by name or filter by provider.

    Args:
        query: Partial model name to search for (e.g. 'gpt-4', 'claude', 'llama').
        provider: Filter by provider name (e.g. 'OpenAI', 'Anthropic', 'Google').
    """
    results = search_models(query=query or None, provider=provider or None)
    models = [
        {
            "model": model_id,
            "provider": info["provider"],
            "input_per_mtok_usd": info["input_per_mtok"],
            "output_per_mtok_usd": info["output_per_mtok"],
            "context_window": info["context_window"],
        }
        for model_id, info in results
    ]
    return {"models": models, "count": len(models)}


def main():
    """Entry point for the MCP server (stdio transport)."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
