import requests
import json
from datetime import datetime
from typing import List
from types import SimpleNamespace
import logging
import time

logging.basicConfig(filename='app.log',level=logging.INFO)

class Telegram_Alert:
    def telegram_bot_sendAlert(self, bot_message):
        bot_token = '1726050183:AAGsjhZup42pobeG3f-sdxCZ886ikP4el2Q'
        bot_chatID = '-1001403785719'

        send_text = 'https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id=' +bot_chatID +'&text=' +bot_message
        response = requests.get(send_text)

        return response.json()


class CowinVaccination:
    def get_default_headers(self) -> dict:
        return {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}

    def getUrl(self):
        todaysDate = datetime.today().strftime('%d-%m-%Y')
        return "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(
            389, todaysDate)
            

    def call_cowin_APi(self):
        try:
            url = self.getUrl()
            headers = self.get_default_headers()
            response = requests.get(url, headers=headers)

            if response.status_code == 200: #or use response.ok
                centers = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))
                telegram_alert = Telegram_Alert()
                for center in centers.centers:
                    if center.sessions:
                        for session in center.sessions:
                            if session.min_age_limit == 18:
                                alert_message = ("Min Age:" +str(session.min_age_limit) + "\n"
                                        "Center Name:"+ str(center.name) +"\n"
                                        "Pin Code:" + str(center.pincode) + "\n"
                                        "Date:" + str(session.date) + "\n"
                                        "Available Capacity:" + str(session.available_capacity) + "\n"
                                        "Fee type:" + str(center.fee_type) + "\n"
                                        "Vaccine:" + str(session.vaccine) + "\n"
                                        )
                                telegram_alert.telegram_bot_sendAlert(alert_message)
        except Exception  as e:
             logging.exception('Error occurred at' +str(datetime.today()) +":" + str(e))

            


if __name__ == "__main__":
    c = CowinVaccination()
    while True:
        c.call_cowin_APi()
        time.sleep(10)
