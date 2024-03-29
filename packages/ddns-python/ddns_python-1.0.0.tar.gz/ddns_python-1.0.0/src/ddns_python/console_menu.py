#!/usr/bin/python3
#

from .constants import DEFAULT_CONFIGS, GLOBALS
from sys import stderr
import argparse
import configparser

defaultSection = DEFAULT_CONFIGS['default_section']


class MenuConfig:
    args = None
    config = None

    @classmethod
    def init(cls):
        cls.config = configparser.ConfigParser()

        config_parser, cls.args, remainingArgv = cls._parse_config_location()

        # if configuration should be tested, stop initialization here
        if cls.args.test_configuration:
            return

        # reading configuration not necessary to show help
        if '-h' not in remainingArgv and '--help' not in remainingArgv:
            cls._read_configuration_file()

        cls.args = cls._init_main_argparser(config_parser)

    @classmethod
    def get_default_items(cls):
        try:
            return dict(MenuConfig.config.items(defaultSection))
        except Exception as err:
            print('ERROR: Failed to read Defaults section. Run configuration test for details', file=stderr)
            exit(1)

    @classmethod
    def _init_main_argparser(cls, config_parser):
        main_parser = argparse.ArgumentParser(
            prog=GLOBALS['program_name'],
            parents=[config_parser]
        )
        subparsers = main_parser.add_subparsers(dest='command')
        cls._init_update_parser(subparsers)

        return main_parser.parse_args()

    @classmethod
    def _init_update_parser(cls, subparsers):
        parser = update_parser = subparsers.add_parser(
            'update',
            description='update DDNS entries configured',
        )

        parser.add_argument(
            '-d',
            '--daemonize',
            action='store_true',
            help='runs the client as daemon'
        )

    @classmethod
    def _parse_config_location(cls):
        # create parser
        config_parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            add_help=False
        )

        config_parser.add_argument(
            '--configuration',
            action='store',
            type=str,
            nargs='?',
            default=DEFAULT_CONFIGS['configuration'],
            metavar='filepath',
            help='configuration to use [{}]'.format(DEFAULT_CONFIGS['configuration'])
        )

        config_parser.add_argument(
            '--test-configuration',
            action='store_true',
            help='Check configuration file'
        )

        args, remaining_argv = config_parser.parse_known_args()
        return config_parser, args, remaining_argv

    @classmethod
    def _read_configuration_file(cls):
        cls.config.read([cls.args.configuration])
