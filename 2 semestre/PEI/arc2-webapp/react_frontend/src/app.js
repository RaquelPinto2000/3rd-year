

const { FALSE, TRUE } = require('node-sass')

Stream = require('node-rtsp-stream')

var WebSocketServer = require('websocket').server;
var WebSocketClient = require('websocket').client;
var WebSocketFrame  = require('websocket').frame;
var WebSocketRouter = require('websocket').router;
var W3CWebSocket = require('websocket').w3cwebsocket;


/*
console.log("Hello World!")

var flag = FALSE

var http = require('http');

var server = http.createServer(function(request, response) {
    console.log((new Date()) + ' Received request for ' + request.url);
    response.writeHead(404);
    response.end();
});
server.listen(8080, function() {
    console.log((new Date()) + ' Server is listening on port 8080');
});

wsServer = new WebSocketServer({
    httpServer: server,
    autoAcceptConnections: false
});

function originIsAllowed(origin) {
  // put logic here to detect whether the specified origin is allowed.
  return true;
}

wsServer.on('request', function(request) {
    if (!originIsAllowed(request.origin)) {
      // Make sure we only accept requests from an allowed origin
      request.reject();
      console.log((new Date()) + ' Connection from origin ' + request.origin + ' rejected.');
      return;
    }
    
    var connection = request.accept('echo-protocol', request.origin);
    console.log((new Date()) + ' Connection accepted.');
    connection.on('message', function(message) {
        if (message.type === 'utf8') {
            console.log('Received Message: ' + message.utf8Data);
            connection.sendUTF(message.utf8Data);
        }
        else if (message.type === 'binary') {
            console.log('Received Binary Message of ' + message.binaryData.length + ' bytes');
            connection.sendBytes(message.binaryData);
        }
    });
    connection.on('close', function(reasonCode, description) {
        console.log((new Date()) + ' Peer ' + connection.remoteAddress + ' disconnected.');
    });
});*/



  stream1 = new Stream({
    name: 'BigBuckBunny',
    streamUrl: 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov',
    wsPort: 9999,
    ffmpegOptions: { // options ffmpeg flags
      '-stats': '', // an option with no neccessary value uses a blank string
      '-r': 30 // options with required values specify the value after the key
    }
  })
  
  stream2 = new Stream({
      name: 'IT',
      streamUrl: 'rtsp://atcll-p1-camera.nap.av.it.pt/11',
      wsPort: 9900,
      ffmpegOptions: { // options ffmpeg flags
        '-stats': '', // an option with no neccessary value uses a blank string
        '-r': 30 // options with required values specify the value after the key
      }
  })




/*
const io = require("socket.io")(5000);

io.on("connection", socket => {
  // either with send()
  socket.send("Hello!");

  // or with emit() and custom event names
  socket.emit("greetings", "Hey!", { "ms": "jane" }, Buffer.from([4, 3, 3, 1]));

  // handle the event sent with socket.send()
  socket.on("message", (data) => {
    console.log(data);
  });

  // handle the event sent with socket.emit()
  socket.on("salutations", (elem1, elem2, elem3) => {
    console.log(elem1, elem2, elem3);
  });
});*/