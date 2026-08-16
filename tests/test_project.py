from pathlib import Path

def test_foundation_files():
    assert Path('main.py').exists()
    assert Path('buildozer.spec').exists()
