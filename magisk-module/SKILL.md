---
name: magisk-module
description: >
  Use this skill whenever the user wants to create, scaffold, edit, package,
  or debug a root manager module — including Magisk modules, KernelSU (KSU)
  modules, SukiSU-Ultra modules, APatch modules, or modules that must run on
  multiple managers. Triggers include any mention of "Magisk module",
  "KSU module", "KernelSU module", "SukiSU module", "SukiSU-Ultra", "APatch
  module", "root module", "systemless mod", "module.prop", "customize.sh",
  "service.sh", "post-fs-data", "sepolicy.rule", "system.prop (Android module)",
  "Zygisk", "SUSFS", "KPM", "kernel patch module", "MMRL", or requests to
  "make something systemless", "inject into /system", "replace a system file",
  "patch Android at boot", or "publish a module". Do NOT use for general
  Android development, Xposed/LSPosed frameworks (unless they also ship a
  module wrapper), or kernel compilation tasks unrelated to module packaging.
license: MIT
---

# Magisk / KernelSU Module Builder Skill

## Overview

This skill guides a coding agent to produce **installable root-manager modules**
that work correctly on:

| Root manager | Module path | Notes |
|---|---|---|
| Magisk (>= v20) | `/data/adb/modules/$MODID` | Magic mount (bind mount) |
| KernelSU (KSU) | `/data/adb/modules/$MODID` | OverlayFS via metamodule |
| SukiSU-Ultra | `/data/adb/modules/$MODID` | KSU fork; adds SUSFS and KPM support |
| APatch | `/data/adb/modules/$MODID` | Magisk-compatible API |

All four share the same on-disk layout and script API, so a single module ZIP
can target all of them when written carefully. SukiSU-Ultra exposes `$KSU`
exactly as KernelSU does — existing KSU detection code works without changes.
KPM (Kernel Patch Module) is a SukiSU-Ultra / APatch-exclusive binary module
type that runs in kernel space; it requires a separate workflow and is outside
the scope of standard Magisk-format modules.

---

## 0. Agent Workflow

Follow these steps in order for every module request:

1. **Identify scope.** Determine: target root manager (Magisk, KSU, SukiSU-Ultra, APatch, or all), Android API floor, whether Zygisk is required, and what the module must do (file injection, property patch, SELinux rule, runtime script, or a mix). If the request matches a known archetype (font injection, audio driver, prop-only, debloater, performance tweaks, Play Integrity stack), route to `references/module-recipes.md` for a type-specific template before proceeding.

2. **Scaffold the layout.** Generate all required files using the canonical
   layout in §1. Never omit `module.prop`. Omit optional scripts only when
   they are explicitly not needed.

3. **Write module.prop.** Apply all hard rules from §2 before writing.

4. **Write customize.sh.** Use only the allowed functions; see
   `references/customize-api.md` for the full variable and function reference.
   Never call `exit` — use `abort` for fatal errors. Always include root manager
   detection and an API level guard.

5. **Choose boot scripts.** Prefer `service.sh` for runtime work. Use
   `post-fs-data.sh` only when strictly necessary (it is blocking: 40 s max on
   Magisk, 10 s max on KSU). For KSU-targeting modules, add `post-mount.sh` or
   `boot-completed.sh` as needed.

6. **Populate system/, system.prop, sepolicy.rule.** Apply rules from §§5-7.

7. **Apply cross-compatibility patterns.** If targeting both managers, apply
   the patterns from §8.

8. **Run pitfalls check.** Before producing final output, verify every
   generated file against the forbidden patterns table in §14.

9. **Package.** Provide the ZIP layout (§1 ZIP section) or refer to
   `references/build-reference.md` for the full build script.

---

## 1. Canonical Directory Layout

Always generate the **full** directory tree. Never omit required files.

