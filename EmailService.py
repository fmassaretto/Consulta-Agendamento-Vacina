from dotenv import dotenv_values
import smtplib
import DoseEnum
import FileUtils
from string import Template
import logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(dose):
    logger.write_log_msg("Sending e-mail...")
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(dotenv_values().get('GMAIL_USER'), dotenv_values().get('GMAIL_PASSWORD'))

    names, emails = get_contacts(FileUtils.build_dir_file('contacts.txt'))  # read contacts
    if dose == DoseEnum.DoseEnum.PRIMEIRA_DOSE:
        subject = '[Primeira Dose] Coorreeee!!! Verifique o site vacina Jundiaí'
        message_template = read_template(FileUtils.build_dir_file('message_email_dose_1.txt'))
        logger.write_log_msg('loaded template for Primeira dose')
    else:
        subject = '[Segunda Dose] Verifique o site vacina Jundiaí'
        message_template = read_template(FileUtils.build_dir_file('message_email_dose_2.txt'))
        logger.write_log_msg('loaded template for Segunda dose')

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()  # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title())

        # setup the parameters of the message
        msg['From'] = dotenv_values().get('GMAIL_EMAIL')
        msg['To'] = email
        msg['Subject'] = subject

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        logger.write_log_msg('e-mail sent for {}'.format(name))

        del msg


def get_contacts(filename):
    names = []
    emails = []
    with open(str(filename), mode='r+', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails


def read_template(filename):
    with open(str(filename), 'r+', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)
