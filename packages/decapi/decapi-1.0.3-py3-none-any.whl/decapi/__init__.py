"""
DECAPI for DECTalk
"""
print("DECAPI for DECTalk version 1.0.0")
from .init import init
from .say import say
from .sayAsync import sayAsync
from .useVoice import useVoice
from .Defaults import Defaults
from .dv import dv
from .Voice import Voice
from .EmptyClass import emptyClass
from .DecApiError import DecApiError
from . import init2
"""
Class for DECTalk default voices.
Available voices:
    Paul
"""

__all__=["init","say","sayAsync","useVoice","Defaults","dv","Voice","emptyClass","DecApiError"]