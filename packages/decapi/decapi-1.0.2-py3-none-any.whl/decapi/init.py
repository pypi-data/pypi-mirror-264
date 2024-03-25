from . import DecApiError
from . import Defaults
from .init2 import dectalkpath
import os
def init():
    """
    Function to initialize DECTalk.
    """
    # DECTalk initialization (which is actually just double checking that everything is OK)
    if not os.path.exists(dectalkpath):
        raise DecApiError("SAY executable does not exist")
    if dectalkpath=="":
        raise DecApiError("SAY executable path not set")
    currVoice=Defaults().Paul