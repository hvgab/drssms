import logging

from drssms import NeverAPI

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    input('Create object and login')
    napi = NeverAPI()

    test_number = 12345678
    test_text = 'push test'
    test_service_text = 'service test'
    test_service = 2684  # IT-Test
    test_ani = 'IT-Test'

    # Download
    print('Test downloads')
    input('Download with start and end date')
    print(napi.download_sms_file('2018-04-09', '2018-04-10'))
    input('Download with startdate')
    print(napi.download_sms_file('2018-04-10'))
    input('Download without args')
    print(napi.download_sms_file())

    # test push sms
    input('Send push SMS')
    napi.send_push_sms(test_number, 'push test', ani=test_ani)

    # Service
    input('Send service SMS')
    napi.stop(test_number)
    napi.send_service_sms(test_number, test_service)

    input('Send custom service SMS')
    napi.stop(test_number)
    napi.send_service_sms(test_number, test_service, test_service_text)
