class NaiveIndex:
    """ Naive Index based on sequential search """

    def __init__(self, table):
        self.keys = [item.key() for item in table]
        self.is_deleted = [False for i in range(len(table))]

    def look_up(self, key):
        result = []
        for rid, k in enumerate(self.keys):
            if not self.is_deleted[rid] and k == key:
                result.append(rid)
        return result

    def insert(self, key):
        self.keys.append(key)
        self.is_deleted.append(False)

    def update(self, rid, key):
        self.keys[rid] = key

    def delete(self, rid):
        self.is_deleted[rid] = True
