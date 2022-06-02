#!/usr/bin/env python3

import argparse
import mysql.connector

# it-novum GmbH
# MIT License

# Example to Check
#
# python3 check_znuny_queue.py --mysql-user oitc_agent --mysql-password asdasd --id 13 --warning 1 --critical 2
#Warning: 1 tickets are waiting in the Queue. | tickets=1;1;2
#Ticket [2022060194000623] Das ist ein Test Ticket

# Example to Query all Queues
#
# python3 check_znuny_queue.py --list-queues --mysql-user oitc_agent --mysql-password asdasd
#1 - Eingang
#2 - Raw
#3 - Junk

# Znuny state ids
# ticket_state_id
# Source: https://doc.znuny.org/doc/api/otrs/6.0/Perl/Kernel/System/State.pm.html#StateList
# 1 => "new",
# 2 => "closed successful",
# 3 => "closed unsuccessful",
# 4 => "open",
# 5 => "removed",
# 6 => "pending reminder",
# 7 => "pending auto close+",
# 8 => "pending auto close-",
# 9 => "merged",
# 
# 
# ticket_lock_id
# Source: https://doc.znuny.org/doc/api/otrs/6.0/Perl/Kernel/System/Lock.pm.html#LockList
# 1 => 'unlock',
# 2 => 'lock',
# 3 => 'tmp_lock',

parser = argparse.ArgumentParser(description='openITCOCKPIT / Naemon check plugin to monitor the length of a Znuny Queue.')

parser.add_argument(
    '--list-queues',
    help='List all available Znuny Queues',
    action='store_true'
)

parser.add_argument(
    '--id',
    help='ID of the Queue',
    type=int
)


parser.add_argument(
    '--warning',
    help='Warning number of tickets in queue',
    type=int
)

parser.add_argument(
    '--critical',
    help='Critical number of tickets in queue',
    type=int
)

parser.add_argument(
    '--mysql-user',
    help='MySQL username',
    default='otrs',
)

parser.add_argument(
    '--mysql-password',
    help='MySQL password',
    required=True
)

parser.add_argument(
    '--mysql-database',
    help='MySQL database name',
    default='otrs'
)

parser.add_argument(
    '--znuny-url',
    help='URL to the Znuny Server',
)

def run_mysql_query(mysql_credentials, sql, params=None):
    cnx = mysql.connector.connect(
        host="localhost",
        user=mysql_credentials['username'],
        password=mysql_credentials['password'],
        database=mysql_credentials['database']
    )

    cursor = cnx.cursor(prepared=True)
    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)

    columns = cursor.description
    result = []
    for value in cursor.fetchall():
        tmp = {}
        for (index,column) in enumerate(value):
            tmp[columns[index][0]] = column
        result.append(tmp)

    cursor.close()
    cnx.close()

    return result

def get_queues(mysql_credentials)-> dict:
    return run_mysql_query(mysql_credentials, ("SELECT id, name from queue ORDER BY id ASC"))

def get_tickets(mysql_credentials, qid)-> dict:
    # Only return unlocked ticketes in 
    sql = ("SELECT id, tn, title, ticket_lock_id, ticket_state_id FROM ticket WHERE queue_id = %s AND ticket_lock_id IN (1) AND ticket_state_id IN (1,4) ORDER BY id ASC")
    return run_mysql_query(mysql_credentials, sql, (qid,))

if __name__ == "__main__":
    args = parser.parse_args()
    znuny_url = args.znuny_url

    mysql_credentials = {
        'username': args.mysql_user,
        'password': args.mysql_password,
        'database': args.mysql_database
    }

    if args.list_queues is True:
        queues = get_queues(mysql_credentials)
        print("id - name")
        for queue in queues:
            print("{} - {}".format(queue['id'], queue['name']))
        exit(0)


    qid = args.id
    warning = args.warning
    critical = args.critical

    tickets = get_tickets(mysql_credentials, qid)
    l = len(tickets)

    rc = 0 #OK
    state = 'Ok'
    if l >= warning:
        rc = 1
        state = 'Warning'
    
    if l >= critical:
        rc = 2
        state = 'Critical'

    ticket_states = {
        0: ''
    }

    print ("{}: {} tickets are waiting in the Queue. | tickets={};{};{}".format(state, l, l, warning, critical))
    for ticket in tickets:
        if znuny_url:
            print("Ticket [url={}index.pl?Action=AgentTicketZoom;TicketID={}][{}][/url] {}".format(znuny_url, ticket['id'], ticket['tn'], ticket['title']))
        else:
            print("Ticket [{}] {}".format(ticket['tn'], ticket['title']))

    exit(rc)
    
