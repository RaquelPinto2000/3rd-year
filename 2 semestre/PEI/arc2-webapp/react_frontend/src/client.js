Stream = require('node-rtsp-stream')

  const io = require("socket.io-client");

  const socket = io("ws://steamcity02.nap.av.it.pt:5000/");

  var all_streams = {};
  var streamsMap = {};

  socket.on("connect", () => {
    console.log('Connected to the backend');
  });

  // handle the event sent with socket.send()
  socket.on("message", data => {
      console.log("here");
    console.log(data);
  });


  socket.on("teste", (data) => {
      console.log(data['data']);
    });

  socket.on("rtsp", (data) => {
      console.log("Creating stream object");

      try {
        const port = parseInt(data['carID']) + 9000;

        console.log(data['rtspLink']);
        stream = new Stream({
            name: 'LiveStream ' + data['carID'],
            streamUrl: data['rtspLink'],
            wsPort: port,
            ffmpegOptions: {            // options ffmpeg flags
              '-stats': '',             // an option with no neccessary value uses a blank string
              '-r': 30,                 // options with required values specify the value after the key
              '-rtsp_transport': 'tcp'  // without this option obu live feed won't work
            }
          });

        streamsMap[port] = stream;
        
      } catch (error) {
        console.error(error)
      }
  });

  socket.on("stop", (data) => {
      console.log("Stopping Stream");
      port = data['port'];
      if(streamsMap[port] != undefined)
      {
        streamsMap[port].stop();
        delete streamsMap[port];
      }
      else
      {
        console.log("\n>Stream doesnt exist<")
      }

  });

  socket.on("getLives", (data) => {
    console.log("Getting livestreams for: " + data['id']);
    console.log(all_streams[data['id']]);
    console.log(data['id']);
    
    if (all_streams[data['id']] == undefined) {
      socket.emit('response2', data['id'], [ ]);
    }else{
      socket.emit('response2', data['id'], all_streams[data['id']]);
    }
});