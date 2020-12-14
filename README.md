
# DRS API FOR NEVER.NO

Downloads sms logs and sends smses via old sms system no longer in use.

## USAGE

Init
```python
from drssms import NeverAPI

napi = NeverAPI()
napi.login()  # Needed for downloading and sending sms.

test_number = 12345678
test_text = 'Test SMS'

test_ani = 'Santa Claus'
```

Download sms file
Args: start and end date-string.
Try to limit timeframe to a month here. There might be dragons.
```python
napi.download_sms_file('2018-01-01', '2018-02-01')
napi.download_sms_file('2018-01-01')
napi.download_sms_file()
```

Test service sms
```python
napi.stop_dialog(test_number)  # Stop if open dialog
napi.send_service_sms(test_number, test_service, message=None)
```

Test push sms
```python
napi.send_push_sms(test_number, test_text, ani=test_ani)
```

## cli script

```
sms --help
sms push 12345678 "my message"
sms service 12345678 10
sms download_sms
```


That's about it.
