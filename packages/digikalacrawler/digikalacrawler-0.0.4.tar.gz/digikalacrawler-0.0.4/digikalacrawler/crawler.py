import requests
class DigiKalaCrawler():
    def __init__(self, base_url):
        self.BASE_URL= base_url
    
    def crawl(self, product_id):
        response = requests.get(self.BASE_URL+"/"+product_id)
        return response.text