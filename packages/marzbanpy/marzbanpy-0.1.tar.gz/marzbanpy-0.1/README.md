# marzbanpy
An unofficial package for marzban panel

## Donation
This project was and is being written under a beer :)

If you want to support me and help the development of the project, here are ways to donate:

- BTC: `bc1qmrwu6uv00xcvsjvjkwnaw2ky6aenhjgqewg0w4`

- USDT (TRC-20): `TJUUhJpeaZBBXpG6yUtzLsQmT3XQjViowV`

- ETH: `0x052D18812fA247Ce6853a6D95213CEbdb45c6277`

- BANK CARD (RU): `5536 9139 1278 5017`

## Installation
```shell
pip install marzbanpy
```

## Usage example

```python
import asyncio

from marzbanpy import Marzban
from marzbanpy.types import User

Marzban.setup('https://xray.penetrates.everything', 'admin', 'GodSaveTheQueen')

async def main():
    admin_token = await Marzban.get_token()
    admin_token = await Marzban.get_token(renewal=True)
    users: list[User] = await User.all()
    print(len(users))
    print(users[:5])
    user: User = await User.create(
        username='example',
        proxies={},
        inbounds={},
        status='active',
        expire=0
    )
    print(user) # {'username': 'example', 'proxies': {}, ...}
    user['status'] = 'disabled'
    await user.save()
    await user.delete()

asyncio.run(main())

```

## License

The project is under the [MIT](https://github.com/YoungVPN/marzbanpy/blob/main/LICENSE) licence

## Contacts

Email: <bertollo@gunship.su>

Telegram: [@blackbloodredkiss](https://t.me/blackbloodredkiss)