import time

class SimpleKVStoreWithTTL:
    def __init__(self):
        self.store = {}
        self.expiry = {}

    def set(self, key, value, ttl=None):
        self.store[key] = value
        if ttl:
            self.expiry[key] = time.time() + ttl

    def get(self, key):
        if key in self.expiry and time.time() > self.expiry[key]:
            self.delete(key)
            return None
        return self.store.get(key, None)

    def delete(self, key):
        if key in self.store:
            del self.store[key]
        if key in self.expiry:
            del self.expiry[key]

    def mset(self, kv_pairs, ttl=None):
        for key, value in kv_pairs.items():
            self.set(key, value, ttl)

    def mget(self, *keys):
        return [self.get(key) for key in keys]

