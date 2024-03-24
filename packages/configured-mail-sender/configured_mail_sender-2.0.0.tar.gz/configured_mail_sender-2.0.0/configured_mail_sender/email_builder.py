import mimetypes

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from pathlib import Path
from email import encoders
from typing import Union, List

TEXT_TYPE = 'text'

ENCODING_ASCII = 'us-ascii'
ENCODING_UTF8 = 'utf8'


class EmailBuilder(object):
    def __init__(self):
        """
        Create EmailBuilder to construct a MIME email with possible attachments.
        :rtype EmailBuilder:
        """
        self._msg = MIMEMultipart()
        self._to = []
        self._cc = []
        self._bcc = []

    def subject(self, subject: str):
        """
        Set the subject of the message.
        :param subject: The email subject
        :return: self
        """
        self._msg['Subject'] = subject

    def to(self, to: Union[str, List[str]]):
        """
        Add mail email recipient(s)
        :param to: One or more receiver addresses, list or comma separated
        """
        self._to += [to] if isinstance(to, str) else to

    def bcc(self, bcc: Union[str, List[str]]):
        """
        Add hidden email recipient(s)
        :param bcc: One or more receiver addresses, list or comma separated
        """
        self._bcc += [bcc] if isinstance(bcc, str) else bcc

    def cc(self, cc: Union[str, List[str]]):
        """
        Add email copy recipient(s)
        :param cc: One or more receiver addresses, list or comma separated
        """
        self._cc += [cc] if isinstance(cc, str) else cc

    def message(self,
                content: str,
                subtype: str = 'plain',
                encoding: str = 'us-ascii'):
        """
        Add message main content.
        :param content: Main message content.
        :param mimetype: MIME type (default 'text')
        :param subtype: MIME subtype (default 'plain')
        :param encoding: Content encoding (default 'us-ascii')
        """
        part = MIMEText(content, subtype, encoding)
        self._msg.attach(part)

    def attach(self,
               content: Union[str, bytes],
               mimetype: str = TEXT_TYPE,
               subtype: str = 'plain',
               encoding: str = 'us-ascii',
               name: str = None):
        """
        Add an attachment to the message.
        :param content: Content to build (bytes or string)
        :param mimetype: MIME type. text, image, audio, etc.
        :param subtype: MIME subtype. mpg, mpr, html, csv, etc.
        :param encoding: Encoding for string content
        :param name: Name of file if known
        """
        part = self._make_part(content, mimetype, subtype, encoding, name=name)
        self._msg.attach(part)

    def attach_file(self,
                    path: Union[str, Path],
                    mimetype: str = None,
                    subtype: str = None,
                    encoding: str = None):
        """
        Add email attachment from a file. Attempt to determine MIME type/subtype
        from file extension if not given explicitly.
        :param path: Path to the file
        :param mimetype: Explicit MIME type to use.
        :param subtype: Explicit MIME subtype to use
        :param encoding: encoding for text attachments
        """
        if not isinstance(path, Path):
            path = Path(path)

        if not (mimetype or subtype):
            typesubtype = mimetypes.guess_type(path)[0]
            typesubtype = typesubtype if typesubtype else 'application/unknown'
            mtst = typesubtype.split('/', 1)
            mimetype = mimetype if mimetype else mtst[0]
            subtype = subtype if subtype else mtst[1]

        if not encoding:
            encoding = ENCODING_ASCII if mimetype == TEXT_TYPE else ENCODING_UTF8

        content = path.read_text() if mimetype == TEXT_TYPE else path.read_bytes()
        self.attach(content, mimetype, subtype, encoding, name=path.name)

    def _make_part(self,
                   content: Union[str, bytes],
                   mimetype: str,
                   subtype: str,
                   encoding: str = 'utf-8',
                   name: str = None):
        """
        Build a MIMEBase part
        :param content: Content to build (bytes or string)
        :param mimetype: MIME type. text, image, audio, etc.
        :param subtype: MIME subtype. mpg, mpr, html, csv, etc.
        :param encoding: Encoding for string content
        :param name: Optional name for section. (File name, for example.)
        :return: Constructed MIME part
        """
        part = MIMEBase(mimetype, subtype, Name=name)
        if mimetype == TEXT_TYPE:
            try:
                part.set_payload(content, encoding)
            except UnicodeEncodeError:
                # We thought that this was a text file but there are bad
                # characters. Instead, make it utf-8.
                part = MIMEBase(mimetype, subtype, Name=name)
                part.set_payload(content, 'utf-8')
                encoders.encode_base64(part)
        else:
            # Create binary part
            part.set_payload(content)
            encoders.encode_base64(part)
        return part

    @property
    def email(self) -> MIMEMultipart:
        """
        Return the completed message
        :return: MIMEMultiPart
        """
        if self._to:
            self._msg['To'] = ','.join(self._to)
        if self._cc:
            self._msg['Cc'] = ','.join(self._cc)
        if self._bcc:
            self._msg['Bcc'] = ','.join(self._bcc)
        return self._msg

