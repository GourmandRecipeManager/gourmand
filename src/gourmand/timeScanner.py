"""Scan text for time and show links that will pop up a timer if the
user clicks on any time in the TextView."""

from typing import Optional, Union

from gi.repository import GObject, Gtk

from gourmand import timer
from gourmand.convert import Converter, time_matcher
from gourmand.gtk_extras.LinkedTextView import LinkedPangoBuffer, LinkedTextView


def make_time_links(s: str) -> str:
    """Given a string return the string with time links inserted.

    The links are of the form <a href="## unit"> Text </a>, similar to html
    links.  In a later step these will be changed to span tags with formatting.

    The simplest time phrase is transformed as follows:
    - "15 minutes" -> '<a href="15 minutes">15 minutes</a>'

    Multiple formats of time spans are correctly parsed including:
    - "15 - 20 minutes" -> '<a href="15 minutes">15 - </a><a href="20 minutes">20 minutes</a>'
    - "15-20 minutes" -> '<a href="15 minutes">15-</a><a href="20 minutes">20 minutes</a>'
    - "15 to 20 minutes" -> '<a href="15 minutes">15 to </a><a href="20 minutes">20 minutes</a>'

    Although minutes is the only time unit shown in the above examples, other
    units such as seconds, hours and days are also recognized.
    """
    start = 0
    while True:
        result = time_matcher.search(s, start)

        # When there are no more matches to make time links, return string
        if result is None:
            return s

        # Only substitute in the string where the match was found in case repeating patterns
        # are present.  Use start and Match.end() to know bounds.
        end = result.end()

        # Occurs when there is only one number value (e.g. 15 minutes)
        if result['secondnum'] is None:
            subbed_text = time_matcher.sub(r'<a href="\g<firstnum> \g<unit>">\g<0></a>', s[start:end])
        # Occurs when there is a range (e.g. 35 to 40 minutes)
        else:
            subbed_text = time_matcher.sub(
                r'<a href="\g<firstnum> \g<unit>">\g<firstnum>\g<range></a>'
                r'<a href="\g<secondnum> \g<unit>">\g<secondnum> \g<unit></a>',
                s[start:end])

        # Substitute the text with a link in for the text that was matched.
        s = s[:start] + subbed_text + s[end:]

        # Update variable for next round
        start = start + len(subbed_text)


class TimeBuffer(LinkedPangoBuffer):
    def set_text(self, txt: Union[bytes, str]) -> None:
        if isinstance(txt, bytes):
            txt = txt.decode("utf-8")
        super().set_text(make_time_links(txt))

    def get_text(self, start: Optional[Gtk.TextIter] = None, end: Optional[Gtk.TextIter] = None, include_hidden_chars: bool = False) -> str:
        """Get the buffer content.

        If `include_hidden_chars` is set, then the html markup content is
        returned.
        Time links are always stripped.
        """
        return super().get_text(start, end, include_hidden_chars, ignore_links=True)


class LinkedTimeView(LinkedTextView):
    __gtype_name__ = "LinkedTimeView"

    __gsignals__ = {
        "time-link-activated": (GObject.SignalFlags.RUN_LAST, GObject.TYPE_STRING, [GObject.TYPE_STRING, GObject.TYPE_STRING]),
    }

    def make_buffer(self):
        return TimeBuffer()

    def follow_if_link(self, text_view: "LinkedTimeView", itr: Gtk.TextIter) -> bool:
        """Launch a timer if a link was clicked.

        This is done by emitting the `time-link-activated` signal defined in
        this class.
        Whether or not the it was a link, the click won't be processed further.
        """
        # Get the displayed text sentence, to use as a label in the timer.
        start_sentence = itr.copy()
        start_sentence.backward_sentence_start()

        end_sentence = itr.copy()
        if not end_sentence.ends_sentence():
            end_sentence.forward_sentence_end()

        sentence = self.get_buffer().get_slice(start_sentence, end_sentence, False)

        # Get the time duration (target of the link).
        start_ts = itr.copy()
        start_ts.backward_to_tag_toggle()
        itr.forward_to_tag_toggle()
        end_ts = itr.copy()
        time_string = self.get_buffer().get_slice(start_ts, end_ts, False)

        # Confirm that is is in the links dictionary.
        time_ = self.get_buffer().markup_dict.get(time_string)
        if time_ is not None:
            self.emit("time-link-activated", time_, sentence)

        return False  # Do not process the event further.


def show_timer_cb(tv: LinkedTimeView, line: str, note: str) -> None:
    """Callback that expects a widget, a time string, and a note to display"""
    timer.show_timer(Converter.instance().timestring_to_seconds(line), note)


if __name__ == "__main__":
    tv = LinkedTimeView()
    tv.connect("time-link-activated", show_timer_cb)
    tv.get_buffer().set_text(
        """Cook potatoes for 1/2 hour.

        When you are finished, leave in the refrigerator for up to three days.

        After that, boil onions for 20 to 30 minutes.

        When finished, bake everything for two and a half hours.

        15-25 seconds.
        """
    )

    w = Gtk.Window()
    w.add(tv)
    w.connect("delete-event", lambda *args: Gtk.main_quit())
    w.show_all()
    Gtk.main()
