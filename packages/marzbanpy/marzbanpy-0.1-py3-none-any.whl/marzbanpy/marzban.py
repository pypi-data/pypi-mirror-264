import aiohttp


class Marzban(object):

    host: str = None
    login: str = None
    password: str = None
    token: str = None

    @staticmethod
    def setup(host: str, login: str, password: str) -> None:
        Marzban.host = host
        Marzban.login = login
        Marzban.password = password

    @staticmethod
    async def get_token(renew: bool = False) -> str:
        if not renew and Marzban.token is not None:
            return Marzban.token
        data = {
            "username": Marzban.login,
            "password": Marzban.password
        }
        resp = await Marzban._send_request("POST", "/api/admin/token", data=data, use_data=True)
        Marzban.token = resp["access_token"]
        return Marzban.token
    
    @staticmethod
    async def system_info() -> dict:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", "/api/system", headers=headers)
        return resp
    
    @staticmethod
    async def inbounds() -> dict:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", "/api/inbounds", headers=headers)
        return resp
    
    @staticmethod
    async def get_hosts() -> dict:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("GET", "/api/hosts", headers=headers)
        return resp

    @staticmethod
    async def update_hosts(data: dict) -> dict:
        headers = {
            'Authorization': f'Bearer {Marzban.token}'
        }
        resp = await Marzban._send_request("PUT", "/api/hosts", headers=headers, data=data)
        return resp
    
    @staticmethod
    async def _send_request(method, path, headers=None, params=None, data=None, use_data: bool = False) -> dict | list:
        async with aiohttp.ClientSession() as session:
            if use_data:
                async with session.request(method, Marzban.host + path, headers=headers, params=params, data=data) as resp:
                    if 200 <= resp.status < 300:
                        body = await resp.json()
                        return body
                    else:
                        raise Exception(f"Error: {resp.status}; Body: {await resp.text()}; Data: {data}")
            else:
                async with session.request(method, Marzban.host + path, headers=headers, params=params, json=data) as resp:
                    if 200 <= resp.status < 300:
                        body = await resp.json()
                        return body
                    else:
                        raise Exception(f"Error: {resp.status}; Body: {await resp.text()}; Data: {data}")