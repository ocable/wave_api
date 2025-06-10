from curl_cffi import requests
import os
from pydantic import BaseModel
from rich import print

higgins_spot_id = "5842041f4e65fad6a77089dc"


class WindData(BaseModel):
    timestamp: int
    speed: float
    direction: float
    directionType: str
    gust: float
    optimalScore: int

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "speed": self.speed,
            "direction": self.direction,
            "directionType": self.directionType,
            "gust": self.gust,
            "optimalScore": self.optimalScore
    }



def new_session():
    session = requests.Session(impersonate = "chrome", proxy = os.getenv("stickyproxy"))
    return session

def getWindData(session: requests.Session, spotId: str):
    url = f"https://services.surfline.com/kbyg/spots/forecasts/wind?spotId={spotId}&days=5&intervalHours=1&corrected=false&cacheEnabled=true&units%5BwindSpeed%5D=KTS"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'}
    resp = session.get(url, headers = headers)
    resp.raise_for_status()
    wind_data_list = resp.json()["data"]["wind"]
    data = [WindData(**item) for item in wind_data_list]
    return data



def main():
    session = new_session()
    windData = getWindData(session, higgins_spot_id)
    data = []
    for item in windData:
        data.append(item)
    return data
    


if __name__ == "__main__":
    print(main())

