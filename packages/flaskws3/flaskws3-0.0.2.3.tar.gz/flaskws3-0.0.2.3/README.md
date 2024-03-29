# `flaskws3`

Actually good WebSocket for Flask.

Keep in mind that this is just a patched version; no changes were made, so original docs are still valid.

For convenience, the module name didn't change too.

## Usage

Info is *mostly* taken from the original docs.

Here's some starting code for this mini tutor:

```py
import flaskws
app = Flask(__name__, template_folder="templates")
app.wsgi_app = flaskws.WsMiddleware(app.wsgi_app)
```
<!-- # app.run() -->

### Splitted path!

#### Method #1

For this method, simply create a class for your WebSocket server.

```py
@app.route("/ws/<int:some_id>")
@flaskws.ws_server
class SampleServer():
	def __init__(self, ws_sock, **req_args):
		self.ws_sock = ws_sock
		print(req_args["some_id"])
	def on_open(self, ws_sock): pass
	def on_message(self, ws_sock, frame):
		fin, op, payload = frame # TODO: Search around code to find what info lurks in `frame`.
	def on_close(self, ws_sock): pass
```

#### Method #2

This method uses a function. A little harder to control than Method #1, but no one says you can't pick this one!..

```py
@app.route("/ws/<int:some_id>")
@flaskws.ws_server_view
def echo_server(ws_sock, some_id=None):
	while True:
		frame = ws_sock.recv(timeout=5.0)
		if frame:
			fin, op, msg = frame
			if msg:
				ws_sock.send(msg)
				if msg == "close": # Likely a module-implemented way of closing??
					break
```

## Client

As in the unpatched version, there's also a client. The client wasn't changed in any way. Still no SSL support though...

Here's some sample code for you:

```py
from flaskws import ws_connect

with ws_connect("ws://test.host/ws/123") as c: # Could be used as a class too, just remember to `close`!!
	if c.handshake():
		c.send("somethingsomething")
		for frame in c:
			print(frame)
```