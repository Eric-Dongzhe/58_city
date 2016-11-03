

class PageController():

    def __call__(self, channel, page_num):
        pages = []
        for page in range(page_num+1):
            view_list = '{}/{}'.format(channel, page)
            pages.append(view_list)
