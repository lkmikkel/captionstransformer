"""
TODO: This code is very old and depends on HTMLParser
Tried to replace it with BeautifulSoup but can't find
a way to set <time> as a non-nestable element
(recursion depth issues!)
"""

import codecs
from datetime import datetime, timedelta
from HTMLParser import HTMLParser, HTMLParseError
from captionstransformer import core

class RtParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.caption = None
        self.captions = []
        self.allow_tags = ('i', 'b', 'pre', 'strong', 'tt')
        self.duration = None

    def handle_starttag(self, tag, attrs):
        if tag == 'time':
            if self.caption: self.captions.append(self.caption)
            self.caption = dict(text='')
            for key, val in attrs:
                if key == 'begin': self.caption['start'] = self.get_time(val)#timestr2float(val)

        if tag == 'br':
            self.caption['text'] += '\n'

        if tag == 'window':
            for key, val in attrs:
                if key == 'duration': self.duration = self.get_time(val)

        if tag in self.allow_tags:
            self.caption['text'] += '<%s>'%tag

    def handle_endtag(self, tag):
        if tag in self.allow_tags:
            self.caption['text'] += '</%s>'%tag

    def handle_data(self, data):
        if self.caption:
            self.caption['text'] += data

    def get_time(self, val):
        return datetime.strptime(val[0:15], '%H:%M:%S.%f')

class Reader(core.Reader):
    def text_to_captions(self):
        parser = RtParser()
        parser.feed(self.rawcontent)

        if parser.caption: parser.captions.append(parser.caption)
        parser.caption = None
        for i in range(len(parser.captions)):
            cap = parser.captions[i]
            caption = core.Caption()
            caption.start = cap['start']
            if i < len(parser.captions) - 1:
                caption.end = parser.captions[i+1]['start']
            caption.text = cap['text'].strip().replace('\n\r', '\n').replace('\n\n', '\n')
            self.add_caption(caption)

        if parser.duration and len(self.captions) and not self.captions[-1].end:
            self.captions[-1].end = parser.duration

class Writer(core.Writer):
    def __init__(self):
        raise NotImplementedError()
