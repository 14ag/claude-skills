# Tool Catalog

This catalog organizes 80+ Sysinternals and NirSoft tools into 8 capability domains.

For detailed specifications of each tool (flags, output formats, prerequisites, chaining notes, and examples), see the individual tool files in `tools/`.

## A. Process & Memory

- [procexp64.exe](tools/procexp64-exe.md) — Interactive process explorer with full process tree, DLL, and handle detail.
- [Procmon64.exe](tools/Procmon64-exe.md) — Real-time file system, registry, and process/thread activity monitor.
- [procdump64.exe](tools/procdump64-exe.md) — Capture process memory dumps on trigger conditions (CPU spike, crash, hang).
- [pslist64.exe](tools/pslist64-exe.md) — List running processes with CPU and memory stats.
- [pskill64.exe](tools/pskill64-exe.md) — Terminate a process by name or PID.
- [pssuspend64.exe](tools/pssuspend64-exe.md) — Suspend or resume a process without terminating it.
- [handle64.exe](tools/handle64-exe.md) — Show open file, registry, and object handles for all or specific processes.
- [vmmap64.exe](tools/vmmap64-exe.md) — Visualise virtual memory layout of a process.
- [RAMMap64.exe](tools/RAMMap64-exe.md) — Physical memory usage breakdown by type (file, heap, standby, etc.).
- [Listdlls.exe](tools/Listdlls-exe.md) — List DLLs loaded by processes, including unsigned or unsigned-path DLLs.
- [ProcessActivityView.exe](tools/ProcessActivityView-exe.md) — Show file and registry activity of a running process.
- [ProcessThreadsView.exe](tools/ProcessThreadsView-exe.md) — Display threads of a process with start address and module info.
- [HeapMemView.exe](tools/HeapMemView-exe.md) — Display heap memory blocks allocated by a process.
- [GDIView.exe](tools/GDIView-exe.md) — Monitor GDI object usage per process to detect GDI handle leaks.
- [Cacheset64.exe](tools/Cacheset64-exe.md) — View and adjust the system file cache working set size.
- [CPUSTRES64.exe](tools/CPUSTRES64-EXE.md) — Stress CPU threads to test thermal and stability limits.
- [shmnview.exe](tools/shmnview-exe.md) — Display shared memory sections and the processes accessing them.

## B. Network & Traffic

- [tcpvcon64.exe](tools/tcpvcon64-exe.md) — List active TCP and UDP connections with owning process.
- [tcpview64.exe](tools/tcpview64-exe.md) — Interactive GUI network connection viewer with real-time updates.
- [psping64.exe](tools/psping64-exe.md) � Measure TCP/UDP latency and bandwidth; ICMP ping with statistics.
- [whois64.exe](tools/whois64-exe.md) � WHOIS lookup for IP addresses and domain names.
- [cports.exe](tools/cports-exe.md) � Display open TCP/UDP ports with process and module info.
- [NetworkTrafficView.exe](tools/NetworkTrafficView-exe.md) � Capture and display network traffic statistics per connection.
- [smsniff.exe](tools/smsniff-exe.md) � Packet sniffer that captures raw network packets.
- [WebSiteSniffer.exe](tools/WebSiteSniffer-exe.md) � Capture HTTP/HTTPS web traffic and save page content.
- [WebCookiesSniffer.exe](tools/WebCookiesSniffer-exe.md) � Capture cookies transmitted over HTTP/HTTPS.
- [WirelessKeyView.exe](tools/WirelessKeyView-exe.md) � Recover WEP/WPA keys stored on the local machine.

## C. Disk & File System

