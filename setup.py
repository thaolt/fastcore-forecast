from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["numpy", "tkinter", "matplotlib"], "excludes": []}

# Determine the base for the executable
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="forecast_app",
    version="0.1",
    description="Forecast Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("forecast.py", base=base)]
)