```
$MODID/
├── module.prop           <- REQUIRED — module identity
├── customize.sh          <- optional — runs at install time (sourced, not exec'd)
│
├── system/               <- files overlaid onto /system at boot
│   ├── app/
│   ├── bin/
│   ├── etc/
│   └── ...
│
├── zygisk/               <- Magisk-only Zygisk native libs (omit for KSU-only)
│   ├── arm64-v8a.so
│   ├── armeabi-v7a.so
│   ├── x86.so
│   └── x86_64.so
│
├── post-fs-data.sh       <- blocking early-boot script (use sparingly)
├── post-mount.sh         <- KSU-only: runs after OverlayFS is mounted
├── service.sh            <- non-blocking late-start script (preferred)
├── boot-completed.sh     <- KSU-only: runs after ACTION_BOOT_COMPLETED
├── late-load.sh          <- KSU LKM late-load mode replacement for post-fs-data
├── action.sh             <- runs when user taps "Action" button in manager UI
├── uninstall.sh          <- cleanup script run on module removal
│
├── system.prop           <- system properties loaded via resetprop
└── sepolicy.rule         <- one SELinux policy statement per line
```

### ZIP layout for installation

```
module.zip
├── META-INF/com/google/android/
│   ├── update-binary     <- copy of module_installer.sh (Magisk recovery flash)
│   └── updater-script    <- must contain exactly: #MAGISK
├── customize.sh
├── module.prop
├── system/
│   └── ...
└── ... (all other module files)
```

---

## 2. module.prop — Required Fields & Rules

```properties
id=my_module_id
name=My Module Name
version=v1.0.0
versionCode=1
author=YourName
description=Short single-line description of what this module does
updateJson=https://example.com/update.json   # optional
actionIcon=icon/action.png                   # optional, KSU WebUI
webuiIcon=icon/webui.png                     # optional, KSU WebUI
```

### Hard rules (enforce all of these):

- `id` **must** match `/^[a-zA-Z][a-zA-Z0-9._-]+$/` — never start with digit or dash.
- `versionCode` **must** be an integer (no quotes, no `v` prefix).
- Every value is a **single line** — no newlines inside values.
- File **must** use **Unix LF** line endings (`\n`), never CRLF or CR.
- Never change `id` after publishing — it is the module's permanent identity.

---

## 2a. Platform Compatibility Reference

| Android version | Magisk | KernelSU | APatch |
|---|---|---|---|
| 4.2–4.3 | Yes (legacy) | Not officially | Not officially |
| 4.4–5.x | Yes | Not officially | Not officially |
| 6–8 | Yes | Not officially | Not officially |
| 9–11 | Yes | Yes (manual build; kernels 4.14+) | Yes (kernels 3.18–6.12 with CONFIG_KALLSYMS=y) |
| 12 | Yes | Yes (GKI; kernel 5.10+) | Yes (kernels 3.18–6.12 with CONFIG_KALLSYMS=y) |
| 13+ | Yes | Yes (GKI; kernel 5.10+) | Yes (kernels 3.18–6.12 with CONFIG_KALLSYMS=y) |

Note: For KSU, official GKI support starts at kernel 5.10 (Android 12); 4.14+ requires a manual build. For APatch, the kernel must be 3.18–6.12 with `CONFIG_KALLSYMS=y`.

---

## 3. customize.sh — Installation Script

`customize.sh` is **sourced** (not executed) by the installer.

### Critical rules:

- **Never call `exit`** — use `abort "message"` for fatal errors.
- **Never hardcode module paths** — always use `MODDIR=${0%/*}` or `$MODPATH`.
- **Never add a file named `install.sh`** — reserved and will break things.
- `SKIPUNZIP=1` at the top gives you full control; you must then handle all
  file extraction yourself.

For the full variable and function reference, see `references/customize-api.md`.

### Detecting the root manager at install time

```sh
if [ "$KSU" = "true" ]; then
    ui_print "- Running under KernelSU $KSU_VER"
    # KSU-specific install logic
elif [ "$APATCH" = "true" ]; then
    ui_print "- Running under APatch"
    # APatch-specific install logic
else
    ui_print "- Running under Magisk $MAGISK_VER"
    # Magisk-specific install logic
fi
```

