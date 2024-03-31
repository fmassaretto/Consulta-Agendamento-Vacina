import requests
import EmailService
import SmsService
import DoseEnum
import FileUtils
from dotenv import dotenv_values
from datetime import datetime
import logger
from bs4 import BeautifulSoup

# https://vacina.jundiai.sp.gov.br
page = requests.get(dotenv_values().get('URL'))
soup = BeautifulSoup(page.content, 'html.parser')
# soup = BeautifulSoup(URL_TEST, 'html.parser')

which_dose = DoseEnum.DoseEnum.PRIMEIRA_DOSE


def find_id_element():
    # print(soup.select('#vagas-esgotadas > h2'))
    return soup.select('#vagas-esgotadas > h2')


def find_segunda_dose():
    return soup.select('#home-menu > li > a')


def contain_segunda_dose():
    for tags_a_item in find_segunda_dose():
        if str(tags_a_item).find('segunda dose') > 0:
            return True
    return False


def check_availibility():
    global which_dose
    if (not find_id_element()) or str(find_id_element()[0]).find('esgotadas') == -1:
        if contain_segunda_dose():
            print('tem vagas segunda dose')
            which_dose = DoseEnum.DoseEnum.SEGUNDA_DOSE
            logger.log_whether_has_vacancy(True)
        else:
            print('tem vagas primeira dose')
            which_dose = DoseEnum.DoseEnum.PRIMEIRA_DOSE
            logger.log_whether_has_vacancy(True)
        schedule_sending()
    else:
        print('esgotado')
        # sendMessage('Fabio', '+551195XXXXXX', False)
        SmsService.d7_sms_api('Fabio', '+551195XXXXXX', False)
        logger.log_whether_has_vacancy(False)


def past_time_for_next_sms(count_datetime):
    date_time_obj = datetime.strptime(count_datetime, '%Y-%m-%d %H:%M:%S.%f')
    return (datetime.now() - date_time_obj).seconds / 60 >= 180


def schedule_sending():
    count_reader = counter('read')
    count_reader = count_reader.split('=>')

    if count_reader.__len__() > 1:
        count_datetime = count_reader[0].strip()
        count = int(count_reader[1])
    else:
        count = 0

    if count == 0:
        logger.write_log_msg("Sending e-mail/SMS right way without wait")
        # send first sms right way
        sms_provider()
        EmailService.send_email(which_dose)
        counter('write', 1)
    else:
        logger.write_log_msg('Passed the time for the next e-mail/SMS? {}'
                             .format('yes' if past_time_for_next_sms(count_datetime) else 'no'))
        if past_time_for_next_sms(count_datetime):
            counter('write')
            sms_provider()
            # TODO ajustar isso pq sempre vai mandar email de primeira dose
            EmailService.send_email(which_dose)
            logger.log_whether_has_vacancy(
                'Sending e-mail/SMS after pass X hours')


def sms_provider():
    # SmsService.sendMessage('Fabio', '+551195XXXXXX', True)
    # SmsService.sendMessage('Vivian', '+551195XXXXXX', True)
    # SmsService.d7_sms_api('Fabio', '+551195XXXXXX', True)
    # SmsService.d7_sms_api('Vivian', '+551195XXXXXX', True)
    SmsService.vonage_sms('Fabio', '551195XXXXXX', True)
    SmsService.vonage_sms('Vivian', '551195XXXXXX', True)
    # SmsService.message_bird('Fabio', '+551195XXXXXX', True)
    # SmsService.message_bird('Vivian', '+551195XXXXXX', True)


def counter(mode='read', count=0):
    if mode == 'write':
        permissions = 'w+'
    else:
        permissions = 'r+'

    with open('data/counter.txt', permissions) as writer_reader:
        if mode == 'write':
            writer_reader.write('{} => {}'.format(datetime.now(), count))
        else:
            return writer_reader.read()


if __name__ == "__main__":
    FileUtils.build_dir_file('log.txt')
    FileUtils.build_dir_file('counter.txt')
    check_availibility()
