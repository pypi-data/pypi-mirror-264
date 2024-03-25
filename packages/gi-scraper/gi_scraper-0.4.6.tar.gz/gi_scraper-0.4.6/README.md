# Google-Image-Scraper

## About

This module is based on web-scraping technology and uses Google Images to provide a Streamable Image API.

### Supported Browsers

- **Chrome**

## How to Use?

```python
# import Scraper class
from gi_scraper import Scraper


# Pass a Cache instance with a custom directory path and timeout
# Set cache timeout to -1 for caching indefinitely

"""
from gi_scraper import Cache

cache = Cache(dir_path="gi_cache", timeout=-1)
sc = Scraper(workers=8, headless=False, cache=cache)
"""

# The object creation has an overhead time
# The same object can be reused to fire multiple queries
sc = Scraper(headless=False)

for query, count in {"Naruto": 20, "Gintoki": 30}.items():
    print("Scraping...", query, ":", count)

    # scrape method returns a stream object
    stream = sc.scrape(query, count)

    # stream.get method yields Response object with following attributes
    # - query (str): The query associated with the response.
    # - name (str): The name attribute of the response.
    # - src_name (str): The source name attribute of the response.
    # - src_page (str): The source page attribute of the response.
    # - thumbnail (str): The thumbnail attribute of the response.
    # - image (str): The image attribute of the response.
    # - width (int): The width attribute of the response.
    # - height (int): The height attribute of the response.

    for index, response in enumerate(stream.get()):
        if index == 10:
            sc.terminate_query()  # Terminate current query midway
            break
        # response.to_dict returns python representable dictionary
        print(response.width, "x", response.height, ":", response.image)


# call this to terminate scraping (auto-called by destructor)
sc.terminate()
```
