import os
from captionstransformer import sbv, srt, transcript, ttml, vtt, rt

"""
See https://support.google.com/youtube/answer/2734698?hl=en
for a nice format listing
"""

REGISTRY = {
    'ttml': {
        'id': 'ttml',
        'reader': ttml.Reader,
        'writer': ttml.Writer,
        'mimetype': 'application/ttml+xml',
        'extensions': ('.dfxp', '.ttml', '.xml',)
    },
    'transcript':{
        'id': 'transcript',
        'reader': transcript.Reader,
        'writer': transcript.Writer,
        'mimetype': 'text/xml',
        'extensions': '.xml'
    },
    'sbv': {
        'id': 'sbv',
        'reader': sbv.Reader,
        'writer': sbv.Writer,
        'mimetype': 'text/plain',
        'extensions': ('.sbv', '.sub')
    },
    'srt': {
        'id': 'srt',
        'reader': srt.Reader,
        'writer': srt.Writer,
        'mimetype': 'text/plain',
        'extensions': '.srt'
    },
    'vtt': {
        'id': 'vtt',
        'reader': vtt.Reader,
        'writer': vtt.Writer,
        'mimetype': 'text/plain',
        'extensions': '.vtt'
    },
    'rt': {
        'id': 'rt',
        'reader': rt.Reader,
        'writer': rt.Writer,    # @TODO will raise NotImplementedError
        'mimetype': 'text/plain',
        'extensions': '.rt'
    }
}

def get_formats(filename):
    "Returns formats that could apply based on a filename"
    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    formats = []
    for name, data in REGISTRY.items():
        exts = data.get('extensions')
        if type(exts) not in (list, tuple):
            exts = (exts,)
        if ext in exts:
            formats.append(name)
    return formats
