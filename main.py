import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.wsgi
import tornado.template
import tornado.iostream
import os
import tornadio
import tornadio.router
import tornadio.server

from tornado.options import define, options

participants = set()

class SIOHandler(tornadio.SocketConnection):
	def on_open(self, *args, **kwargs):
		participants.add(self)

	def on_message(self, message):
		for p in participants:
			p.send(message)

	def on_close(self):
		participants.remove(self)

class BubbleServer(tornadio.SocketConnection):
	def __init__(self):
		self.x=1

	def send_to_everyone(self, message):
		for p in participants:
			p.send(message)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		loader = tornado.template.Loader("/home/erik/Desktop/Projects/tornadobubbler/templates")
		self.write(loader.load("bubbler.html").generate())
		
class BubblePostHandler(tornado.web.RequestHandler):
	def post(self):
		newBubble = self.get_argument('newBub[]')
		server.send_to_everyone(newBubble)


server = BubbleServer()

MyRouter = tornadio.get_router(SIOHandler)

application = tornado.web.Application([
				#(r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
				(r"/", MainHandler),
				(r"/a/postbubble", BubblePostHandler),
				MyRouter.route()],
				enabled_protocols = ['websocket',
								 'xhr-multipart',
								  'xhr-polling'],
						  socket_io_port = 24432,
)


if __name__ == "__main__":

	import logging
	logging.getLogger().setLevel(logging.DEBUG)

	tornadio.server.SocketServer(application)
