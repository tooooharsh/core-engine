import statistics


def calculate_iqr_rent_range(rents: list[float]) -> dict[str, float]:
    if not rents:
        return {"q1": 0, "median": 0, "q3": 0, "iqr": 0, "recommended_min": 0, "recommended_max": 0}

    sorted_rents = sorted(rents)

    median = statistics.median(sorted_rents)
    q1 = statistics.quantiles(sorted_rents, n=4)[0] if len(sorted_rents) > 1 else sorted_rents[0]
    q3 = statistics.quantiles(sorted_rents, n=4)[2] if len(sorted_rents) > 1 else sorted_rents[0]

    iqr = q3 - q1

    return {
        "q1": q1,
        "median": median,
        "q3": q3,
        "iqr": iqr,
        "recommended_min": q1,
        "recommended_max": q3,
    }
