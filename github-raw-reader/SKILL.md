---
name: github-raw-reader
description: Teach agent access public repo files via GitHub Raw URLs. Bypass HTML pages for direct source code parsing.
---

# GitHub Raw Access Skill

Access repository files via direct raw URLs or git clone. Two methods are available — use Method A first, fall back to Method B if `raw.githubusercontent.com` is blocked.

---

## Method A — Raw URL (preferred)

### Step 1: Enumerate files

Tree pages (`/tree/`) return full HTML via `curl` and contain all file/subdir paths. Use this to enumerate before constructing raw URLs.

**Root listing:**
```bash
curl -s "https://github.com/<user>/<repo>/tree/<branch>" \
  | grep -oP '"/<user>/<repo>/(?:blob|tree)/<branch>/[^"&]+"' \
  | sort -u
```

**Subdir listing (recurse for each `tree/` path found):**
```bash
curl -s "https://github.com/<user>/<repo>/tree/<branch>/<subdir>" \
  | grep -oP '"/<user>/<repo>/(?:blob|tree)/<branch>/[^"&]+"' \
  | sort -u
```

`blob/` entries are files. `tree/` entries are subdirectories — recurse into them.

### Step 2: Convert blob URLs to raw URLs

| From | To |
| :--- | :--- |
| `https://github.com/` | `https://raw.githubusercontent.com/` |
| `/blob/` | `/` (remove) |

**Example:**
- Input:  `https://github.com/14ag/python-arc/blob/master/2024/snake_essentials.py`
- Output: `https://raw.githubusercontent.com/14ag/python-arc/master/2024/snake_essentials.py`

### Step 3: Fetch file content

```bash
curl -s "https://raw.githubusercontent.com/<user>/<repo>/<branch>/<path/to/file>"
```

---

## Method B — Git sparse clone (fallback)

Use when `raw.githubusercontent.com` is blocked but `github.com` git smart HTTP is reachable. This uses the git pack protocol over HTTPS, which is allowed even in restricted environments.

```bash
# Clone with no blobs (tree only), then sparse-checkout the needed paths
git clone --depth=1 --no-tags --filter=blob:none --sparse \
  https://github.com/<user>/<repo>.git /tmp/repo

cd /tmp/repo
git sparse-checkout set <subdir1>/ <subdir2>/

# Read any file directly
cat /tmp/repo/<path/to/file>
```

To verify git smart HTTP is reachable before cloning:
```bash
curl -s "https://github.com/<user>/<repo>.git/info/refs?service=git-upload-pack" | head -c 4
# Should return a git pkt-line (e.g. "001e"), not "Host not in allowlist"
```

---

## Notes

- **`/tree/` pages**: accessible via `curl`, return full HTML with file listings.
- **`/blob/` pages**: return 0 bytes via `curl` (JS-rendered). Do not use for enumeration.
- **`github.com/raw/<branch>/<path>`**: redirects to `raw.githubusercontent.com` — blocked if the CDN domain is.
- **Branch name**: default is usually `main` or `master`. Check `packed-refs` after clone, or inspect the root tree page title if unsure.
- Always fetch raw content. Do not parse rendered HTML for code.
