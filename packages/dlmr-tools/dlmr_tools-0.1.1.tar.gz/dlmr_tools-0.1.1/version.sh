version=$(grep -oP '__version__ = "\K[^"]+' src/dlmr_tools/version.py)


MAJOR=$(echo $version | cut -d. -f1)
MINOR=$(echo $version | cut -d. -f2)
PATCH=$(echo $version | cut -d. -f3)


PATCH=$((PATCH + 1))


echo "__version__ = \"$MAJOR.$MINOR.$PATCH\"" > src/dlmr_tools/version.py