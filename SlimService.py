import traceback
import ListSerializer
import ListDeserializer
from ListExecutor import ListExecutor

import sys
logfile = open('log', 'w')
sys.path.append('/home/epronk/stuff/pyfit/fitnesse/slim')

def log(entry):
    #print entry
    #logfile.write(entry)
    logfile.flush()

import SocketServer

class RequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        self.wfile.write('Slim -- V0.0\n')
        while True:
            instructionLength = int(self.rfile.read(6))
            self.rfile.read(1)
            instructions = self.rfile.read(instructionLength)
            if instructions == 'bye':
                return
            log('instructions {%s}' % instructions)
            statements = ListDeserializer.deserialize(instructions)
            self.executor = ListExecutor()
            results = self.executor.execute(statements)
            x = ListSerializer.serialize(results)
            log(x)
            self.wfile.write('%06d:%s' % (len(x), x))

class Server(SocketServer.TCPServer):

    allow_reuse_address = True

    def __init__(self, server_address):

        SocketServer.TCPServer.__init__(self, server_address, RequestHandler)

    def serve_until_stopped(self):
        """Serve requests until self.stop() is called.

        This is an alternative to BaseServer.serve_forever()
        """

        self.log('started')
        self.__stopped = False
        while not self.__stopped:
            self.handle_request()
        self.log('stopped')

try:

    log('args : %s' % sys.argv)
    path = sys.argv[1]
    #util.add_to_python_path(path)

    port =  int(sys.argv[3])
    server_address = ('localhost', port)
    server = Server(server_address)
    server.handle_request()
    log('done')

except Exception, e:
    log(traceback.format_exc())

