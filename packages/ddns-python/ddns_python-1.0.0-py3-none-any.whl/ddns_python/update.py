#!/usr/bin/python3
#

from .console_menu import MenuConfig
from .constants import DEFAULT_CONFIGS
from .utils import Terminator,Tempfolder
from http.client import HTTPResponse
from os import path
from sys import stderr
from urllib.parse import urlencode
from urllib.request import urlopen,Request
import base64
import time

default_section = DEFAULT_CONFIGS['default_section']

class DDNSEntry(object):
    def __init__(self):

        self.authentication = MenuConfig.config.get(default_section, 'authentication', fallback=(DEFAULT_CONFIGS['authentication']))
        self.enable_v4 = MenuConfig.config.getboolean(default_section, 'enable_v4', fallback=bool(DEFAULT_CONFIGS['enable_v4']))
        self.enable_v6 = MenuConfig.config.getboolean(default_section, 'enable_v6', fallback=bool(DEFAULT_CONFIGS['enable_v6']))
        self.ip_v4_param = MenuConfig.config.get(default_section, 'ip_v4_param', fallback=DEFAULT_CONFIGS['ip_v4_param'])
        self.ip_v6_param = MenuConfig.config.get(default_section, 'ip_v6_param', fallback=DEFAULT_CONFIGS['ip_v6_param'])
        self.enable_ip_include_disabled_param_empty = MenuConfig.config.getboolean(default_section, 'enable_ip_include_disabled_param_empty', fallback=bool(DEFAULT_CONFIGS['enable_ip_include_disabled_param_empty']))
        self.ip_check_mode_v4 = MenuConfig.config.get(default_section, 'ip_check_mode_v4', fallback=DEFAULT_CONFIGS['ip_check_mode_v4'])
        self.ip_check_mode_v6 = MenuConfig.config.get(default_section, 'ip_check_mode_v6', fallback=DEFAULT_CONFIGS['ip_check_mode_v6'])
        self.web_check_ip_service_v4 = MenuConfig.config.get(default_section, 'web_check_ip_service_v4', fallback=DEFAULT_CONFIGS['web_check_ip_service_v4'])
        self.web_check_ip_service_v6 = MenuConfig.config.get(default_section, 'web_check_ip_service_v6', fallback=DEFAULT_CONFIGS['web_check_ip_service_v6'])

        self.domain = None
        self.update_server = None
        self.username = None
        self.password = None
        self.ipv4 = None
        self.ipv6 = None

class MissingConfigError(Exception):
    def __init__(self, message):
        self.message = message

