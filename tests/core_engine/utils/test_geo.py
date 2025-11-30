from src.core_engine.utils.geo import calculate_distance_km


def test_calculate_distance_same_point():
    distance = calculate_distance_km(0.0, 0.0, 0.0, 0.0)
    assert distance == 0.0


def test_calculate_distance_known_points():
    distance = calculate_distance_km(0.0, 0.0, 0.01, 0.01)
    assert 1.5 < distance < 1.6


def test_calculate_distance_negative_coordinates():
    distance1 = calculate_distance_km(0.0, 0.0, 0.01, 0.01)
    distance2 = calculate_distance_km(0.0, 0.0, -0.01, -0.01)
    assert abs(distance1 - distance2) < 0.0001


def test_calculate_distance_real_world():
    # New York (approx)
    ny_lat, ny_lon = 40.7128, -74.0060
    # London (approx)
    london_lat, london_lon = 51.5074, -0.1278

    distance = calculate_distance_km(ny_lat, ny_lon, london_lat, london_lon)
    # Approximate distance between NY and London is 5570km
    assert 5500 < distance < 5600
