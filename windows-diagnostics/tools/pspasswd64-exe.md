# pspasswd64.exe - Remote Password Changer

## Purpose
Change account passwords on local or remote Windows systems. Part of PsTools suite for remote system administration.

## Syntax
```powershell
./systeminternals/pspasswd64.exe [\\computer] [username] [new_password] [options]
```

## Key Flags
- `\\computer` - Target computer name or IP address (local if omitted)
- `username` - Account name to change password for
- `new_password` - New password to set
- `-u username` - Username for authentication on remote system
- `-p password` - Password for authentication on remote system
- `-accepteula` - Accept EULA automatically

## Output Format
Returns success/failure status and error messages.

## Prerequisites
- **[ADMIN]** - Requires administrator privileges
- **[DESTRUCTIVE]** - Permanently changes account passwords
- Network connectivity for remote operations
- Administrative credentials on target system

## Examples
```powershell
# Change local user password
./systeminternals/pspasswd64.exe -accepteula localuser NewPassword123

# Change password on remote system
./systeminternals/pspasswd64.exe -accepteula \\REMOTEPC -u admin -p adminpass targetuser NewPassword123

# Change password using current credentials
./systeminternals/pspasswd64.exe -accepteula \\192.168.1.100 serviceaccount NewServicePass456
```

## Use Cases
- **Bulk password changes**: Update passwords across multiple systems
- **Service account management**: Change service account passwords
- **Security response**: Force password changes during incidents
- **Automated deployment**: Set initial passwords on new systems

## Chaining Notes
- **Use with**: PsExec64.exe (remote execution), PsService64.exe (service management)
- **Output to**: Console status messages
- **Parse with**: Check exit code for success/failure

## Error Handling
- **Tool not found**: Check for 32-bit variant (pspasswd.exe)
- **Access denied**: Verify administrative privileges and credentials
- **Network failure**: Check connectivity with psping64.exe
- **Invalid password**: Ensure password meets complexity requirements
- **Account locked**: May need to unlock account first

## Security Considerations
- **Password visibility**: Passwords appear in command line (use with caution)
- **Credential storage**: Avoid storing credentials in scripts
- **Audit logging**: Password changes are logged in Security event log
- **Network traffic**: Credentials transmitted over network (use secure channels)

## Related Tools
- **PsExec64.exe** - Execute commands on remote systems
- **PsService64.exe** - Manage services (for service account passwords)
- **PsLoggedon64.exe** - Check who is logged on before password changes
- **PsInfo64.exe** - Verify system connectivity before operations