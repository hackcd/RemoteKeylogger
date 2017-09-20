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

# Drawbacks of this being a FREE and PUBLIC tool
Because this tool is free, there will be some limitations to preserve analysis in the wild.
Unlike the private version of my Remote Access Tool(DARTEN) which this sources from, There is no...
	-Directory Traversal
	-Process Hollowing
	-File Dropping
	-Dll Injection
	-Dynamic Registry Modification
	-Process Monitoring

# Persistance
This tool does create a registry key to ensure persistance
