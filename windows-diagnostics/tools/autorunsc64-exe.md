**autorunsc64.exe** [ADMIN]
Purpose: CLI version of Autoruns. Enumerate all autostart entries.
Flags: `-accepteula -a *` (all categories) | `-c` (CSV output) | `-nobanner` | `-s` (verify signatures) | `-v` (VirusTotal check) | `-u` (unsigned only)
Output: CSV. Columns: Time, Entry Location, Entry, Enabled, Category, Profile, Description, Signer, Company, Image Path, Version, Launch String, VT detection, VT permalink.
Chaining: Feeds image paths to `sigcheck64` and `strings64`.
Example: `.\systeminternals\autorunsc64.exe -accepteula -nobanner -a * -c -s > .\autoruns.csv`

