# mxBak
This tool downloads the config file for all mobotix cameras listed in the csv file. The *.cfg file will be placed in a folder matching the computers current date.

Prerequisites
Python 3.X (https://www.python.org/downloads/)

 1. Create a csv file named in the same folder as main.py called input.csv with header rows for url,login,password each row should contain the cameras ip or hostname followed by :portNumber, user name, and password.
 The login specified in the csv file must be able to access http://xxx.xxx.xxx.xxx/admin/m1cam.cfg

url,login,password
000.000.000.001:80,admin,password
000.000.000.002:80,admin,password


usage: main.py [-h] [-i INPUT]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        specify name of input file, default: 'input.cs