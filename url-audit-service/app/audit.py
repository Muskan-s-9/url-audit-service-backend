import asyncio
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def analyze_url(url: str) -> dict[str, object]:
    try:
        parsed = urlparse(url)
    except Exception:
        return {"is_valid": False, "domain": "", "scheme": "", "path": "", "status_code": None, "title": ""}

    if not parsed.scheme or not parsed.netloc:
        return {"is_valid": False, "domain": "", "scheme": parsed.scheme or "", "path": parsed.path or "", "status_code": None, "title": ""}

    try:
        response = requests.get(url, timeout=15, allow_redirects=True)
        print("response",response.status_code)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.get_text(strip=True) if soup.title else ""
        return_reponse =  {
            "is_valid": True,
            "domain": parsed.netloc, 
            "scheme": parsed.scheme,
            "path": parsed.path,
            "status_code": response.status_code,
            "title": title,
        }
        print("return_reponse",return_reponse)
        return return_reponse
    except requests.RequestException:
        print("error", parsed.netloc)
        return {"is_valid": False, "domain": parsed.netloc, "scheme": parsed.scheme, "path": parsed.path, "status_code": None, "title": ""}


async def analyze_url_async(url: str, timeout_seconds: float) -> dict[str, object]:
    return await asyncio.wait_for(asyncio.to_thread(analyze_url, url), timeout=timeout_seconds)
