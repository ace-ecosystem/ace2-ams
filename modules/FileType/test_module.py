from ace2.test import *
from module import FileType
import pytest

@pytest.mark.parametrize('path,tags,file_type,mime_type', [
    ('exe', ['executable'], 'PE32+ executable (console) x86-64, for MS Windows', 'application/x-dosexec'),
    ('jar', ['zip', 'jar'], 'Zip archive data, at least v1.0 to extract', 'application/zip'),
    ('lnk', ['lnk'], 'Windows shortcut file', 'application/octet-stream'),
    ('ole', ['ole', 'microsoft_office'], 'Microsoft Office Document', 'application/octet-stream'),
    ('pdf', ['pdf'], 'PDF document, version 1.3', 'application/pdf'),
    ('rtf_1', ['rtf', 'microsoft_office'], 'Rich Text Format data, version 1, ANSI', 'text/rtf'),
    ('rtf_2', ['rtf', 'microsoft_office'], 'ASCII text, with CRLF line terminators', 'text/plain'),
    ('x509.der', ['x509'], 'DER certificate', 'application/octet-stream'),
    ('x509.pem', ['x509'], 'PEM certificate', 'text/plain'),
    ('zip', ['zip'], 'Zip archive data, at least v2.0 to extract', 'application/zip'),
    ('zip', ['zip'], 'Zip archive data, at least v2.0 to extract', 'application/zip'),
    ('zip', ['zip'], 'Zip archive data, at least v2.0 to extract', 'application/zip'),
])
def test_file_type_analysis(path, tags, file_type, mime_type):
    # create analysis to run
    analysis = {
        'id': 1,
        'type': 'FileType',
        'target': {
            'type': 'File',
            'value': path,
        },
    }

    # run the module
    analysis = FileType(**analysis)
    assert analysis.execute(analysis.target) == None

    # verify analysis
    assert analysis.target.tags == tags
    assert analysis.details.file_type == file_type
    assert analysis.details.mime_type == mime_type
    assert analysis.summary == f'FileType: ({file_type}) ({mime_type})'
