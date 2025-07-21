import re
from datetime import datetime, timedelta
import tkinter as ab
from tkinter import ttk, PhotoImage
from PIL import Image, ImageTk

# Global dictionaries and constants (original class attributes)
pre_shift_schedules = {
    "07": ("04:40", [2, 3]),
    "08": ("05:40", [2, 3]),
    "09": ("06:40", [2, 3]),
    "10": ("07:40", [2, 3]),
    "11": ("08:00", [2, 10, 21]),
    "12": ("08:00", [2, 8, 5, 21]),
    "13": ("08:00", [2, 8, 19, 5, 21]),
    "14": ("08:00", [2, 8, 19, 5, 10, 21]),
    "15": ("08:00", [2, 8, 15, 13, 16, 21]),
    "16": ("08:00", [2, 8, 16, 9, 13, 21]),
    "17": ("08:00", [2, 8, 15, 9, 13, 10, 21]),
    "18": ("09:00", [2, 8, 16, 9, 13, 10, 3]),
    "19": ("11:00", [2, 8, 16, 9, 13, 21]),
    "20": ("13:00", [2, 8, 16, 13, 20, 21]),
    "21": ("14:00", [2, 8, 16, 13, 20, 21]),
    "22": ("14:00", [2, 8, 16, 13, 10, 20, 3]),
    "00": ("08:00", [2, 8, 16, 9, 5, 0, 10, 16, 11, 7, 0, 13, 6, 17, 18]),
}

post_shift_schedules = {
    "11": [3, 5, 8, 16, 9, 7, 13, 10, 16, 11, 5, 17, 18],
    "12": [3, 5, 8, 16, 9, 7, 13, 10, 6, 17, 18],
    "13": [3, 5, 8, 7, 10, 13, 10, 6, 17, 18],
    "14": [3, 5, 8, 7, 10, 13, 6, 17, 18],
    "15": [3, 14, 8, 15, 13, 6, 17, 18],
    "16": [3, 14, 8, 13, 6, 17, 18],
    "17": [3, 14, 13, 6, 17, 18],
    "18": [3, 14, 19, 6, 17, 18],
    "19": [3, 19, 6, 17, 18],
    "20": [3, 19, 6, 18],
    "21": [3, 6, 18],
    "22": [3, 6, 18],
    "23": [3, 6, 18],
    "00": [3, 18],
    "01": [3, 18],
    "02": [3, 18],
    "03": [3, 18],
    "04": [3, 18],
    "05": [3, 18],
    "06": [3, 18],
    "07": [3, 18],
}

wakeup_time = {
    "08": [2, 8, 15, 9, 0, 5, 10, 15, 11, 13, 7, 0, 13, 6, 17, 18],
    "09": [2, 8, 15, 9, 0, 5, 10, 15, 13, 7, 0, 13, 6, 17, 18],
    "10": [2, 8, 16, 9, 0, 5, 13, 7, 12, 16, 10, 6, 17, 18],
    "11": [2, 8, 16, 9, 0, 5, 13, 7, 10, 16, 11, 6, 17, 18],
    "12": [2, 8, 16, 9, 5, 13, 7, 10, 16, 11, 6, 17, 18],
    "13": [2, 8, 16, 9, 5, 13, 7, 10, 6, 17, 18],
    "14": [2, 8, 16, 9, 5, 13, 6, 17, 18],
    "15": [2, 8, 16, 9, 5, 13, 6, 10, 16, 18],
    "16": [2, 8, 16, 9, 5, 19, 6, 10, 16, 18],
    "17": [2, 8, 16, 9, 5, 19, 6, 10, 16, 18],
    "18": [2, 8, 16, 9, 5, 19, 6, 10, 16, 18],
}

phases = [
    ("cooking", timedelta(minutes=40)),
    ("express_WU", timedelta(minutes=25)),
    ("sorted_WU", timedelta(minutes=50)),
    ("the_tfl", timedelta(minutes=90)),
    ("breakfast", timedelta(minutes=25)),
    ("lunch", timedelta(minutes=20)),
    ("dinner", timedelta(minutes=20)),
    ("tea_snack", timedelta(minutes=30)),
    ("primary", timedelta(minutes=90)),
    ("primary2", timedelta(minutes=90)),
    ("secondary1", timedelta(minutes=45)),
    ("secondary2", timedelta(minutes=45)),
    ("coding", timedelta(minutes=120)),
    ("run_gym", timedelta(minutes=150)),
    ("post_shift", timedelta(minutes=20)),
    ("break30", timedelta(minutes=30)),
    ("break20", timedelta(minutes=20)),
    ("reading", timedelta(minutes=60)),
    ("sleep", timedelta(minutes=10)),
    ("run_gym_short", timedelta(minutes=80)),
    ("pre_night_shift_ritual", timedelta(minutes=30)),
    ("express_tfl", timedelta(minutes=70)),
]

# Functions (converted from methods)
# Helper functions
def datetime_add_today(datetime_obj):
    # Add today's date to datetime object
    a = datetime.today()
    b = datetime.combine(a.date(), datetime_obj)
    return b

