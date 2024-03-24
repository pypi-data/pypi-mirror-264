import configured_mail_sender
import argparse
import platformdirs
import os
import logging
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from pathlib import Path
from email import encoders

APPLICATION_NAME = 'send_email'
DEFAULT_LOG_FILE = os.path.join(platformdirs.user_log_dir(), APPLICATION_NAME + '.log')

# BINARY_TYPES = {'jpg', 'jpeg', 'gif', 'png', 'pdf'}
PLAINTEXT_TYPES = {'plain', 'txt', 'text', 'html', 'csv'}

APPLICATION_TYPE = 'application'
VIDEO_TYPE = 'video'
IMAGE_TYPE = 'image'
TEXT_TYPE = 'text'
AUDIO_TYPE = 'audio'

TYPE_SUBTYPES = {
    'zip': (APPLICATION_TYPE, 'zip'),
    'mpeg': (VIDEO_TYPE, 'mpeg'),
    'bmp': (IMAGE_TYPE, 'bmp'),
    'jpg': (IMAGE_TYPE, 'jpg'),
    'jpeg': (IMAGE_TYPE, 'jpg'),
    'gif': (IMAGE_TYPE, 'gif'),
    'png': (IMAGE_TYPE, 'png'),
    'txt': (TEXT_TYPE, 'plain'),
    'text': (TEXT_TYPE, 'plain'),
    'html': (TEXT_TYPE, 'html'),
    'csv': (APPLICATION_TYPE, 'csv'),
    'tsv': (APPLICATION_TYPE, 'tab-separated-values'),
    'mp4': (VIDEO_TYPE, 'mp4'),
    'pdf': (APPLICATION_TYPE, 'pdf')
}


def _list_domains(sender_module, args):
    domains = sender_module.known_domains(overrides=args.email_servers)
    print("Known email domains:")
    for domain, text in domains.items():
        print(f'   {domain}: {text}')


