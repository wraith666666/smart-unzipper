import os
import shutil
import threading
import subprocess
import tempfile
import tkinter as tk

from pathlib import Path
from tkinter import ttk, filedialog, messagebox


class ZipExtractorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Bulk ZIP Extractor")
        self.root.geometry("850x620")
        self.root.minsize(750, 550)
        self.root.configure(bg="#1e1e1e")

        icon_path = Path(__file__).parent / "icon.ico"
        if icon_path.exists():
            self.root.iconbitmap(str(icon_path))

        self.current_folder = os.getcwd()
        self.zip_vars = {}
        self.is_extracting = False

        self.setup_styles()
        self.create_ui()
        self.load_zip_files()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        bg = "#1e1e1e"
        fg = "#ffffff"

        style.configure(".", background=bg, foreground=fg, fieldbackground="#2b2b2b")
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg)
        style.configure("TLabelframe", background=bg, foreground=fg)
        style.configure("TLabelframe.Label", background=bg, foreground=fg)
        style.configure("TCheckbutton", background=bg, foreground=fg)
        style.configure("TRadiobutton", background=bg, foreground=fg)
        style.configure("TButton", padding=6)
        style.configure(
            "Blue.Horizontal.TProgressbar",
            troughcolor="#2b2b2b",
            background="#4a90e2",
            bordercolor="#2b2b2b",
            lightcolor="#4a90e2",
            darkcolor="#4a90e2",
            thickness=22,
        )

    def create_ui(self):
        # --- Top bar ---
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Folder:").pack(side="left")
        self.folder_label = ttk.Label(top, text=self.current_folder, foreground="#4a90e2")
        self.folder_label.pack(side="left", padx=5)
        ttk.Button(top, text="Browse", command=self.browse_folder).pack(side="right")

        # --- Options ---
        options = ttk.LabelFrame(self.root, text="Options", padding=10)
        options.pack(fill="x", padx=10, pady=5)

        self.mode_var = tk.StringVar(value="individual")

        ttk.Label(options, text="Extraction Mode:").grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(
            options, text="Individual Folders",
            variable=self.mode_var, value="individual",
            command=self.toggle_common,
        ).grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(
            options, text="Common Folder",
            variable=self.mode_var, value="common",
            command=self.toggle_common,
        ).grid(row=0, column=2, sticky="w")

        ttk.Label(options, text="Common Folder Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.common_entry = ttk.Entry(options, width=35)
        self.common_entry.insert(0, "Combined")
        self.common_entry.grid(row=1, column=1, sticky="w")

        self.rename_duplicates_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options, text="Rename duplicate files",
            variable=self.rename_duplicates_var,
        ).grid(row=2, column=0, columnspan=3, sticky="w")

        self.delete_zip_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options, text="Delete ZIP after extraction",
            variable=self.delete_zip_var,
        ).grid(row=3, column=0, columnspan=3, sticky="w")

        # --- ZIP file list ---
        list_frame = ttk.LabelFrame(self.root, text="ZIP Files", padding=10, height=260)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(5, 0))
        list_frame.pack_propagate(False)

        self.canvas = tk.Canvas(list_frame, bg="#1e1e1e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)

        self.scroll_frame = ttk.Frame(self.canvas)
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Progress ---
        progress_frame = ttk.LabelFrame(self.root, text="Progress", padding=10)
        progress_frame.pack(fill="x", padx=10, pady=5)

        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            style="Blue.Horizontal.TProgressbar",
        )
        self.progress.pack(fill="x", pady=5)
        self.status = ttk.Label(progress_frame, text="Idle")
        self.status.pack(anchor="w")

        # --- Bottom buttons ---
        bottom = ttk.Frame(self.root, padding=10, height=50)
        bottom.pack(fill="x")
        bottom.pack_propagate(False)

        ttk.Button(bottom, text="Refresh", command=self.load_zip_files).pack(side="left", padx=5)
        ttk.Button(bottom, text="Select All", command=self.select_all).pack(side="left", padx=5)
        ttk.Button(bottom, text="Unselect All", command=self.unselect_all).pack(side="left", padx=5)

        self.extract_btn = ttk.Button(bottom, text="Extract Selected", command=self.start_thread)
        self.extract_btn.pack(side="right", padx=5)

        self.toggle_common()

    def load_zip_files(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.zip_vars.clear()

        zips = sorted([f for f in os.listdir(self.current_folder) if f.lower().endswith(".zip")])

        if not zips:
            ttk.Label(self.scroll_frame, text="No ZIP files found.").pack(anchor="w")
            return

        for zip_name in zips:
            var = tk.BooleanVar(value=True)
            self.zip_vars[zip_name] = var
            ttk.Checkbutton(self.scroll_frame, text=zip_name, variable=var).pack(anchor="w", pady=2)

    def browse_folder(self):
        if self.is_extracting:
            return
        folder = filedialog.askdirectory()
        if folder:
            self.current_folder = folder
            self.folder_label.config(text=folder)
            self.load_zip_files()

    def toggle_common(self):
        state = "disabled" if self.mode_var.get() == "individual" else "normal"
        self.common_entry.config(state=state)

    def select_all(self):
        for var in self.zip_vars.values():
            var.set(True)

    def unselect_all(self):
        for var in self.zip_vars.values():
            var.set(False)

    def safe_path(self, path):
        """Return a non-conflicting path by appending a counter suffix."""
        if not os.path.exists(path):
            return path
        base = Path(path).stem
        ext = Path(path).suffix
        parent = os.path.dirname(path)
        counter = 1
        while True:
            new_path = os.path.join(parent, f"{base}_{counter}{ext}")
            if not os.path.exists(new_path):
                return new_path
            counter += 1

    def start_thread(self):
        if self.is_extracting:
            return
        threading.Thread(target=self.extract, daemon=True).start()

    def extract_zip(self, zip_path, target):
        """Extract a ZIP file to target using Windows built-in tar."""
        subprocess.run(
            ["tar", "-xf", zip_path, "-C", target],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

    def merge_folders(self, src, dst):
        """Recursively merge src into dst, handling duplicate filenames."""
        os.makedirs(dst, exist_ok=True)
        for item in os.listdir(src):
            src_item = os.path.join(src, item)
            dst_item = os.path.join(dst, item)
            if os.path.isdir(src_item):
                self.merge_folders(src_item, dst_item)
            else:
                if os.path.exists(dst_item):
                    if self.rename_duplicates_var.get():
                        dst_item = self.safe_path(dst_item)
                    else:
                        continue
                shutil.move(src_item, dst_item)

    def smart_merge(self, temp_extract, final_target):
        """Unwrap single-root ZIPs automatically before merging."""
        items = os.listdir(temp_extract)
        if len(items) == 1 and os.path.isdir(os.path.join(temp_extract, items[0])):
            self.merge_folders(os.path.join(temp_extract, items[0]), final_target)
        else:
            self.merge_folders(temp_extract, final_target)

    def extract(self):
        self.is_extracting = True
        self.extract_btn.config(state="disabled")

        selected = [z for z, v in self.zip_vars.items() if v.get()]

        if not selected:
            self.finish()
            messagebox.showwarning("No Selection", "Please select at least one ZIP file.")
            return

        total = len(selected)
        success = 0
        failed = []

        common_target = None
        if self.mode_var.get() == "common":
            folder_name = self.common_entry.get().strip() or "Combined"
            common_target = os.path.join(self.current_folder, folder_name)
            os.makedirs(common_target, exist_ok=True)

        for index, zip_name in enumerate(selected):
            try:
                self.progress_var.set((index / total) * 100)
                self.status.config(text=f"Extracting: {zip_name}")
                self.root.update_idletasks()

                zip_path = os.path.join(self.current_folder, zip_name)

                if self.mode_var.get() == "individual":
                    final_target = os.path.join(self.current_folder, Path(zip_name).stem)
                else:
                    final_target = common_target

                os.makedirs(final_target, exist_ok=True)

                with tempfile.TemporaryDirectory() as temp_dir:
                    self.extract_zip(zip_path, temp_dir)
                    self.smart_merge(temp_dir, final_target)

                if self.delete_zip_var.get():
                    os.remove(zip_path)

                success += 1

            except Exception as e:
                failed.append(f"{zip_name}: {e}")

        self.progress_var.set(100)
        self.status.config(text="Completed")

        msg = f"Successfully extracted {success} ZIP(s)."
        if failed:
            msg += "\n\nFailed:\n" + "\n".join(failed)

        messagebox.showinfo("Done", msg)
        self.load_zip_files()
        self.finish()

    def finish(self):
        self.extract_btn.config(state="normal")
        self.is_extracting = False


if __name__ == "__main__":
    root = tk.Tk()
    app = ZipExtractorApp(root)
    root.mainloop()
