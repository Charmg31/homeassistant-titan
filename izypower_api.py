import asyncio
import aiohttp
import json
from typing import Dict, Any, List

class IzyPowerAPI:
    """Gère la communication HTTP avec les appareils Titan IzyPower."""

    def __init__(self, host: str, port: int, session: aiohttp.ClientSession):
        self.host = host
        self.port = port
        self.session = session
        self.base_url = f"http://{host}:{port}/rpc"
        self.timeout = aiohttp.ClientTimeout(total=60)

    async def fetch_data(self, keys: List[str]) -> Dict[str, Any]:
        """Récupère les données JSON depuis le dispositif Titan."""
        config_param = json.dumps({"t": keys}).replace(" ", "")
        url = f"{self.base_url}/IzyPower.GetData?config={config_param}"

        try:
            async with self.session.post(url, timeout=self.timeout) as response:
                if response.status != 200:
                    raise Exception(f"Erreur HTTP: {response.status}")
                return await response.json()

        except asyncio.TimeoutError:
            raise Exception("IzyPower.GetData délai dépassé (timeout)")
        except aiohttp.ClientError as err:
            raise Exception(f"IzyPower.GetData erreur réseau: {err}")

    async def set_data(self, f: int, t: int, v: list) -> Dict[str, Any]:
        """Envoie des données JSON brutes au dispositif Titan."""
        config_param = json.dumps({"f": f, "t": t, "v": v}).replace(" ", "")
        url = f"{self.base_url}/IzyPower.SetData?config={config_param}"

        try:
            async with self.session.post(url, timeout=self.timeout) as response:
                if response.status != 200:
                    raise Exception(f"Erreur HTTP: {response.status}")
                return await response.json()

        except asyncio.TimeoutError:
            raise Exception("IzyPower.SetData délai dépassé (timeout)")
        except aiohttp.ClientError as err:
            raise Exception(f"IzyPower.SetData erreur réseau: {err}")

