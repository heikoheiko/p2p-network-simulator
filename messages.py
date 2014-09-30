#from peer import Peer

class BaseMessage(object):
    base_size = 20

    def __init__(self, sender, data=None):
#        assert isinstance(sender, Peer)
        self.sender = sender
        self.data = data

    @property
    def size(self):
        return self.base_size + len(repr(self.data))

    def __repr__(self):
        return '<%s>' % self.__class__.__name__