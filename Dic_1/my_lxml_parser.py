# encoding: utf-8

from lxml import etree


class ChannelPageParser:
    def __init__(self, html):
        self.html = html

    def __call__(self):
        """"""
        tree = etree.HTML(self.html)
        links = []
        try:
            links_nodes = tree.xpath("//td[@class='t']")
            for url in links_nodes:
                try:
                    link = url.xpath("a/@href")
                except:
                    link = None
                links.append(link[0])
        except:
            links = None
        return links

    def get_data(self):
        """"""
        tree = etree.HTML(self.html)
        result = []
        nodes = tree.xpath("tr[@class]")

        for node in nodes:
            res_data = {'title': node.xpath("td[@class='t']/a/text()"),
                        'price': node.xpath("td[@class='t']//span[@class='price']/text()"),
                        # 'price': node.xpath("//span[@class='price']/text()"),
                        'location': node.xpath("td[@class='t']/span[@class='fl']/span/text()"),
                        'img': node.xpath("td[@class='img']/a/@href"),
                        'link': node.xpath("td[@class='t']/a/@href"),
                        }
            result.append(res_data)
        return result
