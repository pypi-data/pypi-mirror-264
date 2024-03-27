from src.minigame import count
import pytest


@pytest.fixture
def screen_dimensions():
    return 800, 600

def test_generate_objects_count(screen_dimensions):
    screen_width, screen_height = screen_dimensions
    for _ in range(1000):
        circles = count.generate_objects(screen_width, screen_height)
        assert len(circles) >=1, "The generate_objects function creates circles < 1"
        assert len(circles) <=4, "The generate_objects function creates circles > 4"

def test_generate_objects_no_overlap(screen_dimensions):
    screen_width, screen_height = screen_dimensions
    for _ in range(1000):
        circles = count.generate_objects(screen_width, screen_height)
        for i in range(len(circles)):
            for j in range(i + 1, len(circles)):
                dx, dy = circles[i][0] - circles[j][0], circles[i][1] - circles[j][1]
                distance = (dx**2 + dy**2)**0.5
                assert distance >= 60, "Generated circles overlap."

def test_generate_objects_within_boundaries(): #test 100 times
    screen_width, screen_height = 800, 600
    for _ in range(1000):
        circles = count.generate_objects(screen_width, screen_height)
        for circle in circles:
            assert 30 <= circle[0] <= screen_width - 30, "Circle x-coordinate is out of screen boundaries."
            assert 30 <= circle[1] <= screen_height - 30, "Circle y-coordinate is out of screen boundaries."

