import os
import platformdirs
import yaml
from abc import abstractmethod
from email.mime.base import MIMEBase
from os import environ, path
from typing import Union, MutableMapping, List, Dict, Mapping
import combine_settings
from filelock import FileLock

_OUTLOOK_SERVER = {
    'server': 'smtp-mail.outlook.com',
    'port': 587,
}
_BUILTIN_DOMAINS = {
    'yahoo.com': {
        'protocol': 'smtp',
        'server': 'smtp.mail.yahoo.com',
        'port': 587,
    },
    'aol.com': {
        'server': 'smtp.aol.com',
        'port': 465,
    },
    'gmail.com': {
        'server': 'smtp.gmail.com',
    },
    'verizon.com': {
        'server': 'outgoing.verizon.net',
    },
    'outlook.com': _OUTLOOK_SERVER,
    'hotmail.com': _OUTLOOK_SERVER,
    'live.com': _OUTLOOK_SERVER,
    'comcast.net': {
        'server': 'smtp.comcast.net',
        'port': 587,
    },
}

CONFIG_FILE_NAME = 'mailsender_domains.yml'
CREDS_FILE_NAME = 'mailsender_creds.yml'
CONFIG_APPLICATION_NAME = 'MailSender'
DEFAULT_CREDS_FILE = path.join(platformdirs.user_config_dir(CONFIG_APPLICATION_NAME),
                               CREDS_FILE_NAME)


class MailSenderException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class MailSenderUnsupportedException(MailSenderException):
    def __init__(self, *args, **kwargs):
        MailSenderException.__init__(self, *args, **kwargs)


class MailSender:
    def __init__(self,
                 sender: str,
                 domain_spec: Dict,
                 **kwargs: Dict):
        """
        Generic (abstract) MailSender - Class to send email from a specified sender
        :param sender str: Email address we'll be sending as
        :param domain_spec dict: Settings for this domain
        :param **creds_file str: Path to user credentials file
        """

        # Save these in case someone wants other parameters
        self.kwargs = kwargs

        # This has domain-specific settings
        self.domain_spec = domain_spec

        # Load user service-specific credentials (passwords or whatever).
        # User credentials are from the first specified of:
        #   - The creds_file parameter.
        #   - The MAILSENDER_CREDS environment variable
        #   - mailsender_creds.yml in the user's standard configuration file
        # default_file =
        #             path.join(platformdirs.user_config_path(CONFIG_APPLICATION_NAME),
        #                          'mailsender_creds.yml')
        self.user_cred_file = _get_user_cred_file(**kwargs)
        creds_dir = path.split(self.user_cred_file)[0]
        # Make sure the credentials directory exists, even with no actual credentials.
        os.makedirs(creds_dir, mode=0o700, exist_ok=True)

        self.user_cred_lock = f'{self.user_cred_file}.lock'
        self.cred_locker = FileLock(self.user_cred_lock)
        self.user_credentials = self._read_creds_file().get(sender)
        if not self.user_credentials:
            self.user_credentials = {}
        self.sender = sender

    def open(self) -> 'MailSender':
        """Do initialization. Variables can be initialized in __init__, but any
        interactions with externals should happen here.

        :returns: self
        """
        return self

    def _read_creds_file(self) -> MutableMapping:
        """
        Return current content of creds file.
        :return: Content of creds file
        """
        with self.cred_locker:
            if path.exists(self.user_cred_file):
                try:
                    with open(self.user_cred_file, 'r') as f:
                        # Question: is there a way to tell safe_load to allow tabs?
                        creds = yaml.load(f, Loader=yaml.Loader)
                    return creds
                except IOError as e:
                    raise MailSenderException(e, f"Error opening {self.user_cred_file}")
            else:
                return {}

    def _update_creds(self) -> None:
        """
        Update the user credentials file from the current content of user_creds.
        :return: None
        """
        with self.cred_locker:
            # First, reload old credentials
            current_creds = self._read_creds_file()
            current_creds[self.sender] = self.user_credentials

            temp_file = f'{self.user_cred_file}.temp'
            try:
                # Write the new file, then replace the old file, to avoid damaging
                # the old file if something breaks in the middle.
                fd = os.open(temp_file, (os.O_CREAT | os.O_TRUNC | os.O_WRONLY), 0o600)
            except IOError as e:
                raise MailSenderException(e, f"Can't write {self.user_cred_file}")

            try:
                os.write(fd, bytes(yaml.safe_dump(current_creds), 'utf-8'))
                os.replace(temp_file, self.user_cred_file)
            except Exception as e:
                raise MailSenderException(e,
                                          "Problem writing new credentials" +
                                          temp_file)
            finally:
                os.close(fd)

    @abstractmethod
    def send_message(self, message: MIMEBase) -> None:
        """
        Send an email message. (Recipients are encoded in the message.)
        :param message: Message to send
        :return: None
        """

    @abstractmethod
    def get_service_name(self) -> str:
        """Return name of service.
        Extending class should override this to return
        the appropriate service name.

        :return: Name of service
        """


