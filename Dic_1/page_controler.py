class PageControler:
    def __init__(self, channel_url):
        self.channel_url = channel_url

    def get_pages_url(self, page_num):

        page_url = []
        for page in range(1, page_num+1):
             page_url.append(self.channel_url + page)

