# openITCOCKPIT Plugin Exchange

A place where the openITCOCKPIT community share and exchange custom monitoring plugins

All this monitoring plugins can be used by openITCOCKPIT, the openITCOCKPIT Monitoring Agent, Naemon Core and Nagios
Core.

Please see [Table of contents](#table-of-contents) to get a list of all available plugins group by operating system.

# Table of contents

- **Linux**
    - Database
      - https://github.com/lausser/check_mssql_health - Health checking of Microsoft SQL Server
      - https://github.com/lausser/check_mysql_health - Health checking for MySQL and MariaDB
      - https://github.com/lausser/check_oracle_health - Health checking of Oracle database servers
    - Disk
        - https://github.com/it-novum/check_diskstats - Basically `iostat` but as monitoring plugin.
        - https://github.com/zlacelle/nagios_check_zfs_linux - Health state of ZFS pools
    - Hardware
        - https://github.com/it-novum/check_nvidia_smi - Checks the health of Nvidia graphics card within VMware ESXi via SSH
    - Memory
      - https://github.com/hugme/Nag_checks/blob/master/check_linux_memory - Check for memory usage
- **macOS**
    - Be the first one :)
- **Windows**
    - Be the first one :)

# Contributing

Basically there are two types of contributions

## Adding an already existing plugin to this collection
You are using a monitoring plugin, but you are not the author of it? As long as the plugin is hosted on GitHub or
GitLab feel free to add a link to the plugin followed by a short description.

## Submitting your own work
You have written a handcrafted plugin to monitor a particular application, service or sensor and want to share your work with the world? Awesome!

You can either submit a link to your GitHub or GitLab repository or push the plugin code into this repository.

If you plan to push your code, please consider the following rules:
1. Create a new Folder for your Plugin. (Example: `windows/check_eventlog.ps1`)
2. Only plugins with a proper open source license will be accepted. (MIT license, GPL, LGPL or Apache License to name a few)
3. Commit messages **must** contain Signed-off-by
4. Plugins must contain a `README.md` file which describes how to build and us the plugin

Commit messages **must** contain a Signed-off-by line. Use `git commit -s` to get the Signed-off-by for free.
The Signed-off-by telling us that you have the permission and right from the company you are working for, to submit your code.

**Only submit your code if you have permission for. We do not want to get contacted by any lawyers demanding that we have to remove your contributions**

# License

All plugins are contributed by community members and volunteers. Please see the license information provided by each
plugin.

# Questions

If you have any questions, please create a new [issue](https://github.com/it-novum/openITCOCKPIT-Plugin-Exchange/issues)
or visit our [Discord Server](https://discord.gg/G8KhxKuQ9G).
