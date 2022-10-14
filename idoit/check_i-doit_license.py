#!/usr/bin/env python3

'''
i-doit Licencecheck
Change Line 21 & 22 for DB Credentials!!!!!!!!
Requires: python-pip, pip mysql-connector, datetime, argparse, sys
example: check_i-doit_license.py --warn 80 --crit 90 --exp 90

it-novum GmbH
MIT License
'''

import os
import mysql.connector
import argparse
import sys
import datetime

# Database password and User
# You can also use the root DB User
DBPW = 'idoit'
DBUSER = 'idoit'

idoit_data = mysql.connector.connect(
    host="localhost",
    user=DBUSER,
    password=DBPW,
    database="idoit_data"
)
idoit_system = mysql.connector.connect(
    host="localhost",
    user=DBUSER,
    password=DBPW,
    database="idoit_system"
)


def getExpireDate():
    iscursor = idoit_system.cursor()
    iscursor.execute(
        "select isys_licence__expires from isys_licence;")
    temp = iscursor.fetchone()

    expire = temp[0]

    return expire


def getLicenceCount():
    iscursor = idoit_system.cursor()
    iscursor.execute(
        "select isys_mandator__license_objects from isys_mandator where isys_mandator__id=1;")
    temp = iscursor.fetchone()

    licount = int(temp[0])

    return licount


def getCurrentObj():
    idcursor = idoit_data.cursor()
    idcursor.execute(
        "select count(isys_obj__property) from isys_obj WHERE isys_obj__status=2 AND isys_obj__const IS NULL AND isys_obj__isys_obj_type__id NOT IN (60);")
    temp = idcursor.fetchone()
    curOJ = int(temp[0])

    return curOJ


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get Licence-Status from i-doit')
    parser.add_argument('--warn', metavar='int',
                        required=True, help='Warning Value in percent')
    parser.add_argument('--crit', metavar='int',
                        required=True, help='Critical Value in percent')
    parser.add_argument('--expire', metavar='int',
                        required=True, help='Time to expire in days')
    args = parser.parse_args()


def main(warn, crit, expdays):
    vwarn = float(warn) * 0.1
    vcrit = float(crit) * 0.1
    current = getCurrentObj()
    licence = getLicenceCount()
    expire = getExpireDate()
    today = datetime.datetime.now()
    expwarn = today + datetime.timedelta(days=int(expdays))

    if current < licence * vwarn:
        if expwarn < expire:
            print("OK, Currently using " + str(current) +
                  " Objectlicense from " + str(licence)+" . License valid until: "+str(expire)+"| current="+str(current))
            sys.exit(0)
        else:
            print("Critical, Licence expiring in under "+str(expwarn)+" days. Currently using " + str(current) +
                  " Objectlicense from " + str(licence)+" . License valid until: "+str(expire)+"| current="+str(current))
            sys.exit(2)
    elif current > licence * vwarn and current < licence * vcrit:
        if expwarn < expire:
            print("Warning, Currently using " + str(current) +
                  " Objectlicense from " + str(licence)+" . License valid until: "+str(expire)+"| current="+str(current))
            sys.exit(1)
        else:
            print("Critical, Licence expiring in under "+str(expwarn)+" days. Currently using " + str(current) +
                  " Objectlicense from " + str(licence)+" . License valid until: "+str(expire)+"| current="+str(current))
            sys.exit(2)
    elif current > licence * vcrit:
        if expwarn < expire:
            print("Critical, Currently using " + str(current) +
                  " Objectlicense from " + str(licence)+" . License valid until: "+str(expire)+"| current="+str(current))
            sys.exit(2)
        else:
            print("Critical, Licence expiring in under "+str(expwarn)+" days. Currently using " + str(current) +
                  " Objectlicense from " + str(licence)+" . Lizenz valid until: "+str(expire)+"| current="+str(current))
            sys.exit(2)


main(warn=args.warn, crit=args.crit, expdays=args.expire)
