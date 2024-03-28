

def resize_text(text=None, max_width=0, separator="~"):
    """
    Resize the text , and return a new text

    example: return '123~789' for '123456789' where max_width = 7 or 8

    :param text: the original text to resize
    :type text: str
    :param max_width: the size of the text
    :type max_width: int
    :param separator: a separator an in middle of the resize text
    :type separator: str
    :return: a resize text
    :rtype: str
    """
    if not isinstance(text, str):
        raise TypeError('"text" must be a str type')
    if not isinstance(max_width, int):
        raise TypeError('"max_width" must be a int type')
    if not isinstance(separator, str):
        raise TypeError('"separator" must be a str type')

    if max_width < len(text):
        if max_width <= 0:
            return ""
        if max_width == 1:
            return text[:1]
        if max_width == 2:
            return text[:1] + text[-1:]
        if max_width == 3:
            return text[:1] + separator[:1] + text[-1:]
        max_width -= len(separator[:1])
        return (
                text[: int(max_width / 2)] + separator[:1] + text[-int(max_width / 2):]
        )

    return text


def center_text(text=None, max_width=None):
    """
    Return a centred text from max_width, if max_width is None it will use the terminal width size.

    example:
    center_text(text="DLA", max_width=5) return " DLA "

    :param text: text to center
    :type text: str
    :param max_width: the maximum width
    :type max_width: int
    :return: the centred text
    :rtype: str
    """
    if not isinstance(text, str):
        raise TypeError('"text" must be a str type')
    if max_width is None:
        max_width = 80
    if not isinstance(max_width, int):
        raise TypeError('"max_width" must be a int type')
    symbol = " "
    start = "%s %s" % (str(symbol) * int((max_width - 1 - len(text)) / 2), text)
    return "%s %s" % (start, str(symbol) * int(max_width - 1 - len(start)))


def bracket_text(text=None, symbol_inner="[", symbol_outer="]"):
    """
    Surround a text with an inner and outer char.

    Not you should center you text with center_text()before call it function

    :param symbol_inner: the symbol to use for as inner, generally that '[', '<', '('
    :type symbol_inner: str
    :param symbol_outer: the symbol to use for as outer, generally that ']', '>', ')'
    :type symbol_outer: str
    :param text: the text it will be sur surround by the inner and outer chars
    :type text: str
    :return: the text surrounded by inner and outer
    :rtype: str
    """
    if not isinstance(text, str):
        raise TypeError('"text" must be a str type')
    if not isinstance(symbol_inner, str):
        raise TypeError('"symbol_inner" must be a str type')
    if not isinstance(symbol_outer, str):
        raise TypeError('"symbol_outer" must be a str type')

    return f"{symbol_inner}{text}{symbol_outer}"
