from __future__ import annotations


def cp(usl: float, lsl: float, std_dev: float) -> float:
    """Calculate process capability Cp."""
    if std_dev <= 0:
        raise ValueError("standard deviation must be greater than zero")
    if usl <= lsl:
        raise ValueError("USL must be greater than LSL")
    return (usl - lsl) / (6 * std_dev)


def cpk(mean: float, usl: float, lsl: float, std_dev: float) -> float:
    """Calculate process capability Cpk."""
    if std_dev <= 0:
        raise ValueError("standard deviation must be greater than zero")
    return min((usl - mean) / (3 * std_dev), (mean - lsl) / (3 * std_dev))


def capability_summary(mean: float, usl: float, lsl: float, std_dev: float) -> dict[str, float]:
    """Return Cp/Cpk and a simple capability interpretation."""
    cp_value = cp(usl, lsl, std_dev)
    cpk_value = cpk(mean, usl, lsl, std_dev)
    return {
        "cp": round(cp_value, 4),
        "cpk": round(cpk_value, 4),
        "is_capable": cpk_value >= 1.33,
    }
