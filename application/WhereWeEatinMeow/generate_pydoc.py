import os
import pydoc
import django

django.setup()

project_root = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(project_root, "aboutus")

for root, dirs, files in os.walk(app_dir):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            module_name = (
                file_path.replace(os.path.join(project_root, ""), "")
                .replace("/", ".")
                .replace(".py", "")
            )
            module = __import__(module_name)
            pydoc.writedoc(module)
