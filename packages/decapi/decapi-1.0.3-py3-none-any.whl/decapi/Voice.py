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