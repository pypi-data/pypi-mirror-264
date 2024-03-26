from typing import TypeVar, Type, Any

from .base import Base
from ..marzban import Marzban

USER_TEMPLATE = TypeVar("USER_TEMPLATE", bound="UserTemplate")

class UserTemplate(Base):
    def __init__(
        self, **kwargs
    ) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    @classmethod
    async def create(cls: Type[USER_TEMPLATE], **kwargs) -> USER_TEMPLATE:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("POST", "/api/user_template", headers=headers, data=kwargs)
        return cls(**resp)
    
    async def save(self) -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("PUT", f"/api/user_template/{self.__dict__['id']}", headers=headers, data=self.__dict__)
        for k, v in resp.items():
            setattr(self, k, v)
    
    async def delete(self) -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        await Marzban._send_request("DELETE", f"/api/user_template/{self.__dict__['id']}", headers=headers)
    
    @classmethod
    async def get(cls: Type[USER_TEMPLATE], template_id: int) -> USER_TEMPLATE:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", f"/api/user_template/{template_id}", headers=headers)
        return cls(**resp)

    @classmethod
    async def all(cls: Type[USER_TEMPLATE]) -> list[USER_TEMPLATE]:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", f"/api/user_template", headers=headers)
        res = [cls(**x) for x in resp]
        return res