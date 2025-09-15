import tkinter as tk
from datetime import datetime


class TimerApp:
    def __init__(self, root):
        self.root = root
        root.title("Timer")
        root.attributes("-topmost", True)
        root.geometry("220x180")

        self.total_seconds = 0
        self.running = False

        # Real-time clock display
        self.clock_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.clock_label.pack(pady=5)
        self.update_clock()  # start updating the clock

        # Inputs
        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(pady=5)

        tk.Label(self.entry_frame, text="Min:").grid(row=0, column=0)
        self.minute_entry = tk.Entry(self.entry_frame, width=4, justify="center")
        self.minute_entry.grid(row=0, column=1)

        tk.Label(self.entry_frame, text="Sec:").grid(row=0, column=2)
        self.second_entry = tk.Entry(self.entry_frame, width=4, justify="center")
        self.second_entry.grid(row=0, column=3)

        # Timer display
        self.timer_label = tk.Label(root, text="00:00", font=("Helvetica", 30))
        self.timer_label.pack(expand=True)

        # Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = tk.Button(self.button_frame, text="Pause", command=self.toggle_pause)
        self.pause_button.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_timer)
        self.reset_button.grid(row=0, column=2, padx=5)

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)  # update every second

    def start_timer(self):
        # Start fresh
        try:
            minutes = int(self.minute_entry.get() or 0)
            seconds = int(self.second_entry.get() or 0)
            new_total = minutes * 60 + seconds
            if new_total <= 0:
                self.timer_label.config(text="Invalid!")
                return
            self.total_seconds = new_total
            self.running = True
            self.pause_button.config(text="Pause")  # reset label
            self.countdown()
        except ValueError:
            self.timer_label.config(text="Invalid!")

    def toggle_pause(self):
        if self.running:
            # Pause the timer
            self.running = False
            self.pause_button.config(text="Resume")
        else:
            # Resume the timer
            if self.total_seconds > 0:
                self.running = True
                self.pause_button.config(text="Pause")
                self.countdown()

    def reset_timer(self):
        self.running = False
        self.total_seconds = 0
        self.timer_label.config(text="00:00")
        self.pause_button.config(text="Pause")  # reset label

    def countdown(self):
        if self.running and self.total_seconds >= 0:
            mins, secs = divmod(self.total_seconds, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            self.total_seconds -= 1
            self.root.after(1000, self.countdown)
        elif self.total_seconds < 0:
            self.timer_label.config(text="Time's up!")
            self.running = False
            self.pause_button.config(text="Pause")  # reset button


root = tk.Tk()
app = TimerApp(root)
root.mainloop()
