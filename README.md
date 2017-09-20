## RemoteKeylogger

# Description
This is keylogger tool which will stream keys from a victim machine to a remote python server

# Setup
To setup the server, simple copy `server.py` onto an internet-facing linux machine (a VPS would do) and run the server code using python
i.e `python server.py`

The server is automatically set to open port 31337...DO NOT CHANGE THIS.

To setup your own binary exe, run the setup tool and enter the IP address of your callback server when prompted.

The setup tool will then generate an exe by the name of `keylogger.exe`

`keylogger.exe` will be the malware file that you will put on the target machine.
This file can be renamed to anything you want.

Keylogs will be saved to the server backend in the same directory as `server.py` and will be named by the IP address of the victim the log came from.

# Connecting to the server
You can connect to the server as a client by making a telnet connection to your server's IP address via port `12345`

Login using the default username and password
username: username
password: password

These default passwords can be changed in the code.

If you would like to add more logins, there is a file by the name `ADMINS.txt` which will be found in the same directory as `server.py`
You can add one login per line in this file using the following format...<br />
`username1:password1`<br />
`username2:password2`<br />
`username3:password3`<br />
`username4:password4`<br />

# Drawbacks of this being a FREE and PUBLIC tool
Because this tool is free, there will be some limitations to preserve analysis in the wild.
Unlike the private version of my Remote Access Tool(DARTEN) which this sources from, There is no...<br />
	`-Directory Traversal`<br />
	`-Process Hollowing`<br />
	`-File Dropping`<br />
	`-Dll Injection`<br />
	`-Dynamic Registry Modification`<br />
	`-Process Monitoring`<br />

# Persistance
This tool does create a registry key to ensure persistance
