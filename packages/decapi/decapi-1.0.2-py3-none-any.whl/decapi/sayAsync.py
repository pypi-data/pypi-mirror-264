import asyncio, os
from . import dectalkpath, DecApiError, currVoice
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