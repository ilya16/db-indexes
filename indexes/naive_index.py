class NaiveIndex:
    """ Naive Index based on sequential search """

    def __init__(self, table):
        self.table = table

    def look_up(self, item_k):
        for ind, p in enumerate(self.table):
            if p.key() == item_k.key():
                return p
