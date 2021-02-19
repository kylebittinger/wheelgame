from .wheel import (
    Wheel
)

def test_spin_step():
    w = Wheel("ABCD")
    vals = w._spin_step(3.1)
    assert(list(vals) == ["A", "B", "C"])
    assert(w.fortune == "D")

def test_spin_step_beyond():
    w = Wheel("ABCD")
    vals = w._spin_step(4.1)
    assert(list(vals) == ["A", "B", "C", "D"])
    assert(w.fortune == "A")

def test_spin_step_waybeyond():
    w = Wheel("ABCD")
    vals = w._spin_step(9.1)
    expected = [
        "A", "B", "C", "D",
        "A", "B", "C", "D", "A"
    ]
    assert(list(vals) == expected)
    assert(w.fortune == "B")