class Update:
    defaults = None

    @classmethod
    def run(cls):
        first_run = True
        Terminator().init()

        while (first_run or MenuConfig.args.daemonize) and not Terminator().interrupt:
            first_run = False
            cls.__update()

            if MenuConfig.args.daemonize:
                interval = MenuConfig.config.getint(default_section, 'interval', fallback=DEFAULT_CONFIGS['interval'])
                print('entered daemon mode with interval of %d minutes' % interval)
                last_run = int(time.time())
                next_run = last_run + 60 * interval
                while not Terminator().interrupt and next_run > int(time.time()):
                    time.sleep(3)


    @classmethod
    def __update(cls):
        print('update started')
        cls.defaults = MenuConfig.get_default_items()

        sections = list(filter(lambda s: s != default_section, MenuConfig.config.sections()))

        for s in sections:
            if not MenuConfig.config.getboolean(s, 'enabled', fallback=False):
                continue

            print('section: %s' % s)

            try:
                entry = cls.__prepare_section(s)
            except MissingConfigError as err:
                print('ERROR: {}: {} ...skipping'.format(s, err.message))
                continue
            except Exception as err:
                print('ERROR: Section: {}: couldn\'t read configuration. Run configuration test for details'.format(s), file=stderr)
                raise err

            if not entry.enable_v4 and not entry.enable_v6:
                print('neither v4 nor v6 is enabled, nothing todo', file=stderr)
                continue

            if entry.enable_v4 and entry.ip_check_mode_v4 == 'web':
                try:
                    response: HTTPResponse = urlopen(entry.web_check_ip_service_v4)

                    charset = response.info().get_content_charset()
                    entry.ipv4 = response.read().decode('utf-8' if charset is None else charset)
                except Exception as err:
                    print('ERROR: requesting IPv4 failed: %s' % err, file=stderr)

            if entry.enable_v6 and entry.ip_check_mode_v6 == 'web':
                try:
                    response: HTTPResponse = urlopen(entry.web_check_ip_service_v6)
                    charset = response.info().get_content_charset()
                    entry.ipv6 = response.read().decode('utf-8' if charset is None else charset)
                except Exception as err:
                    print('ERROR: requesting IPv6 failed: %s' % err, file=stderr)

            need_update = False
            if entry.enable_v4 and entry.ipv4 is not None:
                valid = False
                try:
                    with open(path.join(Tempfolder.folder.name, '%s-ipv4' % entry.domain), 'r') as f:
                        if f.readline() == entry.ipv4:
                            valid = True
                except FileNotFoundError as err:
                    print('\tno cached v4 found')
                except Exception as err:
                    print('\tcouldn\'t read cached v4: %s' % err, file=stderr)
                finally:
                    if not valid:
                        need_update = True
            if entry.enable_v6 and entry.ipv6 is not None:
                valid = False
                try:
                    with open(path.join(Tempfolder.folder.name, '%s-ipv6' % entry.domain), 'r') as f:
                        if f.readline() == entry.ipv6:
                            valid = True
                except FileNotFoundError as err:
                    print('\tno cached v6 found')
                except Exception as err:
                    print('\tcouldn\'t read cached v6: %s' % err, file=stderr)
                finally:
                    if not valid:
                        need_update = True

            if not need_update:
                print('\tnothing changed, skipping update')
                continue

            params = dict()
            params['hostname'] = entry.domain
            if entry.enable_v4 and entry.ipv4 is not None or entry.enable_ip_include_disabled_param_empty and not entry.enable_v4:
                params[entry.ip_v4_param] = entry.ipv4 or '' if not entry.ip_v4_param in params else params[entry.ip_v4_param] + ',' + entry.ipv4 or ''
            if entry.enable_v6 and entry.ipv6 is not None or entry.enable_ip_include_disabled_param_empty and not entry.enable_v6:
                params[entry.ip_v6_param] = entry.ipv6 or '' if not entry.ip_v6_param in params else params[entry.ip_v6_param] + ',' + entry.ipv6 or ''

            url = entry.update_server + '/?' + urlencode(params)

            if entry.authentication == 'Basicauth':
                base64passwd = base64.b64encode(bytes('%s:%s' % (entry.username, entry.password), 'ascii'))

                req = Request(url)
                req.add_header('Authorization', 'Basic %s' % str(base64passwd, 'ascii'))

            else:
                print('ERROR: %s: unknown authentication setting: %s' % (s, entry.authentication), file=stderr)

            try:
                response = urlopen(req)
                charset = response.info().get_charset() or 'utf-8'
                if entry.enable_v4:
                    print('\tsent v4: %s' % entry.ipv4)
                if entry.enable_v6:
                    print('\tsent v6: %s' % entry.ipv6)
                print('\tresponse was %d/%s' % (response.code, response.read().decode(charset)))

                if entry.enable_v4 and entry.ipv4 is not None:
                    try:
                        with open(path.join(Tempfolder.folder.name, '%s-ipv4' % entry.domain), 'w') as f:
                            f.writelines(entry.ipv4)
                    except Exception as err:
                        print('\tcouldn\'t write v4 cache: %s' % err, file=stderr)
                if entry.enable_v6 and entry.ipv6 is not None:
                    try:
                        with open(path.join(Tempfolder.folder.name, '%s-ipv6' % entry.domain), 'w') as f:
                            f.writelines(entry.ipv6)
                    except Exception as err:
                        print('\tcouldn\'t write v6 cache: %s' % err, file=stderr)
            except Exception as err:
                print('ERROR: %s: update call failed with: %s' % (s, err), file=stderr)

            wait_time = int(time.time()) + 60 * MenuConfig().config.getint(
                default_section,
                'wait_between_two_requests',
                fallback=DEFAULT_CONFIGS['wait_between_two_requests']
            )
            while wait_time > int(time.time()):
                if Terminator.interrupt:
                    return
                time.sleep(3)

    @classmethod
    def __prepare_section(cls, section):
        entry = DDNSEntry()
        config = dict(MenuConfig.config.items(section))

        mandatory_config = ['domain', 'update_server']
        if entry.authentication == 'Basicauth':
            for c in ['username', 'password']:
                mandatory_config.append(c)

        for c in mandatory_config:
            if not c in config:
                raise MissingConfigError('{} not set'.format(c))

        entry.domain = config['domain']
        entry.update_server = config['update_server']

        if entry.authentication == 'Basicauth':
            entry.username = config['username']
            entry.password = config['password']

        optional_configuration = list(filter(lambda c: c in DEFAULT_CONFIGS, config))
        for c in optional_configuration:
            if c.startswith('enable_'):
                entry.__setattr__(c, MenuConfig.config.getboolean(section, c))
            else:
                entry.__setattr__(c, config[c])

        return entry