def main(sender_module=configured_mail_sender):
    """
    Send an email with limited content from command line
    :param sender_module: For testing only, class to create sender.
    :return: None
    """
    # First, figure out what we'll be doing
    parser = argparse.ArgumentParser(sys.argv[0],
                                     description='Send a simple email message')
    parser.add_argument('--from',
                        dest='sender',
                        metavar='sender',
                        help='Sending email address (required in most cases)')
    parser.add_argument('--subject',
                        metavar='<subject>',
                        help='Email subject')
    parser.add_argument('--to',
                        metavar='recipient(s)',
                        help='Public recipients, comma separated')
    parser.add_argument('--cc',
                        metavar='<copy recipient(s)>',
                        help='Copy recipients, comma separated')
    parser.add_argument('--bcc',
                        metavar='<blind recipient(s)>',
                        help='Hidden recipients, comma separated')
    parser.add_argument('--email_creds',
                        metavar='<email credential file>',
                        help='File with email passwords if not standard')
    parser.add_argument('--email_servers',
                        metavar='<email domain specification file>',
                        help='File with email domain configuration if not standard')
    parser.add_argument('--attach',
                        metavar='<list of files to attach to the email',
                        help='Attach files (comma separated) to the email')
    parser.add_argument('--list_directories',
                        default=False,
                        action='store_true',
                        help='List data and configuration directories and exit')
    parser.add_argument('--list_domains',
                        default=False,
                        action='store_true',
                        help='Print known email domains and exit')
    parser.add_argument('--logfile',
                        default=DEFAULT_LOG_FILE,
                        metavar='<logfile>',
                        help='File for application logs')
    parser.add_argument('--log_level',
                        default='info',
                        metavar='<log level>',
                        help='Logging level, default=info')
    parser.add_argument('--message',
                        metavar='<message file>',
                        help='File with message, or \'stdin\' to read from stdin')
    parser.add_argument('content',
                        nargs='*',
                        help='The message if no --message provided')

    args = parser.parse_args()

    if args.logfile == 'stdout':
        out = {'stream': sys.stdout}
    elif args.logfile == 'stderr':
        out = {'stream': sys.stderr}
    else:
        out = {'filename': args.logfile}
        directory, file_name = os.path.split(args.logfile)
        Path(directory).mkdir(exist_ok=True, parents=True)

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=getattr(logging, args.log_level.upper()),
        **out
    )

    logging.info(f'Running {" ".join(sys.argv)}')

    if args.list_domains:
        _list_domains(sender_module, args)
        sys.exit(0)

    if args.list_directories:
        # Making it easy to note where users should look for files on this platform.
        mailsender_configs = sender_module.config_file_list()
        print('configured_mail_sender configuration files:')
        for f in mailsender_configs:
            print(f'\t{f}')
        print(f'log output\n\t{args.logfile}')
        sys.exit(0)

    if not args.sender:
        parser.error('--from=sender is required')

    if not (args.to or args.bcc or args.cc):
        parser.error('At least one of --to, --cc, or --bcc is required')

    sender = sender_module.create_sender(args.sender,
                                         creds_file=args.email_creds,
                                         overrides=args.email_servers,
                                         )

    msg = MIMEMultipart()
    if args.to:
        msg['to'] = args.to
    if args.bcc:
        msg['bcc'] = args.bcc
    if args.cc:
        msg['cc'] = args.cc
    if args.subject:
        msg['Subject'] = args.subject

    body_type = 'plain'
    if args.message:
        if args.message == 'stdin':
            body = sys.stdin.read()
        else:
            dir, file = os.path.split(args.message)
            parts = file.rsplit('.', 1)
            if len(parts) > 1:
                body_type = parts[1]
            with open(args.message, 'r') as infile:
                body = infile.read()
    else:
        body = ' '.join(args.content) + '\n'
    if body:
        part = MIMEText(body, body_type)
        # encoders.encode_base64(part)
        msg.attach(part)

    if args.attach:
        for attachment in args.attach.split(','):
            direct, file_name = os.path.split(attachment)
            # Support text, pdf, jpeg, jpg, png, gif, binary, html
            parts = file_name.rsplit('.', 1)
            file_type = parts[1] if len(parts) > 1 else 'unk'
            file_type = file_type.lower()
            mimetype, subtype = TYPE_SUBTYPES.get(file_type,
                                                  ('application', 'octet-stream'))
            if mimetype == 'text':
                with open(attachment, 'r') as reader:
                    content = reader.read()
                part = MIMEBase(mimetype, subtype, Name=file_name)
                part.set_payload(content, 'utf-8')
            else:
                with open(attachment, 'rb') as reader:
                    content = reader.read()
                part = MIMEBase(mimetype, subtype, Name=file_name)
                part.set_payload(content)
                encoders.encode_base64(part)

            part.add_header('Content-Decomposition',
                            f'attachment; filename={file_name}')
            msg.attach(part)

    sender.send_message(msg)

    sys.exit(0)


APDF = '/Users/davidwillcox/Documents/GarageKeypadInstructionsDomino.pdf'
ACSV = '/Users/davidwillcox/Downloads/EnergyandPower-PV-Month-Willcox-2022-04.csv'
# BCSV = '/Users/davidwillcox/PycharmProjects/configured_mail_sender/test.csv'
ATEXT = '/Users/davidwillcox/PycharmProjects/configured_mail_sender/test_attach.txt'
BCSV = '/Users/davidwillcox/Downloads/solar_csv.csv'
AJPG = ('/Users/davidwillcox/Downloads/blood-donation-chart-r'
        'ecipient-and-donor-vector-23523010.jpg')
AHTML = '/Users/davidwillcox/test_html.html'

if __name__ == "__main__":
    # sys.argv = ['foo', '--from', 'daw30410@yahoo.com', '--to', 'daw30410@yahoo.com',
    #             '--subject', 'Testing email send - Downloaded PDF (original)',
    #             # '--attach', ','.join([ATEXT, AHTML, APDF, ACSV, BCSV, AJPG]),
    #             '--attach', ','.join([APDF]),
    #             # '--attach', ','.join([BCSV]),
    #             # '--attach', ','.join([AHTML]),
    #             'This', 'is', 'the', 'message']
    main()
