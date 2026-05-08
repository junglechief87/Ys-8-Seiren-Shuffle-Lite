import customtkinter as ctk
from threading import Thread
import traceback


class ProgressWindow(ctk.CTkToplevel):
    """
    Progress window with real-time per-file progress tracking.

    Each task is a (callable, label_str) tuple.
    The callable must have signature:  func(progress_callback=None)
    where progress_callback(message: str) is called once per file written/processed.
    """

    def __init__(self, parent, tasks, total_files, operation_name="Processing", on_complete=None, icon_path=None):
        super().__init__(parent)
        self.title(operation_name)
        self.resizable(False, False)
        self.geometry("560x400")
        self.minsize(560, 400)
        self.maxsize(560, 400)
        self.attributes('-topmost', True)
        self.protocol("WM_DELETE_WINDOW", self._on_close_attempt)

        if icon_path:
            # CTkToplevel resets the icon after __init__, so defer the call
            self.after(200, lambda: self._apply_icon(icon_path))

        self._tasks = tasks
        self._total_files = max(total_files, 1)
        self._files_done = 0
        self._operation_name = operation_name
        self._on_complete = on_complete
        self._finished = False

        self._build_ui()
        self.lift()
        self.focus()
        self.update()

        # Worker thread: daemon=False so Python waits for it on exit
        Thread(target=self._worker_main, daemon=False).start()

    def _apply_icon(self, icon_path):
        try:
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Warning: Could not load icon: {e}")

    # -- UI construction ---------------------------------------------------

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        self._title_lbl = ctk.CTkLabel(
            self, text=self._operation_name, font=("Segoe UI", 15, "bold")
        )
        self._title_lbl.grid(row=0, column=0, padx=20, pady=(18, 6), sticky="w")

        bar_row = ctk.CTkFrame(self, fg_color="transparent")
        bar_row.grid(row=1, column=0, padx=20, pady=4, sticky="ew")
        bar_row.grid_columnconfigure(0, weight=1)

        self._bar = ctk.CTkProgressBar(bar_row, height=18)
        self._bar.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self._bar.set(0)

        self._pct_lbl = ctk.CTkLabel(bar_row, text="0%", width=44, font=("Segoe UI", 10, "bold"))
        self._pct_lbl.grid(row=0, column=1)

        self._task_lbl = ctk.CTkLabel(
            self, text="Starting...", font=("Segoe UI", 11, "bold"),
            text_color="#FFA500", anchor="w"
        )
        self._task_lbl.grid(row=2, column=0, padx=20, pady=(10, 2), sticky="ew")

        self._count_lbl = ctk.CTkLabel(
            self, text=f"0 / {self._total_files} files",
            font=("Segoe UI", 10), text_color="#AAAAAA", anchor="w"
        )
        self._count_lbl.grid(row=3, column=0, padx=20, pady=(0, 4), sticky="ew")

        self._log_box = ctk.CTkTextbox(self, height=170, font=("Consolas", 9))
        self._log_box.grid(row=4, column=0, padx=20, pady=6, sticky="ew")
        self._log_box.configure(state="disabled")

        self._close_btn = ctk.CTkButton(
            self, text="Please wait...", state="disabled",
            width=120, command=self._on_close
        )
        self._close_btn.grid(row=5, column=0, padx=20, pady=(4, 18), sticky="e")

    # -- Main-thread UI helpers (always reached via after()) ---------------

    def _append_log(self, text):
        self._log_box.configure(state="normal")
        self._log_box.insert("end", text + "\n")
        self._log_box.see("end")
        self._log_box.configure(state="disabled")

    def _on_task_start(self, label):
        self._task_lbl.configure(text=label)
        self._append_log(f"\n>>>  {label}")

    def _on_file_done(self, message):
        pct = self._files_done / self._total_files
        self._bar.set(pct)
        self._pct_lbl.configure(text=f"{int(pct * 100)}%")
        self._count_lbl.configure(text=f"{self._files_done} / {self._total_files} files")
        self._append_log(f"    {message}")

    def _on_finished(self, error, msg, tb):
        self._finished = True
        if error:
            self._title_lbl.configure(text=f"{self._operation_name} - Failed")
            self._task_lbl.configure(text="Error - see log below", text_color="red")
            self._append_log(f"\nError: {msg}")
        else:
            self._bar.set(1.0)
            self._pct_lbl.configure(text="100%")
            self._count_lbl.configure(text=f"{self._files_done} / {self._total_files} files")
            self._title_lbl.configure(text=f"{self._operation_name} - Done")
            self._task_lbl.configure(text="Completed successfully!", text_color="#00CC66")
            self._append_log("\nAll done!")

        self._close_btn.configure(text="Close", state="normal")
        if self._on_complete:
            self._on_complete(error, msg, tb)

    # -- Worker thread -----------------------------------------------------

    def _progress_callback(self, message):
        """Called from worker thread each time one file is processed.
        Increments the counter and schedules a UI update on the main thread."""
        self._files_done += 1
        self.after(0, self._on_file_done, message)

    def _worker_main(self):
        try:
            for func, label in self._tasks:
                self.after(0, self._on_task_start, label)
                func(self._progress_callback)
            self.after(0, self._on_finished, False, "", "")
        except Exception as exc:
            self.after(0, self._on_finished, True, str(exc), traceback.format_exc())

    # -- Close handling ----------------------------------------------------

    def _on_close_attempt(self):
        if self._finished:
            self._on_close()

    def _on_close(self):
        self.destroy()
