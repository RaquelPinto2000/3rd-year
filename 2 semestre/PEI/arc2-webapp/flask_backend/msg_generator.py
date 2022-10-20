import paho.mqtt.client as mqtt
from time import sleep
import sys

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client,userdata,result):             #create function for callback
    #print("data published \n")
    #print(userdata,result)
    pass


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


f_name = 'samples/full_sample.txt'
#10.0.20.32:1883 is the debug broker
#10.0.20.32:1884 is the real broker
broker_ip = '10.0.20.32'
port = 1884

#USAGE: python message_generator.py <input_file> [server_ip] [server_port]
#Ex: python message_generator.py samples/vams/format_vams.txt atcll-bosch.nap.av.it.pt 1883

if len(sys.argv) > 1:
    f_name = sys.argv[1]
    if len(sys.argv) > 2:
        broker_ip = sys.argv[2]
        if len(sys.argv) > 3:
            port = int(sys.argv[3])

#Connects to the broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
print('Publishing messages from ´%s´ into broker hosted at %s:%d' % (f_name,broker_ip,port))
try: 
    client.connect(broker_ip, port)
except:
    print('ERROR: Could not connect to broker %s:%d' % (broker_ip,port))

# Publishes all the messages in the file and then
# reopens the file. Does this forever
while True:
    with open(f_name) as f_in:
        for line in f_in.readlines():
            tmp = line.strip()
            if len(tmp) == 0:
                continue
            tmp = line.split(' ')
            receiving_topic = tmp[0]
            line = ' '.join(tmp[1:])
            #print(receiving_topic,line.strip())
            client.publish(receiving_topic, payload=line)
            sleep(0.05)

client.loop_forever()
