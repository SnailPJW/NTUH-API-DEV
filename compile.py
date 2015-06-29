__author__ = 'admin'

import docopt
import os
import re

DEBUG = True

# ----------------------------------------------------------------------------------------------------------------------
# Default variables:
CWD = os.getcwd()
TEMPLATE = 'template.apib'
RESULT = 'result.apib'


class Parser(object):
    _apiary_file_type = re.compile(r'.+\.apib$').match
    _section_start_tag_match = re.compile(r'^[\s\t\ ]*\{\%[\ \s\t]+[a-zA-Z0-9\_\-]+[\ \s\t]+\%\}').match
    _section_end_tag_match = re.compile(r'^[\s\t\ ]*\{\%[\ \s\t]+end[\ \s\t]+\%\}').match

    @staticmethod
    def _get_tag_from_filename(filename):
        assert isinstance(filename, str) and Parser._apiary_file_type(filename)
        return filename[:-5]

    @staticmethod
    def _get_filename_from_tag(tag):
        assert isinstance(tag, str) and not Parser._apiary_file_type(tag)
        return '%s.%s' % (tag, 'apib')

    @staticmethod
    def _get_tag_from_line(line):
        assert isinstance(line, str)
        buffer = ''
        for chart in line:
            if chart not in ' \t{%}':
                buffer += chart
            elif len(buffer):
                break
        return buffer

    def __init__(self):
        self.default_tag = None
        self.template_lines = None
        self.current_parsing_tag = None
        self.parsed_content = None

    def parse(self, template_filename):
        assert isinstance(template_filename, str), 'The filename should be a string'
        if DEBUG:
            print('start parsing: %s' % template_filename)

        self.default_tag = Parser._get_tag_from_filename(template_filename)
        self.parsed_content = list()
        try:
            with open(template_filename, 'r') as f:
                self.template_lines = f.readlines()
        except FileNotFoundError as e:
            print("Error: %s" % e.strerror)
            return self.parsed_content

        line_count = 0
        for line in self.template_lines:
            line_count += 1
            if DEBUG:
                print('%d %s' % (line_count, line))

            if Parser._section_start_tag_match(line):
                sub_parser = Parser()
                content = sub_parser.parse(Parser._get_filename_from_tag(Parser._get_tag_from_line(line)))
                for sub_line in content:
                    self.parsed_content.append(sub_line)
            else:
                self.parsed_content.append(line)

        return self.parsed_content



# ----------------------------------------------------------------------------------------------------------------------
# the operation entry point:
if __name__ == '__main__':
    print('start compiling process ...')
    print('cwd: %s' % CWD)

    # TODO: get the related parameters

    # Parse the template:
    main_parser = Parser()
    contents = main_parser.parse(TEMPLATE)

    if DEBUG:
        for line in contents:
            print(line)

    exit(0)