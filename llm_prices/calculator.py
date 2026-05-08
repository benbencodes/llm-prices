from .data import MODELS


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> dict:
    """Return cost breakdown for a given model and token counts."""
    key = model.lower()
    if key not in MODELS:
        # Normalize hyphens/underscores/spaces then try substring match
        def normalize(s):
            return s.replace("-", "").replace("_", "").replace(" ", "")

        nkey = normalize(key)
        matches = [m for m in MODELS if nkey in normalize(m) or normalize(m) in nkey]
        if len(matches) == 1:
            key = matches[0]
        elif len(matches) > 1:
            raise ValueError(
                f"Ambiguous model '{model}'. Did you mean one of: {', '.join(matches)}?"
            )
        else:
            raise ValueError(
                f"Unknown model '{model}'. Run `llm-prices list` to see available models."
            )

    info = MODELS[key]
    input_cost = (input_tokens / 1_000_000) * info["input_per_mtok"]
    output_cost = (output_tokens / 1_000_000) * info["output_per_mtok"]
    total_cost = input_cost + output_cost

    return {
        "model": key,
        "provider": info["provider"],
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost_usd": round(input_cost, 8),
        "output_cost_usd": round(output_cost, 8),
        "total_cost_usd": round(total_cost, 8),
        "input_per_mtok": info["input_per_mtok"],
        "output_per_mtok": info["output_per_mtok"],
    }


def format_usd(value: float) -> str:
    if value == 0:
        return "$0.000000"
    if value < 0.000001:
        return f"${value:.2e}"
    if value < 0.01:
        return f"${value:.6f}"
    if value < 1:
        return f"${value:.4f}"
    return f"${value:.4f}"


def search_models(query: str = "", provider: str = "") -> list:
    results = []
    q = query.lower()
    p = provider.lower()
    for name, info in MODELS.items():
        if q and q not in name.lower() and q not in info["provider"].lower():
            continue
        if p and p not in info["provider"].lower():
            continue
        results.append((name, info))
    return results
