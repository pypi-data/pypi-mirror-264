sh version.sh

rm dist/*
hatch build
twine upload dist/*

pip install --upgrade dlmr_tools
pip install --upgrade dlmr_tools