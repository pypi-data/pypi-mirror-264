import shutil

def generate_template() -> None:
    """
    Copy the file template.py in the current directory.
    """
    shutil.copyfile("template.py", "main.py")