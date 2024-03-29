#!/usr/bin/python3
#

GLOBALS = {
    'program_name': 'ddns-python',
}

DEFAULT_CONFIGS = {
    'configuration': '/etc/%s.conf' % GLOBALS['program_name'],
    'default_section': 'Defaults',
    'interval': 60,
    'wait_between_two_requests': 0,

    'authentication': 'Basicauth',
    'enable_v4': 1,
    'enable_v6': 1,
    'ip_v4_param': 'myip',
    'ip_v6_param': 'myip',
    'enable_ip_include_disabled_param_empty': 0,
    'ip_check_mode_v4': 'web',
    'ip_check_mode_v6': 'web',
    'web_check_ip_service_v4': 'https://checkipv4.dedyn.io/',
    'web_check_ip_service_v6': 'https://checkipv6.dedyn.io/',
}
