# check_znuny_queue.py
This Plugin for openITCOCKPIT will monitor the length of a given Znuny Queue. By default, only Tickets with
lock state `unlock (1)` and state `new (1)` and `open (4)` will be counted.

Available Tickets will be written to the Long Output, including a Link to the Znuny System.
When `--znuny-url` is not set, the Plugin will only print out the ticket number and title.

## Tested with
- Python 3.8.10
- Znuny LTS

## Requirements
- `apt-get install python3-mysql.connector`


## Usage

### List all availalbe Znuny queues

```
[09:25][130][root@znuny01:~]# /opt/check_znuny_queue.py --list-queues --mysql-user oitc_agent --mysql-password abc123
id - name
1 - Eingang
2 - Raw
3 - Junk
4 - Misc
[09:25][0][root@znuny01:~]#
```

### Monitor the length of a queue
```
[09:25][0][root@znuny01:~]# /opt/check_znuny_queue.py --mysql-user oitc_agent --mysql-password abc123 --id 4 --warning 1 --critical 1 --znuny-url"https://znuny.it-novum.com/"
Critical: 1 tickets are waiting in the Queue. | tickets=1;1;1
Ticket [url=https://znuny.it-novum.com/index.pl?Action=AgentTicketZoom;TicketID=23214][2022060194000563][/url] Help! I need somebody
[09:26][2][root@znuny01:~]#
```
