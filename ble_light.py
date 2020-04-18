
import pexpect
import time
import paho.mqtt.client as mqtt

LIGHT01 = "20:C3:8F:8D:8C:9E"
VALUE = ["00000000", "FF000000", "00FF0000", "0000FF00", "000000FF", "00000000"];
RGBW = "00000000"

child = pexpect.spawn("gatttool -I")

child.sendline("connect {0}".format(LIGHT01))
child.expect("Connection successful", timeout=5)
print ("Connected to the light!")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ip_v1/BLE_light_all/RGBW")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global RGBW
    print(msg.topic+" "+str(msg.payload))
    l = len((str(msg.payload)))
    if l == 8:
        RGBW = str(msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect_async("mqtt.eclipse.org", 1883, 60)
client.loop_start()
while True:
	# for i in range(6):
	child.sendline("char-write-req 0x0031 {0}".format(RGBW)) #VALUE[i]))
	child.expect("Characteristic value was written successfully", timeout=5)
	time.sleep(1);

child.sendline("disconnect")

child.close()

print ("Light Turned OFF")

