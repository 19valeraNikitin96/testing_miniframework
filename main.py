# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import unittest

from app_remote.app_remote import AppRemote
from testcases import Testcase, MonolithicTestcase
from testcases.users import UserTests, UsersCreateFailed, UsersCreatePassed, UsersReadPassed
import multiprocessing
import json
import logging
import importlib


def validate_config(config: dict) -> None:
    for k in ['testing', 'app-settings']:
        if config.get(k, None) == None:
            raise ConfigParseException('Could not find key \'{}\''.format(k), [k])
    for k in ["resources"]:
        if config['testing'].get(k, None) == None:
            raise ConfigParseException('Could not find key \'{}\' in \'testing\''.format(k), [k])
    for k in ["protocol", "domain", "port", "access_token"]:
        if config['app-settings'].get(k, None) == None:
            raise ConfigParseException('Could not find key \'{}\' in \'app-settings\''.format(k), [k])


# Press the green button in the gutter to run the script.
class ConfigException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

class ConfigParseException(Exception):
    def __init__(self, message, problem_keys):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.problem_keys = problem_keys


def test(resource: dict, app_remote: AppRemote):
    module = importlib.import_module('testcases.{}'.format(resource['name']))
    for suite in resource['suites']:
        klass = getattr(module, suite)
        suite = unittest.TestSuite()
        if issubclass(klass, MonolithicTestcase):
            suite.addTest(Testcase.parametrize(klass, app_remote=app_remote, test_data=resource.get('test-data', None)))
        else:
            suite.addTest(klass(app_remote=app_remote, test_data=resource.get('test-data', None)))
        unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    data = None
    try:
        with open('config.json') as json_file:
            data = json.load(json_file)
            validate_config(data)
    except FileNotFoundError:
        raise ConfigException('Could not find config file. Please, check that config exists and has proper name')

    logger = logging.getLogger()
    logging_value = data['testing'].get('logging-level', 'INFO')
    if logging_value == 'INFO':
        logger.level = logging.INFO
    if logging_value == 'DEBUG':
        logger.level = logging.DEBUG
    if logging_value == 'WARNING':
        logger.level = logging.WARNING
    if logging_value == 'CRITICAL':
        logger.level = logging.CRITICAL
    logging.info('Logging level: {}'.format(logging_value))

    app_remote = AppRemote(**data['app-settings'])
    logger.info('Created app remote instance')

    resources = data['testing']['resources']
    processors = multiprocessing.cpu_count()
    multiproc_enabled = data['testing'].get('concurrent-testing', False)
    logging.info('Multiprocessing enabled')

    if multiproc_enabled:
        processes = []
        for r in resources:
            if multiproc_enabled:
                p = multiprocessing.Process(target=test, args=(r, app_remote))
                processes.append(p)
                p.start()
                processes.append(p)
        for p in processes:
            p.join()
    else:
        for r in resources:
            for suite in r['suites']:
                test(suite, app_remote)