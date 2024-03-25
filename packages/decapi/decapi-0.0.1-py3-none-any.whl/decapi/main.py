# DECAPI for DECTalk
print("DECAPI for DECTalk")

class DecApiError(Exception):
    pass

dectalkpath=""
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

import os
import asyncio
import subprocess

class Voice:
    """
    Class for DECTalk voices.
    
    ap - Average pitch, in Hz
    
    as - Assertiveness, in % 
    
    b4 - Fourth formant bandwidth, in Hz 
    
    b5 - Fifth formant bandwidth, in Hz 
    
    bf - Baseline fall, in Hz 
    
    br - Breathiness, in decibels (dB) 
    
    f4 - Fourth formant resonance frequency, in Hz 
    
    f5 - Fifth formant resonance frequency, in Hz 
    
    hr - Hat rise, in Hz 
    
    hs - Head size, in % 
    
    la - Laryngealization, in % 
    
    lx - Lax breathiness, in % 
    
    nf - Number of fixed samples of open glottis 
    
    pr - Pitch range, in % 
    
    qu - Quickness, in % 
    
    ri - Richness, in % 
    
    sm - Smoothness, in % 
    
    sr - Stress rise, in Hz 
    
    sx - Sex 1 (male) or 0 (female)
    """    
    def __init__(self,ap,as_,b4,b5,bf,br,f4,f5,hr,hs,la,lx,nf,pr,qu,ri,sm,sr,sx):
        self.voice=[ap,as_,b4,b5,bf,br,f4,f5,hr,hs,la,lx,nf,pr,qu,ri,sm,sr,sx]
    def getString(self):
        dvcmd=dv("ap",self.voice[0])
        dvcmd+=dv("as",self.voice[1])
        dvcmd+=dv("b4",self.voice[2])
        dvcmd+=dv("b5",self.voice[3])
        dvcmd+=dv("bf",self.voice[4])
        dvcmd+=dv("br",self.voice[5])
        dvcmd+=dv("f4",self.voice[6])
        dvcmd+=dv("f5",self.voice[7])
        dvcmd+=dv("hr",self.voice[8])
        dvcmd+=dv("hs",self.voice[9])
        dvcmd+=dv("la",self.voice[10])
        dvcmd+=dv("lx",self.voice[11])
        dvcmd+=dv("nf",self.voice[12])
        dvcmd+=dv("pr",self.voice[13])
        dvcmd+=dv("qu",self.voice[14])
        dvcmd+=dv("ri",self.voice[15])
        dvcmd+=dv("sm",self.voice[16])
        dvcmd+=dv("sr",self.voice[17])
        dvcmd+=dv("sx",self.voice[18])
        return dvcmd
def dv(opt,val):
    return "[:dv "+str(opt)+" "+str(val)+"]"
class emptyClass:
    """
    An... empty class?
    
    Well of course.
    """
    pass
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
currVoice=Defaults().Paul

defaultVoices=Defaults()
"""
Class for DECTalk default voices.
Available voices:
    Paul
"""

def useVoice(voice):
    """
    Function to use a DECTalk voice.
    Usage:
        useVoice(voice)
    """
    currVoice=voice
    #print("Using voice: "+str(currVoice))

async def sayAsync(text):
    """
    Function to say text using DECTalk.
    Usage:
        await sayAsync(text)
    """
    global currVoice
    if not currVoice.getString():
        raise DecApiError("Voice not set")
    with open('text.txt', 'w') as f:
        f.write(currVoice.getString())
        f.write(text)
        f.write('\n')
    # check if failed to exec
    proc=await asyncio.create_subprocess_exec(
        dectalkpath,"-fi","text.txt",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise DecApiError("SAY failed: "+str(stderr))
    os.remove('text.txt')
def say(text):
    """
    Function to say text using DECTalk.
    Usage:
        say(text)
    """
    global currVoice
    if not currVoice.getString():
        raise DecApiError("Voice not set")
    with open('text.txt', 'w') as f:
        f.write(currVoice.getString())
        f.write(text)
        f.write('\n')
    # check if failed to exec
    proc=subprocess.run(
        [dectalkpath,"-fi","text.txt"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stderr = proc.stderr
    if proc.returncode != 0:
        raise DecApiError("SAY failed: "+str(stderr))
    os.remove('text.txt')