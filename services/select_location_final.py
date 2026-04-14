from telegram.ext import Updater, MessageHandler, filters
from telegram import Update
import requests
import pyodbc
from datetime import datetime, timedelta

TOKEN = '7853397371:AAGqaogOkZdD3Vm9caXcFHWA0Qtzc9RMHyM'
SQL_SERVER = 'DESKTOP-OM6KNI2\\MSSQLSERVER2'
SQL_DATABASE = 'location'


def save_to_sql(location):
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};Trusted_Connection=yes;'
        )
        cursor = conn.cursor()

        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='locationDev' AND xtype='U')
            CREATE TABLE locationDev (
                id INT IDENTITY(1,1) PRIMARY KEY,
                latitude FLOAT,
                longitude FLOAT,
                address_ar NVARCHAR(MAX),
                governorate_ar NVARCHAR(100),
                timestamp DATETIME DEFAULT GETDATE()
            )
        """)

        
        ten_minutes_ago = datetime.now() - timedelta(minutes=10)
        cursor.execute("""
            SELECT COUNT(*) FROM locationDev 
            WHERE address_ar = ? AND governorate_ar = ? AND timestamp > ?
        """, location['address'], location['governorate'], ten_minutes_ago)
        count = cursor.fetchone()[0]

        if count > 0:
            print("⚠️ تم تسجيل هذا العنوان مؤخرًا، لن يتم تكراره.")
            return False

        cursor.execute("""
            INSERT INTO locationDev (latitude, longitude, address_ar, governorate_ar)
            VALUES (?, ?, ?, ?)
        """, location['lat'], location['lon'], location['address'], location['governorate'])

        conn.commit()
        print(" تم حفظ الموقع في قاعدة البيانات.")
        return True

    except Exception as e:
        print(f" Database Error: {str(e)}")
        return False
    finally:
        conn.close()


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
        return '، '.join(filter(None, components)), addr.get('state', 'غير معروف')
    except:
        return "غير معروف", "غير معروف"


def handle_location(update, context):
    msg = update.edited_message or update.message
    if msg and msg.location:
        lat = msg.location.latitude
        lon = msg.location.longitude
        print(f" موقع جديد: {lat}, {lon}")
        address, governorate = reverse_geocode(lat, lon)
        location_data = {
            'lat': lat,
            'lon': lon,
            'address': address,
            'governorate': governorate
        }
        save_to_sql(location_data)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(filters.location | filters.update.edited_message, handle_location))

    print(" البوت شغال وبيسجل المواقع تلقائيًا")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
