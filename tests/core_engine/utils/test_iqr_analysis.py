from src.core_engine.utils.iqr_analysis import calculate_iqr_rent_range


def test_iqr_calculation_basic():
    rents = [15000.0, 16000.0, 18000.0, 20000.0, 22000.0, 25000.0, 28000.0]
    result = calculate_iqr_rent_range(rents)

    assert "q1" in result
    assert "median" in result
    assert "q3" in result
    assert "iqr" in result
    assert "recommended_min" in result
    assert "recommended_max" in result

    assert result["q1"] == 16000
    assert result["median"] == 20000
    assert result["q3"] == 25000
    assert result["iqr"] == 9000


def test_iqr_with_outliers():
    rents = [15000.0, 16000.0, 18000.0, 20000.0, 22000.0, 25000.0, 50000.0]
    result = calculate_iqr_rent_range(rents)

    assert result["median"] == 20000
    assert result["q1"] < result["median"]
    assert result["q3"] > result["median"]


def test_iqr_with_single_value():
    rents = [20000.0]
    result = calculate_iqr_rent_range(rents)

    assert result["q1"] == 20000
    assert result["median"] == 20000
    assert result["q3"] == 20000
    assert result["iqr"] == 0


def test_iqr_with_empty_list():
    rents: list[float] = []
    result = calculate_iqr_rent_range(rents)

    assert result["q1"] == 0
    assert result["median"] == 0
    assert result["q3"] == 0
    assert result["iqr"] == 0
    assert result["recommended_min"] == 0
    assert result["recommended_max"] == 0


def test_iqr_with_two_values():
    rents = [15000.0, 25000.0]
    result = calculate_iqr_rent_range(rents)

    assert result["median"] == 20000
    assert result["q1"] == 12500.0
    assert result["q3"] == 27500.0


def test_iqr_recommended_range():
    rents = [10000.0, 15000.0, 18000.0, 20000.0, 22000.0, 25000.0, 30000.0]
    result = calculate_iqr_rent_range(rents)

    assert result["recommended_min"] == result["q1"]
    assert result["recommended_max"] == result["q3"]


def test_iqr_with_identical_values():
    rents = [20000.0, 20000.0, 20000.0, 20000.0]
    result = calculate_iqr_rent_range(rents)

    assert result["q1"] == 20000
    assert result["median"] == 20000
    assert result["q3"] == 20000
    assert result["iqr"] == 0
