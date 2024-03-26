import shutil
import sys

def generate_template() -> None:
    """
    Copy the file template.py in the current directory.
    """
    try:
        shutil.copyfile("template.py", "main.py")
    except FileNotFoundError:
        print("Error: 'template.py' file not found.")
        sys.exit(1)

if __name__ == "__main__":
    generate_template()
