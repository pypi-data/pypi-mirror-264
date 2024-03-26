from typing import TypeVar, Type, Any

from .base import Base
from ..marzban import Marzban

ADMIN = TypeVar("ADMIN", bound="Admin")

class Admin(Base):
    def __init__(
        self, **kwargs
    ) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    async def current() -> dict:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", f"/api/admin", headers=headers)
        return resp

    @classmethod
    async def create(cls: Type[ADMIN], **kwargs) -> ADMIN:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("POST", "/api/admin", headers=headers, data=kwargs)
        return cls(**resp)
    
    async def save(self) -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("PUT", f"/api/admin/{self.__dict__['username']}", headers=headers, data=self.__dict__)
        for k, v in resp.items():
            setattr(self, k, v)
    
    async def delete(self) -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        await Marzban._send_request("DELETE", f"/api/admin/{self.__dict__['username']}", headers=headers)

    @classmethod
    async def all(cls: Type[ADMIN]) -> list[ADMIN]:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", f"/api/admins", headers=headers)
        res = [cls(**x) for x in resp]
        return res