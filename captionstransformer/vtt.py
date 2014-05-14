from datetime import datetime
from captionstransformer import core

class Reader(core.Reader):

    FORMATS = ('%H:%M:%S.%f', '%M:%S.%f')

    def text_to_captions(self):
        node = None
        caption = None
        lines = self.rawcontent.split('\n')

        # @TODO this is not according to standard
        # should be 'WEBVTT *' (* being anything but '-->' and newline)
        # and then TWO newlines!
        if lines[0].startswith('WEBVTT'): lines = lines[1:]

        for line in lines:
            stripped_line = line.strip()
            if not stripped_line:
                node = None
                if caption and caption.start:
                    self.add_caption(caption)
                    caption = core.Caption()
                continue
            if not node:
                # note started
                if stripped_line.startswith('NOTE'):
                    node = 'note'
                    continue
                # cue started (id or time)
                else:
                    node = 'caption'
                    caption = core.Caption()
                    if '-->' not in stripped_line:
                        caption.id = stripped_line
                        continue
                    # if --> in line, time will be processed at the end of the loop (node == 'caption')
            if node == 'note':
                continue
            if node == 'caption':
                if '-->' in stripped_line and not caption.start:
                    caption.start, caption.end = self.get_time(stripped_line)
                else:
                    caption.text += u'%s\n'%stripped_line
        if caption and caption.start:
            self.add_caption(caption)
        return self.captions

    def get_time(self, line):
        line = ' '.join(line.split(' ')[0:3])   # disregard cue settings @TODO ??
        parts = line.split(' --> ')
        times = [None, None]
        if len(parts) != 2:
            return None, None
        for i in (0,1):
            for format in self.FORMATS:
                try:
                    times[i] = datetime.strptime(parts[i], format)
                    continue
                except ValueError:
                    pass
        return times[0], times[1]

class Writer(core.Writer):
    DOCUMENT_TPL = u"WEBVTT\n\n%s"
    CAPTION_TPL = u"""%(index)s\n%(start)s --> %(end)s\n%(text)s\n"""

    def format_time(self, caption):
        """Return start and end time for the given format"""

        return {'start': caption.start.strftime('%H:%M:%S.%f')[:-3],
                'end': caption.end.strftime('%H:%M:%S.%f')[:-3]}

    def get_template_info(self, caption):
        info = super(Writer, self).get_template_info(caption)
        info['index'] = self.captions.index(caption)
        return info
