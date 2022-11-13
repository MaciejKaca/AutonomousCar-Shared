from enum import Enum
import time
import json


class MessageType(Enum):
    NULL = 1
    SPEED = 2
    ANGLE = 3
    VOLTAGE = 4
    JOYSTICK = 5
    HEARTBEAT = 6
    CURRENT = 7


class MessageFields(Enum):
    MESSAGE_TYPE = 1
    SENT_TIME = 2
    DATA = 3


class Direction(Enum):
    FORWARD = 1
    BACKWARD = 2
    BRAKE = 3


class Property:
    NAME: str = str()
    value = 0

    def __init__(self, name: str, value):
        self.NAME = name
        self.value = value


def deserialize_message(message):
    message = message.decode("utf-8")
    message_dict = dict(json.loads(message))
    message_type = MessageType(message_dict.get(MessageFields.MESSAGE_TYPE.name))

    data = DataMessage()
    if message_type == MessageType.SPEED:
        data = SpeedData()
    elif message_type == MessageType.JOYSTICK:
        data = JoystickData()
    elif message_type == MessageType.HEARTBEAT:
        data = Heartbeat()

    data.deserialize(message_dict)
    return data


def get_time():
    return round(time.time() * 1000)


class DataMessage:
    def __init__(self):
        self.messageType = MessageType.NULL
        self.sentTime = get_time()
        pass

    def _get_data(self) -> dict:
        pass

    def _set_data(self, data: dict):
        pass

    def serialize(self) -> str:
        data = self._get_data()
        message = {MessageFields.MESSAGE_TYPE.name: self.messageType.value,
                   MessageFields.SENT_TIME.name: self.sentTime, MessageFields.DATA.name: data}

        return json.dumps(message)

    def deserialize(self, message):
        self.messageType = MessageType(message.get(MessageFields.MESSAGE_TYPE.name))
        self.sentTime = int(message.get(MessageFields.SENT_TIME.name))

        data = dict(message.get(MessageFields.DATA.name))
        self._set_data(data)


class SpeedData(DataMessage):
    def __init__(self):
        super().__init__()
        self.messageType = MessageType.SPEED
        self.speed: Property = Property("speed", 0)
        self.direction: Property = Property("direction", Direction.FORWARD.value)

    def _get_data(self) -> dict:
        data = dict()
        data[self.speed.NAME] = str(self.speed.value)
        data[self.direction.NAME] = str(self.direction.value)
        return data

    def _set_data(self, data: dict):
        self.speed.value = int(data.get(self.speed.NAME))
        self.direction.value = Direction(int(data.get(self.direction.NAME)))


class JoystickData(DataMessage):
    def __init__(self):
        super().__init__()
        self.messageType = MessageType.JOYSTICK
        self.eventType: Property = Property("eventType", 0)
        self.inputValue: Property = Property("value", 0)
        self.axis: Property = Property("axis", 0)
        self.button: Property = Property("button", 0)

    def _set_data(self, data: dict):
        self.eventType.value = int(data.get(self.eventType.NAME))
        self.axis.value = int(data.get(self.axis.NAME))
        if str(data.get(self.inputValue.NAME)).find(".") == -1:
            self.inputValue.value = int(data.get(self.inputValue.NAME))
        else:
            self.inputValue.value = float(data.get(self.inputValue.NAME))
        self.button.value = int(data.get(self.button.NAME))

    def _get_data(self) -> dict:
        data = dict()
        data[self.eventType.NAME] = str(self.eventType.value)
        data[self.inputValue.NAME] = str(self.inputValue.value)
        data[self.axis.NAME] = str(self.axis.value)
        data[self.button.NAME] = str(self.button.value)
        return data


class Heartbeat(DataMessage):
    def __init__(self):
        super().__init__()
        self.messageType = MessageType.HEARTBEAT
        self.systemID: Property = Property("systemID", 0)

    def _get_data(self) -> dict:
        data = dict()
        data[self.systemID.NAME] = self.systemID.value
        return data

    def _set_data(self, data: dict):
        self.systemID.value = int(data.get(self.systemID.NAME))


class CurrentData(DataMessage):
    def __init__(self):
        super().__init__()
        self.messageType = MessageType.HEARTBEAT
        self.voltage: Property = Property("voltage", 0)
        self.current: Property = Property("current", 0)

    def _get_data(self) -> dict:
        data = dict()
        data[self.voltage.NAME] = self.voltage.value
        data[self.current.NAME] = self.current.value
        return data

    def _set_data(self, data: dict):
        self.voltage.value = float(data.get(self.voltage.NAME))
        self.current.value = float(data.get(self.current.NAME))
