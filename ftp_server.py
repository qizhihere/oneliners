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
    parser.add_argument('-A, --no-anonymous', dest='anon', action='store_false',
                        help='Disable anonymous user.')
    parser.add_argument('-D, --directory', dest='dir', default=os.getcwd(),
                        help='The default serving directory.')
    parser.add_argument('users', nargs='*',
                        help='[USER:rw:DIR:PASSWORD [... USER:ro:DIR:PASSWORD]]')
    return parser.parse_args()

def main():
    args = parse_args()
    users = [x.split(':') for x in args.users]

    authorizer = DummyAuthorizer()
    args.anon and authorizer.add_anonymous(args.dir)
    credentials = []
    for x in users:
        user, _perm, _dir, pwd = x
        _dir = args.dir if _dir.strip() is '' else _dir
        perm = 'elradfmwM' if _perm is 'rw' else 'elr'
        credentials.append((user, pwd))
        authorizer.add_user(user, pwd, _dir, perm=perm)

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "Ftp server ready."

    address = (args.server, args.port)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    print('Login credentials: %s\nAnonymous user is %s.' %
          (credentials, 'enabled' if args.anon else 'disabled'))

    server.serve_forever()

if __name__ == '__main__':
    main()
