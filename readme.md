= gevent StreamServer examples

I couldn't find a nice, concise gevent SSL StreamServer example anywhere, so I
threw this together to demonstrate how you might go about building a very
basic version of Twisted's Factory/Protocol pattern using gevent. It lacks
error handling, but hopefully that helps to clarify what's going on.

The Factory/Protocol model is a little more complicated than it needs to be as
far as understanding gevent/StreamServer goes, but I do think it is very
useful. If you're just looking for StreamServer, take a look at how the Handler
functions.

* echo_server.py simply echoes any line sent.
* stateful_server.py shows an example of a slightly more complicated server,
  using states. This demonstrates how each connection can be in a different
  state - try running 2 clients simultaneously, you'll see that they can both
  call login happily, and only logged in clients can call ping.
* client.py is a working client for both servers.
