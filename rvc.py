import alsaaudio
import paho.mqtt.client as mqtt
import json

audio_mixer = alsaaudio.Mixer()
mute_volume = 0
mqttc = mqtt.Client()


def set_master_volume(new_level):
    audio_mixer.setvolume(new_level)  # Set the volume to 70%.


def increase_master_volume():
    current_volume = audio_mixer.getvolume()  # Get the current Volume
    if current_volume <= 90:
        audio_mixer.setvolume(current_volume + 10)  # Set the volume to 70%.


def decrease_master_volume():
    current_volume = audio_mixer.getvolume()  # Get the current Volume
    if current_volume >= 10:
        audio_mixer.setvolume(current_volume - 10)  # Set the volume to 70%.


def mute_master_volume():
    current_volume = audio_mixer.getvolume()  # Get the current Volume
    if current_volume == 0:
        audio_mixer.setvolume(mute_volume)  # Set the volume to 70%.
    else:
        mute_volume = current_volume
        audio_mixer.setvolume(0)  # Set the volume to 70%.


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    # Message Examples....
    # {"louder": false} {"louder": true}
    # {"mute": false} {"mute": true}
    # {"volume": 10} {"volume 20": true}
    print('message received...')
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    new_message = json.loads(msg.payload)
    if "volume" in new_message:
        print("Volume Change Requested")
        print(new_message['volume'])
        set_master_volume(new_message['volume'])
    elif "mute" in new_message:
        print("Mute Change Requested")
        print(new_message['mute'])
        mute_master_volume()
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
mqttc.connect("192.168.0.43", 1883, 60)
mqttc.subscribe("desktop/control", 0)
mqttc.loop_forever()

