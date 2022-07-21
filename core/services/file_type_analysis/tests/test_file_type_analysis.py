from ace2 import *
from services.file_type_analysis.service import FileTypeAnalysis
import pytest
from sys import platform


def test_file_type_run_condition():
    # test run condition True
    analysis = {
        'id': 1,
        'type': 'file_type_analysis',
        'target': {
            'type': 'file',
            'value': 'blah',
        },
    }
    assert Module(**analysis).should_run()

    # test run condition False
    analysis = {
        'id': 1,
        'type': 'file_type_analysis',
        'target': {
            'type': 'foo',
            'value': 'blah',
        },
    }
    assert not Module(**analysis).should_run()


@pytest.mark.parametrize('path,extension,tags,file_type,mime_type', [
    # test files
    ('docx', '', ['zip', 'microsoft_office'], 'Microsoft Word 2007+', 'application/msword'),
    ('exe', '', ['executable'], 'PE32+ executable (console) x86-64, for MS Windows', 'application/x-dosexec'),
    ('jar', '', ['zip', 'jar'], 'Zip archive data, at least v1.0 to extract', 'application/zip'),
    ('lnk', '', ['lnk'], 'Windows shortcut file', 'application/octet-stream'),
    ('ole', '', ['ole', 'microsoft_office'], 'Microsoft Office Document', 'application/octet-stream'),
    ('ooxml', '', ['zip', 'microsoft_office'], 'Microsoft OOXML', 'application/octet-stream'),
    ('pdf', '', ['pdf'], 'PDF document, version 1.3', 'application/pdf'),
    ('pptx', '', ['zip', 'microsoft_office'], 'Microsoft PowerPoint 2007+', 'application/vnd.ms-powerpoint'),
    ('rtf_1', '', ['rtf', 'microsoft_office'], 'Rich Text Format data, version 1, ANSI', 'text/rtf'),
    ('rtf_2', '', ['rtf', 'microsoft_office'], 'ASCII text, with CRLF line terminators', 'text/plain'),
    ('x509.der', '', ['x509'], 'DER certificate', 'application/octet-stream'),
    ('x509.pem', '', ['x509'], 'PEM certificate', 'text/plain'),
    ('xlsx', '', ['zip', 'microsoft_office'], 'Microsoft Excel 2007+', 'application/vnd.ms-excel'),
    ('zip', '', ['zip'], 'Zip archive data, at least v2.0 to extract', 'application/zip'),

    # test microsoft office extensions
    ('empty', '.doc', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.docb', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.dochtml', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.docm', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.docx', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.docxml', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.dot', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.dothtml', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.dotm', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.dotx', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.odt', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.rtf', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.wbk', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.wiz', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.csv', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.dqy', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.iqy', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.odc', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.ods', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.slk', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.xla', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.xlam', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.xlk', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.xll', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.xlm', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.xls', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.xlsb', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.xlshtml', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.xlsm', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.xlsx', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.xlt', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.xlthtml', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.xltm', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.xltx', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.xlw', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.odp', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.pot', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.pothtml', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.potm', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.potx', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.ppa', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.ppam', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.pps', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.ppsm', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.ppsx', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.ppt', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.ppthtml', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.pptm', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.pptx', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.pptxml', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.pwz', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.sldm', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.sldx', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.thmx', ['microsoft_office'], 'empty', 'inode/x-empty'),
    ('empty', '.odt', ['microsoft_office'], 'empty', 'inode/x-empty'),
])
def test_file_type(path, extension, tags, file_type, mime_type, mock_queue):
    # create analysis to run
    analysis = {
        'id': 1,
        'type': 'file_type_analysis',
        'target': {
            'type': 'file',
            'value': path,
            'metadata': [
                {'type': 'display_value', 'value': f'{path}{extension}' },
            ],
        },
    }

    # run the module
    analysis = Module(**analysis)
    analysis.execute()

    # verify analysis
    assert analysis.status == 'complete'
    assert analysis.summary == f'FileType: ({file_type}) ({mime_type})'
    assert analysis.details.file_type == file_type
    assert analysis.details.mime_type == mime_type
    assert analysis.target.tags == tags
