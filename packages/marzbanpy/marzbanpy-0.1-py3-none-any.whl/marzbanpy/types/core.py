from .base import Base
from ..marzban import Marzban

class Core(Base):
    @staticmethod
    async def get() -> dict:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", f"/api/core", headers=headers)
        return resp
    
    @staticmethod
    async def restart() -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        await Marzban._send_request("POST", f"/api/core/restart", headers=headers)
    
    @staticmethod
    async def get_config() -> dict:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", f"/api/core/config", headers=headers)
        return resp
    
    @staticmethod
    async def update_config(data: dict) -> None:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("PUT", f"/api/core/config", headers=headers, data=data)