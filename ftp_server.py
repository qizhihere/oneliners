#!/usr/bin/env python

import os
import sys
import argparse

def has_pkg(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        return False
    return True

def pip_install(package):
    import pip
    pip.main(['install', package])

def ensure_pkg(package):
    has_pkg(package) or pip_install(package)

ensure_pkg('pyftpdlib')

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def parse_args():
    parser = argparse.ArgumentParser(description='Create a simple ftp server.')
    parser.add_argument('-s, --server', dest='server', default='0.0.0.0',
                        help='IP address for ftp server.')
    parser.add_argument('-p, --port', dest='port', type=int, default=21,
                        help='Port number for ftp server.')
    parser.add_argument('-D, --directory', dest='dir', default=os.getcwd(),
                        help='The root directory to serve.')
    parser.add_argument('-U, --user', dest='user', default='ftpuser',
                        help='Login username.')
    parser.add_argument('-P, --pass', dest='passwd', default='ftppass',
                        help='Login password.')
    parser.add_argument('-A, --anonymous', dest='anon', action='store_true',
                        help='Enable anonymous user.')
    return parser.parse_args()

def main():
    args = parse_args()

    authorizer = DummyAuthorizer()
    authorizer.add_user(args.user, args.passwd, args.dir, perm='elradfmwM')
    args.anon and authorizer.add_anonymous(args.dir)

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "Ftp server ready."

    address = (args.server, args.port)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    print('You can login as [%s] with password [%s]. Anonymous user is %s.' %
          (args.user, args.passwd, 'enabled' if args.anon else 'disabled'))

    server.serve_forever()

if __name__ == '__main__':
    main()