RULE: Never use `$MAGISK_VER`, `$KSU`, or `$APATCH` to infer a platform not explicitly set. An unset variable means Magisk.

### Removing files via REMOVE variable

```sh
# Both Magisk and KSU support this pattern
REMOVE="
/system/app/Bloatware
/system/fonts/NotoSerif.ttf
"
```

### Replacing directories via REPLACE variable

```sh
# Magisk: creates .replace file inside dir
# KSU:    sets OverlayFS opaque attribute on dir
REPLACE="
/system/app/YouTube
"
```

---

## 4. Boot Scripts — Execution Stages

### Magisk boot stages

| Script | Mode | Blocking | When |
|---|---|---|---|
| `post-fs-data.sh` | post-fs-data | YES (40 s max) | Before modules mount, before Zygote |
| `service.sh` | late_start | NO | After boot, parallel to system |
| `action.sh` | on-demand | — | User taps Action in Magisk app |
| `uninstall.sh` | on removal | — | Module uninstalled |

### KSU additional boot stages

| Script | Mode | Blocking | When |
|---|---|---|---|
| `post-fs-data.sh` | post-fs-data | YES (10 s max) | Before modules mount |
| `post-mount.sh` | post-mount | YES | After OverlayFS is mounted |
| `service.sh` | late_start | NO | After boot, parallel |
| `boot-completed.sh` | boot-completed | NO | After ACTION_BOOT_COMPLETED |
| `late-load.sh` | late-load (LKM) | YES | Replaces post-fs-data in LKM late-load mode |
| `action.sh` | on-demand | — | User taps Action in KSU app |

### Script best practices

```sh
#!/system/bin/sh
# Always derive MODDIR dynamically — never hardcode
MODDIR=${0%/*}

# Detect KSU vs Magisk at runtime
if [ "$KSU" = "true" ]; then
    # KSU-specific behaviour
    :
fi

# Detect late-load mode (KSU LKM only)
if [ "$KSU_LATE_LOAD" = "1" ]; then
    # Skip early-boot-only operations
    :
fi

# Use resetprop, NOT setprop (setprop deadlocks in post-fs-data)
resetprop -n ro.debuggable 1

# Always use MODDIR for relative paths
cp "$MODDIR/myfile" /data/local/tmp/
```

#### BusyBox paths by manager

| Manager | BusyBox path |
|---|---|
| Magisk | /data/adb/magisk/busybox |
| KernelSU/SukiSU | /data/adb/ksu/bin/busybox |
| APatch | /data/adb/ap/bin/busybox |

Rule: Always derive the BusyBox path from the manager detection block. Never hardcode a single path in scripts targeting multiple managers.

### post-fs-data.sh — use only when truly necessary

```sh
#!/system/bin/sh
# BLOCKING — keep this script fast
# WARNING: setprop DEADLOCKS here — use resetprop -n instead
MODDIR=${0%/*}
resetprop -n persist.sys.timezone "Africa/Nairobi"
```

### service.sh — preferred for most use cases

```sh
#!/system/bin/sh
# NON-BLOCKING — safe to do heavier work here
MODDIR=${0%/*}
# Wait for a prop if needed
while [ "$(getprop sys.boot_completed)" != "1" ]; do
    sleep 1
done
# Your logic here
```

---

## 5. system/ Directory — File Injection Rules

### Magisk (magic mount / bind mount)

- Files in `system/` are bind-mounted over their counterparts in `/system`.
- To **replace a directory entirely**: create a `.replace` file inside it.
- To **delete** a file: `mknod $MODPATH/system/path/to/file c 0 0`

### KSU (OverlayFS via meta-overlayfs metamodule)

- Files in `system/` are overlaid via the kernel's OverlayFS.
- To **replace a directory**: set opaque attribute via
  `setfattr -n trusted.overlay.opaque -v y <dir>`.
  KSU handles this automatically when you use the `REPLACE` variable.
