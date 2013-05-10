
class MockQuery(object):
    def __init__(self, store=None):
        self._store = store
        if store is None:
            self._store = []

    def __call__(self, *args):
        return self

    def filter_by(self, **kwargs):
        if not kwargs:
            return self
        new_store = []
        for item in self._store:
            matching = True
            for key, value in kwargs.items():
                if not hasattr(item, key):
                    return
                if getattr(item, key) != value:
                    matching = False
            if matching:
                new_store.append(item)

        self._store = new_store
        return self

    def order_by(self, *args):
        return self

    def all(self):
        return self._store

    def first(self):
        if len(self._store) > 0:
            return self._store[0]
        else:
            return None

    def get(self, primary_key_val):
        if len(self._store) > 0:
            return self._store[0]
        else:
            return None

    def delete(self, *args):
        # match the SQLAlchemy API
        num_deleted = len(self._store)
        self._store = []
        return num_deleted

    def filter(self, *args):
        # This doesn't actually apply the filter logic,
        # stuff from the Comparator and InstrumentedAttributes
        # classes need to be mocked for it to do so well.
        return self

    def count(self):
        return len(self._store)


class MockSession(object):
    def __init__(self, store=None):
        self._store = store
        if store is None:
            self._store = []

        self.query = MockQuery(store=self._store)

    def __call__(self):
        return self

    def delete(self, obj):
        if obj in self._store:
            self._store.remove(obj)