- [du64.exe](tools/du64-exe.md) � Report disk usage for a directory tree.
- [diskext64.exe](tools/diskext64-exe.md) � Show disk extents (physical location) for volumes.
- [Diskmon64.exe](tools/Diskmon64-exe.md) � Monitor real-time disk I/O activity.
- [DiskView64.exe](tools/DiskView64-exe.md) � Graphical cluster map of disk usage.
- [ntfsinfo64.exe](tools/ntfsinfo64-exe.md) � Display NTFS volume metadata (cluster size, MFT location, etc.).
- [Contig64.exe](tools/Contig64-exe.md) � Defragment individual files or analyse fragmentation.
- [streams64.exe](tools/streams64-exe.md) � List or delete NTFS alternate data streams on files or directories.
- [FindLinks64.exe](tools/FindLinks64-exe.md) � Find all hard links pointing to a file.
- [junction64.exe](tools/junction64-exe.md) � Create, list, or delete NTFS junction points (directory symlinks).
- [sdelete64.exe](tools/sdelete64-exe.md) � Securely delete files or wipe free space.
- [sync64.exe](tools/sync64-exe.md) � Flush file system buffers to disk.
- [movefile64.exe](tools/movefile64-exe.md) � Schedule a file move or delete to occur at next reboot.
- [pendmoves64.exe](tools/pendmoves64-exe.md) � List pending file rename/delete operations scheduled for next boot.
- [OpenedFilesView.exe](tools/OpenedFilesView-exe.md) � Show all files currently opened by processes on the system.
- [disk2vhd64.exe](tools/disk2vhd64-exe.md) — Create a VHD/VHDX snapshot of a live volume.
- [Volumeid64.exe](tools/Volumeid64-exe.md) — Change the volume ID (serial number) of FAT and NTFS volumes.
- [pagedfrg.exe](tools/pagedfrg-exe.md) � Defragment paged pool, non-paged pool, and registry hives.

## D. Registry

- [Autoruns64.exe](tools/Autoruns64-exe.md) — GUI view of all autostart locations across the system.
- [autorunsc64.exe](tools/autorunsc64-exe.md) — CLI version of Autoruns. Enumerate all autostart entries.
- [RegScanner.exe](tools/RegScanner-exe.md) — Search the registry for values, keys, or data matching a pattern.
- [RegFromApp.exe](tools/RegFromApp-exe.md) — Monitor and log registry changes made by a specific process.
- [RegDelNull64.exe](tools/RegDelNull64-exe.md) — Scan and optionally delete registry keys containing embedded null characters.
- [regjump.exe](tools/regjump-exe.md) — Open Regedit and jump directly to a specified registry path.
- [ru64.exe](tools/ru64-exe.md) — Show registry disk usage by key, useful for inventorying large hives.
- [RegDllView.exe](tools/RegDllView-exe.md) — Display registered DLL/OCX/ActiveX files in the Windows registry.

## E. System Info & Security

