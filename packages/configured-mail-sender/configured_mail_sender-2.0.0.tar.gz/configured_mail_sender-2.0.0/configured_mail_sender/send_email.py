import configured_mail_sender
import argparse
import platformdirs
import os
import logging
import sys

from pathlib import Path
from configured_mail_sender.email_builder import EmailBuilder

APPLICATION_NAME = 'send_email'
DEFAULT_LOG_FILE = os.path.join(platformdirs.user_log_dir(), APPLICATION_NAME + '.log')

# BINARY_TYPES = {'jpg', 'jpeg', 'gif', 'png', 'pdf'}
# PLAINTEXT_TYPES = {'plain', 'txt', 'text', 'html', 'csv'}

# APPLICATION_TYPE = 'application'
# VIDEO_TYPE = 'video'
# IMAGE_TYPE = 'image'
# TEXT_TYPE = 'text'
# AUDIO_TYPE = 'audio'


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
    parser.add_argument('--from', '-f',
                        dest='sender',
                        metavar='<sender>',
                        help='Sending email address (required in most cases)')
    parser.add_argument('--subject', '-s',
                        metavar='<subject>',
                        help='Email subject')
    parser.add_argument('--to', '-t',
                        metavar='<recipient>',
                        action='append',
                        default=[],
                        help='Public recipient')
    parser.add_argument('--cc', '-c',
                        metavar='<copy recipient>',
                        action='append',
                        default=[],
                        help='Copy recipient')
    parser.add_argument('--bcc',
                        action='append',
                        default=[],
                        metavar='<blind recipient>',
                        help='Hidden recipient')
    parser.add_argument('--attach', '-a',
                        metavar='<file>',
                        action='append',
                        default=[],
                        help='Attach file to the email')
    parser.add_argument('--message',
                        metavar='<message file>',
                        # dest='msgsource',
                        help='File with message, or \'stdin\' to read from stdin'
                             ' (Only one allowed)')
    parser.add_argument('--email_creds',
                        metavar='<email credential file>',
                        help='File with email passwords if not standard')
    parser.add_argument('--email_servers',
                        metavar='<email domain specification file>',
                        help='File with email domain configuration if not standard')
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
    parser.add_argument('text',
                        nargs='*',
                        default=[],
                        help='The message if no --message')

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

    ebuilder = EmailBuilder()

    ebuilder.to(','.join(args.to))
    ebuilder.bcc(','.join(args.bcc))
    ebuilder.cc(','.join(args.cc))
    ebuilder.subject(args.subject)

    if args.message:
        if args.message == 'stdin':
            msg = sys.stdin.read()
        else:
            with open(args.message, 'r') as f:
                msg = f.read()
        ebuilder.message(msg)
    elif args.text:
        ebuilder.message(' '.join(args.text) + '\n')

    #
    # if args.stdin:
    #     ebuilder.message(sys.stdin.read())
    # elif args.message:
    #     ebuilder.message(' '.join(args.message) + '\n')

    for att in args.attach:
        for attachment in att.split(','):
            ebuilder.attach_file(attachment)

    sender = sender_module.create_sender(args.sender,
                                         creds_file=args.email_creds,
                                         overrides=args.email_servers,
                                         )
    sender.send_message(ebuilder.email)

    sys.exit(0)


if __name__ == "__main__":
    # APDF = '/Users/davidwillcox/Documents/GarageKeypadInstructionsDomino.pdf'
    # ACSV = '/Users/davidwillcox/Downloads/EnergyandPower-PV-Month-Willcox-2022-04.csv'
    # BCSV = '/Users/davidwillcox/PycharmProjects/configured_mail_sender/test.csv'
    # ATEXT = '/Users/davidwillcox/PycharmProjects/configured_mail_sender/test_attach.txt'
    # # BCSV = '/Users/davidwillcox/Downloads/solar_csv.csv'  # BAD
    # AJPG = ('/Users/davidwillcox/'
    #         'Downloads/blood-donation-chart-recipient-and-donor-vector-23523010.jpg')
    # AHTML = '/Users/davidwillcox/test_html.html'
    # sys.argv = ['foo', '--from', 'daw30410@yahoo.com', '--to', 'daw30410@yahoo.com',
    #             '--help',
    #             # '-t', 'dwillcoxster@gmail.com',
    #             '--subject', 'Testing email send - Everything',
    #             # '--attach', ','.join([ATEXT, AHTML, APDF, ACSV, BCSV, AJPG]),
    #             # '--attach', ','.join([ATEXT, AHTML, APDF, BCSV, AJPG]),
    #             '--attach', ACSV,
    #             '--attach', BCSV,
    #             '-a', APDF,
    #             '--attach', AHTML,
    #             '--attach', AJPG,
    #             'This', 'is', 'the', 'message',
    #             ]
    main()
