from typing import TypeVar, Type, Any

from .base import Base
from ..marzban import Marzban

NODE = TypeVar("NODE", bound="Node")

class Node(Base):
    def __init__(
        self, **kwargs
    ) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    @classmethod
    async def create(cls: Type[NODE], **kwargs) -> NODE:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("POST", "/api/node", headers=headers, data=kwargs)
        return cls(**resp)
    
    async def save(self) -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("PUT", f"/api/node/{self.__dict__['id']}", headers=headers, data=self.__dict__)
        for k, v in resp.items():
            setattr(self, k, v)
    
    async def delete(self) -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        await Marzban._send_request("DELETE", f"/api/node/{self.__dict__['id']}", headers=headers)
    
    async def reconnect(self) -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        await Marzban._send_request("POST", f"/api/node/{self.__dict__['id']}/reconnect", headers=headers)
    
    @staticmethod
    async def settings() -> dict:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", f"/api/node/settings", headers=headers)
        return resp

    @staticmethod
    async def usage() -> dict:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", f"/api/nodes/usage", headers=headers)
        return resp
    
    @classmethod
    async def get(cls: Type[NODE], node_id: int) -> NODE:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", f"/api/node/{node_id}", headers=headers)
        return cls(**resp)

    @classmethod
    async def all(cls: Type[NODE]) -> list[NODE]:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", f"/api/nodes", headers=headers)
        res = [cls(**x) for x in resp]
        return res