- [PsInfo64.exe](tools/PsInfo64-exe.md) — Display system information (OS version, uptime, CPU, RAM, hotfixes).
- [Coreinfo64.exe](tools/Coreinfo64-exe.md) — Display CPU topology, cache, NUMA, and virtualisation features.
- [Clockres64.exe](tools/Clockres64-exe.md) — Report the current system timer resolution.
- [accesschk64.exe](tools/accesschk64-exe.md) — Show effective permissions for users or groups on files, registry keys, services, and objects.
- [AccessEnum.exe](tools/AccessEnum-exe.md) — Scan a directory or registry tree and show where permissions differ from parent.
- [sigcheck64.exe](tools/sigcheck64-exe.md) — Verify file signatures, check VirusTotal, and display version info.
- [strings64.exe](tools/strings64-exe.md) — Extract printable strings from binary files.
- [efsdump.exe](tools/efsdump-exe.md) — Display EFS encryption information for files.
- [DriverView.exe](tools/DriverView-exe.md) — List all loaded kernel drivers with version and path info.
- [LoadOrd64.exe](tools/LoadOrd64-exe.md) — Show the order in which drivers and services are loaded at boot.
- [LoadOrdC64.exe](tools/LoadOrdC64-exe.md) — Console version of LoadOrd for scripting and automation.
- [logonsessions64.exe](tools/logonsessions64-exe.md) — List active logon sessions and the processes running in each.
- [PsLoggedon64.exe](tools/PsLoggedon64-exe.md) — Show users logged on locally and via resource shares.
- [pipelist64.exe](tools/pipelist64-exe.md) — List named pipes on the system.
- [ShareEnum64.exe](tools/ShareEnum64-exe.md) — Enumerate network shares and their permissions.
- [Winobj64.exe](tools/Winobj64-exe.md) — Browse the Windows Object Manager namespace.
- [RootkitRevealer.exe](tools/RootkitRevealer-exe.md) — Advanced rootkit detection using API comparison techniques.
- [shexview.exe](tools/shexview-exe.md) — View and disable Shell Extension handlers.
- [dllexp.exe](tools/dllexp-exe.md) — Display exported functions from DLL files.
- [FileTypesMan.exe](tools/FileTypesMan-exe.md) — View and edit file type associations in the registry.
- [URLProtocolView.exe](tools/URLProtocolView-exe.md) — Display registered URL protocol handlers.
- [SpecialFoldersView.exe](tools/SpecialFoldersView-exe.md) — Display paths of all Windows special folders.
- [Testlimit64.exe](tools/Testlimit64-exe.md) — Test Windows limits by consuming handles, threads, memory, or other resources.
- [notmyfault64.exe](tools/notmyfault64-exe.md) — Deliberately crash the system or leak memory for testing crash dump configuration.
- [notmyfaultc64.exe](tools/notmyfaultc64-exe.md) — Console version of notmyfault for scripted crash testing.
- [ldmdump.exe](tools/ldmdump-exe.md) — Dump Logical Disk Manager (LDM) database information for dynamic disks.
- [exiftool.exe](tools/exiftool-exe.md) — Read and write metadata from image, audio, video, and document files.
- [sysexp.exe](tools/sysexp-exe.md) — System Explorer for viewing processes, modules, windows, and system information.

## F. Monitoring & Logging

- [Sysmon64.exe](tools/Sysmon64-exe.md) � Log detailed process creation, network, file, and registry events to the Windows Event Log.
- [dbgview64.exe](tools/dbgview64-exe.md) � Capture OutputDebugString and kernel debug messages in real time.
- [livekd64.exe](tools/livekd64-exe.md) � Run kernel debugger commands against a live system without a remote debugger.
- [psloglist64.exe](tools/psloglist64-exe.md) � Dump Windows event log entries from local or remote systems.

## G. Remote & Admin Operations

- [PsExec64.exe](tools/PsExec64-exe.md) � Execute processes on remote systems with optional interactive session.
- [PsService64.exe](tools/PsService64-exe.md) � View and control services on local or remote systems.
- [psfile64.exe](tools/psfile64-exe.md) � List files opened remotely on the local system via network shares.
- [PsGetsid64.exe](tools/PsGetsid64-exe.md) � Translate between account names and SIDs.
- [psshutdown64.exe](tools/psshutdown64-exe.md) � Shut down, restart, or log off local or remote systems.
- [ShellRunas.exe](tools/ShellRunas-exe.md) — Launch a program as a different user from the shell context menu.
- [pspasswd64.exe](tools/pspasswd64-exe.md) — Change account passwords on local or remote Windows systems.
- [RDCMan.exe](tools/RDCMan-exe.md) � Manage multiple Remote Desktop connections in a tabbed GUI.

## H. Active Directory

- [ADExplorer64.exe](tools/ADExplorer64-exe.md) � Browse and snapshot Active Directory as an LDAP client.
- [ADInsight64.exe](tools/ADInsight64-exe.md) � Real-time LDAP traffic analyser — captures all LDAP calls from client applications.
- [adrestore64.exe](tools/adrestore64-exe.md) � List and restore deleted Active Directory objects from the tombstone.

