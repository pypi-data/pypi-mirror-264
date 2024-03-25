import requests
from typing_extensions import Self
import json

class Crawler():
    def __init__(self, **kwargs):
        self.params = dict()
        for key, value in kwargs.items():
            self.params[key] = value
    
    def crawl(self, *params, **kwargs) -> str:
        if('url' in self.params.keys()):
            try:
                response = requests.get(self.params['url'].format(*params))
                if 'type' in kwargs.keys():
                    if kwargs['type'] == 'json':
                        return json.loads(response.text)
                return response.text
            except:
                raise Exception("Number of paremeters {}, not match number of parameters in url {}".format(len(params) , self.params['url'].count("{}")))
        else:
            raise Exception("url parameter not set in crawler object. Use setUrl(url) method for setting it.")
    
    def setUrl(self, url: str) -> Self:
        self.params['url'] = url
        return self