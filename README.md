
# Nagios check_haproxy
## requirements:
- python 2.7, python 3.7
- requests

use url to check haproxy backend status
default port is 8000

Options:

  - --version             show program's version number and exit
  - -h, --help            show this help message and exit
  - -u URL, --url=URL     url haproxy stat default 127.0.0.1
  - -U USER, --user=USER  user to login in
  - -P PASSWORD, --pass=PASSWORD
                        haproxy password
  - -p PORT               port stats default 8000

check_haproxy.py -u http://127.0.0.1 -U admin -P admin -P 8001
