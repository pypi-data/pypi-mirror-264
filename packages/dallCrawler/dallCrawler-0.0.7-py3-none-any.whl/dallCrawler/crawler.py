import requests
from typing_extensions import Self, Any
import json
from bs4 import BeautifulSoup

class Crawler():
    def __init__(self, **kwargs):
        self.config = dict()
        for key, value in kwargs.items():
            self.config[key] = value
    
    def crawl(self, *params, **kwargs) -> Any:
        if('url' in self.params.keys()):
            try:
                response = requests.get(self.config['url'].format(*params))
                if 'type' in kwargs.keys():
                    if kwargs['type'] == 'json':
                        return json.loads(response.text)
                    elif kwargs['type'] == 'html':
                        soup = BeautifulSoup(response.text, 'html.parser')
                        return soup
                return response.text
            except:
                raise Exception("Number of paremeters {}, not match number of parameters in url {}".format(len(params) , self.config['url'].count("{}")))
        else:
            raise Exception("url parameter not set in crawler object. Use setUrl(url) method for setting it.")
    
    def setUrl(self, url: str) -> Self:
        self.params['url'] = url
        return self