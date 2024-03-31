from dotenv import dotenv_values
import messagebird
import requests
import vonage
from twilio.rest import Client


def create_body_msg(firstName, has_vacancy):
    if has_vacancy:
        return 'CORREEEEEE!!!!! {}, Pode ser que abriram as vagas para a vacinacao, entao da uma olhada no site: {} \n'.format(
            firstName, dotenv_values().get('URL'))
    else:
        return 'Vagas Esgotadas! {}, parece que nao tem vagas ainda \n'.format(firstName)


def sendMessage(firstName, toNumber, temVaga):
    body_msg = create_body_msg(firstName, temVaga)

    twilio().messages.create(from_=dotenv_values().get('TWILIO_FROM_TEL'),
                             to=toNumber,
                             body=body_msg)


def twilio():
    account_sid = dotenv_values().get('TWILIO_ACCOUNT_SID')
    auth_token = dotenv_values().get('TWILIO_AUTH_TOKEN')

    return Client(account_sid, auth_token)


def d7_sms_api(firstName, toNumber, has_vacancy):
    url = "https://http-api.d7networks.com/send"
    querystring = {
        "username": dotenv_values().get('D7_SMS_USERNAME'),
        "password": dotenv_values().get('D7_SMS_PASSWORD'),
        "from": dotenv_values().get('D7_SMS_FROM'),
        "content": create_body_msg(firstName, has_vacancy),
        "dlr-method": "POST",
        "dlr-url": "https://4ba60af1.ngrok.io/receive",
        "dlr": "no",
        "dlr-level": "3",
        "to": toNumber
    }
    headers = {
        'cache-control': "no-cache"
    }
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    print(response.text)


def vonage_sms(first_name, to_number, has_vacancy):
    client = vonage.Client(
        key=dotenv_values().get('VONAGE_KEY'), secret=dotenv_values().get('VONAGE_SECRET')
    )
    sms = vonage.Sms(client)

    responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": to_number,
            "text": create_body_msg(first_name, has_vacancy),
        }
    )

    if responseData['messages'][0]['status'] == '0':
        print('Message sent successfully.')
    else:
        print('Message failed with error: {}'.format(
            responseData['messages'][0]['error-text']))


def message_bird(first_name, to_number, has_vacancy):
    client = messagebird.Client(dotenv_values().get('MESSAGE_BIRD_CLIENT'))

    try:
        msg = client.message_create(
            'Fabio', to_number, create_body_msg(first_name, has_vacancy))
        print(msg.__dict__)
    finally:
        print('Message bird ended.')
