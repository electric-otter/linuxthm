import dearpygui.dearpygui as dpg
import os
import shutil
import subprocess

THEME_DIR = os.path.expanduser("~/lthmthemes/")

# Create the theme directory if it doesn't exist
os.makedirs(THEME_DIR, exist_ok=True)

# Function to import a user-named theme file
def import_theme(sender, app_data):
    file_path = app_data['file_path_name']

    if file_path.endswith(".css"):
        # Extract theme name from file name (without extension)
        theme_name = os.path.splitext(os.path.basename(file_path))[0]

        if theme_name.lower() == "gtk":
            print("Please use a custom name for your theme file (not gtk.css).")
            return

        theme_path = os.path.join(THEME_DIR, theme_name)
        gtk_target = os.path.join(theme_path, os.path.basename(file_path))

        try:
            os.makedirs(theme_path, exist_ok=True)
            shutil.copy(file_path, gtk_target)
            print(f"Theme '{theme_name}' imported successfully.")

            dpg.add_text(f"Theme '{theme_name}' added. You must log out/log in or restart.")

        except Exception as e:
            print(f"Failed to import theme: {e}")
    else:
        print("Only .css files are allowed.")

# Function to apply a selected theme
def apply_theme(sender, app_data, user_data):
    theme_name = user_data
    print(f"Applying theme: {theme_name}")

    # Set GTK theme using gsettings
    try:
        subprocess.run(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", theme_name], check=True)
        print("Applied theme for Cinnamon.")
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", theme_name], check=True)
            print("Applied theme for GNOME.")
        except subprocess.CalledProcessError as e:
            print(f"Error applying theme: {e}")

# GUI Setup
dpg.create_context()

# File dialog to import theme
with dpg.file_dialog(directory_selector=False, show=False, callback=import_theme, tag="file_dialog_id"):
    dpg.add_file_extension(".css", color=(150, 255, 150, 255))

# Main window
with dpg.window(label="Linux Theme Manager", width=520, height=300):
    dpg.add_text("LinuxTHM - Manage your downloaded LTHM themes")

    dpg.add_button(label="Import a community-made .css theme", callback=lambda: dpg.show_item("file_dialog_id"))

    dpg.add_separator()
    dpg.add_text("Available Themes:")

    # Load themes from directory
    themes = [name for name in os.listdir(THEME_DIR) if os.path.isdir(os.path.join(THEME_DIR, name))]

    if not themes:
        dpg.add_text("No themes found.")
    else:
        for theme in themes:
            dpg.add_button(label=f"Apply '{theme}'", callback=apply_theme, user_data=theme)

# Launch GUI
dpg.create_viewport(title="Linux Theme Manager", width=550, height=350)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