- To **delete** a file: `mknod $MODPATH/system/path/to/file c 0 0` (whiteout).
  KSU handles this automatically when you use the `REMOVE` variable.
- `system/` overlay is **only active** if a compatible metamodule (e.g.
  `meta-overlayfs`) is installed. Scripts, `system.prop`, and `sepolicy.rule`
  work without a metamodule.

### Vendor / product / system_ext

Place files at these paths inside `system/`:

```
system/vendor/...     -> overlaid onto /vendor
system/product/...    -> overlaid onto /product
system/system_ext/... -> overlaid onto /system_ext
```

Both Magisk and KSU handle partition-agnostic mounting transparently.

---

## 6. system.prop

```properties
# Loaded via resetprop at boot
# Format identical to build.prop
ro.adb.secure=0
persist.sys.usb.config=mtp,adb
debug.sf.hw=1
```

Rules:
- One `key=value` per line, Unix LF.
- Use `ro.` prefix for read-only props; use `persist.` for persistent props.
- Props here are set with `resetprop -n` (pre-Zygote) and again with `resetprop`
  (no `-n`) post-boot. The `-n` flag skips native property callbacks.

---

## 7. sepolicy.rule

```
# One policy statement per line
# Uses magiskpolicy / ksupolicy syntax (superpolicy language)
allow untrusted_app shell_exec:file execute
allow system_server myservice:unix_stream_socket connectto
```

Useful references:
- `allow <source> <target>:<class> <permission>`
- `auditallow`, `dontaudit`, `neverallow` follow same syntax.
- Test rules with: `magiskpolicy --test --apply sepolicy.rule`

---

## 8. Cross-Compatibility Patterns

### Pattern: Single ZIP, both managers

```sh
# customize.sh
ui_print "- Detecting root manager..."
if [ "$KSU" = "true" ]; then
    ui_print "  KernelSU $KSU_VER (kernel $KSU_KERNEL_VER_CODE)"
    KSU_COMPAT=1
else
    ui_print "  Magisk $MAGISK_VER"
    KSU_COMPAT=0
fi

# Conditional ABI installation
case "$ARCH" in
    arm64) ABI_DIR="arm64-v8a" ;;
    arm)   ABI_DIR="armeabi-v7a" ;;
    x64)   ABI_DIR="x86_64" ;;
    x86)   ABI_DIR="x86" ;;
esac
ui_print "- Installing $ARCH ($ABI_DIR) binaries"
cp "$TMPDIR/libs/$ABI_DIR/libmymod.so" "$MODPATH/system/lib64/"

# API level guard — adjust the floor to match your module's requirements
if [ "$API" -lt 29 ]; then
    abort "! This module requires Android 10 (API 29) or higher"
fi
```

### Pattern: runtime detection in service.sh

```sh
#!/system/bin/sh
MODDIR=${0%/*}

# Detect manager at runtime
if [ "$KSU" = "true" ]; then
    MANAGER="KernelSU/SukiSU"
    MANAGER_BIN="/data/adb/ksu/bin/busybox"
elif [ "$APATCH" = "true" ]; then
    MANAGER="APatch"
    MANAGER_BIN="/data/adb/ap/bin/busybox"
else
    MANAGER="Magisk"
    MANAGER_BIN="/data/adb/magisk/busybox"
fi

echo "[$MANAGER] Module service started" >> /data/local/tmp/mymod.log
```

### Pattern: SUSFS awareness

SukiSU-Ultra (and some KSU builds) mount SUSFS — a kernel-level filesystem
hiding layer used to conceal root from apps. Modules must not conflict with it.

Rules:
- Never bind-mount over `/data/adb/` or any SUSFS-managed path from inside your module.
- Do not create files under paths SUSFS hides (consult your SUSFS config). Stick to `$MODDIR`, `/data/local/tmp/`, or your own `/data/<your-namespace>/` directory.
- If your module depends on SUSFS being present, document this in `module.prop` description and in any user-facing README.
- If your module should work without SUSFS, test on both SUSFS-enabled and SUSFS-disabled builds.

