"""
The class viewer
"""
from datetime import datetime
from shutil import get_terminal_size
from glxviewer.utils import resize_text
from glxviewer.utils import center_text
from glxviewer.utils import bracket_text
from glxviewer.singleton import Singleton

from glxviewer.term import writeLine
from glxviewer.term import writeString
from glxviewer.term import pos
from glxviewer.term import clearLineFromPos
from glxviewer.term import OFF
from glxviewer.term import BLACK
from glxviewer.term import RED
from glxviewer.term import GREEN
from glxviewer.term import BOLD
from glxviewer.term import YELLOW
from glxviewer.term import BLUE
from glxviewer.term import MAGENTA
from glxviewer.term import CYAN
from glxviewer.term import WHITE
from glxviewer.term import BG_WHITE
from glxviewer.term import DIM


class Viewer(metaclass=Singleton):
    """
    The class viewer
    """

    def __init__(self):
        # protected variables
        self.__with_date = None
        self.__status_text = None
        self.__status_text_color = None
        self.__status_symbol = None
        self.__text_column_1 = None
        self.__text_column_2 = None
        self.__text_column_3 = None
        # self.__size_line_actual = None
        # self.__size_line_previous = None

        # init property's
        self.with_date = None
        self.status_text = None
        self.status_text_color = None
        self.status_symbol = None
        self.text_column_1 = None
        self.text_column_2 = None
        self.text_column_3 = None
        self.size_line_actual = None
        self.size_line_previous = None

    @property
    def with_date(self):
        """
        Property use for show date

        :return: with date property value
        :rtype: str
        """
        return self.__with_date

    @with_date.setter
    def with_date(self, value):
        """
        set the with_date property

        Default value is True

        :param value: the `with_date` property value
        :type value: bool
        :raise TypeError: if ``value`` is not a bool type
        """
        if value is None:
            value = True
        if not isinstance(value, bool):
            raise TypeError("'with_date' property must be a bool type")
        if self.with_date != value:
            self.__with_date = value

    @property
    def status_text(self):
        """
        Property it stores text of the status text like "DEBUG" "LOAD"

        Later the Viewer will add bracket's around it text, and set the color during display post-processing.

        see: ``status_text_color`` property

        :return: status_text property value
        :rtype: str
        """
        return self.__status_text

    @status_text.setter
    def status_text(self, value=None):
        """
        Set the status_text property value

        :param value: the status_text property value
        :type value: str
        :raise TypeError: if ``value`` is not a str type
        """
        if value is None:
            value = "DEBUG"
        if not isinstance(value, str):
            raise TypeError("'status_text' property must be a str type")
        if self.status_text != value:
            self.__status_text = value

    @property
    def allowed_colors(self):
        """
        Allowed colors:

        ORANGE, RED, RED2, YELLOW, YELLOW2, WHITE, WHITE2, CYAN, GREEN, GREEN2

        Note that Upper, Lower, Tittle case are allowed

        :return: A list of allowed colors
        :rtype: list
        """
        return ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE"]

    @property
    def status_text_color(self):
        """
        Property it stores one allowed color value, it values will be used to display ``status_text`` color.

        see: ``status_text`` property for more details

        :return: the ``status_text_color`` property value
        :rtype: str
        """
        return self.__status_text_color

    @status_text_color.setter
    def status_text_color(self, value):
        """
        Set the value of the ``status_text_color`` property.

        see: ``allowed_colors`` for more details

        :param value: The ``status_text_color`` property value
        :type value: str
        :raise TypeError: When ``status_text_color`` is not a str
        :raise ValueError: When ``status_text_color`` value is not an allowed color
        """
        if value is None:
            value = "WHITE"
        if not isinstance(value, str):
            raise TypeError("'status_text_color' property must be a str type")
        if value.upper() not in self.allowed_colors:
            raise ValueError(
                "{0} is not a valid color for 'status_text_color' property"
            )
        if self.status_text_color != value:
            self.__status_text_color = value

    @property
    def status_symbol(self):
        """
        Property it stores a symbol of one letter. like ! > < / - | generally for show you application fo something.

        its thing exist that because I use it for show if that an input or output message.

        Actually the symbol use CYAN color, and have 1 space character on the final template. Certainly something it can
        be improved. Will see in future need's ...

        :return: status_symbol character
        :rtype: str
        """
        return self.__status_symbol

    @status_symbol.setter
    def status_symbol(self, value):
        """
        Set the symbol of ``status_symbol`` you want. Generally > or < or ?

        :param value: the symbol of ``status_symbol``
        :type value: str
        :raise TypeError: when ``status_symbol`` value is not a str type
        """
        if value is None:
            value = " "
        if not isinstance(value, str):
            raise TypeError("'status_symbol' property must be set with str value")
        if self.status_symbol != value:
            self.__status_symbol = value

    @property
    def text_column_1(self):
        """
        Property it stores ``text_column_1`` value. Its value is use by template for display the column 1

        :return: The ``text_column_1`` value
        :rtype: str
        """
        return self.__text_column_1

    @text_column_1.setter
    def text_column_1(self, value):
        """
        Set the ``text_column_1`` value.

        :param value: The text you want display on it column
        :type value: str
        :raise TypeError: When ``text_column_1`` value is not a str type
        """
        if value is None:
            value = ""
        if not isinstance(value, str):
            raise TypeError("'text_column_1' property must be set with str value")
        if self.text_column_1 != value:
            self.__text_column_1 = value

    @property
    def text_column_2(self):
        """
        Property it stores ``text_column_2`` value. Its value is use by template for display the column 2

        :return: The ``text_column_2`` value
        :rtype: str
        """
        return self.__text_column_2

    @text_column_2.setter
    def text_column_2(self, value):
        """
        Set the ``text_column_2`` value.

        :param value: The text you want display on it column
        :type value: str
        :raise TypeError: When ``text_column_2`` value is not a str type
        """
        if value is None:
            value = ""
        if not isinstance(value, str):
            raise TypeError("'text_column_2' property must be set with str value")
        if self.text_column_2 != value:
            self.__text_column_2 = value

    @property
    def text_column_3(self):
        """
        Property it stores ``text_column_3`` value. Its value is use by template for display the column 3

        :return: The ``text_column_3`` value
        :rtype: str
        """
        return self.__text_column_3

    @text_column_3.setter
    def text_column_3(self, value):
        """
        Set the ``text_column_3`` value.

        :param value: The text you want display on it column
        :type value: str
        :raise TypeError: When ``text_column_3`` value is not a str type
        """
        if value is None:
            value = ""
        if not isinstance(value, str):
            raise TypeError("'text_column_3' property must be set with str value")
        if self.text_column_3 != value:
            self.__text_column_3 = value

    @staticmethod
    def flush_a_new_line():
        writeLine()

    @property
    def formatted_date(self):
        return str(datetime.now().replace(microsecond=0).isoformat())

    def write(
        self,
        with_date=None,
        status_text=None,
        status_text_color=None,
        status_symbol=" ",
        column_1=None,
        column_2=None,
        column_3=None,
        prompt=None,
    ):
        """
        Flush a line a bit like you want

        :param with_date: show date if True
        :type with_date: bool
        :param status_text: The text to display ton the status part
        :type status_text: str
        :param status_text_color: allowed : BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
        :type status_text_color: str
        :param status_symbol: A symbol like >, in general that a one char string
        :type status_symbol: str or None
        :param column_1: The thing to print in column 1
        :type column_1: str or None
        :param column_2: The thing to print in column 2
        :type column_2: str or None
        :param column_3: The thing to print in column 3
        :type column_3: str or None
        :param prompt: Add a new line if ``True``
        :type prompt: None, -1, +1
        """

        self.with_date = with_date
        self.status_text = status_text
        self.status_text_color = status_text_color
        self.status_symbol = status_symbol
        self.text_column_1 = column_1
        self.text_column_2 = column_2
        self.text_column_3 = column_3

        if self.status_text_color.lower() == "black":
            status_text_color = BLACK
        elif self.status_text_color.lower() == "red":
            status_text_color = RED
        elif self.status_text_color.lower() == "green":
            status_text_color = GREEN + BOLD
        elif self.status_text_color.lower() == "yellow":
            status_text_color = YELLOW + BOLD
        elif self.status_text_color.lower() == "blue":
            status_text_color = BLUE
        elif self.status_text_color.lower() == "magenta":
            status_text_color = MAGENTA
        elif self.status_text_color.lower() == "cyan":
            status_text_color = CYAN
        elif self.status_text_color.lower() == "white":
            status_text_color = WHITE + DIM

        # Status Clean up
        status_text = resize_text(text=self.status_text, max_width=5)
        status_text = center_text(text=status_text, max_width=5)
        status_text = bracket_text(text=status_text)

        line = get_terminal_size().lines

        pos(line, 1)
        # Column state
        if self.with_date:
            string_print = "{0:} {1:<5} {2:<3}".format(
                BG_WHITE + BLACK + self.formatted_date + OFF,
                status_text_color + status_text + OFF,
                BOLD + CYAN + self.status_symbol + OFF,
            )

        else:
            string_print = "{0:<5} {1:<3}".format(
                status_text_color + status_text + OFF,
                BOLD + CYAN + status_symbol + OFF,
            )
        if len(self.text_column_1):
            string_print += " {0:<10}".format(self.text_column_1)

        if len(self.text_column_2):
            string_print += " {0:<10}".format(self.text_column_2)

        if prompt is None or not prompt:
            writeLine(text=string_print)
        else:
            writeString(text=string_print)

        clearLineFromPos()
