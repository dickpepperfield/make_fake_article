from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from pexels_api import API
import requests

def getImage(get_args):
    # Setup requests.get resiliancy
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    # Connect PEXELS API
    api = API(PEXELS_API_KEY)
    api.search(get_args.category, page=random.randint(0,20), results_per_page=1)
    photos = api.get_entries()
    # Grab landscape image
    for photo in photos:
        response = http.get(photo.landscape, allow_redirects=True, timeout=10)
        open('tmp/temp_img.png', 'wb').write(response.content)