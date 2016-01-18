from gevent import monkey; monkey.patch_all()
import logging
from gevent.server import StreamServer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Receiver(object):
    def __init__(self):
        self.socket = None
        self.address = None

    def connection_made(self, socket, address):
        self.socket = socket
        self.address = address

    def connection_lost(self):
        pass

    def line_received(self, line):
        pass

    def send_line(self, line):
        self.socket.sendall(line + '\n')


class State(object):
    def __init__(self, receiver):
        self.receiver = receiver


class AnonymousState(State):
    """ Anonymous connections can only log in.
    """
    def login(self, username, password):
        logger.info('Login %s:%s', username, password)

        self.receiver.state = AuthenticatedState(self.receiver)


class AuthenticatedState(State):
    """ Once authenticated (by calling login), connections can call ping.
    """
    def ping(self, *args):
        self.receiver.send_line('pong')


class StatefulReceiver(Receiver):
    def __init__(self):
        super(StatefulReceiver, self).__init__()

        # All new connections start out anonymous
        self.state = AnonymousState(self)

    def line_received(self, line):
        command, args = line.split(' ', 1)
        args = args.split()
        logger.info('Command: %s, args: %s', command, args)
        getattr(self.state, command)(*args)


def Handler(receiver_class):
    def handle(socket, address):
        logger.info('Client (%s) connected', address)

        receiver = receiver_class()
        receiver.connection_made(socket, address)

        try:
            f = socket.makefile()

            while True:
                line = f.readline().strip()
                if line == "":
                    break
                logger.info('Received line from client: %s', line)
                receiver.line_received(line)
            logger.info('Client (%s) disconnected.', address)

        except Exception, e:
            logger.exception(e)
        finally:
            try:
                f.close()
                receiver.connection_lost()
            except:
                pass
    return handle


server = StreamServer(('0.0.0.0', 8088), Handler(StatefulReceiver), keyfile='server.key', certfile='server.crt')
logger.info('Server running')
server.serve_forever()
