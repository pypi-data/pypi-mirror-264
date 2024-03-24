================
Package Contents
================

-----------------
Table of Contents
-----------------
* `Configured Mail Sender`_
    * `Overview`_
    * `How It Works`_
* `send_email Command`_
* `Email Builder`_

----------------------
Configured Mail Sender
----------------------

++++++++
Overview
++++++++
There are multitudinous Python packages for sending emails with widely
varying interfaces. Some concentrate on constructing the email message,
others concentrate on the delivery. But virtually all require the caller to
have explicit knowledge of *how* the email will be delivered. Typically the
caller needs to know at least:

* The address and port for the SMTP server. (The fact that servers
  may have different connection encryption schems is generally ignored.)
* The sending email address.
* Login name for the smtp server, if different from the sender's address.
* Login credentials, typically password.

All the above vary by sending email address of course. This of course
puts the onus on the email package user to maintain the above for each
potential sender. And for password (or other protocol-specific authentication
values), they need to be protected in some way, at least readable only by
the user.

And, of course, they don't support more secure authentication systems like
Google's OAuth2.

With ``configured_email_sender``, the application only needs to know the sending email address.
``configured_email_sender`` uses
`combine-settings <https://pypi.org/project/combine-settings/>`_
to find all it needs to deliver the mail. Public settings, e.g, SMTP
address and port can be public for the whole site. Private information
(passwords) should be readable only by the user.

++++++++++++
How It Works
++++++++++++

``configured_mail_sender`` makes it easy for a Python script to send emails on behalf of a user
without dealing with the details of interaction with the sending email provider.
Your script only needs to know the sending email address. ``create_sender()`` uses configuration
files (system-wide or user-specific) to figure out how to communicate with the sender's
email domain.

The sending Python script creates a ``MailSender`` object for the sending email address.
It can then construct emails in the form of ``Mime`` objects and use the ``MailSender`` object
to send them.

Here's a simple example:

.. code-block::

    import configured_mail_sender
    from email.mime.text import MIMEText

    sender = configured_mail_sender.create_sender('sending-email@somedomain.com')
    msg = MIMEText("This is a test message", 'plain')
    msg['Subject'] = 'Success!'
    msg['To'] = 'receiver@gmail.com'
    msg['Cc'] = ['ccer1@somewhere.org', 'ccer2@elswhere.com']
    msg['Bcc'] = 'private@somedomain.com'

    sender.send_message(msg)


See the `DOCUMENTATION <https://github.com/dawillcox/configured_mail_sender/blob/main/DOCUMENTATION.rst>`_ for details on how to
configure ``configured_mail_sender``.

------------------
send_email Command
------------------

This package also provides a ``send_email`` command that lets you send a simple email message
from the command line. This can be handy to, for example, send a notification when your
system reboots or detects some kind of anomaly. The command exposes most of the
capabilities of ``configured_mail_sender``. Here's a simple example:

.. code-block::

    send_email --from me@me.Running --subject 'This is the subject' And this is the message

Will send an email from me@ to you@, with subject "This is the subject" and a message body
of "And this is the message".

See the detailed documentation for more.

-------------
Email Builder
-------------

And finally, the package provileds ``email_builder``, a class that simplifies building
a ``MimeMultipart`` message including attachments.

At a high level you'd use ``email_builder`` like this:

.. code-block::

    ebuilder = configured_mail_sender.email_builder.EmailBuilder()
    # Call methods (see below) to construct the email
    # A very simple example:
    ebuilder.subject('This is a sample email')
    ebuilder.to('receiver@somewhere.com')
    ebuilder.message('Here's a message with a pdf attachment.')
    ebuilder.attach_file('a_pdf_file.pdf')

    # Now, send the email.
    sender = configured_mail_sender.create_sender('sender@somewhere_else.com')
    sender.send_message(ebuilder.email)

That's it. See the detailed documentation for specifics.