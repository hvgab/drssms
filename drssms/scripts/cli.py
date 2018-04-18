
from drssms import NeverAPI
import click
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.group()
def main():
    napi = NeverAPI()

@main.command()
@click.argument('number')
@click.argument('text')
@click.option('--ani')
def push(number, text, ani):
    """ Sent push SMS to number without service. """
    napi = NeverAPI()
    napi.login()

    napi.send_push_sms(number, text, ani)

@main.command()
@click.argument('number')
@click.argument('serviceid')
@click.option('--text', help='sms text to overwrite service. remember quotationmarks')
def service(serviceid, number, text):
    """ Send service SMS to number, optionally overwrite text """
    napi = NeverAPI()
    napi.login()

    napi.send_service_sms(number, serviceid, text)


@main.command()
@click.argument('number')
def stop(number):
    """ Stop an active SMS dialog. """
    napi = NeverAPI()
    napi.login()

    napi.stop_dialog(number)

@main.command()
@click.option('--start', help='startdate in isoformat 2018-01-31 (inclusive)')
@click.option('--end', help='enddate in isoformat 2018-01-31 (exclusive)')
def download_sms(start, end, name='download-sms'):
    """ Download sms dialog file.

        \b
        No options: get yesterday.
        Only start: 24hours from start.
        Start and end: start(inclusive) to end(exclusive).
     """
    napi = NeverAPI()
    napi.login()

    napi.download_sms_file(start, end)
