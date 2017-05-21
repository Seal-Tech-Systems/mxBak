Prerequisites
Python 3.X (https://www.python.org/downloads/)


1. Create a csv file named in the same folder as main.py called input.csv with header rows for url,login,password each row should contain the cameras ip or hostname followed by :portNumber, user name, and password. If public access is enabled than leave username and password blank. If public access is disabled any user account that can load http://000.000.000.000/control/camerainfo will work.

In this example the first camera has public access disabled and the second has it enabled

url,login,password
http://000.000.000.001:80,admin,password
http://000.000.000.002:80,


2. Navigate to the location where main.py is stored and execute main.py

usage: main.py [-h] [-i INPUT] [-n] [-s] [-x XSIZE] [-y YSIZE] [-q QUALITY]
               [-g] [-c]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        specify name of input file, default:
                        'CONFIGS_FOLDER/input.csv'
  -n, --non-interactive
                        Intercative mode
  -s, --backupstills    Backup stills
  -x XSIZE, --xsize XSIZE
                        Still X size, default 320
  -y YSIZE, --ysize YSIZE
                        Still Y size, default 240
  -q QUALITY, --quality QUALITY
                        Still quality, default 60
  -g, --generateinfo    Generate info file
  -c, --backupconfigs   Backup config files
  -r, --runcommand      Run Command (from commands.txt)
