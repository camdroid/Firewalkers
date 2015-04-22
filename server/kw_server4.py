from twisted.internet import reactor, protocol

class Echo(protocol.Protocol):
	"""This is just about the simplest possible protocol"""

	def dataReceived(self, data):
		"As soon as any data is received, write it back."
		print "Received: \n"+data
		self.transport.write("HTTP/1.1 200 OK\nConnection: keep-alive\nServer: Python/2.7.2\nAccept-Ranges: bytes\nContent-Type: text/html\nContent-Length: 4\nLast-Modified: Tue, 31 March 2015 13:00:05 GMT\n\nhola\n")
		

def main():
	"""This runs the protocol on port 8000"""
	factory = protocol.ServerFactory()
	factory.protocol = Echo
	reactor.listenTCP(80, factory)
	reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
	main()
