

from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import rest_framework




@api_view(["GET", "POST"])
def Dlist(request):
    if request.method == "GET":
        all_data = Dht11.objects.all()
        data_ser = DHT11serialize(all_data, many=True)  # Les données sont sérialisées en JSON
        return Response(data_ser.data)

    elif request.method == "POST":
        serial = DHT11serialize(data=request.data)

        if serial.is_valid():
            serial.save()
            derniere_temperature = Dht11.objects.last().temp
            print(derniere_temperature)

            if serial.is_valid():
                serial.save()
                derniere_temperature = Dht11.objects.last().temp
                print(derniere_temperature)

                if derniere_temperature > 5:
                    # Alert Email
                    subject = 'Alerte'
                    message = 'La température dépasse le seuil de 25°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = ['Youssef.ourdi732@gmail.com']
                    send_mail(subject, message, email_from, recipient_list)

                    # Alertwhatsapp

                    from twilio.rest import Client
                    account_sid = 'AC2d88af686190af50c112e527d4603e7b'
                    auth_token = '1ca9f5f0afed7d3d334767eaab7b1a98'
                    client = Client(account_sid, auth_token)
                    message = client.messages.create(
                        from_='whatsapp:+14155238886',
                        body='bien Youssef',
                        to='whatsapp:+212637770186'
                    )

                    # Alert Telegram
                    import requests
                    def send_telegram_message(token, chat_id, message):
                        url = f"https://api.telegram.org/bot{token}/sendMessage"
                        payload = {
                            'chat_id': chat_id,
                            'text': message
                        }
                        response = requests.post(url, data=payload)
                        return response

                    telegram_token = '8156066307:AAGsEGJi6wHuiYXFZdh2wwBsUDKuw-KciPs'
                    chat_id = '6133334901'  # Remplacez par votre ID de chat
                    telegram_message = 'La température dépasse le seuil de 25°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                    send_telegram_message(telegram_token, chat_id, telegram_message)

                return Response(serial.data, status=status.HTTP_201_CREATED)

            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)




