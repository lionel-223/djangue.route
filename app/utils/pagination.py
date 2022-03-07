import math


class Page(object):

    def __init__(self, items, page, page_size, total):
        self.items = items
        self.prev = None
        self.next = None
        self.has_prev = page > 1
        if self.has_prev:
            self.prev = page - 1
        previous_items = (page - 1) * page_size
        self.has_next = previous_items + len(items) < total
        if self.has_next:
            self.next = page + 1
        self.total = total
        self.pages = int(math.ceil(total / float(page_size)))


def paginate(query, page, page_size):
    if page <= 0:
        raise AttributeError('page needs to be >= 1')
    if page_size <= 0:
        raise AttributeError('page_size needs to be >= 1')
    items = query.limit(page_size).offset((page - 1) * page_size).all()
    total = query.order_by(None).count()  # We remove the ordering for better peroformance
    return Page(items, page, page_size, total)
