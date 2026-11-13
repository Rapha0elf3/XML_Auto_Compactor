
import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

from settings import SettingsWindow
import processor


CONFIG_FILE = Path(__file__).resolve().parent / "config.json"


class XmlCompactor:

    def __init__(self, root):
        self.root = root

        self.root.title("XML Auto Compactor")
        screen_width = self.root.winfo_screenwidth()

        x = screen_width - 380 - 100
        y = 100

        self.root.geometry(f"380x180+{x}+{y}")
        self.root.resizable(False, False)

        self.config = self.load_config()

        self.settings_window = None

        self.create_interface()

    def load_config(self):

        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r") as file:
                    return json.load(file)

            except (json.JSONDecodeError, OSError):
                messagebox.showwarning(
                    "Configuration",
                    "Could not read config.json. Default settings will be used."
                )

        return {
            "storage_path": "",
            "working_path": "",
            "sender_email": "",
            "receiver_email": ""
        }

    def save_config(self, config):

        try:
            with open(CONFIG_FILE, "w") as file:
                json.dump(config, file, indent=4)

            self.config = config

        except OSError as error:
            messagebox.showerror(
                "Error",
                f"Could not save configurations:\n{error}"
            )

    def create_interface(self):

        # Application title
        title_label = tk.Label(
            self.root,
            text="XML AUTO COMPACTOR",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(25, 15))

        # Button container
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)

        # Configurations button
        config_button = tk.Button(
            button_frame,
            text="CONFIG",
            font=("Arial", 12, "bold"),
            width=8,
            height=2,
            cursor="hand2",
            command=self.open_settings
        )
        config_button.grid(row=0, column=0, padx=5)

        # Start button
        self.start_button = tk.Button(
            button_frame,
            text="START",
            font=("Arial", 12, "bold"),
            width=18,
            height=2,
            cursor="hand2",
            command=self.start_process
        )
        self.start_button.grid(row=0, column=1, padx=5)

    def open_settings(self):

        if self.settings_window is not None:
            if self.settings_window.window.winfo_exists():
                self.settings_window.window.lift()
                return

        self.settings_window = SettingsWindow(
            self.root,
            self.config,
            self.save_config
        )

    def start_process(self):

        if not self.config.get("storage_path"):
            messagebox.showerror(
                "Error",
                "Please configure the Storage Folder."
            )
            return

        if not self.config.get("working_path"):
            messagebox.showerror(
                "Error",
                "Please configure the Working Folder."
            )
            return

        # Create the message window
        log_window = tk.Toplevel(self.root)
        log_window.title("XML Auto Compactor - Progress")
        self.root.update_idletasks()

        x = self.root.winfo_x()
        y = self.root.winfo_y() + self.root.winfo_height() + 10

        log_window.geometry(f"370x100+{x}+{y}")
        log_window.resizable(False, False)

        # Message area
        log_widget = tk.Text(
            log_window,
            width=50,
            height=15,
            state="normal"
        )
        log_widget.pack(padx=10, pady=10, fill="both", expand=True)

        # Logging function
        def log(message):
            log_widget.insert("end", message + "\n")
            log_widget.see("end")
            log_window.update_idletasks()

        # Start processing
        processor.process_file(self.config, log)

if __name__ == "__main__":

    root = tk.Tk()

    app = XmlCompactor(root)

    root.mainloop()
