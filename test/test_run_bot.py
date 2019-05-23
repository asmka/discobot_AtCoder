import pytest
import run_bot as rb

def test_convert_week_knj():
    assert rb.convert_week_knj(0) == '月'
    assert rb.convert_week_knj(1) == '火'
    assert rb.convert_week_knj(2) == '水'
    assert rb.convert_week_knj(3) == '木'
    assert rb.convert_week_knj(4) == '金'
    assert rb.convert_week_knj(5) == '土'
    assert rb.convert_week_knj(6) == '日'
    with pytest.raises(ValueError, match=r"\[ERROR\] week_id is invalid: -1"):
        rb.convert_week_knj(-1)
    with pytest.raises(ValueError, match=r"\[ERROR\] week_id is invalid: 7"):
        rb.convert_week_knj(7)
