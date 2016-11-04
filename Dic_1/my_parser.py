# encoding: utf-8

from bs4 import BeautifulSoup


class ChannelPageParser:
    def __init__(self, html):
        self.html = html

    def __call__(self):
        """"""
        soup = BeautifulSoup(self.html.text, 'lxml')
        links = []
        try:
            links_nodes = soup.find_all("td", class_="t")
            for url in links_nodes:
                try:
                    link = url.find("a")
                except:
                    link = None

                links.append(link['href'])
        except:
            links = None
        # try:
        #     item_url = soup.find('li', class_="next").find(href=re.compile(r"/page/"))
        # except:
        #     return None
        # return urlparse.urljoin(page_url, item_url['href'])
        return links

    def get_data(self):
        """"""
        soup = BeautifulSoup(self.html.text, 'lxml')
        result = []
        title_nodes = soup.select('td.t > a')

        for title in title_nodes:
            # put these datas in a dic respectly
            res_data = {'title': title.get_text()}
            result.append(res_data)
        return result