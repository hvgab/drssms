
# DRS API FOR NEVER.NO

## USAGE

THIS IS OUTDATED

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
Try to limit length here. There might be dragons.
```python
napi.download_sms_file('2018-01-01', '2018-02-01')
```

Test service sms
```python
napi.stop_dialog(12345678)  # Stop if open dialog
napi.send_service_sms(test_service, test_number, test_service)
```

Test push sms
```python
napi.send_push_sms(test_number, test_text, ani_text=test_ani)
```

That's about it.
