# DICE Python SDK

Official Python SDK for the DICE multi-channel messaging platform by Auxilo Finserve.
Send messages via WhatsApp, SMS, and Email with a single unified client.

---

## Requirements

- Python >= 3.8
- requests

---

## Installation

### Via pip (GitHub)

```bash
pip install git+https://github.com/Tushar216-507/auxilo-dice-sdk.git
```

### Specific version

```bash
pip install git+https://github.com/Tushar216-507/auxilo-dice-sdk.git@v1.0.0
```

### Add to requirements.txt

```
git+https://github.com/Tushar216-507/auxilo-dice-sdk.git@v1.0.0
```

---

## Setup

Add your DICE credentials to your `.env` file:

```env
DICE_USERNAME=your_username
DICE_PASSWORD=your_password
DICE_BASE_URL=https://apimartech.auxilo.com
```

---

## Usage

### Initialize the Client

```python
import os
from dotenv import load_dotenv
from dice_sdk import DiceClient

load_dotenv()

dice = DiceClient(
    username=os.getenv('DICE_USERNAME'),
    password=os.getenv('DICE_PASSWORD'),
    base_url=os.getenv('DICE_BASE_URL')
)
```

---

### Send Email

```python
result = dice.email.send(
    email='vendor@example.com',
    template_id='invoice_cleared',
    template_attr={
        'invoice_number': 'INV-001',
        'vendor': 'Acme Pvt Ltd'
    },
    subject='Invoice Cleared'
)

if result['success']:
    print('Email sent successfully')
    print('Ref ID:', result['data']['ref_id'])
else:
    print('Failed:', result['error'])
```

---

### Send WhatsApp

```python
result = dice.whatsapp.send(
    mobile_no='917977251637',
    template_id='invoice_cleared',
    template_attr={
        'header_value': {'value': 'Acme Pvt Ltd'},
        'body_value': ['INV-001', '15 Apr 2026']
    }
)

if result['success']:
    print('WhatsApp sent successfully')
```

---

### Send SMS

```python
result = dice.sms.send(
    mobile_no='917977251637',
    template_id='otp_template',
    template_attr={'otp': '123456'}
)

if result['success']:
    print('SMS sent successfully')
```

---

## Method Signatures

### Email

```python
dice.email.send(
    email: str,
    template_id: str,
    template_attr: dict,
    subject: str,
    source: str = 'SDK',
    email_from_name: str = 'DICE SDK'
)
```

### WhatsApp

```python
dice.whatsapp.send(
    mobile_no: str,
    template_id: str,
    template_attr: dict,
    source: str = 'SDK',
    message_type: str = 'transactional'
)
```

### SMS

```python
dice.sms.send(
    mobile_no: str,
    template_id: str,
    template_attr: dict,
    source: str = 'SDK',
    message_type: str = 'transactional'
)
```

---

## Response Format

Every `send()` call returns a dictionary:

### Success
```python
{
    'success': True,
    'response_status': 200,
    'data': {
        'message': 'Communication processed successfully.',
        'ref_id': '0109019db93c...',
        'status': 'success'
    }
}
```

### Failure
```python
{
    'success': False,
    'response_status': 401,
    'error': 'Token expired'
}
```

---

## Error Handling

```python
from dice_sdk import (
    DiceClient,
    DiceSendError,
    DiceAuthError,
    DiceTokenExpiredError,
    DiceNewIPError,
    DiceTemplateError,
    DiceValidationError,
    DiceConnectionError
)

try:
    result = dice.email.send(...)
except DiceTokenExpiredError:
    print('Token expired — create a new token on the DICE dashboard')
except DiceNewIPError:
    print('New IP detected — check your email to approve access')
except DiceTemplateError:
    print('Template not found — check your template ID')
except DiceValidationError as e:
    print(f'Validation error: {e}')
except DiceConnectionError:
    print('Could not reach DICE server — check your network')
except DiceSendError as e:
    print(f'DICE error: {e}')
```

---

## Exception Reference

| Exception | When it's raised |
|---|---|
| `DiceAuthError` | Token could not be fetched |
| `DiceTokenExpiredError` | Token has expired |
| `DiceNewIPError` | Request blocked — unrecognised IP |
| `DiceTemplateError` | Template ID not found in DICE |
| `DiceValidationError` | Missing required field (e.g. template_id) |
| `DiceConnectionError` | Could not reach DICE server |

---

## Mobile Number Formatting

WhatsApp and SMS channels automatically normalize Indian mobile numbers:

| Input | Formatted |
|---|---|
| `9177XXXXXXXX` (10 digits) | `919177XXXXXXXX` |
| `919177XXXXXXXX` (12 digits) | `919177XXXXXXXX` |
| Any other format | Last 10 digits with `91` prefix |

---

## Security

- Credentials are never stored in the SDK — passed in at runtime via environment variables
- Bearer token is cached in memory and refreshed automatically — never written to disk
- SDK sends metadata headers on every request (`X-Dice-SDK-Version`, `X-Dice-SDK-Runtime`, `X-Dice-SDK-Platform`) for IP tracking and audit logs on the DICE dashboard
- New IP detection — if a request comes from an unrecognised IP, DICE blocks it and emails the token owner for approval

---

## How Authentication Works

```
First call:
  username + password → DICE Auth API → Bearer token → cached in memory

Subsequent calls:
  cached Bearer token reused → no auth call

Token expired:
  Bearer token auto-refreshed → seamless, no developer action needed
```

---

## Versioning

This SDK follows [Semantic Versioning](https://semver.org):

- `PATCH` — bug fixes (1.0.0 → 1.0.1)
- `MINOR` — new features, backward compatible (1.0.0 → 1.1.0)
- `MAJOR` — breaking changes (1.0.0 → 2.0.0)

---

## License

MIT