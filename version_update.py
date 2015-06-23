import os
import re
import sys
import shlex
import subprocess
from subprocess import PIPE

API_FILE 		= '%s/apiary.apib' % os.getcwd()
VERSION_LINE 	= r'.* Web Service'
VERSION_PATTERN = r'v[0-9]+\.[0-9]+\.[0-9]+'
DEBUG           = True


def system(cmd, stdout=sys.stdout, stderr=sys.stderr):
    output, err = subprocess.Popen(shlex.split(cmd), stdout=stdout, stderr=stderr).communicate()
    if output is not None:
        output = output.decode('utf-8')
    return output, err

def sed_operation(sed_cmd, document):
    print('sed \%s\' %s > tmp.apib' % (sed_cmd, document))
    os.system('sed \'%s\' %s > tmp.apib' % (sed_cmd, document))
    print('mv tmp.apib %s' % document)
    os.system('mv tmp.apib %s' % document)

def get_git_version():
    git_version = None
    output, err = system('git describe', stdout=PIPE, stderr=PIPE)
    if output:
        git_version_search = re.search(VERSION_PATTERN, output)
        if git_version_search:
            git_version = git_version_search.group()

    return git_version

def get_document_version(document):
    with open(document, 'r') as f:
        lines = f.readlines()
        line_count = 0
        for line in lines:
            line_count += 1

            if re.search(VERSION_LINE, line):
                version_string_search = re.search(VERSION_PATTERN, line)
                if version_string_search:
                    return version_string_search.group()
    return None


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    document = API_FILE
    document_version = get_document_version(document)
    assert document_version, 'Cannot read version from document: %s' % document
    git_version = get_git_version()
    assert git_version, 'Cannot fetch the version from git'

    if document_version != git_version:
        print('update version from %s (original) to %s (latest)' % (document_version, git_version))
        sed_operation('s/Web Service %s/Web Service %s/g' % (document_version, git_version), document)

    else:
        print('the document version is the latest one: %s' % document_version)

    exit(0)
