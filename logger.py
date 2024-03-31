import os
import FileUtils
from datetime import datetime
import logging
import logging.handlers


def log_whether_has_vacancy(has_vacancy):
    body = 'Vaga está {}'.format('Disponivel' if has_vacancy else 'Esgotada')
    write_log_msg(body)


def write_log_msg(msg):
    try:
        os.chmod(str(FileUtils.build_dir_file('log.txt')), 0o777)
    except FileNotFoundError:
        print("Oops!  That was invalid path.")

    with open(str(FileUtils.build_dir_file('log.txt')), 'a+') as writer:
        writer.write('{} - Message: {} \n'.format(datetime.now(), msg))

    log_to_syslog(msg)


def log_to_syslog(msg):
    my_logger = logging.getLogger('Vacina Jundiai App ')
    my_logger.setLevel(logging.DEBUG)

    try:
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        my_logger.addHandler(handler)

        my_logger.debug(msg)
    except AttributeError:
        print('log to syslog ended with error.')
