import os
import sys

from logbag import Logger
from supervisor import childutils


class SupervisorEventListener:
    """
    Simple example that logs everything with level 'debug'
    except PROCESS_STATE_FATAL which is logged as 'critical':

        def main():
            from logbag import SupervisorEventListener
            levelmap = {
                'PROCESS_STATE_FATAL': 'critical'
            }
            prog = SupervisorEventListener('http://example.com/logger', 'john', 'doeproject', levelmap, 'debug')
            prog.runforever()

        if __name__ == '__main__':
            main()
    """
    def __init__(self, url, user, project, levelmap=None, defaultlevel='info'):
        if not 'SUPERVISOR_SERVER_URL' in os.environ:
            sys.stderr.write('script must be run as a supervisor event '
                             'listener\n')
            sys.stderr.flush()
            return sys.exit(1)
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.defaultlevel = defaultlevel
        self.levelmap = {} if levelmap is None else levelmap
        self.logger = Logger(url, user, project)

    def runforever(self):
        while 1:
            headers, payload = childutils.listener.wait(self.stdin, self.stdout)
            level = self.levelmap.get(headers['eventname'], self.defaultlevel)
            msg = u'[%s]: %s' % (headers['eventname'], payload)
            self.logger.log(level, msg)
            childutils.listener.ok(self.stdout)
