import subprocess

# Variables
printer_name = "recepcion_ticket"  # Your Samba printer name
varchivo = "../07042025185812.bin"  # The file you want to print
samba_share = r"//192.168.100.23/recepcion_ticket"  # Samba server share path
username = "printer"
password = "GPS2022."

# Use smbclient to print (authenticate with username and password)
command = f'smbclient {samba_share} -U {username}%{password} -c "print {varchivo}"'

# Execute the command
subprocess.run(command, shell=True)