### Pattern: KSU-only features with Magisk fallback

```sh
# post-fs-data.sh
MODDIR=${0%/*}

if [ "$KSU" = "true" ]; then
    # Use KSU post-mount hook (service.sh or post-mount.sh is better here)
    :
fi

# Common logic for both
resetprop -n ro.secure 0
```

---

## 9. Zygisk (Magisk) & ZygiskNext (KSU)

### Magisk native Zygisk

Place compiled `.so` libraries under `zygisk/`:
```
zygisk/
├── arm64-v8a.so
├── armeabi-v7a.so
├── x86.so
├── x86_64.so
└── unloaded     <- create this file to mark libs as incompatible/disabled
```

### KSU + ZygiskNext

KSU has no built-in Zygisk. Users install
[ZygiskNext](https://github.com/Dr-TSNG/ZygiskNext) as a separate module.
The Zygisk module directory layout is **identical** to Magisk's — no changes
needed in your module. Document the ZygiskNext dependency in `module.prop`
description and in any user-facing README.

---

## 10. Update JSON and Module Repository Publishing

### update.json (OTA self-update)

```json
{
    "version": "v1.2.0",
    "versionCode": 120,
    "zipUrl": "https://example.com/releases/mymod-v1.2.0.zip",
    "changelog": "https://example.com/releases/changelog.md"
}
```

Reference this URL in `module.prop`:
```
updateJson=https://example.com/mymod/update.json
```

### Publishing via MMRL-compatible repositories

The Magisk online module repository is inactive. Active repositories as of 2025:

| Repository | URL | Notes |
|---|---|---|
| MMRL module repo (Androidacy AMR) | https://repo.androidacy.com | Most widely used; MMRL default |
| MMAR (Magisk Module Alt Repo) | https://github.com/Magisk-Modules-Alt-Repo | GitHub-based; open submissions |
| MMRL itself | https://github.com/MMRLApp/MMRL | The app; hosts a repo index |

To submit to MMAR: fork the repo, add your module entry to the index JSON, and open a pull request. MMRL will pick it up automatically from the index.

For Androidacy AMR, follow the submission process at `https://www.androidacy.com/module-repository/`.

---

## 11. KSU WebUI (optional)

KSU (and SukiSU-Ultra) support a web-based settings UI rendered inside the
manager app. MMRL also renders WebUI panels for modules it manages.

### Directory structure

```
$MODID/
└── webroot/
    ├── index.html       <- entry point
    ├── style.css        <- optional
    └── main.js          <- optional
```

In `module.prop`:
```
webuiIcon=icon/webui.png
```

### KSU WebUI JS API

The `ksu` object is injected by the manager into the WebUI's `window` context.

```javascript
// Execute a shell command as root and get stdout/stderr
const result = await ksu.exec("getprop ro.build.version.release");
// result: { errno: 0, stdout: "14\n", stderr: "" }

// Show a toast notification in the manager app
ksu.toast("Settings saved.");

// Read a key from the module's persistent config store
const value = await ksu.moduleConfig.get("my_module_id", "my_key");

// Write a key to the module's persistent config store
await ksu.moduleConfig.set("my_module_id", "my_key", "my_value");

// Spawn a background service command (fire-and-forget)
ksu.spawn("sh", ["-c", "/data/adb/modules/my_module/action.sh"]);
```

### Minimal working WebUI

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Module</title>
</head>
<body>
  <h2>My Module Settings</h2>

  <label>
    <input type="checkbox" id="toggle">
    Enable feature
  </label>

  <button id="apply">Apply</button>
  <p id="status"></p>

  <script>
    const MODULE_ID = "my_module";
    const KEY = "feature_enabled";

    // Load saved setting
    window.addEventListener("load", async () => {
      const val = await ksu.moduleConfig.get(MODULE_ID, KEY);
      document.getElementById("toggle").checked = val === "1";
    });

    // Save on apply
    document.getElementById("apply").addEventListener("click", async () => {
      const enabled = document.getElementById("toggle").checked ? "1" : "0";
      await ksu.moduleConfig.set(MODULE_ID, KEY, enabled);
      ksu.toast("Saved. Reboot to apply.");
      document.getElementById("status").textContent = "Saved.";
    });
  </script>
</body>
</html>
```

### WebUI notes

- `ksu.exec` is asynchronous. Always `await` it and check `errno` before using
  `stdout`. A non-zero `errno` means the command failed.
- The `ksu` object is only available inside the manager app's WebView. Do not
  use it in browser-based testing — it will be undefined.
- MMRL renders `webroot/index.html` in its own module detail panel in addition
  to the KSU app. Ensure your UI degrades gracefully if `ksu` is undefined:
  ```javascript
  if (typeof ksu === "undefined") {
    document.body.innerHTML = "<p>Open this in KSU or MMRL.</p>";
  }
  ```
- Refer to https://kernelsu.org/guide/module-webui.html for the full API
  surface; the JS API surface changes across KSU versions.

---

## 12. Action Button (action.sh and WebUI trigger)

`action.sh` runs when the user taps the "Action" button in Magisk or KSU.
Use it for one-shot operations: toggle a feature, force-apply settings, clear
a cache, or run a diagnostic.

### action.sh patterns

```sh
#!/system/bin/sh
# Runs as root when user taps Action in the manager UI
MODDIR=${0%/*}

# Pattern 1: Toggle a flag file
FLAG="$MODDIR/flags/feature_enabled"
if [ -f "$FLAG" ]; then
    rm "$FLAG"
    # Output shown in manager UI toast (KSU) or log (Magisk)
    echo "Feature disabled."
else
    mkdir -p "$MODDIR/flags"
    touch "$FLAG"
    echo "Feature enabled."
fi

# Pattern 2: Apply a setting immediately without reboot
resetprop ro.example.setting 1
echo "Property applied."

# Pattern 3: Collect a diagnostic log and place it where the user can find it
LOGFILE="/sdcard/mymod-diag-$(date +%Y%m%d-%H%M%S).txt"
{
    echo "=== My Module Diagnostic ==="
    echo "Date: $(date)"
    echo "Manager: $( [ '$KSU' = 'true' ] && echo KernelSU || echo Magisk )"
    getprop | grep "ro.build"
    cat /proc/mounts | grep "$MODID"
} > "$LOGFILE"
echo "Log saved to $LOGFILE"
```

### Triggering action.sh from WebUI

```javascript
// In webroot/main.js — run action.sh when user clicks a button
document.getElementById("run-action").addEventListener("click", async () => {
  const result = await ksu.exec(
    "sh /data/adb/modules/my_module/action.sh"
  );
  if (result.errno === 0) {
    ksu.toast(result.stdout.trim());
  } else {
    ksu.toast("Action failed: " + result.stderr.trim());
  }
});
```

**Notes:**
- `action.sh` output is shown as a toast in KSU. In Magisk it goes to the
  app's module log. Keep output short — one or two lines maximum.
- Do not run long-blocking operations in `action.sh`. For heavy work, spawn a
  background process and return immediately.
- `action.sh` is not guaranteed to run before `service.sh` on every manager.
  Never depend on execution order between them.

---

## 13. Packaging the ZIP

For the full build script with dependency checks, see
`references/build-reference.md`.

Quick reference — essential ZIP commands:

```sh
#!/bin/bash
MODID="my_module"
VERSION="v1.0.0"
OUT="${MODID}-${VERSION}.zip"

rm -f "$OUT"
mkdir -p META-INF/com/google/android

# NOTE: This raw GitHub URL tracks the master branch and may change between
# Magisk releases. See references/build-reference.md for a hardened version
# with a fallback instruction.
curl -fsSL -o META-INF/com/google/android/update-binary \
  https://raw.githubusercontent.com/topjohnwu/Magisk/master/scripts/module_installer.sh

echo "#MAGISK" > META-INF/com/google/android/updater-script

zip -r9 "$OUT" \
    META-INF module.prop customize.sh system system.prop \
    sepolicy.rule post-fs-data.sh service.sh \
    boot-completed.sh post-mount.sh action.sh uninstall.sh

echo "Built: $OUT"
```

---

## 14. Common Pitfalls & Forbidden Patterns

| Don't do this | Do this instead |
|---|---|
| `exit 1` in customize.sh | `abort "reason"` |
| `echo "msg"` in install scripts | `ui_print "msg"` |
| Hardcode `/data/adb/modules/mymod` | Use `$MODDIR` or `$MODPATH` |
| `setprop` in post-fs-data | `resetprop -n key value` |
| Use `MAGISK_VER_CODE` to detect KSU | Check `$KSU = "true"` |
| Create `install.sh` in ZIP | Use `customize.sh` only |
| Modify `update-binary` with custom logic | It gets overwritten by Magisk app |
| Mix CRLF line endings in scripts | Always use LF (`\n`) |
| `id` starting with a digit or dash | Must match `^[a-zA-Z][a-zA-Z0-9._-]+$` |
| Call `su` from inside module scripts | Scripts already run as root |
| Use `/sbin` paths for Magisk tmpfs | Use `${MAGISKTMP}` in rc scripts |
| Module has no system/ folder but no skip_mount flag | Create an empty file named `skip_mount` at the module root |

---

## 15. Minimal Working Module Template

A coding agent should produce at minimum the following files for any module:

### module.prop
```properties
id=my_module
name=My Module
version=v1.0.0
versionCode=1
author=Author
description=What this module does
```

### customize.sh
```sh
# Sourced by module installer — do NOT call exit
SKIPUNZIP=0

ui_print "- Installing My Module..."

# Detect root manager
if [ "$KSU" = "true" ]; then
    ui_print "  Root manager: KernelSU $KSU_VER"
else
    ui_print "  Root manager: Magisk $MAGISK_VER"
fi

# Architecture and API info
ui_print "- Architecture: $ARCH (API $API)"

# Minimum API guard — Android 8.0 (API 26); adjust floor to match your module
if [ "$API" -lt 26 ]; then
    abort "! Android 8.0 (API 26) or higher required"
fi

ui_print "- Done."
```

### service.sh
```sh
#!/system/bin/sh
MODDIR=${0%/*}
# Module is enabled and boot has completed by the time this runs
# Your non-blocking startup logic here
```

---

## 16. Bootloop Recovery and On-Device Testing

Bootloops are the most common failure mode for module hobbyists. Always include
this information in any generated README.

### Disabling a broken module without boot

If a module causes a bootloop, the user can disable it before Android finishes
booting:

```
Method 1 — Volume key safe mode (Magisk):
  Hold Volume Down while the boot animation plays. Magisk will disable all
  modules for that boot only.

Method 2 — Create a disable file (all managers):
  Boot into TWRP or another recovery. Create an empty file at:
  /data/adb/modules/<MODID>/disable
  The manager will skip loading that module on next boot.

Method 3 — Delete the module folder:
  Boot into recovery. Delete /data/adb/modules/<MODID>/ entirely.
```

Always document Method 2 in your module's README so users can recover without
wiping.

### Testing a module on-device before releasing

```sh
# Install directly via Magisk CLI (no app UI needed)
magisk --install-module /path/to/module.zip

# Watch Magisk and module-related logs during boot
adb logcat -s Magisk | tee /tmp/magisk-boot.log

# Check if your module is loaded
ls /data/adb/modules/

# Verify bind-mount is active (Magisk magic mount)
cat /proc/mounts | grep "$MODID"

# Verify resetprop changes took effect
getprop ro.debuggable

# Check for SELinux denials caused by your module
adb logcat | grep "avc: denied"
```

### Safe test cycle before publishing

1. Flash the module ZIP in the manager app.
2. Reboot and capture `adb logcat -s Magisk` for the full boot sequence.
3. Verify your target files are present under the bind-mount tree.
4. Test intended functionality (the actual reason for the module).
5. Verify no unexpected SELinux denials in logcat.
6. Test uninstall: remove the module, reboot, confirm clean state.
7. Test on a second device or Android version if possible.

---

## 17. Play Integrity Safety for Module Authors

Play Integrity (successor to SafetyNet, mandatory from early 2025) runs
integrity checks inside the Play Services process. Modules that modify system
paths or hook system processes can fail these checks and break banking apps,
Google Wallet, and apps that enforce device attestation.

> **APatch SuperKey note:** APatch uses a SuperKey with higher privileges than standard root. Treat it as a root credential: never store it in module files, never log it, and never expose it via WebUI or action.sh output. A compromised SuperKey cannot be revoked without re-patching the kernel.

### What triggers Play Integrity failures

| Module behavior | Risk level |
|---|---|
| Modifying files under `/system/` via magic mount | Low (generally safe) |
| Patching or hooking GMS/Play Services processes via Zygisk | High |
| Modifying `build.prop` or `ro.*` props to spoof device model | High (intentional, use PIF) |
| Writing to `/data/data/com.google.android.gms/` | Critical — never do this |
| Installing SELinux rules that affect GMS contexts | Medium |
| Changing `ro.debuggable` or `ro.secure` | Medium |

### Rules for module authors

- If your module hooks GMS or modifies device attestation properties, declare
  that it requires a Play Integrity Fix (PIF) companion module. Document this
  in `module.prop` description and README.
- If your module modifies system paths that GMS reads, test with Play Integrity
  check apps (`Simple Play Integrity Checker` on Play Store) before releasing.
- Never write to `/data/data/com.google.android.gms/` or any GMS data path.
- Respect DenyList / Umount Modules on a per-app basis. If your module should
  be hidden from specific apps, document how users should configure DenyList.
- Document clearly if your module is incompatible with TrickyStore or ReZygisk
  stacks — do not silently break them.

### Play Integrity companion module reference

- PIF (Play Integrity Fix): https://github.com/chiteroman/PlayIntegrityFix
- TrickyStore: https://github.com/5ec1cff/TrickyStore
- ReZygisk: https://github.com/PerformanC/ReZygisk

---

## References

### Official documentation

- Magisk Developer Guides: https://topjohnwu.github.io/Magisk/guides.html
- Magisk module_installer.sh: https://github.com/topjohnwu/Magisk/blob/master/scripts/module_installer.sh
- KernelSU Module Guide: https://kernelsu.org/guide/module.html
- KernelSU Metamodule Guide: https://kernelsu.org/guide/metamodule.html
- KernelSU WebUI Guide: https://kernelsu.org/guide/module-webui.html
- KernelSU Module Config: https://kernelsu.org/guide/module-config.html
- SukiSU-Ultra: https://github.com/SukiSU-Ultra/SukiSU-Ultra
- SUSFS for KSU: https://gitlab.com/simonpunk/susfs4ksu
- ZygiskNext (KSU Zygisk support): https://github.com/Dr-TSNG/ZygiskNext
- Zygisk Module Sample: https://github.com/topjohnwu/zygisk-module-sample
- Linux OverlayFS docs: https://docs.kernel.org/filesystems/overlayfs.html
- MMRL App: https://github.com/MMRLApp/MMRL
- Magisk Modules Alt Repo (MMAR): https://github.com/Magisk-Modules-Alt-Repo

### Skill references

- `references/customize-api.md` — full variable and function reference for customize.sh
- `references/build-reference.md` — hardened build script with dependency checks
- `references/module-recipes.md` — canonical templates for common module archetypes
