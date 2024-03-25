# Dall Crawler Package

This is a crawler.

```
from dallCrawler import Crawler

crawler = Crawler(urls = "https://example.com/{}/v2/{}")
crawler.crawl("41257", "1", type='json')
```