# -*- coding: utf-8 -*-

'''
    Custom DRS API for sms-tjeneste fra Never.
'''

import logging
import os
import shutil
import datetime as dt
import re
import requests

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class NeverAPI(object):
    """docstring for NeverAPI."""

    def __init__(self, path='./', user_agent=os.getenv('DRSSMS_USERAGENT')):
        super(NeverAPI, self).__init__()
        self.path = path  # gjørra no her ell?
        self.user_agent = user_agent
        self.session = requests.Session()
        self.logged_in = False
        logger.debug('NeverAPI init')

    def login(self):
        logger.debug('[~] login')

        if not os.getenv('DRSSMS_USER'):
            raise ValueError('DRSSMS_USER not in env vars. Cannot login.')
        if not os.getenv('DRSSMS_PW'):
            raise ValueError('DRSSMS_PW not in env vars. Cannot login.')
        if not os.getenv('DRSSMS_LOGIN_URL'):
            raise ValueError('DRSSMS_LOGIN_URL not in env vars. Cannot login.')

        logindata = {'u': os.getenv('DRSSMS_USER'), 'p': os.getenv('DRSSMS_PW')}
        # Logger inn
        headers = {'user-agent': self.user_agent}
        response = self.session.post(os.getenv('DRSSMS_LOGIN_URL'), headers=headers, data=logindata)

    # Finner en cookie vi fikk tilbake
        cookie_resp = response.request.headers['Cookie']
        # Format cookie
        cookie_send = 'Basic ' + cookie_resp[13:]

    # Set headers on object
        headers['Authorization'] = cookie_send
        self.headers = headers
        self.logged_in = True
        logger.debug('[+] Logged in')

    def download_sms_file(self, start=None, end=None, filename=None, download_path=None):
        """ Download SMS-Dialog export
            Args:
                start: date string in format yyyy-mm-dd
                end: date string in format yyyy-mm-dd
                download_path: where to save downloaded file
            Return:
                String: Path to saved file.
        """
        if not os.getenv('DRSSMS_DOWNLOAD_BASE_URL'):
            raise ValueError('DRSSMS_DOWNLOAD_BASE_URL not in env vars. Cannot download SMS Dialogs.')
        # from / to i string-format "2018-01-01" uten chickalacka rundt seg.
        if not download_path:
            download_path = self.path

        if not start:
            start = dt.date.today() + dt.timedelta(days=-1)
            start = start.isoformat()
            logger.debug('start: {}'.format(start))

        if not end:
            end = dt.datetime.strptime(start, '%Y-%m-%d') + dt.timedelta(days=1)
            end = end.date().isoformat()
            logger.debug('end: {}'.format(end))

        url = f'{os.getenv("DRSSMS_DOWNLOAD_BASE_URL")}&from={start}&to={end}&q=&op=messages&action=csv'
        local_filename = filename
        if filename is None:
            local_filename = f'sms_dialoger_start-{start}-end-{end}.csv'
        local_filepath = os.path.join(download_path, local_filename)

        # Kopierer raw bytes rett til fil.
        try:
            r = self.session.get(url, stream=True)
            with open(local_filepath, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            logger.info('[+] File successfully downloaded')
            return local_filepath
        except Exception as e:
            logger.exception('[-] File download failed')
            return

    def send_service_sms(self, phone, serviceID, message=None):
        """ Send a service sms.

            Includes reminder and confirmation SMS.
            Initial service message can be overwritten with <message>
        """

        logger.debug('[~] Send service SMS')

        if message == '':
            message = None

        phone = int(phone)

        if not os.getenv('DRSSMS_SERVICE_URL'):
            raise ValueError('DRSSMS_SERVICE_URL not in env vars. Cannot send service sms.')

        url = os.getenv('DRSSMS_SERVICE_URL')
        smsdata = {
            'service': serviceID,
            'phone': phone,
            'msgfromscript': message,
            'submit': '1'
        }
        sms = self.session.post(url, headers=self.headers, data=smsdata)

        # status = None
        if 'err' in sms.url:
            # status = 'ERROR'
            re_search = '<div class="error">(.*)</div>'
            m = re.search(re_search, sms.text)
            logger.error(f'[!] Send service fail. ({m.group(1)}) ({sms.url})')

            # logger.error(sms.text)
        if 'msg' in sms.url:
            # status = 'SUCCESS'
            logger.info('[+] Send service success.')

    def send_push_sms(self, phone, message, ani=os.getenv('DRSSMS_ANI')):
        """ Push an sms, no dialog """

        logger.debug('[~] Send push')

        if not ani or ani == '':
            ani = os.getenv('DRSSMS_ANI')
        if not ani:
            raise ValueError('ANI must be set. Set fallback ANI with DRSSMS_ANI in env vars or as kwarg in function.')
        if not os.getenv('DRSSMS_PUSH_URL'):
            raise ValueError('DRSSMS_PUSH_URL not in env vars. Cannot send push message.')
        if not os.getenv('DRSSMS_GATEWAY_ACCOUNT_ID'):
            raise ValueError('Missing DRSSMS_GATEWAY_ACCOUNT_ID in env. Cannot push message')

        url = os.getenv('DRSSMS_PUSH_URL')

        smsdata = {
            'action': 'send',
            'submit': 'Send+message',
            'type': '3',
            'phone': '47{}'.format(phone),
            'currency': 'NOK',
            'rate': '0',
            'message': message,
            'systemaddress': ani,
            'gatewayaccountid': os.getenv('DRSSMS_GATEWAY_ACCOUNT_ID')
        }

        logger.debug(smsdata)

        if not self.logged_in:
            self.login()

        sms = self.session.post(url, headers=self.headers, data=smsdata)

        # status = None
        re_search = r"NotificationBar\('(.*)', '(.*)'\);"
        m = re.search(re_search, sms.text)

        if m.group(1) == 'error':
            logger.error(f'[-] Error from Never: {m.group(1)} - {m.group(2)}')
        elif m.group(1) == 'info':
            logger.info(f'[+] Info from Never: {m.group(1)} - {m.group(2)}')
        else:
            logger.error(f'[-] Error could not confirm success or failure from never. ({m.group(1)} - {m.group(2)})')

    def get_services(self):
        """ Get all services """
        raise NotImplementedError
        # url = os.getenv('DRSSMS_GET_SERVICES_URL')
        # r = self.session.get(url)

    def stop_dialog(self, number):
        """ Stop active SMS Dialog """
        logger.debug('[~] Stop dialog')

        if not os.getenv('DRSSMS_STOP_SERVICEID'):
            raise ValueError('DRSSMS_STOP_SERVICEID not in env. Cannot use shortcut to stop dialog. Try sending stop-service id to send_service_sms()')

        self.send_service_sms(number, os.getenv('DRSSMS_STOP_SERVICEID'))
