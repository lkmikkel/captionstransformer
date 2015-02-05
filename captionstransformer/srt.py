from captionstransformer import core
from datetime import datetime, timedelta


from captionstransformer import vtt
class Reader(vtt.Reader):
    """
    Turns out vtt parser is better for srt than old srt parser
    @TODO properly parse srts without header and NOTE support???
    """
    FORMATS = ('%H:%M:%S,%f', '%M:%S,%f')

class Writer(vtt.Writer):
    DOCUMENT_TPL = u"%s"
    CAPTION_TPL = u"""%(index)s\n%(start)s --> %(end)s\n%(text)s\n\n"""

    def format_time(self, caption):
        """Return start and end time for the given format"""

        return {'start': caption.start.strftime('%H:%M:%S,%f')[:-3],
                'end': caption.end.strftime('%H:%M:%S,%f')[:-3]}

