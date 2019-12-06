# rvc
Linux Remote Volume Control
- This is an MQTT based remote volume control
- Using this to remotely control the volume from home assistant

- Control (from HA) topic: "basement/desktop/control"
- Status (to HA) topic: "basement/desktop/status"
- Control Examples:
- {"louder": false} {"louder": true}
- {"mute": 0} {"mute": 1}
- {"volume": 10} {"volume": 20}

