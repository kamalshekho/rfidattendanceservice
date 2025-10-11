import time

class DummyReader:

    def __init__(self):
        self.uids = ["12345678", "87654321", "ABCDEF01"]
        self.index = 0

    def readline(self):
        time.sleep(1)
        uid = self.uids[self.index]
        self.index = (self.index + 1) % len(self.uids)
        return (uid + "\n").encode('utf-8')

    def close(self):
        print("DummyReader closed")