# TODO: Merge smtp_sender into here?


def create_sender(sender: str,
                  base_config: Union[Dict, str] = None,
                  overrides: Union[Dict, str] = None,
                  **kwargs) -> MailSender:
    """
    Create a MailSender instance to send email from the given sender from a
    given user.
    :param sender: Sending email address
    :param base_config: Override built-in base configuration for load_config()
    :param overrides: Settings to override default load in load_config()
    :param kwargs: Other settings that might be needed for specific MailSenders
    :return: A MailSender instance
    :raises: MailSenderException
    """

    if not sender:
        raise MailSenderException('sender is required')

    # Get server configurations (service type, SMTP url and port, etc)
    domains_conf = _get_domain_conf(base_config=base_config,
                                   overrides=overrides)

    # # Load global configurations (service type, SMTP url and port, etc)
    # domains_conf = combine_settings.load_config(CONFIG_FILE_NAME,
    #                                             base_config=base_config,
    #                                             application=CONFIG_APPLICATION_NAME,
    #                                             overrides=overrides)

    (addr, domain) = sender.split('@', 2)
    domain_spec = domains_conf.get(domain)
    if not domain_spec:
        raise MailSenderException(f"Domain {domain} isn't recognized")

    # Primarily for testing, you can provide an explicit "protocol" class specifying
    # the MailSender implementation to instantiate.
    protocol = domain_spec.get('protocol', 'smtp')

    # Will add this back if/when I add gmail OAuth2 support
    # if protocol == 'gmail':
    #   try:
    #     from gmail_sender import gmail_sender
    #     return gmail_sender.GmailSender(sender,
    #                                     domain_spec=domain_spec, **kwargs).open()
    #   except ModuleNotFoundError as e:
    #     raise MailSenderUnsupportedException(e,
    #                                        "mail_sender_gmail package not installed")

    if protocol == 'smtp':
        from configured_mail_sender import smtp_sender
        return smtp_sender.SMTPSender(sender, domain_spec=domain_spec, **kwargs).open()

    if ':' not in protocol:
        raise MailSenderException(f'No implementation specified for domain {domain}')

    # Maybe an explicit module:class?
    (module_, class_) = protocol.split(':', 1)
    try:
        import importlib
        mod = importlib.import_module(module_)
        cls = getattr(mod, class_)
        inst = cls(sender, domain_spec=domain_spec, **kwargs)
        if not isinstance(inst, MailSender):
            raise MailSenderException(f'{module_}:{class_} for '
                                      f'{domain} is not a MailSender')
        return inst.open()
    except (ModuleNotFoundError, AttributeError) as e:
        raise MailSenderUnsupportedException(e,
                                             f'{module_}:{class_} '
                                             f'for email domain {domain} unknown)')


def _get_user_cred_file(creds_file=None,
                        **kwargs) -> str:
    """
    Return path to user credentials file
    :param creds_file: User-specified file
    :return: Creds file
    """
    if not creds_file:
        creds_file = environ.get('MAILSENDER_CREDS', DEFAULT_CREDS_FILE)
    return creds_file


def config_file_list(base_config: str = None,
                     overrides: str = None,
                     creds_file: str = None) -> List[str]:
    """
    Get configuration file list
    :param base_config: Optional base configuration for load_config
    :param overrides: An additional file with domain specifications
    :param creds_file: Explicit path to user credentials file
    :return: List of directories searched
    """
    file_list = combine_settings.config_file_list(
        CONFIG_FILE_NAME,
        base_config=base_config,
        application=CONFIG_APPLICATION_NAME,
        overrides=overrides)

    file_list.append(_get_user_cred_file(creds_file))
    return file_list


def _get_domain_conf(base_config: Union[str, Dict] = None,
                     overrides: Union[str, Dict] = None) -> Mapping[str, Dict]:

    base_config = base_config if base_config else _BUILTIN_DOMAINS
    # Load global configurations (service type, SMTP url and port, etc)
    return combine_settings.load_config(CONFIG_FILE_NAME,
                                        base_config=base_config,
                                        application=CONFIG_APPLICATION_NAME,
                                        overrides=overrides)


def known_domains(base_config: str = None,
                  overrides: str = None) -> Dict[str, str]:
    """
    Return domain to server mapping for known domains
    :param base_config: Alternate base configuration
    :param overrides: User-specified override file
    :return: Mapping from domain to server
    """
    domains_conf = _get_domain_conf(base_config=base_config,
                                    overrides=overrides)
    ret = {}
    for domain, params in domains_conf.items():
        protocol = params.get('protocol', 'smtp')
        ret[domain] = params.get('server') if protocol == 'smtp' else protocol
    return ret
