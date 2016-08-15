# uwsgi setup

OS: CentOS 7.1  
`$ yum install uwsgi uwsgi-plugin-python uwsgi-logger-file`

uwsgi.ini is placed in contrib/ folder:  
```
[uwsgi]
module = restlos
callable = application

master = true
processes = 5

# This can be dangerous. You should use user with permissions to read and write to output folder defined in config.json
uid=root
gid=root

# in case that you use nginx as proxy to uwsgi, let uwsgi bind to unix socket
#socket = /tmp/restlos.sock
#chmod-socket = 660
#vacuum = true

# in other cases, let it use tcp socket
http-socket = :8080

plugins = python, logfile

# If you want specific files for request and general logging. Otherwise, uwsgi writes to stdout, or journal if systemd is used.
#req-logger = file:/tmp/reqlog
#logger = file:/tmp/errlog

die-on-term = true
```

Systemd service unit, /etc/systemd/system/uwsgi.service:  
```
[Unit]
Description=uWSGI
After=syslog.target

[Service]
WorkingDirectory=/opt/RESTlos/contrib
ExecStart=/usr/sbin/uwsgi --ini uwsgi.ini
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/bin/kill -9 $MAINPID
# Requires systemd version 211 or newer
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```
/opt/RESTlos is project directory.
 
 
## Nginx  

It's recommanded that nginx<->uwsgi communication should be over unix socket, so just adapt uwsgi.ini above.

```
server {
      listen 80 default_server;

      root /usr/share/nginx/html;
      index index.html index.htm;

      server_name localhost whatever;

      location / {
                include uwsgi_params;
                uwsgi_pass unix:/tmp/restlos.sock;
      }
}
```
