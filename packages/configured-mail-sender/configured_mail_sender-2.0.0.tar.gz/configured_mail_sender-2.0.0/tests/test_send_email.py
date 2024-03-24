import unittest
import sys
import tempfile
import os
import base64
from typing import List, Union

try:
    # This seems to work differently depending how it's run.
    # Pycharm is different from "normal."
    from . import test_send_email
except ImportError:
    import test_send_email

from configured_mail_sender import send_email
from email.mime.multipart import MIMEMultipart
from io import StringIO

TEST_FILES_DIR = os.path.join(os.path.split(__file__)[0], 'test_files')
TEST_PDF = os.path.join(TEST_FILES_DIR, 'apdf.pdf')
TEST_JPG = os.path.join(TEST_FILES_DIR, 'ajpg.jpg')
TEST_HTML = os.path.join(TEST_FILES_DIR, 'ahtml.html')

CONFIG_FILE_LIST = ['test_config_file.json']
KNOWN_DOMAIN = 'foo.com'
KNOWN_SERVER = 'foo.server'
KNOWN_DOMAINS = {KNOWN_DOMAIN: KNOWN_SERVER}
LATEST_OVERRIDES = None


class MockSender(object):
    def __init__(self,
                 sender: str,
                 creds_file: str = None,
                 overrides: str = None):
        self.message: MIMEMultipart = None
        self.sender = sender
        self.creds_file = creds_file
        self.overrides = overrides

    def send_message(self, message: MIMEMultipart):
        self.message = message


MOCK_MAIL_SENDER: MockSender = None


def extract_text(msg: MIMEMultipart) -> List[str]:
    ret = []
    for ent in msg.walk():
        if ent.get_content_maintype() == 'text':
            ret += [ent.get_payload()]
    return ret


def create_sender(sender: str,
                  creds_file: str = None,
                  overrides: str = None):
    global MOCK_MAIL_SENDER
    MOCK_MAIL_SENDER = MockSender(sender, creds_file, overrides)
    return MOCK_MAIL_SENDER


def config_file_list():
    return CONFIG_FILE_LIST


def known_domains(overrides=None):
    global LATEST_OVERRIDES
    LATEST_OVERRIDES = overrides
    return KNOWN_DOMAINS


