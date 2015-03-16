# -*- coding: utf-8 -*-
"""
Helper functions used in templates.
"""
import ConfigParser
import logging
import os
import urllib

INI_FILENAME = os.path.join(os.path.dirname(__file__),
                            '..', '..', 'runtime', 'debug.ini')

LOG = logging.getLogger(__name__)


def get_users_xml_file(ini_file_name=INI_FILENAME):
    """ Get users xml file location from configuration file. """
    config = ConfigParser.ConfigParser()
    config.readfp(open(ini_file_name))
    return config.get("users", "users_xml_file")


def get_users_url(ini_file_name=INI_FILENAME):
    """ Get users xml url address from configuration file. """
    config = ConfigParser.ConfigParser()
    config.readfp(open(ini_file_name))
    return config.get("users", "users_url")


def save_users_from_www(ini_filename=INI_FILENAME):
    """ Get users xml url address from configuration file. """
    url_file = get_users_url(ini_filename)
    try:
        with open(urllib.urlretrieve(url_file)[0]) as _file:
            lines = _file.readlines()
            if [line for line in lines if '<users>' in line]:
                with open(get_users_xml_file(ini_filename), 'w') as _xfile:
                    _xfile.writelines(lines)
                return True
            #else:
            #    LOG.debug('Improper users xml file !', exc_info=True)
    except (IOError, TypeError):
        LOG.debug("Problem during processing url %s! ",
                  url_file, exc_info=True)
    return False


if __name__ == "__main__":
    if save_users_from_www():
        print 'The users file correctly saved'
    else:
        print 'The users file NOT saved !'
