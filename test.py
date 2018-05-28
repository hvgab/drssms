from drs_sms import NeverAPI
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    print('Create object and login')
    napi = NeverAPI()
    napi.login()

    test_number = 123
    test_text = 'MY TEST TEXT'
    test_service = 2684  # IT-Test
    test_ani = 'MY NAME'

    # Download
    print('Test downloads')
    print('download with start and end date')
    print(napi.download_sms_file('2018-04-09', '2018-04-10'))
    print('download with startdate')
    print(napi.download_sms_file('2018-04-10'))
    print('download without args')
    print(napi.download_sms_file())

    # test push sms
    print('Send push SMS')
    napi.send_push_sms(test_number, test_text, ani=test_ani)

    # Service
    print('Send service SMS')
    napi.stop_dialog(test_number)
    napi.send_service_sms(test_number, test_service, ani=test_ani)
