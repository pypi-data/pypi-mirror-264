# Dall Crawler Package

This is a crawler.

```
from dallCrawler import Crawler

crawler = Crawler(url="https://example.com/{}/v2/{}")
# url can be set by setUrl(url) method
# type is optional
crawler.crawl("41257", "1", type='json')
```