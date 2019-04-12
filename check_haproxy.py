# -*- coding: utf-8 -*-
import csv
import requests
from requests.auth import HTTPBasicAuth
from optparse import OptionParser


def build_parser():
    """
    define param command line
    :return: parser config
    """
    parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
    parser.add_option("-u", "--url", dest="url", help="url haproxy")
    parser.add_option("-U", "--user", dest="user", help="user to login in")
    parser.add_option("-P", '--pass', dest="password", help="haproxy password")
    parser.add_option("-p", dest="port", default="8000", help="port stats default 8000")
    return parser


class CheckHaproxy(object):

    def __init__(self, url, user, password, port):
        self.haproxy_csv = ":" + port + "/haproxy?stats;csv"
        self.url = url + self.haproxy_csv
        self.user = user
        self.password = password
        self.status = []

    def get_status(self):
        try:
            res = requests.get(self.url, 'r', auth=HTTPBasicAuth(self.user, self.password))
            text_csv = res.iter_lines()
        
            csv_reader = csv.reader(text_csv, delimiter=',')

            for rows in csv_reader:
                # print(rows)
                if rows[1] != "FRONTEND" and rows[1] != "BACKEND" and rows[1] != "svname":
                    if rows[17] != "UP":
                        self.status.append("backend: {} serveur: {} is OFF line".format(rows[0], rows[1]))

        except Exception as e:
            print("CRITICAL: {}".format(e))
            exit(2)

    def nagios(self):
        if self.status:
            print("CRITITCAL: {}".format(self.status))
            exit(2)
        else:
            print("OK - ALL backend")
            exit(0)


if __name__ == "__main__":
    pars = build_parser()
    options, args = pars.parse_args()
    if len(args) != 0:
        pars.error("wrong number of arguments")
        exit(0)
    else:
        check = CheckHaproxy(options.url, options.user, options.password, options.port)
        check.get_status()
        check.nagios()

