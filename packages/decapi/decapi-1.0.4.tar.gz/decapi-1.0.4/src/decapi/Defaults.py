from . import Voice

class Defaults:
    """
    Class for DECTalk default voices.
    Available voices:
        Paul
    """
    def __init__(self):
        self.Paul=Voice(112,100,280,330,18,0,3300,3650,18,100,0,0,10,100,40,80,30,25,1)
        """
        Perfect Paul.
        """