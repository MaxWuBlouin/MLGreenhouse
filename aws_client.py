import time
import json
import threading

import paho.mqtt.client as mqtt


ROOT_CERTIFICATE = "certifications/AmazonRootCA1.pem"
CERTIFICATE = "certifications/certificate.pem.crt"
PRIVATE_KEY = "certifications/private.pem.key"

HOST_ADDRESS = "airxh5i12mupp-ats.iot.us-east-2.amazonaws.com"
HOST_PORT = 8883
KEEPALIVE_INTERVAL = 60


def on_connect(client, userdata, flags, return_code, properties=None):
    print("Client:", client)
    print("User data:", userdata)
    print("Flags:", flags)
    print("Return code:", return_code)


#def on_message(mqttc)


client = mqtt.Client(protocol=mqtt.MQTTv5)
client.on_connect = on_connect
client.tls_set(ca_certs=ROOT_CERTIFICATE,
               certfile=CERTIFICATE,
               keyfile=PRIVATE_KEY,
               tls_version=2)
client.tls_insecure_set(True)
client.connect(host=HOST_ADDRESS,
               port=HOST_PORT,
               keepalive=KEEPALIVE_INTERVAL)


def run():
    client.loop_forever()
    print("Connection ended")


t1 = threading.Thread(target=run)

client_active = True
t1.start()
time.sleep(5)
client.publish("raspi/data", payload="hello")
client.subscribe("raspi/command")
time.sleep(5)
client.disconnect()
t1.join()

print("Program ends.")