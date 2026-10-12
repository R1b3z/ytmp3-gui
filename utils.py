# test_utils.py
from utils import is_valid_youtube_url

def test_valid_url():
    assert is_valid_youtube_url("https://www.youtube.com/watch?v=abc123")

def test_invalid_url():
    assert not is_valid_youtube_url("")
    assert not is_valid_youtube_url("https://example.com")
