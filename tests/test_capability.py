from traffic_quality.capability import capability_summary, cp, cpk


def test_cp():
    assert round(cp(10, 0, 1), 2) == 1.67


def test_cpk():
    assert round(cpk(mean=5, usl=10, lsl=0, std_dev=1), 2) == 1.67


def test_capability_summary():
    result = capability_summary(mean=5, usl=10, lsl=0, std_dev=1)
    assert result["is_capable"] is True
