from cryptography import x509
from cryptography.hazmat.backends import default_backend
from pydantic import Field
import subprocess
from typing import Optional
from zipfile import ZipFile

from ace2 import *

class FileType(Analysis):
    ''' Determines the type of a file '''

    class Details(Analysis.Details):
        file_type: Optional[str] = Field(default=None, description='human readable file type of the target')
        mime_type: Optional[str] = Field(default=None, description='mime type of the target')

    def execute(self, target):
        # get the human readable type
        process = subprocess.run(['file', '-b', '-L', target.path], capture_output=True, text=True)
        # TODO: handle stderr
        self.details.file_type = process.stdout.strip()

        # get the mime type
        process = subprocess.run(['file', '-b', '--mime-type', '-L', target.path], capture_output=True, text=True)
        # TODO: handle stderr
        self.details.mime_type = process.stdout.strip()

        # set the summary
        self.summary = f'File Type Analysis: ({self.details.file_type}) ({self.details.mime_type})'

        # determine if file is ole
        with open(target.path, 'rb') as f:
            if f.read(8) == b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1':
                target.add(Tag, 'ole')

        # determine if file is rtf
        with open(target.path, 'rb') as f:
            data = f.read(4)
            if data[:3] == b'\\rt' or data == b'{\\rt':
                target.add(Tag, 'rtf')

        # determine if file is pdf
        with open(target.path, 'rb') as f:
            if b'%PDF-' in f.read(1024):
                target.add(Tag, 'pdf')

        # determine if file is an executable
        with open(target.path, 'rb') as f:
            if f.read(2) == b'MZ':
                target.add(Tag, 'executable')

        # determine if file is a jar or zip file by attempting to read the namelist
        try:
            with ZipFile(target.path, 'r') as f:
                if f.namelist():
                    target.add(Tag, 'zip')
        except:
            pass

        # determine if file is a lnk
        with open(target.path, 'rb') as f:
            if f.read(8) == b'\x4C\x00\x00\x00\x01\x14\x02\x00':
                target.add(Tag, 'lnk')

        # determine if file is x509
        with open(target.path, 'rb') as f:
            data = f.read()
            try:
                x509.load_pem_x509_certificate(data, backend=default_backend())
                is_x509 = True
            except:
                try:
                    x509.load_der_x509_certificate(data, backend=None)
                    is_x509 = True
                except:
                    is_x509 = False
            if is_x509:
                target.add(Tag, 'x509')
                if analysis.details.file_type == 'data':
                    analysis.details.file_type = 'DER certificate'

        # determine if file is jar
        try:
            with ZipFile(target.path, 'r') as f:
                if 'META-INF/MANIFEST.MF' in f.namelist():
                    target.add(Tag, 'jar')
        except:
            pass

        # determine if file is office document
        is_office_document = target.extension in [
            # see https://en.wikipedia.org/wiki/List_of_Microsoft_Office_filename_extensions
            # 2/19/2018 - removed MSO file ext (relying on OLE format instead)
            # 6/29/2018 - https://docs.google.com/spreadsheets/d/1LXneVF8VxmOgkt2W_NG5Kl3lzWW45prE7gxtuPcO-4o/edit#gid=1950593040
            # Microsoft Word
            'doc',
            'docb',
            'dochtml',
            'docm',
            'docx',
            'docxml',
            'dot',
            'dothtml',
            'dotm',
            'dotx',
            'odt',
            'rtf',
            'wbk',
            'wiz',
            # Microsoft Excel
            'csv',
            'dqy',
            'iqy',
            'odc',
            'ods',
            'slk',
            'xla',
            'xlam',
            'xlk',
            'xll',
            'xlm',
            'xls',
            'xlsb',
            'xlshtml',
            'xlsm',
            'xlsx',
            'xlt',
            'xlthtml',
            'xltm',
            'xltx',
            'xlw',
            # Microsoft Powerpoint
            'odp',
            'pot',
            'pothtml',
            'potm',
            'potx',
            'ppa',
            'ppam',
            'pps',
            'ppsm',
            'ppsx',
            'ppt',
            'ppthtml',
            'pptm',
            'pptx',
            'pptxml',
            'pwz',
            'sldm',
            'sldx',
            'thmx',
            # OpenOffice
            'odt',
        ]
        is_office_document |= 'microsoft powerpoint' in self.details.file_type.lower()
        is_office_document |= 'microsoft excel' in self.details.file_type.lower()
        is_office_document |= 'microsoft word' in self.details.file_type.lower()
        is_office_document |= 'microsoft ooxml' in self.details.file_type.lower()
        is_office_document |= 'ole' in target.tags
        is_office_document |= 'rtf' in target.tags
        if is_office_document:
            target.add(Tag, 'microsoft_office')