def user_entry_to_datetime_obj(x):
    pattern_24 = r"^(?:[01]?[0-9]|2[0-3])(?::?[0-5][0-9])?$"
    pattern_ampm = r"^(?:0?[1-9]|1[0-2])(?::?[0-5][0-9])?(am|pm)$"
    if re.search(pattern_ampm, x):
        try:
            if len(x) <= 4:
                return datetime_add_today(datetime.strptime(x, "%I%p").time())
            elif len(x) == 6:
                return datetime_add_today(datetime.strptime(x, "%I%M%p").time())
            elif len(x) <= 7:
                return datetime_add_today(datetime.strptime(x, "%I:%M%p").time())
        except ValueError:
            return "Invalid format"
    elif re.match(pattern_24, x):
        try:
            if len(x) in {1, 2}:
                return datetime_add_today(datetime.strptime(x.zfill(2), "%H").time())
            elif len(x) == 4:
                return datetime_add_today(datetime.strptime(x, "%H%M").time())
            elif len(x) == 5:
                return datetime_add_today(datetime.strptime(x, "%H:%M").time())
        except ValueError:
            return "Invalid format"
    return "Please enter correct time format"

def datetime_to_am_pm(dt):
    return dt.strftime("%I%M %p")

def multiple_timeremapping(start_time, phase_list):
    result = ""
    for name, duration in phase_list:
        end_time = start_time + duration
        result += f"{name}: {datetime_to_am_pm(start_time)} - {datetime_to_am_pm(end_time)}.\n\n"
        start_time = end_time
    return result

def entrytime_to_2digit(dt):
    return dt.strftime("%H")

def final_execution(shift_start, shift_end):
    result = ""
    if shift_start in pre_shift_schedules:
        wake_str, sched = pre_shift_schedules[shift_start]
        wake_time = datetime_add_today(datetime.strptime(wake_str, "%H:%M").time())
        result += multiple_timeremapping(wake_time, [phases[i] for i in sched])
    else:
        result += "enter valid time in hh:mm format.\n"
    try:
        s, e = datetime.strptime(shift_start, "%H"), datetime.strptime(shift_end, "%H")
        result += f"\nActual Shift {datetime_to_am_pm(s)} - {datetime_to_am_pm(e)}\n\n"
    except ValueError:
        result += "\nActual Shift: Invalid format\n\n"
    if shift_end in post_shift_schedules:
        end_time = datetime_add_today(datetime.strptime(shift_end, "%H").time())
        result += multiple_timeremapping(end_time, [phases[i] for i in post_shift_schedules[shift_end]])
    else:
        result += "enter valid time in hh:mm format\n"
    return result

def final_execution_wake_up(wakeup_hour):
    if wakeup_hour in wakeup_time:
        start_time = datetime_add_today(datetime.strptime(wakeup_hour, "%H").time())
        return multiple_timeremapping(start_time, [phases[i] for i in wakeup_time[wakeup_hour]])
    return ("Specialised schedule required. Avoid waking up at these hours. Don't feel guilty. "
            "Use the 4-7-8 breathing technique to relax.\n")

# GUI
root = ab.Tk()
root.title("The Synapto")
root.geometry("700x500")
main_frame = ab.Frame(root)
main_frame.pack(fill="both", expand=True)

left_frame = ab.Frame(main_frame)
left_frame.pack(side="left", fill="y", padx=10, pady=10)
ab.Frame(main_frame, width=2, bg="grey").pack(side="left", fill="y", padx=2)

resized_image = Image.open("logo.png").resize((240, 60), Image.LANCZOS)
logo_image = ImageTk.PhotoImage(resized_image)
ttk.Label(left_frame, image=logo_image).pack(pady=10)

shift_start_time = ttk.Entry(left_frame, width=5)
shift_end_time = ttk.Entry(left_frame, width=5)
wake_up_time = ttk.Entry(left_frame, width=5)

ttk.Label(left_frame, text="Enter Shift Start Time:").pack(pady=10)
shift_start_time.pack(pady=5)
ttk.Label(left_frame, text="Enter Shift End Time:").pack(pady=5)
shift_end_time.pack(pady=5)
ttk.Label(left_frame, text="I woke up at...:").pack(pady=10)
wake_up_time.pack(pady=5)

def button_click():
    start = shift_start_time.get().strip()
    end = shift_end_time.get().strip()
    woke_up = wake_up_time.get().strip()
    if woke_up and (start or end) or (not woke_up and (not start or not end)):
        output_text.delete(1.0, ab.END)
        output_text.insert(ab.END, " Enter Wake Up Time OR Shift Start & End Time")
        return
    if woke_up:
        dt = user_entry_to_datetime_obj(woke_up)
        if isinstance(dt, str):
            output_text.delete(1.0, ab.END)
            output_text.insert(ab.END, dt)
            return
        result = final_execution_wake_up(entrytime_to_2digit(dt))
    else:
        s_dt = user_entry_to_datetime_obj(start)
        e_dt = user_entry_to_datetime_obj(end)
        if isinstance(s_dt, str) or isinstance(e_dt, str):
            output_text.delete(1.0, ab.END)
            output_text.insert(ab.END, " Invalid shift time format")
            return
        result = final_execution(entrytime_to_2digit(s_dt), entrytime_to_2digit(e_dt))
    output_text.config(state="normal")
    output_text.delete(1.0, ab.END)
    output_text.insert(ab.END, result)
    output_text.config(state="disabled")

ttk.Button(left_frame, text="Generate Schedule", command=button_click).pack(pady=20)

output_frame = ab.Frame(main_frame)
output_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
scrollbar = ab.Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")
output_text = ab.Text(output_frame, height=15, wrap="word", yscrollcommand=scrollbar.set)
output_text.pack(side="left", fill="both", expand=True)
scrollbar.config(command=output_text.yview)

root.mainloop()
