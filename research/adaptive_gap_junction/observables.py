from __future__ import annotations


def final_abs_mean_voltage(voltages: list[float]) -> float:
    return abs(sum(voltages) / len(voltages))


def consensus_fraction(voltages: list[float]) -> float:
    positive = sum(1 for value in voltages if value >= 0.0)
    negative = len(voltages) - positive
    return max(positive, negative) / len(voltages)
