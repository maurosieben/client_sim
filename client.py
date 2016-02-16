import sys
import paho.mqtt.client as mqtt
import random

dev= str(sys.argv[1])
dimmer = '0'

client = mqtt.Client()

def make_con():
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect("192.168.0.100", 1883, 60)
        client.publish("lights/%s" %dev, "Hello AWGES DEV:%s MAC: XX-XX-XX-XX-XX-XX " %dev)
        client.loop_forever()


def on_connect(client, userdata, rc):
        print("\n[MQTT]Conectado ao Broker: 192.168.0.100\n")
        client.subscribe("lights/%s" %dev)
        client.subscribe("lights")

def on_message(client, userdata, msg):
        global dimmer
        data = msg.payload.split(' ')
        frag = data[0].split('-')
        if (len(frag) >= 2):
                dimmer = frag[1]
        else:
                handle_msg(data[0])

def handle_msg(msg):
        if msg == 'R0001':
                 current = random.randrange(0, 2000, 1)
                 client.publish("lights/%s/current" %dev, "%dmA" %current)

        elif msg == 'R0002':
                client.publish("lights/%s/pir" %dev, "PNATIVO")
        
        elif msg == 'R0000':
                client.publish("lights/%s/msp" %dev, "MSP working fine")
        
        elif msg == 'R0003':
                ldr = random.randrange(0, 1000, 1)
                client.publish("lights/%s/ldr" %dev, "%d" %ldr)

        elif msg == 'R0004':
                temp = random.randrange(30, 50, 1)
                client.publish("lights/%s/temperature" %dev, "%d" %temp)
        
        elif msg == 'R0005':
                client.publish("lights/%s/dimmer" %dev, "%s%%" %dimmer)
        
        elif msg == 'R0253':
                client.publish("lights/%s/ip" %dev, "xx.xx.xx.xx")

        elif msg == 'R0254':
                rssi = random.randrange(10, 90, 1)
                client.publish("lights/%s/rssi" %dev, "-%ddBm" %rssi)
        
        elif msg == 'R0255':
                client.publish("lights/%s/status" %dev, "OK-FW-%s/MAC" %dev)

        elif msg == 'kill':
                client.publish("lights/%s/status" %dev, "%s is shutting down" %dev)
                sys.exit()
        else:
                client.publish("lights/%s/status" %dev, "Message is not implemented yet")
        

if __name__ == "__main__":
        make_con()


