# ipscanner

Description
Determining the identity of a webserver is a hard problem. 
One consistant method is to ask the webserver. Unfortunately there's no promise the server will respond honestly.

ipscanner is written as a tool to provide a best guess about webservers based on header response.

ipscanner is written for python3, but may work with some versions of python2.

# Install
ipscanner is written for OSX and linux enviornments running python.

To install, unzip the package and run 
```make install```

To uninstall
```make uninstall```

To clean build folders
```make clean```

For other make targets see makefile

# Usage

Example:
```ipscanner --ips 159.89.34.233, google.com --all --json```

Expected Result:
```[{"url": "http://159.89.34.233,", "listable": null}, {"url": "https://159.89.34.233,", "listable": null}, {"url": "http://google.com", "listable": false}, {"url": "https://google.com", "listable": false}]```

## Flags
```  -h, --help            show this help message and exit
  --ips [IPS [IPS ...]]
                        ips to be scanned,as comma separated list without
                        protocol(http/s)
  --json                Output results as Json
  --all                 Show results for all server types
  --verbose             Verbose output for debugging
```


# Testing
Tests are run using pytest.

All test files are located in the ```tests``` directory and must begin with test_

All tests must pass before install.


# Notes:
 - Alternative to checking Headers: https://www.netcraft.com/
 - wget spider https://superuser.com/questions/642555/
 - List directory contents with bs4 https://stackoverflow.com/questions/11023530