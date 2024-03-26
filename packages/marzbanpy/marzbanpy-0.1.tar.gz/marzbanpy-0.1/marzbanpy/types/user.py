from typing import TypeVar, Type, Any

from .base import Base
from ..marzban import Marzban

USER = TypeVar("USER", bound="User")

class User(Base):
    def __init__(
        self, **kwargs
    ) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    @classmethod
    async def create(cls: Type[USER], **kwargs) -> USER:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("POST", "/api/user", headers=headers, data=kwargs)
        return cls(**resp)
    
    async def save(self) -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("PUT", f"/api/user/{self.__dict__['username']}", headers=headers, data=self.__dict__)
        for k, v in resp.items():
            setattr(self, k, v)
    
    async def usage(self) -> dict:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", f"/api/user/{self.__dict__['username']}/usage", headers=headers)
        return resp

    async def set_owner(self, admin_username: str) -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        data = {
            'admin_username': admin_username
        }
        resp = await Marzban._send_request("PUT", f"/api/user/{self.__dict__['username']}/set-owner", headers=headers, data=data, use_data=True)
        for k, v in resp.items():
            setattr(self, k, v)
    
    async def reset(self) -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("POST", f"/api/user/{self.__dict__['username']}/reset", headers=headers)
        for k, v in resp.items():
            setattr(self, k, v)
    
    async def revoke_sub(self) -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("POST", f"/api/user/{self.__dict__['username']}/revoke_sub", headers=headers)
        for k, v in resp.items():
            setattr(self, k, v)
    
    async def delete(self) -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        await Marzban._send_request("DELETE", f"/api/user/{self.__dict__['username']}", headers=headers)
    
    @classmethod
    async def get(cls: Type[USER], username: str) -> USER:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", f"/api/user/{username}", headers=headers)
        return cls(**resp)

    @classmethod
    async def all(cls: Type[USER]) -> list[USER]:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", f"/api/users", headers=headers)
        res = [cls(**x) for x in resp['users']]
        return res

    @classmethod
    async def get_expired(cls: Type[USER]) -> list[str]:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", f"/api/users/expired", headers=headers)
        return resp

    @staticmethod
    async def reset_all() -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        await Marzban._send_request("POST", f"/api/users/reset", headers=headers)

    @staticmethod
    async def reset_all() -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        await Marzban._send_request("POST", f"/api/users/reset", headers=headers)
    
    @staticmethod
    async def delete_expired() -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        await Marzban._send_request("DELETE", f"/api/users/expired", headers=headers)