**disk2vhd64.exe** [ADMIN]
Purpose: Create a VHD/VHDX snapshot of a live volume.
Flags: `-accepteula <volume> <output.vhdx>` | `-c` (use VSS)
Output: Binary VHDX file at specified path.
Prerequisites: Admin required. Specify explicit output path.
Chaining: Use as part of pre-change snapshot recipe.
Example: `.\systeminternals\disk2vhd64.exe -accepteula C: .\snapshot_C.vhdx`

