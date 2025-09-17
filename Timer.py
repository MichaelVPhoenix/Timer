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
        self.countdown_job = None  # Track the scheduled countdown callback

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

        # Add Time button (separate row)
        self.add_time_frame = tk.Frame(root)
        self.add_time_frame.pack(pady=2)

        self.add_time_button = tk.Button(self.add_time_frame, text="+1 Min", command=self.add_minute)
        self.add_time_button.grid(row=0, column=0, padx=2)

        self.add_30s_button = tk.Button(self.add_time_frame, text="+30s", command=self.add_30_seconds)
        self.add_30s_button.grid(row=0, column=1, padx=2)

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)  # update every second

    def start_timer(self):
        # Cancel any existing countdown first
        self.cancel_countdown()

        # Check if input fields have values - they take priority
        try:
            minutes_input = self.minute_entry.get().strip()
            seconds_input = self.second_entry.get().strip()

            # If either field has content, use input fields (higher priority)
            if minutes_input or seconds_input:
                minutes = int(minutes_input or 0)
                seconds = int(seconds_input or 0)
                new_total = minutes * 60 + seconds
                if new_total <= 0:
                    self.timer_label.config(text="Invalid!")
                    return
                self.total_seconds = new_total
            # Otherwise, if we have time from add buttons, use that
            elif self.total_seconds <= 0:
                self.timer_label.config(text="Invalid!")
                return

        except ValueError:
            self.timer_label.config(text="Invalid!")
            return

        # Start the timer
        self.running = True
        self.pause_button.config(text="Pause")
        self.countdown()

    def toggle_pause(self):
        if self.running:
            # Pause the timer
            self.running = False
            self.cancel_countdown()  # Cancel the scheduled callback
            self.pause_button.config(text="Resume")
        else:
            # Resume the timer
            if self.total_seconds > 0:
                self.running = True
                self.pause_button.config(text="Pause")
                self.countdown()

    def reset_timer(self):
        self.running = False
        self.cancel_countdown()  # Cancel any scheduled callback
        self.total_seconds = 0
        self.timer_label.config(text="00:00")
        self.pause_button.config(text="Pause")  # reset label

    def cancel_countdown(self):
        """Cancel any scheduled countdown callback"""
        if self.countdown_job is not None:
            self.root.after_cancel(self.countdown_job)
            self.countdown_job = None

    def add_minute(self):
        """Add 1 minute to the current timer"""
        # If timer is finished (negative or "Time's up!"), start fresh
        if self.total_seconds < 0:
            self.total_seconds = 60
            self.running = False  # Don't auto-start, wait for Start button
        else:
            self.total_seconds += 60

        # Update display immediately
        mins, secs = divmod(self.total_seconds, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

    def add_30_seconds(self):
        """Add 30 seconds to the current timer"""
        # If timer is finished (negative or "Time's up!"), start fresh
        if self.total_seconds < 0:
            self.total_seconds = 30
            self.running = False  # Don't auto-start, wait for Start button
        else:
            self.total_seconds += 30

        # Update display immediately
        mins, secs = divmod(self.total_seconds, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

    def countdown(self):
        if self.running and self.total_seconds > 0:  # Fixed condition
            mins, secs = divmod(self.total_seconds, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            self.total_seconds -= 1
            # Store the job ID so we can cancel it later
            self.countdown_job = self.root.after(1000, self.countdown)
        elif self.running and self.total_seconds <= 0:  # Timer finished
            self.timer_label.config(text="Time's up!")
            self.running = False
            self.countdown_job = None
            self.pause_button.config(text="Pause")


root = tk.Tk()
app = TimerApp(root)
root.mainloop()
