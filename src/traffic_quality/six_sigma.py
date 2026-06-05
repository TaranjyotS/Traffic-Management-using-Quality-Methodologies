from __future__ import annotations

from statistics import NormalDist


def dpmo(defects: float, units: float, opportunities_per_unit: float = 1) -> float:
    """Calculate Defects Per Million Opportunities."""
    if units <= 0:
        raise ValueError("units must be greater than zero")
    if opportunities_per_unit <= 0:
        raise ValueError("opportunities_per_unit must be greater than zero")
    if defects < 0:
        raise ValueError("defects cannot be negative")
    return defects / (units * opportunities_per_unit) * 1_000_000


def yield_from_dpmo(dpmo_value: float) -> float:
    """Return process yield from DPMO as a value between 0 and 1."""
    if not 0 <= dpmo_value <= 1_000_000:
        raise ValueError("dpmo must be between 0 and 1,000,000")
    return 1 - (dpmo_value / 1_000_000)


def sigma_level(dpmo_value: float, long_term_shift: float = 1.5) -> float:
    """Estimate sigma level using the conventional 1.5 sigma long-term shift."""
    process_yield = yield_from_dpmo(dpmo_value)
    # Clamp to avoid infinite z-scores for perfect/impossible yields.
    process_yield = min(max(process_yield, 1e-12), 1 - 1e-12)
    return NormalDist().inv_cdf(process_yield) + long_term_shift


def summarize_process(defects: float, units: float, opportunities_per_unit: float = 1) -> dict[str, float]:
    """Return DPMO, yield, and sigma level for a process."""
    dpmo_value = dpmo(defects, units, opportunities_per_unit)
    return {
        "defects": float(defects),
        "units": float(units),
        "dpmo": round(dpmo_value, 2),
        "yield_percent": round(yield_from_dpmo(dpmo_value) * 100, 2),
        "sigma_level": round(sigma_level(dpmo_value), 2),
    }
