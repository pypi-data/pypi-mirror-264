import subprocess, os
from . import dectalkpath, DecApiError, currVoice
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