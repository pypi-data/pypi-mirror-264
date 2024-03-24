import unittest
import os
from configured_mail_sender.email_builder import EmailBuilder

TO_ADDR = 'to@to.com,totwo@to.com'
CC_ADDR = 'cc@cc.com'
BCC_ADDR = 'motnahp@hidden.com'
MESSAGE = 'This is a test message\n'

TEST_FILES_DIR = os.path.join(os.path.split(__file__)[0], 'test_files')
TEST_PDF = os.path.join(TEST_FILES_DIR, 'apdf.pdf')
TEST_JPG = os.path.join(TEST_FILES_DIR, 'ajpg.jpg')
TEST_HTML = os.path.join(TEST_FILES_DIR, 'ahtml.html')
TEST_UNK = os.path.join(TEST_FILES_DIR, 'afile.unk')
TEST_NON_ASCII = os.path.join(TEST_FILES_DIR, 'not_text.txt')
SUBJECT = 'This is the test subject'


class TestBuilder(unittest.TestCase):

    def test_build(self):
        builder = EmailBuilder()
        builder.to(TO_ADDR)
        builder.message(MESSAGE)
        builder.message(MESSAGE, subtype='html')
        builder.subject(SUBJECT)
        builder.attach_file(TEST_PDF)
        builder.attach_file(TEST_JPG)
        builder.attach_file(TEST_HTML)
        builder.attach_file(TEST_PDF, mimetype='application', subtype='other')
        builder.attach_file(TEST_UNK)

        msg = builder.email

        self.assertEqual(TO_ADDR, msg['To'])
        self.assertIsNone(msg['Cc'])
        self.assertIsNone(msg['Bcc'])
        self.assertEqual(SUBJECT, msg['subject'])

        parts = [p for p in msg.walk()]
        self.verify_data(parts[1], MESSAGE, 'text', 'plain')
        self.verify_data(parts[2], MESSAGE, 'text', 'html')
        self.verify_attachment(parts[3], TEST_PDF, 'application', 'pdf')
        self.verify_attachment(parts[4], TEST_JPG, 'image', 'jpeg')
        self.verify_attachment(parts[5], TEST_HTML, 'text', 'html')
        self.verify_attachment(parts[6], TEST_PDF, 'application', 'other')
        self.verify_attachment(parts[7], TEST_UNK, 'application', 'unknown')

    def test_other_receivers(self):
        builder = EmailBuilder()
        builder.bcc(BCC_ADDR)
        builder.cc(CC_ADDR)
        msg = builder.email
        self.assertEqual(CC_ADDR, msg['Cc'])
        self.assertEqual(BCC_ADDR, msg['Bcc'])
        builder.attach_file(TEST_PDF, mimetype='application', subtype='pdf')

    def test_non_ascii(self):
        builder = EmailBuilder()
        builder.to(TO_ADDR)
        builder.attach_file(TEST_NON_ASCII)
        msg = builder.email
        parts = [p for p in msg.walk()]
        self.verify_attachment(parts[1], TEST_NON_ASCII, 'text', 'plain')

    def verify_attachment(self, part, file, mimetype, subtype):
        self.assertEqual(mimetype, part.get_content_maintype())
        self.assertEqual(subtype, part.get_content_subtype())
        content = part.get_payload(decode=True)
        with open(file, 'rb') as f:
            expect_content = f.read()

        self.assertEqual(expect_content, content)

    def verify_data(self, part, content, mimetype, subtype):
        self.assertEqual(mimetype, part.get_content_maintype())
        self.assertEqual(subtype, part.get_content_subtype())
        payload = part.get_payload()
        self.assertEqual(content, payload)
