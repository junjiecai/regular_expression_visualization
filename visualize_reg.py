import re
from IPython.display import HTML


def split_by(string, sub_string):
    n = string.find(sub_string) + len(sub_string)
    return string[:n], string[n:]


def get_color_reg_html(p, s):
    black_string = ColoredString(s, 'black')
    r = re.search(p, s)
    if r is None:
        return black_string.render()
    span = r.span()


    matched_string = s[span[0]:span[1]]

    blue_string = ColoredString(matched_string, 'blue')
    black_string.sub_colored_strings = [blue_string]

    green_strings = [ColoredString(captured, 'green') for captured in r.groups()]
    blue_string.sub_colored_strings = green_strings

    return black_string.render()


class ColoredString:
    def __init__(self, string, color, sub_colored_strings=None):
        self.string = string
        self.color = color
        self.sub_colored_strings = sub_colored_strings or []

    def render(self):
        if len(self.sub_colored_strings) == 0:
            return "<span style='color:{}'>{}</span>".format(self.color, self.string)
        else:
            strs = []
            string = self.string
            for sub_colored_string in self.sub_colored_strings:
                first_part, last_part = split_by(string, sub_colored_string.string)
                first_part = first_part.replace(sub_colored_string.string, sub_colored_string.render(), 1)
                strs.append(first_part)
                string = last_part
            strs.append(last_part)

            string = "<span style='color:{}'>{}</span>".format(self.color, ''.join(strs))
            return string


def display_reg_result(patterns, strings):
    html = ''
    for pattern in patterns:
        html += '<td>{}</td>'.format(pattern)
        for string in strings:
            html += "<td>{}</td>".format(get_color_reg_html(pattern, string))
        html = '<tr>' + html + '</tr>'
    header = '<tr><th></th>{}</tr>'.format(''.join(['<th>{}</th>'.format(string) for string in strings]))
    html = '<table>' + header + html + '</table>'
    return HTML(html)