class TestSender(unittest.TestCase):
    def setUp(self):
        self.saved_argv = sys.argv
        self.saved_stdout = sys.stdout
        self.saved_stdin = sys.stdin
        self.saved_stderr = sys.stderr
        self.test_dir = None

    def tearDown(self):
        self.restore()
        sys.argv = self.saved_argv
        if self.test_dir:
            self.test_dir.cleanup()

    def restore(self):
        sys.stdout = self.saved_stdout
        sys.stdin = self.saved_stdin
        sys.stderr = self.saved_stderr

    def runTest(self, params: Union[List[str], str],
                stdin: str = '') -> int:
        if isinstance(params, str):
            params = params.split(' ')
        sys.stdin = StringIO(stdin)
        stdout = StringIO()
        sys.stdout = stdout
        stderr = StringIO()
        sys.stderr = stderr
        sys.argv = ['test', '--logfile', '/dev/null'] + params
        try:
            exit_code = send_email.main(sender_module=test_send_email)
            sys.stdout = self.saved_stdout
        except SystemExit as e:
            exit_code = e.code
        stdout.seek(0)
        stderr.seek(0)
        self.stdout = stdout.read()
        self.stderr = stderr.read()
        return exit_code

    def test_help(self):
        exit_code = self.runTest(['--help'])
        self.assertEqual(0, exit_code)
        self.assertEqual('usage:',self.stdout[0:6])
        self.assertEqual('', self.stderr)

    def test_no_from(self):
        exit_code = self.runTest(['--cc', 'foo@bar',
                                  '--attach', 'foo',
                                  '--attach', 'bar'])
        self.assertEqual(2, exit_code)
        expect = '--from=sender is required'
        self.assertTrue(expect in self.stderr,
                        f"Expected to see '{expect}' in:\n{self.stderr}")

    def test_no_to(self):
        exit_code = self.runTest(['--from', 'foo@bar'])
        self.assertEqual(2, exit_code)
        expect = 'At least one of --to, --cc, or --bcc is required'
        self.assertTrue(expect in self.stderr,
                        f"Expected to see '{expect}' in:\n {self.stderr}")

    def test_simple_send(self):
        to = 't@bar'
        sender = 'f@bar'
        subject = 'This is test subject'
        msg = 'This is test message'
        creds_file = '/tmp/my_creds.json'
        exit_code = self.runTest(['--from', sender,
                                  '--to', to,
                                  '--email_creds', creds_file,
                                  '--subject', subject] + msg.split(' '))
        self.assertEqual(0, exit_code)
        mail_sender = MOCK_MAIL_SENDER
        message = mail_sender.message
        self.assertEqual(sender, mail_sender.sender)
        self.assertEqual(to, message['to'])
        self.assertEqual(subject, message['subject'])
        self.assertEqual(creds_file, mail_sender.creds_file)
        self.assertEqual(None, mail_sender.overrides)

        content = extract_text(message)
        self.assertEqual(1, len(content), "Should be only one text")
        self.assertEqual(f'{msg}\n', content[0])

    def test_send_from_stdin(self):
        to = 't@bar'
        sender = 'f@bar'
        subject = 'This is test from stdin'
        msg = 'This is test from stdin'
        overrides = "/tmp/test_overrides"
        exit_code = self.runTest(['--from', sender,
                                  '--cc', to,
                                  '--email_servers', overrides,
                                  '--message', 'stdin',
                                  '--subject', subject],
                                 stdin=msg)
        self.assertEqual(0, exit_code)
        mail_sender = MOCK_MAIL_SENDER
        self.assertEqual(None, mail_sender.creds_file)
        self.assertEqual(overrides, mail_sender.overrides)
        message = mail_sender.message
        self.assertEqual(sender, mail_sender.sender)
        self.assertEqual(to, message['cc'])
        self.assertEqual(subject, message['subject'])

        content = extract_text(message)
        self.assertEqual(1, len(content), "Should be only one text")
        self.assertEqual(msg, content[0])

    def test_list_domains(self):
        exit_code = self.runTest(['--list_domains'])
        self.assertEqual(None, LATEST_OVERRIDES)
        self.assertEqual(0, exit_code)
        expect = f'{KNOWN_DOMAIN}: {KNOWN_SERVER}'
        self.assertTrue(expect in self.stdout,
                        f"'{expect}' is missing")
        self.assertEqual(3, len(self.stdout.split('\n')),
                         'Wrong number of lines')

    def test_list_configs(self):
        exit_code = self.runTest(['--list_directories'])
        self.assertTrue(CONFIG_FILE_LIST[0] in self.stdout,
                   f"Missing '{CONFIG_FILE_LIST[0]}'")
        self.assertEqual(5, len(self.stdout.split('\n')),
                         'Wrong number of lines')
        self.assertEqual(0, exit_code)

    def test_message_from_file(self):
        self.test_dir = tempfile.TemporaryDirectory()
        test_file = 'message.txt'
        test_file_path = os.path.join(self.test_dir.name, test_file)
        the_message = 'This is a message from a file\nSee if it is correct'
        with open(test_file_path, 'w') as f:
            f.write(the_message)
        to = 't@bar'
        sender = 'f@bar'
        subject = 'This is test from a file'
        exit_code = self.runTest(['--from', sender,
                                  '--bcc', to,
                                  '--message', test_file_path,
                                  '--subject', subject])
        self.assertEqual(0, exit_code)
        mail_sender = MOCK_MAIL_SENDER
        message = mail_sender.message
        self.assertEqual(sender, mail_sender.sender)
        self.assertEqual(to, message['bcc'])
        self.assertEqual(subject, message['subject'])

        content = extract_text(message)
        self.assertEqual(1, len(content), "Should be only one text")
        self.assertEqual(the_message, content[0])

    def test_attachments(self):
        cmd = (f'--to t@foo.com --attach {TEST_PDF},{TEST_JPG},{TEST_HTML}'
               f' --from f@foo.com my message')
        exit_code = self.runTest(cmd)
        self.restore()
        self.assertEqual(0, exit_code)
        mail_sender = MOCK_MAIL_SENDER
        message = mail_sender.message

        parts = [p for p in message.walk()]
        self.verify_attachment(parts[2], TEST_PDF, 'application', 'pdf')
        self.verify_attachment(parts[3], TEST_JPG, 'image', 'jpeg')
        self.verify_attachment(parts[4], TEST_HTML, 'text', 'html')

    def verify_attachment(self, part, file, mimetype, subtype):
        self.assertEqual(mimetype, part.get_content_maintype())
        self.assertEqual(subtype, part.get_content_subtype())
        content = part.get_payload()
        if mimetype == 'text':
            with open(file, 'r') as f:
                expect_content = f.read()
        else:
            content = base64.decodebytes(bytes(content, 'ascii'))
            with open(file, 'rb') as f:
                expect_content = f.read()

        self.assertEqual(expect_content, content)
