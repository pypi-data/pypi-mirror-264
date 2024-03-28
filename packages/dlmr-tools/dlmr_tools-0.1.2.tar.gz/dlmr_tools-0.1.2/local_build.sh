rm dist/*
hatch build

pip uninstall -y dlmr-tools

version=$(grep -oP '__version__ = "\K[^"]+' src/dlmr_tools/version.py)
MAJOR=$(echo $version | cut -d. -f1)
MINOR=$(echo $version | cut -d. -f2)
PATCH=$(echo $version | cut -d. -f3)
pip install --upgrade dist/dlmr_tools-$MAJOR.$MINOR.$PATCH-py3-none-any.whl