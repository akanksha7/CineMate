import subprocess

# Run the pyuic5 command to convert the .ui file to a .py file
# TODO don't hardcode this
subprocess.run(["pyuic5.exe", "ui/ui_main.ui", "-o", "ui/ui_main.py"])
