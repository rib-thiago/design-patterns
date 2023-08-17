import sys
import syslog
import socket

class Logger(object):
    def __init__(self, file):
        self.file = file

    def log(self, message):
        self.file.write(message + '\n')
        self.file.flush()

class FilteredLogger(Logger):
    def __init__(self, pattern, file):
        self.pattern = pattern
        super().__init__(file)

    def log(self, message):
        if self.pattern in message:
            super().log(message)

class FileLikeSocket:
    def __init__(self, sock):
        self.sock = sock

    def write(self, message_and_newline):
        self.sock.sendall(message_and_newline.encode('ascii'))

    def flush(self):
        pass

def main():
    sock1, sock2 = socket.socketpair()

    fs = FileLikeSocket(sock1)
    logger = FilteredLogger('Error', fs)
    logger.log('Warning: message number one')
    logger.log('Error: message number two')

    print('The socket received: %r' % sock2.recv(512))

if __name__ == '__main__':
    main()
