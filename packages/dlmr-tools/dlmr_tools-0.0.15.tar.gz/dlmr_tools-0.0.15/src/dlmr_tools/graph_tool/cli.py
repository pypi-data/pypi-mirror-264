import shutil
import sys
import os

def generate_template(banane: str = "dummy") -> None:
    """
    Copy the file template.py from the directory of this module to the current directory.
    """
    print(banane)
    module_dir = os.path.dirname(os.path.abspath(__file__))
    template_file = os.path.join(module_dir, "template.py")
    
    try:
        shutil.copyfile(template_file, "main.py")
        print("Template copied successfully!")
    except FileNotFoundError:
        print("Error: 'template.py' file not found in the module directory.")
        sys.exit(1)

if __name__ == "__main__":
    generate_template()