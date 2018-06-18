import logging

import hug
from drssms import NeverAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

napi = NeverAPI()
# napi.login()


@hug.get()
def services(name: hug.types.text = None):
    """Get all available services.

    search with 'name'
    """
    services = napi.get_services()
    # gjør om [0, 1] til {id=0, name=1}
    print(f'name: {name}')
    if name:
        services = [
            dict(id=_[0], name=_[1]) for _ in services
            if name.lower() in _[1].lower()
        ]
    else:
        services = [dict(id=_[0], name=_[1]) for _ in services]
    return services


@hug.post()
def push(number: hug.types.number,
         text: hug.types.text,
         ani: hug.types.text = None):
    """ Send push SMS to number without service. """
    result = napi.send_push_sms(number, text, ani)
    return dict(result=result)


@hug.post()
def service(number: hug.types.number,
            serviceid: hug.types.number,
            text: hug.types.text = None):
    """ Send service SMS to number, optionally overwrite text """

    napi = NeverAPI()
    result = napi.send_service_sms(number, serviceid, text)
    print(result)
    return result


@hug.post()
def stop(number: hug.types.number):
    """Stop an active SMS dialog."""
    napi = NeverAPI()
    napi.login()

    result = napi.stop_dialog(number)
    return result


@hug.get()
def download(
        # help='startdate in isoformat 2018-01-31 (inclusive)'
        start: hug.types.text = None,
        # help='enddate in isoformat 2018-01-31 (exclusive)'
        end: hug.types.text = None,
        filename: hug.types.text = None):
    """Download sms dialog file.

    No options: get yesterday.
    Only start: 24hours from start.
    Start and end: start(inclusive) to end(exclusive).
    """
    napi.download_sms_file(start, end, filename=filename)
