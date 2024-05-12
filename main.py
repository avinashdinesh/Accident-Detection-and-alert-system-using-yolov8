from ultralytics import YOLO
from twilio.rest import Client
from datetime import datetime, timedelta
import keys

def code():
    client = Client(keys.account_sid, keys.auth_token)
    last_accident_detection_time = datetime.min
    last_fire_detection_time = datetime.min

    model = YOLO('best.pt')
    results = model.predict(source="1", show=True, stream=True, verbose=False, conf=0.2)

    for result in results:
        current_time = datetime.now()
        if result.boxes:
            for box in result.boxes:
                class_id = int(box.cls)
                object_name = model.names[class_id]

                if object_name == 'accident':
                    if (current_time - last_accident_detection_time).total_seconds() >= 5:
                        print('An accident has been detected.')
                        message_body = f"An accident has been detected in Central junction at: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                        message = client.messages.create(
                            body=message_body,
                            from_=keys.twilio_number,
                            to=keys.my_phone_number
                        )
                        last_accident_detection_time = current_time

                elif object_name == 'Fire':
                    if (current_time - last_fire_detection_time).total_seconds() >= 5:
                        print('A fire has been detected.')
                        message_body = f"A fire has been detected in Central junction at: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                        message = client.messages.create(
                            body=message_body,
                            from_=keys.twilio_number,
                            to=keys.my_phone_number2
                        )
                        last_fire_detection_time = current_time

code()
