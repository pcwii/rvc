# Message Examples....
# {"louder": false} {"louder": true}
# {"mute": 0} {"mute": 1}
# {"volume": 10} {"volume 20": true}


import alsaaudio
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time

delay = 30 # seconds
audio_mixer = alsaaudio.Mixer()
mute_volume = 50
mqttc = mqtt.Client()
broker = "192.168.0.43"
port = 1883
control_topic = "basement/desktop/control"
status_topic = "basement/desktop/status"
status_data = {}


def get_status_data():
    status_data['volume'] = audio_mixer.getvolume()[0]
    status_data['mute'] = audio_mixer.getmute()[0]
    return json.dumps(status_data)


def set_master_volume(new_level):
    audio_mixer.setvolume(new_level)  # Set the volume to 70%.


def increase_master_volume():
    current_volume = audio_mixer.getvolume()  # Get the current Volume
    print(current_volume)
    if current_volume[0] <= 90:
        audio_mixer.setvolume(current_volume[0] + 10)  # Set the volume to 70%.


def decrease_master_volume():
    current_volume = audio_mixer.getvolume()  # Get the current Volume
    if current_volume[0] >= 10:
        audio_mixer.setvolume(current_volume[0] - 10)  # Set the volume to 70%.


def mute_master_volume(set_mute):
    audio_mixer.setmute(set_mute)


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print('message received...')
    print(msg.payload)
    mqtt_message = str(msg.payload)[2:-1]
    new_message = json.loads(mqtt_message)
    print(msg.topic + " " + str(msg.qos) + ", " + mqtt_message)
    if "volume" in new_message:
        print("Volume Change Requested")
        print(new_message['volume'])
        set_master_volume(new_message['volume'])
    elif "mute" in new_message:
        print("Mute Change Requested")
        print(new_message['mute'])
        mute_master_volume(new_message['mute'])
    elif "louder" in new_message:
        if new_message['louder']:
            print('Increasing Volume!')
            increase_master_volume()
        else:
            print('Decreasing Volume!')
            decrease_master_volume()
    else:
        print("NO key found")


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.connect(broker, port, 60)
mqttc.subscribe(control_topic, 0)
#mqttc.loop_forever()
mqttc.loop_start()
while True:
    mqttc.publish(status_topic, get_status_data())
    time.sleep(delay)
