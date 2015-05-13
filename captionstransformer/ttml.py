from datetime import datetime
from bs4 import BeautifulSoup
from captionstransformer import core

class Reader(core.Reader):
    def read(self):
        soup = BeautifulSoup(open(self.fileobject.name), 'xml')
        texts = soup.find_all('p')
        #print texts
        for text in texts:
            #print text
            caption = core.Caption()
            begin = text.get('begin')
            if begin == None:
                begin = text.get('tt:begin')
            caption.start = self.get_date(begin)
            end = text.get('end')
            if end == None:
                end = text.get('tt:end')
            caption.end = self.get_date(end)
            cap = u''
            for item in text.contents:
                line = u'%s' % item
                if line != '<br/>' and line != '<tt:br/>':
                    cap += line
                else:
                    cap += '\n'
            caption.text = cap
            self.add_caption(caption)

        return self.captions

    def get_date(self, time_str):
        try:
            dt = datetime.strptime(time_str, '%H:%M:%S.%f')
        except ValueError:
            dt = datetime.strptime(time_str[0:8], '%H:%M:%S')
        return dt 

class Writer(core.Writer):
    DOCUMENT_TPL = u"""<tt xml:lang="" xmlns="http://www.w3.org/ns/ttml"><body><div>%s</div></body></tt>"""
    CAPTION_TPL = u"""<p begin="%(start)s" end="%(end)s">%(text)s</p>"""

    def format_time(self, caption):
        """Return start and end time for the given format"""
        #should be seconds by default

        return {'start': caption.start.strftime('%H:%M:%S.%f')[:-3],
                'end': caption.end.strftime('%H:%M:%S.%f')[:-3]}
