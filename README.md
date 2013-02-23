## Content

- [About](#about)
- [Current State](#current-state)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Deployment](#deployment)
- [Authentification](#authentification)
    - [Authentication Modules](#authentication-modules)
    - [Authentication Decorator](#authentication-decorator)
    - [Disable Authentication](#disable-authentication)
- [Config Files](#config-files)
- [Example API Calls](https://github.com/Crapworks/RESTlos/wiki/Examples)
    - [Find Objects](https://github.com/Crapworks/RESTlos/wiki/Examples#wiki-find-objects)
    - [Create Objects](https://github.com/Crapworks/RESTlos/wiki/Examples#wiki-create-objects)
    - [Update Objects](https://github.com/Crapworks/RESTlos/wiki/Examples#wiki-update-objects)
    - [Delete Objetcs](https://github.com/Crapworks/RESTlos/wiki/Examples#wiki-delete-objetcs)
    - [Reload Monitoring Core](https://github.com/Crapworks/RESTlos/wiki/Examples#wiki-reload-monitoring-core)
    - [Verify Configuration](https://github.com/Crapworks/RESTlos/wiki/Examples#wiki-verify-configuration)

## About

[RESTlos] \(german for _completely_, _totally_\) is a generic [Nagios] api. Generic means, it can be used with 
every core that understands the nagios configuration syntax (for example icinga, shinken, etc). It provides a RESTful 
api for generating any standard nagios object, modify it or delete it. 

There are also some convenient functions for reloading the core (via command file) or verify the actual configuration 
via the REST interface.

## Current State

This code is currently in a state of beta testing. For me, everything works as expected. For you... maybe not! So, as 
usual this code is _Open Source_ and so it comes with absolutely no warrenty. 
That means if you f... up you monitoring config: don't blame me!

## Requirements

- [Python] > **2.7**
- [Flask] > **0.9**
- [PyNag] > **0.4.6**
- [SQLAlchemy] 

If you want to use LDAP authentication:

- [Python-LDAP] > **2.4**

## Quick Start

To get everything just up and running, install all of the required packages mentioned above, and check out the current 
version from github:

```
$ git clone https://github.com/Crapworks/RESTlos.git
```

In the newly created directory, edit the file `config.json` to fit your nagios/icinga/whatever configuration. 
To get everything running, you just need to change the properties `nagios_main_cfg` to your main core configuration 
file and `output_dir` to the direcory where the api should manage the object files (and where the user the api is 
running with has the sufficient rights of course).

If you have done so, fire it up!

```
$ ./restlosapi.py
```

Now point your browser to [http://localhost:5000](http://localhost:5000) (if you haven't changed the standard port). 
You should see a page, listing all available endpoints and the corresponding parameters. You can find some 
example api calls [here](https://github.com/Crapworks/RESTlos/wiki/Examples).

If you are prompted for a password, the initial login credentials are `admin:password`. Very creative, isn't it?

## Deployment

If you want to use it in a production environment, it's **REALY** recommended to deploy the api to a wsgi capable web 
server! Why?
- The `Werkzeug` server shipped with [Flask] is single threaded
- This python script is not trying to be a daemon at all
- This api currently only supports _basic auth_ and it is a **VERY BAD IDEA(tm)** to use _basic auth_ over unencrypted HTTP.

To use this api with an apache web server, you need to install `mod-wsgi`. In the `contrib` directory you will find a 
sample apache configuration which can be placed in the `conf.d` directory. You will also find a file called
`application.py`, which have to be placed in the same directory als the executable python script. This will load
the api as a wsgi application into the web server.

As I already mentioned: **PLEASE** enable SSL for this application.

If anyone can provide configurations for nginx, etc. I would be happy to receive a pull request!

## Authentication

As I already mentioned above, this api uses _basic auth_ for authenticating users. To setup the authentication, 
you **HAVE TO CHANGE THE CODE**. But don't panic! Everyone who has a basic understanding of what a line or a 
character is should be able to handle this. So let's see how authentication works.

### Authentication Modules

The authentication modules are located in the subfolder `utils/authentication`. Currently, there are two modules
provided: `AuthDict` and `AuthLDAP`. `AuthDict` is the default authentication module and is defined in the `__init__.py`
file. If you just want to grant a few users access to the api, just add some more users to the `self.auth` dictionary 
in the `AuthDict` class.

For authentication against a ldap server, the class `AuthLDAP` is located in the `ldapauth.py` in the same directory. 
You should be able to use this module without any modifications. However, this works for _me_. If you find some 
problems with the authentication, just open an issue or fix the code and send me a pull request.

The same applies if you write an additional authentication module (for MySQL or whatever).

### Authentication Decorator

To actually use one of the authentication modules, the you have to add it to the decorator list of the view function.
Currently there are only to seperate view functions (which are really classes which inherit from the 
[Flask] _MethodView_ class): `NagiosControlView` and `NagiosObjectView`. The last one handles all of the request to
generate/modify/delete objects, the first one is used to provide convenient functions for handling the core, like 
restarting or validation of the configuration files. It is possible to use different authentication backends for this 
two views.

The decorators are defined in the class header with the `decorators = [...]` attribute. The one which is active in 
the default config is `Authentify` which uses the `AuthDict` class by default. There is also a commented line which 
shows how to use the `AuthLDAP` class. Here you can add your custom authentication modules and their arguments.

Happy authenticating!

### Disable Authentication

If you don't want authentication **at all**, just delete the `decorators = [...]` lines for the two classes mentioned
above.

## Config Files

The configuration file `config.json`, which has to be located in the same directory as the executable, controls the
main behaivior. It uses the JSON sytnax, just like the api itself. The default configuration should fit for a standard 
[Nagios] installation on Debian/Ubuntu systems. 

The most important key are:

**nagios_main_cfg**

>Full path to the main configuration file of the core (nagios.cfg, icinga.cfg, etc.)

**nagios_bin**

>Full path to the core executable (ex: /usr/sbin/icinga). Needed for config checks.

**output_dir**

>Full path to the directory where the configuration files generated by the api should be placed

In consequence minimal configuration file would look like this

```json
{
    "nagios_main_cfg": "/etc/icinga/icinga.cfg",
    "output_dir": "/etc/icinga/objects"
}
```

The two other available keys are:

**port**

>set the port where the stand alone application should listen for incoming tcp connections 

**logging**

>control the loggin behavior of the application. This dictionary is directly passed to `logging.config.dictConfig()`.
>For a complete overview of the available options see: 
>[The official documentation of the logging Module](http://docs.python.org/dev/library/logging.config.html).
>By default, the application logs DEBUG output to stdout and everything with level WARN or higher goes to syslog
>with the `daemon` fascility.

## Example API Calls

There are some example api calls available in the [Wiki](https://github.com/Crapworks/RESTlos/wiki/Examples).

[RESTlos]:https://github.com/Crapworks/RESTlos
[Nagios]:http://nagios.org
[Python]:http://python.org
[Flask]:http://flask.pocoo.org
[PyNag]:https://github.com/pynag/pynag
[Curl]:http://curl.haxx.se
[Python-LDAP]:http://www.python-ldap.org
