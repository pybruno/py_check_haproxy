# -*- coding: utf-8 -*-
import csv
import requests
from requests.auth import HTTPBasicAuth
import argparse


def build_parser():
    """
    define param command line
    :return: parser config
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=True, dest="url", help="url haproxy stat default 127.0.0.1",
                        default="http://127.0.0.1")
    parser.add_argument("-U", "--user", required=True, dest="user", help="user to login in")
    parser.add_argument("-P", '--pass', required=True, dest="password", help="haproxy password")
    parser.add_argument("-p", dest="port", default="8000", help="port stats default 8000")
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
            if res.status_code == 401:
                print("CRITICAL: login or pasword is wrong")
                exit(2)
            else:
                text_csv = res.iter_lines()
                csv_reader = csv.reader(text_csv, delimiter=',')
                for rows in csv_reader:

                    if rows[1] != "FRONTEND" and rows[1] != "BACKEND" and rows[1] != "svname":
                        if rows[17] != "UP":
                            self.status.append("backend: {} serveur: {} is OFF line".format(rows[0], rows[1]))

        except Exception as e:
            print("CRITICAL: {} ".format(e))
            exit(2)

    def nagios(self):
        if self.status:
            print("CRITICAL: {}".format(self.status))
            exit(2)
        else:
            print("OK - ALL backend")
            exit(0)


if __name__ == "__main__":
    pars = build_parser()
    args = pars.parse_args()

    check = CheckHaproxy(args.url, args.user, args.password, args.port)
    check.get_status()
    check.nagios()

