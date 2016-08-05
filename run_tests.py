"""
Test runner
"""
#pylint:disable=redefined-builtin
import logging
import sys
import unittest
import tornado.testing

def all():
    """
    Standard method to set tests up
    """
    return unittest.defaultTestLoader.loadTestsFromNames([
        'tests.test_dogecast',
    ])

def _run():
    """
    Runs the tests
    """
    # Disable logging to make access easier
    logging.getLogger("tornado.access").disabled = True
    # logging.getLogger("tornado.application").disabled = True
    logging.getLogger("tornado.general").disabled = True

    # Run tests. Don't exit as we need to drop database after we're done
    tornado.testing.main(verbosity=2, exit=False)

if __name__ == '__main__':
    _run()
