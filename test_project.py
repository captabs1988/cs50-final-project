import pytest
from datetime import datetime, time, timedelta
from project import (
    datetime_add_today,
    user_entry_to_datetime_obj,
    datetime_to_am_pm,
    multiple_timeremapping,
    entrytime_to_2digit,
    final_execution,
    final_execution_wake_up,
    phases
)

def test_datetime_add_today():
    t = time(10, 0)
    dt = datetime_add_today(t)
    assert dt.hour == 10
    assert isinstance(dt, datetime)

@pytest.mark.parametrize("input_str,expected_hour", [
    ("10am", 10),
    ("5:30pm", 17),
    ("1430", 14),
    ("23:45", 23),
])
def test_user_entry_to_datetime_obj_valid(input_str, expected_hour):
    dt = user_entry_to_datetime_obj(input_str)
    assert isinstance(dt, datetime)
    assert dt.hour == expected_hour

@pytest.mark.parametrize("input_str", [
    "25pm", "99:99", "abcd", "7:65am", ""
])
def test_user_entry_to_datetime_obj_invalid(input_str):
    dt = user_entry_to_datetime_obj(input_str)
    assert isinstance(dt, str) and "format" in dt.lower()

def test_datetime_to_am_pm():
    dt = datetime(2023, 1, 1, 14, 30)
    formatted = datetime_to_am_pm(dt)
    assert formatted == "0230 PM"

def test_multiple_timeremapping_output_format():
    start = datetime(2023, 1, 1, 6, 0)
    phase_list = [("test_phase", timedelta(minutes=60))]
    output = multiple_timeremapping(start, phase_list)
    assert "test_phase" in output
    assert "AM" in output or "PM" in output

def test_entrytime_to_2digit():
    dt = datetime(2023, 1, 1, 5, 15)
    assert entrytime_to_2digit(dt) == "05"

def test_final_execution_valid():
    output = final_execution("08", "11")
    assert "Actual Shift" in output
    assert "cooking" in output or "express_WU" in output

def test_final_execution_invalid_shift():
    output = final_execution("99", "11")
    assert "enter valid time" in output.lower()

def test_final_execution_wake_up_valid():
    output = final_execution_wake_up("08")
    assert "cooking" in output or "express_WU" in output

def test_final_execution_wake_up_invalid():
    output = final_execution_wake_up("03")
    assert "specialised schedule" in output.lower()
