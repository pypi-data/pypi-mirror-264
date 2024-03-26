rm dist/*
hatch build

pip uninstall -y dlmr-tools
pip install --upgrade dist/dlmr_tools-$MAJOR.$MINOR.$PATCH-py3-none-any.whl