__author__ = 'admin'

import re

DEBUG = False

# ----------------------------------------------------------------------------------------------------------------------
# Default variables:
_TEMPLATE  = 'template.apib'
_DUMPFILE = 'result.apib'

# Command Related:
_INCLUDE        = 'include'
_SECTION_START  = 'start'
_SECTION_END    = 'end'

# Static methods:
_apiary_file_type = re.compile(r'.+\.apib$').match
_is_command       = re.compile(r'^####\$[a-zA-Z]+\{[a-zA-Z0-9\_\-\.]+\}').match
_search_tag       = re.compile(r'\{[a-zA-Z0-9\_\-]+(\.[a-zA-Z0-9\_\-]+)?\}').search
_is_section_tag   = re.compile(r'^[a-zA-Z0-9\_\-]+$').match


class Parser(object):

    @staticmethod
    def _get_tag_from_filename(filename):
        assert isinstance(filename, str) and _apiary_file_type(filename)
        return filename[:-5]

    @staticmethod
    def _get_filename_from_tag(tag):
        assert isinstance(tag, str) and not _apiary_file_type(tag)
        return '%s.%s' % (tag, 'apib')

    @staticmethod
    def _get_command_info_from_line(line):
        # @param  {string} line: the input line string to process
        # @return {string, string} command, tag: the command to execute and the tag as the following parameter
        tag_search = _search_tag(line)
        assert tag_search is not None, 'Syntax Error for command in line: %s' % line
        return line[5:tag_search.start()], tag_search.group()[1:-1]

    @staticmethod
    def _include(tag):
        # @param {string} tag should one of the patterns: SOURCE_FILE, SOURCE_FILE.SECTION_TAG
        # @return {list(string)} the content
        tag_contents = tag.split('.')
        assert len(tag_contents) == 1 or len(tag_contents) == 2, 'Syntax Error with tag: %s' % tag
        filename = Parser._get_filename_from_tag(tag_contents[0])
        if len(tag_contents) == 2:
            sub_tag = tag_contents[1]
        else:
            sub_tag = None

        sub_parser = Parser()
        return sub_parser.parse(filename, sub_tag)

    def _execute_command(self, command, tag):
        if DEBUG:
            print('execute command: %s with tag: %s' % (command, tag))

        if command == _INCLUDE:
            sub_content = Parser._include(tag)
            for line in sub_content:
                self._parsed_content.append(line)

        elif command == _SECTION_START:
            assert _is_section_tag(tag), 'Syntax Error with tag: %s for command :%s' % (tag, command)
            self._should_parse = (self._tag == tag)

        elif command == _SECTION_END:
            assert _is_section_tag(tag), 'Syntax Error with tag: %s for command: %s' % (tag, command)
            if self._should_parse and self._tag == tag:
                self._should_parse = False
        else:
            assert False, 'Syntax Error: command %s not defined' % command

    def __init__(self):
        self._parsed_content = None
        self._tag = None
        self._should_parse = False

    def parse(self, filename, tag=None):
        # @param  {string} filename
        # @param  {list(string)} tag, default: empty list
        # @return {list(string)} parsed contents
        assert isinstance(filename, str) and (isinstance(tag, str) or tag is None)
        print('Start parsing: %s with tag %s' % (filename, tag))

        self._parsed_content = list()
        self._tag = tag
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

        except FileNotFoundError:
            print('Error: could not found the related file: %s' % filename)
            return self._parsed_content

        line_count = 0
        self._should_parse = (self._tag is None)
        for line in lines:
            line_count += 1
            if DEBUG:
                print('%d %s' % (line_count, line))

            if _is_command(line):
                command, tag = Parser._get_command_info_from_line(line)
                self._execute_command(command, tag)
            elif self._should_parse:
                self._parsed_content.append(line)

        return self._parsed_content

# ----------------------------------------------------------------------------------------------------------------------
# define the main function for the compile process:
def compile(**kwargs):
    template = kwargs.get('template', _TEMPLATE)
    dumpfile = kwargs.get('dumpfile', _DUMPFILE)

    main_parser = Parser()
    contents = main_parser.parse(template)

    with open(dumpfile, 'w') as file:
        file.writelines(contents)

    pass



# ----------------------------------------------------------------------------------------------------------------------
# the operation entry point:
if __name__ == '__main__':
    print('start compiling process ...')

    compile()

    exit(0)