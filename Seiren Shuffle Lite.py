import traceback
from zipfile import ZipFile

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import sys
import subprocess
from pathlib import Path
from patch.chestPatcher import cleanChests
from patch.fileManagement import copyOriginalGameFiles, downloadFiles, restoreOriginalGameFiles, countOriginalGameFiles, countDownloadFiles, countChestLocations, needs_update
from patch.rngPatcher import rngPatcherMain
from patch.miscPatches import AddWarpToFSCCrystal, readFileIntoBuffer, miscFixes, makeResourceDropsGuaranteed, updateINI
from patch.progressWindow import ProgressWindow
import shared.config as config
# Import file management functions
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patch'))

# Set appearance mode and color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

FRAME_TITLE_STYLE = {
    "text_color": "#D3D3D3",
    "font": ("Segoe UI", 14, "bold"),
    "anchor": "w",
}

SETTINGS_FILE = "seirenShuffleLiteSettings.json"
VERSION_NUM = "1.1.0"


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def find_icon_path():
    """Find the icon file in multiple possible locations"""
    possible_paths = [
        resource_path("./shared/ysR Logo.ico"),
        resource_path("../shared/ysR Logo.ico"),
        resource_path("../../shared/ysR Logo.ico"),
        os.path.join(os.path.dirname(__file__), "shared", "ysR Logo.ico"),
        os.path.join(os.path.dirname(__file__), "..", "shared", "ysR Logo.ico"),
        os.path.join(os.path.dirname(__file__), "..", "..", "shared", "ysR Logo.ico"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


ICON_PATH = find_icon_path()

class patch_data:
    def __init__(self):
        self.item_map = {}
        self.dungeon_entrance_randomization = {}
        self.settings = {}
        self.boss_stats = {}
        

class ExecutableLocationFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)

        # Frame's Title
        self.title = ctk.CTkLabel(self, text="Ys 8 Executable Location", **FRAME_TITLE_STYLE)
        self.title.grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 0), sticky="w")

        # Path Label
        self.path_label = ctk.CTkLabel(self, text="Path: ")
        self.path_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Path Display
        self.path_display = ctk.CTkLabel(
            self,
            text="No executable selected",
            text_color="#888888",
            font=("Segoe UI", 10),
        )
        self.path_display.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Browse Button
        self.browse_button = ctk.CTkButton(
            self, text="Browse", command=self.browseExecutable
        )
        self.browse_button.grid(row=1, column=2, padx=5, pady=5)

        self.executable_path = None

    def browseExecutable(self):
        file_path = filedialog.askopenfilename(
            title="Select Ys8.exe",
            filetypes=(("Executable Files", "*.exe"), ("All Files", "*.*")),
        )
        if file_path:
            self.executable_path = file_path
            self.path_display.configure(text=file_path, text_color="#FFFFFF")
            self.master.on_executable_selected()

    def get_path(self):
        return self.executable_path

    def set_path(self, path):
        self.executable_path = path
        if path:
            self.path_display.configure(text=path, text_color="#FFFFFF")
        else:
            self.path_display.configure(text="No executable selected", text_color="#888888")


class APPatchFileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)

        # Frame's Title
        self.title = ctk.CTkLabel(self, text="AP Patch File", **FRAME_TITLE_STYLE)
        self.title.grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 0), sticky="w")

        # Path Label
        self.path_label = ctk.CTkLabel(self, text="Path: ")
        self.path_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Path Display
        self.path_display = ctk.CTkLabel(
            self,
            text="No patch file selected",
            text_color="#888888",
            font=("Segoe UI", 10),
        )
        self.path_display.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Browse Button
        self.browse_button = ctk.CTkButton(
            self, text="Browse", command=self.browsePatchFile, state="disabled"
        )
        self.browse_button.grid(row=1, column=2, padx=5, pady=5)

        self.patch_file_path = None

    def browsePatchFile(self):
        file_path = filedialog.askopenfilename(
            title="Select AP Patch File",
            filetypes=(("Patch Files", "*.apdana"), ("All Files", "*.*")),
        )
        if file_path:
            self.patch_file_path = file_path
            self.path_display.configure(text=file_path, text_color="#FFFFFF")
            self.master.on_patch_file_selected()

    def get_path(self):
        return self.patch_file_path

    def set_path(self, path):
        self.patch_file_path = path
        if path:
            self.path_display.configure(text=path, text_color="#FFFFFF")
        else:
            self.path_display.configure(
                text="No patch file selected", text_color="#888888"
            )

    def enable_button(self):
        self.browse_button.configure(state="normal")

    def disable_button(self):
        self.browse_button.configure(state="disabled")


class CommandsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.parent_app = master  # Store reference to main app
        
        # Initialize patch data attributes
        self.item_map = {}
        self.dungeon_entrance_randomization = {}
        self.settings = {}

        # Frame's Title
        self.title = ctk.CTkLabel(self, text="Commands", **FRAME_TITLE_STYLE)
        self.title.grid(row=0, column=0, columnspan=3, padx=5, pady=(5, 0), sticky="w")

        # Restore Files Button
        self.restore_button = ctk.CTkButton(
            self, text="Restore Game Files", command=self.restoreFiles, state="disabled"
        )
        self.restore_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Patch Files Button
        self.patch_button = ctk.CTkButton(
            self, text="Patch Files", command=self.patchFiles, state="disabled"
        )
        self.patch_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Generate Seed Button
        self.generate_seed_button = ctk.CTkButton(
            self, text="Generate Seed", command=self.generateSeed, state="disabled"
        )
        self.generate_seed_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        # Play Game Button
        self.play_button = ctk.CTkButton(
            self, text="Play Game", command=self.launchGame, state="disabled"
        )
        self.play_button.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    def restoreFiles(self):
        """Restore original game files from backup"""
        result = messagebox.askyesno(
            "Restore Original Files",
            "This will restore your original game files to their unmodified state.\nContinue?"
        )
        if not result:
            return

        try:
            self.parent_app.set_gui_enabled(False)

            backup_dir = os.path.join(config.executable_directory, 'Original Game Files')
            file_count = len([f for root, dirs, files in os.walk(backup_dir) for f in files]) if os.path.exists(backup_dir) else 100

            def on_complete(error, msg, tb):
                self.parent_app.set_gui_enabled(True)

            tasks = [(restoreOriginalGameFiles, "Restoring Original Game Files")]
            ProgressWindow(self.parent_app, tasks, file_count, "Restore Original Files", on_complete, ICON_PATH)

        except Exception as e:
            self.parent_app.set_gui_enabled(True)
            messagebox.showerror("Error", f"Failed to restore files: {str(e)}")

    def patchFiles(self):
        """Patch game files with AP patch file"""

        if not config.executable_directory:
            messagebox.showerror("Error", "Please select the executable directory")
            return

        if not os.path.exists(config.executable_directory):
            messagebox.showerror("Error", "Selected files do not exist")
            return

        try:
            self.parent_app.set_gui_enabled(False)

            backup_dir = os.path.join(config.executable_directory, 'Original Game Files')

            tasks = []
            total_files = 0

            if not os.path.exists(backup_dir):
                total_files += countOriginalGameFiles()
                tasks.append((copyOriginalGameFiles, "Backing Up Original Game Files"))

            total_files += countDownloadFiles()
            tasks.append((downloadFiles, "Downloading Patch Files"))

            total_files += countChestLocations()
            tasks.append((lambda cb: cleanChests(progress_callback=cb), "Patching Chests"))

            total_files += 1
            tasks.append((makeResourceDropsGuaranteed, "Guaranteeing Resource Drops"))

            total_files += 1
            tasks.append((AddWarpToFSCCrystal, "Adding FSC Crystal Warp"))

            total_files += 1
            tasks.append((updateINI, "Updating Language Setting"))

            total_files += 5
            tasks.append((miscFixes, "Applying Miscellaneous Fixes"))

            def on_complete(error, msg, tb):
                self.parent_app.mark_patch_used()
                self.parent_app.set_gui_enabled(True)

            ProgressWindow(self.parent_app, tasks, total_files, "Patching Game Files", on_complete, ICON_PATH)

        except Exception as e:
            self.parent_app.set_gui_enabled(True)
            messagebox.showerror("Error", f"Failed to patch files: {str(e)}")

    def generateSeed(self):
        """Generate a new seed from the AP patch file"""

        if not config.executable_directory or not config.patch_file_path:
            messagebox.showerror("Error", "Please select both executable and patch file")
            return

        try:
            self.parent_app.set_gui_enabled(False)

            explosivePlant = config.executable_directory + "/chr/enemy/m0660/m0660.mtb"
            plantRespawn = readFileIntoBuffer(explosivePlant)

            if plantRespawn[0xE05] != 0x3C:
                self.parent_app.set_gui_enabled(True)
                messagebox.showerror("Error", "Files are not yet patched! Please patch files first.")
                return

            def seed_gen_task(progress_callback=None):
                self._generate_seed_internal(progress_callback)

            def on_complete(error, msg, tb):
                self.parent_app.set_gui_enabled(True)

            with ZipFile(config.patch_file_path) as zf:
                item_map_preview = json.loads(zf.read("item_location_map.json"))
            total_steps = len(item_map_preview) + 10  # locations + 10 named pipeline steps (matches rngPatcherMain callbacks)

            tasks = [(seed_gen_task, "Generating Randomized Seed")]
            ProgressWindow(self.parent_app, tasks, total_steps, "Generate Seed", on_complete, ICON_PATH)

        except Exception as e:
            self.parent_app.set_gui_enabled(True)
            traceback.print_exc()
            messagebox.showerror("Error", f"Seed generation failed: {str(e)}")
    
    def _generate_seed_internal(self, progress_callback=None):
        """Internal method for the actual seed generation logic"""
        with ZipFile(config.patch_file_path) as zf:
            for name in zf.namelist():
                if name == "settings.json":
                    self.settings = json.loads(zf.read(name))
                elif name == "item_location_map.json":
                    self.item_map = json.loads(zf.read(name))
                elif name == "dungeon_entrance_randomization.json":
                    self.dungeon_entrance_randomization = json.loads(zf.read(name))
                elif name == "boss_stats.json":
                    self.boss_stats = json.loads(zf.read(name))

        patch_data_obj = patch_data()
        patch_data_obj.item_map = self.item_map
        patch_data_obj.dungeon_entrance_randomization = self.dungeon_entrance_randomization
        patch_data_obj.settings = self.settings
        patch_data_obj.boss_stats = self.boss_stats

        rngPatcherMain(patch_data_obj, progress_callback)

    def launchGame(self):
        executable_path = config.executable_path
        if executable_path and os.path.exists(executable_path):
            try:
                subprocess.Popen(executable_path)
                messagebox.showinfo("Success", "Game launched!")
            except Exception as e:
                traceback.print_exc()
                messagebox.showerror("Error", f"Failed to launch game: {e}")
        else:
            messagebox.showerror("Error", "Invalid executable path")

    def enable_patch_button(self):
        self.patch_button.configure(state="normal")

    def disable_patch_button(self):
        self.patch_button.configure(state="disabled")
    
    def enable_generate_seed_button(self):
        self.generate_seed_button.configure(state="normal")

    def disable_generate_seed_button(self):
        self.generate_seed_button.configure(state="disabled")

    def enable_play_button(self):
        self.play_button.configure(state="normal")

    def disable_play_button(self):
        self.play_button.configure(state="disabled")

    def enable_restore_button(self):
        self.restore_button.configure(state="normal")

    def disable_restore_button(self):
        self.restore_button.configure(state="disabled")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"Seiren Shuffle Lite v{VERSION_NUM}")
        
        # Disable DPI scaling on Windows BEFORE creating window
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except:
            pass
        
        # Set fixed size and disable all resizing
        self.geometry("650x300")
        self.resizable(False, False)
        self.minsize(650, 300)
        self.maxsize(650, 300)
        
        if ICON_PATH:
            try:
                self.iconbitmap(ICON_PATH)
            except Exception as e:
                print(f"Warning: Could not load icon from {ICON_PATH}: {e}")
        else:
            print("Warning: Icon file not found in expected locations")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=0)
        self.grid_rowconfigure(3, weight=1)

        # track when the user last ran the patch operation (ISO8601 UTC)
        self.last_patched_at = None

        # Create frames
        self.executable_frame = ExecutableLocationFrame(self)
        self.executable_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.patch_file_frame = APPatchFileFrame(self)
        self.patch_file_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.commands_frame = CommandsFrame(self)
        self.commands_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Load settings on startup
        self.loadSettings()
    
    def set_gui_enabled(self, enabled):
        """Enable or disable the main GUI"""
        
        # Disable/enable specific buttons
        if not enabled:
            self.executable_frame.browse_button.configure(state="disabled")
            self.patch_file_frame.browse_button.configure(state="disabled")
            self.commands_frame.restore_button.configure(state="disabled")
            self.commands_frame.patch_button.configure(state="disabled")
            self.commands_frame.generate_seed_button.configure(state="disabled")
            self.commands_frame.play_button.configure(state="disabled")
        else:
            # Re-enable browse buttons and re-check command button states
            self.executable_frame.browse_button.configure(state="normal")
            if self.executable_frame.get_path() is not None:
                self.patch_file_frame.enable_button()
            self.updateButtonStates()

    def saveSettings(self):
        settings = {
            "executable_path": self.executable_frame.get_path(),
            "patch_file_path": self.patch_file_frame.get_path(),
            "last_patched_at": self.last_patched_at,
        }
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def loadSettings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    settings = json.load(f)

                self.last_patched_at = settings.get("last_patched_at")
                executable_path = settings.get("executable_path")
                patch_file_path = settings.get("patch_file_path")

                if executable_path:
                    self.executable_frame.set_path(executable_path)
                    self.on_executable_selected()

                if patch_file_path:
                    self.patch_file_frame.set_path(patch_file_path)
                    self.on_patch_file_selected()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load settings: {e}")

    def mark_patch_used(self):
        """Record the current UTC time as the last patch usage and save settings."""
        try:
            from datetime import datetime, timezone
            # ISO 8601 UTC timestamp, normalized to 'Z'
            self.last_patched_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
            self.saveSettings()
        except Exception:
            pass

    def on_executable_selected(self):
        """Called when executable location is selected"""
        config.executable_path = self.executable_frame.get_path()
        config.executable_directory = os.path.dirname(config.executable_path)
        self.patch_file_frame.enable_button()
        self.updateButtonStates()

    def on_patch_file_selected(self):
        """Called when patch file is selected"""
        config.patch_file_path = self.patch_file_frame.get_path()
        self.updateButtonStates()

    def updateButtonStates(self):
        """Update button states based on file selections"""
        has_executable = self.executable_frame.get_path() is not None
        has_patch_file = self.patch_file_frame.get_path() is not None

        # Enable/disable restore button based on executable selection
        if has_executable:
            self.commands_frame.enable_restore_button()
            # quick check against repo's last_update marker
            try:
                if needs_update():
                    self.commands_frame.patch_button.configure(text="Patch Files (Update)")
                else:
                    self.commands_frame.patch_button.configure(text="Patch Files")
            except Exception:
                pass
            self.commands_frame.enable_patch_button()
        else:
            self.commands_frame.disable_patch_button()
            self.commands_frame.disable_restore_button()

        # Enable/disable patch and play buttons based on both files being selected
        if has_executable and has_patch_file:
            self.commands_frame.enable_play_button()
            self.commands_frame.enable_generate_seed_button()
        else:
            self.commands_frame.disable_play_button()
            self.commands_frame.disable_generate_seed_button()


        # Save settings whenever selections change
        self.saveSettings()


if __name__ == "__main__":
    app = App()
    app.mainloop()
