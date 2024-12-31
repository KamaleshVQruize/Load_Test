import requests
import time
import tkinter as tk
from tkinter import messagebox, ttk
from threading import Thread
from tkinter import PhotoImage  # For displaying images (logo)

class HTTPRequestSender:
    def __init__(self, root):
        self.root = root
        self.url = ""
        self.total_time = 0
        self.num_requests = 0
        self.interval_unit = "sec"
        self.success_count = 0
        self.failure_count = 0
        self.is_running = False

        # Set up UI components
        self.setup_ui()

    def setup_ui(self):
        """Setup all the UI components for the window"""
        self.root.title("HTTP Request Sender")
        self.root.state('zoomed')  # Maximizing the window
        self.root.geometry("1000x800")
        self.root.config(bg="white")

        # Create a frame to hold the entire layout
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(expand=True, fill="both", padx=40, pady=40)  # Fill the space

        # Create a grid layout with two columns (one for the left side, one for the right side)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=2)

        # Adding a Logo at the top (ensure you have the 'logo.png' file in your project directory)
        self.logo = PhotoImage(file="qruize-logo.png")  # Replace with your logo file path
        self.logo_label = tk.Label(self.main_frame, image=self.logo, bg="white")
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Left side: Input Fields and Buttons
        self.create_input_fields()

        # Right side: Request Log Box
        self.create_log_box()

    def create_input_fields(self):
        """Creates all input fields and buttons on the left side of the layout"""
        # URL Entry
        url_label = tk.Label(self.main_frame, text="URL:", bg="white", font=("Arial", 12, 'bold'), fg="#333")
        url_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.url_entry = tk.Entry(self.main_frame, font=("Arial", 12), width=40, bd=2, relief="solid")
        self.url_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Total Time Entry
        total_time_label = tk.Label(self.main_frame, text="Total Time (sec):", bg="white", font=("Arial", 12, 'bold'), fg="#333")
        total_time_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.total_time_entry = tk.Entry(self.main_frame, font=("Arial", 12), width=40, bd=2, relief="solid")
        self.total_time_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Number of Requests Entry
        num_requests_label = tk.Label(self.main_frame, text="Number of Requests:", bg="white", font=("Arial", 12, 'bold'), fg="#333")
        num_requests_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.num_requests_entry = tk.Entry(self.main_frame, font=("Arial", 12), width=40, bd=2, relief="solid")
        self.num_requests_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Interval Unit OptionMenu
        interval_unit_label = tk.Label(self.main_frame, text="Interval Unit:", bg="white", font=("Arial", 12, 'bold'), fg="#333")
        interval_unit_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.interval_unit_var = tk.StringVar(value="sec")
        interval_unit_menu = tk.OptionMenu(self.main_frame, self.interval_unit_var, "sec", "min")
        interval_unit_menu.config(font=("Arial", 12))
        interval_unit_menu.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Send and Stop Buttons
        self.send_button = tk.Button(self.main_frame, text="Send Requests", font=("Arial", 12), command=self.send_requests_gui, relief="raised", bg="#4CAF50", fg="white", bd=3)
        self.send_button.grid(row=5, column=0, columnspan=2, pady=20, padx=10, sticky="ew")

        self.stop_button = tk.Button(self.main_frame, text="Stop", font=("Arial", 12), state=tk.DISABLED, command=self.stop_requests, relief="raised", bg="#f44336", fg="white", bd=3)
        self.stop_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    def create_log_box(self):
        """Creates the log box on the right side of the layout"""
        # Status Log Area (Text box)
        self.status_log = tk.Text(self.main_frame, height=20, width=60, font=("Arial", 10), bd=2, relief="solid", wrap=tk.WORD)
        self.status_log.grid(row=1, column=2, rowspan=6, padx=10, pady=10, sticky="nsew")

        # Theme Toggle
        theme_var = tk.StringVar(value="Light")
        theme_toggle = ttk.Combobox(self.main_frame, textvariable=theme_var, values=["Light", "Dark"], font=("Arial", 12), state="readonly")
        theme_toggle.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        theme_toggle.bind("<<ComboboxSelected>>", lambda e: self.toggle_theme(theme_var))

    def toggle_theme(self, theme_var):
        """Toggles between light and dark themes"""
        theme = theme_var.get()
        
        # Theme colors for Light and Dark
        if theme == "Dark":
            bg_color = "#2e2e2e"
            fg_color = "white"
            button_bg = "#444"
            button_fg = "white"
            entry_bg = "#555"
            entry_fg = "white"
            label_fg = "#ddd"
        else:
            bg_color = "white"
            fg_color = "black"
            button_bg = "#4CAF50"
            button_fg = "white"
            entry_bg = "white"
            entry_fg = "black"
            label_fg = "#333"
        
        # Apply theme to window
        self.root.config(bg=bg_color)
        
        # Apply theme to widgets
        self.main_frame.config(bg=bg_color)

        for widget in self.main_frame.winfo_children():
            if isinstance(widget, tk.Widget):
                try:
                    widget.config(bg=bg_color, foreground=fg_color, bd=2)
                except tk.TclError:
                    pass
                
        self.send_button.config(bg=button_bg, fg=button_fg)
        self.stop_button.config(bg="#f44336", fg=button_fg)
        self.url_entry.config(bg=entry_bg, fg=entry_fg)
        self.total_time_entry.config(bg=entry_bg, fg=entry_fg)
        self.num_requests_entry.config(bg=entry_bg, fg=entry_fg)

        for label in self.main_frame.winfo_children():
            if isinstance(label, tk.Label):
                label.config(foreground=label_fg)

    def send_requests_gui(self):
        """Handles the button press event to start sending requests"""
        self.url = self.url_entry.get().strip()
        self.total_time = self.total_time_entry.get().strip()
        self.num_requests = self.num_requests_entry.get().strip()
        self.interval_unit = self.interval_unit_var.get()

        # Input validation
        if not self.url or not self.total_time.isdigit() or not self.num_requests.isdigit():
            self.status_log.insert(tk.END, "Invalid inputs. Please check all fields.\n")
            return

        self.total_time = int(self.total_time)
        self.num_requests = int(self.num_requests)

        # Disable the send button to avoid multiple clicks
        self.send_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Start the request process in a background thread
        self.is_running = True
        self.success_count = 0
        self.failure_count = 0
        thread = Thread(target=self.send_requests)
        thread.start()

    def send_requests(self):
        """Sends HTTP requests to the specified URL within the given total time"""
        if self.interval_unit == 'min':
            self.total_time *= 60  # Convert to seconds
        interval = self.total_time / self.num_requests

        for _ in range(self.num_requests):
            if not self.is_running:
                break
            try:
                response = requests.get(self.url)
                if response.status_code == 200:
                    self.success_count += 1
                else:
                    self.failure_count += 1
            except Exception as e:
                self.failure_count += 1

            self.status_log.insert(tk.END, f"Request {_+1}: Success - {self.success_count}, Failure - {self.failure_count}\n")
            self.status_log.yview(tk.END)
            time.sleep(interval)

        self.status_log.insert(tk.END, f"Total Success: {self.success_count}, Total Failure: {self.failure_count}\n")

    def stop_requests(self):
        """Stops the request sending process"""
        self.is_running = False
        self.send_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_log.insert(tk.END, "Requests stopped.\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = HTTPRequestSender(root)
    root.mainloop()
