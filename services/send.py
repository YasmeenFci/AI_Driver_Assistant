from telegram.ext import Updater, MessageHandler, filters
from telegram import Update
from twilio.rest import Client
import requests
import os
from dotenv import load_dotenv


load_dotenv()
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN=os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER=os.getenv('TWILIO_PHONE_NUMBER')
TO_PHONE_NUMBER =os.getenv('TO_PHONE_NUMBER')
TOKEN=os.getenv('TOKEN')

last_sent_location = {
    "address": None,
    "governorate": None
}

def reverse_geocode(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&accept-language=ar"
        headers = {'User-Agent': 'LocationBot/1.0'}
        response = requests.get(url, headers=headers)
        data = response.json()
        addr = data.get('address', {})
        components = [
            addr.get('road'),
            addr.get('neighbourhood'),
            addr.get('city') or addr.get('town'),
            addr.get('state'),
            addr.get('country')
        ]
        full_address = '، '.join(filter(None, components))
        governorate = addr.get('state', 'غير معروف')
        return full_address, governorate
    except Exception as e:
        print(f" خطأ في تحويل الإحداثيات: {e}")
        return "غير معروف", "غير معروف"

def send_sms(lat, lon, address, governorate):
    message_body = f""" السائق في حالة خطر!
 العنوان: {address}
 المحافظة: {governorate}
 الإحداثيات: {lat}, {lon}"""
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )
        print(f" تم إرسال SMS بنجاح. SID: {message.sid}")
    except Exception as e:
        print(f" فشل في إرسال SMS: {e}")

def handle_location(update, context):
    global last_sent_location
    msg = update.edited_message or update.message
    if msg and msg.location:
        lat = msg.location.latitude
        lon = msg.location.longitude
        print(f" تم استلام إحداثيات: {lat}, {lon}")
        address, governorate = reverse_geocode(lat, lon)
        print(f" العنوان المحوّل: {address} | المحافظة: {governorate}")
        if (
            address == last_sent_location["address"]
            and governorate == last_sent_location["governorate"]
        ):
            print(" نفس العنوان والمحافظة، مش هنبعت SMS.")
            return
        send_sms(lat, lon, address, governorate)
        last_sent_location["address"] = address
        last_sent_location["governorate"] = governorate

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(filters.location | filters.update.edited_message, handle_location))
    print(" البوت شغال ومستعد يستقبل مواقع")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
