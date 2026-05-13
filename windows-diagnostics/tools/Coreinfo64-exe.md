**Coreinfo64.exe**
Purpose: Display CPU topology, cache, NUMA, and virtualisation features.
Flags: `-accepteula` | `-c` (cache) | `-n` (NUMA) | `-v` (virtualisation)
Output: Plain text table with feature flags.
Chaining: Precedes `CPUSTRES64` in stability check recipe.
Example: `.\systeminternals\Coreinfo64.exe -accepteula | findstr /V "^$"`

