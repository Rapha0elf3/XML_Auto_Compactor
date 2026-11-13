import tkinter as tk
from tkinter import filedialog, messagebox


class SettingsWindow:

    def __init__(self, parent, config, save_callback):
        self.config = config
        self.save_callback = save_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Configurations")
        self.window.geometry("500x350")
        self.window.resizable(False, False)

        self.window.transient(parent)
        self.window.grab_set()

        self.create_interface()

    def create_interface(self):

        # Main container
        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Storage folder
        tk.Label(
            frame,
            text="Storage Folder",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.storage_entry = tk.Entry(frame, width=43)
        self.storage_entry.grid(row=1, column=0, padx=(0, 8))

        self.storage_entry.insert(
            0, self.config.get("storage_path", "")
        )

        tk.Button(
            frame,
            text="Browse",
            command=self.select_storage
        ).grid(row=1, column=1)

        # Working folder
        tk.Label(
            frame,
            text="Working Folder",
            font=("Arial", 10, "bold")
        ).grid(row=2, column=0, sticky="w", pady=(15, 5))

        self.working_entry = tk.Entry(frame, width=43)
        self.working_entry.grid(row=3, column=0, padx=(0, 8))

        self.working_entry.insert(
            0, self.config.get("working_path", "")
        )

        tk.Button(
            frame,
            text="Browse",
            command=self.select_working
        ).grid(row=3, column=1)

        # Sender email
        tk.Label(
            frame,
            text="Sender Email",
            font=("Arial", 10, "bold")
        ).grid(row=4, column=0, sticky="w", pady=(15, 5))

        self.sender_entry = tk.Entry(frame, width=55)
        self.sender_entry.grid(row=5, column=0, columnspan=2)

        self.sender_entry.insert(
            0, self.config.get("sender_email", "")
        )

        # Receiver email
        tk.Label(
            frame,
            text="Receiver Email",
            font=("Arial", 10, "bold")
        ).grid(row=6, column=0, sticky="w", pady=(15, 5))

        self.receiver_entry = tk.Entry(frame, width=55)
        self.receiver_entry.grid(row=7, column=0, columnspan=2)

        self.receiver_entry.insert(
            0, self.config.get("receiver_email", "")
        )

        # Save button
        tk.Button(
            frame,
            text="SAVE CONFIGURATIONS",
            font=("Arial", 10, "bold"),
            width=25,
            height=2,
            cursor="hand2",
            command=self.save_configurations
        ).grid(row=8, column=0, columnspan=2, pady=25)

    def select_storage(self):

        folder = filedialog.askdirectory(
            title="Select Storage Folder",
            parent=self.window
        )

        if folder:
            self.storage_entry.delete(0, tk.END)
            self.storage_entry.insert(0, folder)

    def select_working(self):

        folder = filedialog.askdirectory(
            title="Select Working Folder",
            parent=self.window
        )

        if folder:
            self.working_entry.delete(0, tk.END)
            self.working_entry.insert(0, folder)

    def save_configurations(self):

        config = {
            "storage_path": self.storage_entry.get().strip(),
            "working_path": self.working_entry.get().strip(),
            "sender_email": self.sender_entry.get().strip(),
            "receiver_email": self.receiver_entry.get().strip()
        }

        self.save_callback(config)

        messagebox.showinfo(
            "Configurations",
            "Configurations saved successfully!",
            parent=self.window
        )

        self.window.destroy()
