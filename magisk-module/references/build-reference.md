# Build Reference — Packaging a Module ZIP

## Full build script with dependency checks

Save this as `build.sh` in your module root directory.

```bash
#!/bin/bash
# build.sh — packages the module source directory into an installable ZIP.
#
# Usage: ./build.sh
# Run from the module root (the directory containing module.prop).
# Requirements: curl, zip (both must be in PATH)

set -euo pipefail

MODID="my_module"
VERSION="v1.0.0"
OUT="${MODID}-${VERSION}.zip"

# Dependency check — abort early with a clear message if tools are missing
for cmd in curl zip; do
    if ! command -v "$cmd" > /dev/null 2>&1; then
        echo "ERROR: '$cmd' not found in PATH." >&2
        echo "       Install it before running this script." >&2
        exit 1
    fi
done

# Clean previous build artifact
rm -f "$OUT"

# Prepare META-INF directory structure
mkdir -p META-INF/com/google/android

# Download module_installer.sh
#
# NOTE: This raw GitHub URL tracks the master branch of the Magisk repo.
# It may change or become unavailable between Magisk releases.
# If the download fails:
#   1. Check the current URL at:
#      https://github.com/topjohnwu/Magisk/blob/master/scripts/module_installer.sh
#   2. Pin to a specific commit hash for reproducible builds:
#      https://raw.githubusercontent.com/topjohnwu/Magisk/<COMMIT>/scripts/module_installer.sh
#
INSTALLER_URL="https://raw.githubusercontent.com/topjohnwu/Magisk/master/scripts/module_installer.sh"
echo "Downloading module_installer.sh..."
if ! curl -fsSL -o META-INF/com/google/android/update-binary "$INSTALLER_URL"; then
    echo "ERROR: Failed to download module_installer.sh." >&2
    echo "       Check the URL above or your network connection." >&2
    exit 1
fi

echo "#MAGISK" > META-INF/com/google/android/updater-script

# Build the file list — include optional files only if they exist,
# so you do not need to create empty placeholders
ZIP_ARGS="META-INF module.prop"

for f in customize.sh system system.prop sepolicy.rule \
          post-fs-data.sh post-mount.sh service.sh \
          boot-completed.sh late-load.sh action.sh uninstall.sh; do
    [ -e "$f" ] && ZIP_ARGS="$ZIP_ARGS $f"
done

# Pack
echo "Packing $OUT..."
# shellcheck disable=SC2086
zip -r9 "$OUT" $ZIP_ARGS

SIZE=$(du -sh "$OUT" | cut -f1)
echo "Built: $OUT ($SIZE)"
```

---

## Notes

- `set -euo pipefail` causes the script to abort immediately on any error,
  unset variable, or failed pipe. This prevents a partial ZIP from being
  delivered silently.
- Optional module files are included only if they exist on disk. You do not
  need to create empty `service.sh` or `post-fs-data.sh` files for modules
  that do not use them.
- To pin `module_installer.sh` to a known-good commit for reproducible builds,
  replace `master` in the URL with a full commit SHA from the Magisk repo.
- Run `chmod +x build.sh` once after creating this file so it is executable.
