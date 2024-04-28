import subprocess

# Run the pyuic5 command to convert the .ui file to a .py file
# TODO don't hardcode this
print('Executing pyuic5.exe ui/ui_main.ui -o ui/ui_main.py')
subprocess.run(["pyuic5.exe", "ui/ui_main.ui", "-o", "ui/ui_main.py"])

print('Executing pyuic5.exe ui/ui_querywidget.ui -o ui/ui_querywidget.py')
subprocess.run(["pyuic5.exe", "ui/ui_querywidget.ui", "-o", "ui/ui_querywidget.py"])
