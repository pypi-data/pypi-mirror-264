import requests
from typing_extensions import Self, Any
import json
from bs4 import BeautifulSoup

class Crawler():
    def __init__(self, **kwargs):
        self.config = {
            "method": "get"
            }
        for key, value in kwargs.items():
            self.config[key] = value
    
    def crawl(self, *params, **kwargs) -> Any:
        if('url' in self.config.keys() or 'url' in kwargs.keys()):
            url = self.config['url'] if 'url' in self.config.keys() else  kwargs['url']
            if len(params) == url.count("{}"):
                try:
                    req = getattr(requests, self.config['method'])
                    response = req(url.format(*params))
                    if 'type' in kwargs.keys():
                        if kwargs['type'] == 'json':
                            return json.loads(response.text)
                        elif kwargs['type'] == 'html':
                            print('html')
                            soup = BeautifulSoup(response.text, 'html.parser')
                            return soup
                    return response.text
                except Exception as e:
                    print(e)
            else:
                raise Exception("Number of paremeters {}, not match number of parameters in url {}".format(len(params) , url.count("{}")))
        else:
            raise Exception("url parameter not set in crawler object. Use setUrl(url) method for setting it.")
    
    def setUrl(self, url: str) -> Self:
        self.params['url'] = url
        return self
    