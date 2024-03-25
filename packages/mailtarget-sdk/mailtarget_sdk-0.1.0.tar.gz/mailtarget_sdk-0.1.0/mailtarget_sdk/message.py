import json
from .validation import *
from .message_component import *

class Message:
    def __init__(
            self, subject="", from_address=Address(), reply_to=[], 
            to=[], cc=[], bcc=[], body_text="", 
            body_html="", headers=[], attachment=[], 
            metadata={}, options_attributes=OptionsAttributes(),
            template_id= "", substitution_data={}):
        self.subject = subject
        self.from_address = from_address
        self.reply_to = reply_to if reply_to else []
        self.to = to if to else []
        self.cc = cc if cc else []
        self.bcc = bcc if bcc else []
        self.body_text = body_text
        self.body_html = body_html
        self.headers = headers if headers else []
        self.attachment = attachment if attachment else []
        self.metadata = metadata if metadata else {}
        self.options_attributes = options_attributes if options_attributes else OptionsAttributes()
        self.template_id = template_id
        self.substitution_data = substitution_data if substitution_data else {}

    def is_valid(self):
        if not self.from_address or not self.from_address.email:
            return "from is empty"
        if not self.body_text and not self.body_html:
            return "text or html is empty"
        if not isEmail(self.from_address.email):
            return self.from_address.email + " is not a valid email address"
        if not self.to:
            return "to is empty"
        for recipient in self.to + self.cc + self.bcc + self.reply_to:
            if not isEmail(recipient.email):
                return recipient.email + " is not a valid email address"
        if self.body_html and not isHTML(self.body_html):
            return "not valid html"
        return None

    def set_reply_to(self, reply_to):
        self.reply_to = reply_to

    def set_cc(self, cc):
        self.cc = cc

    def set_bcc(self, bcc):
        self.bcc = bcc

    def set_headers(self, headers):
        self.headers = headers

    
    def set_attachment(self, attachment=[]):
        """
        Sets the attachment for the object.

        Parameters:
        attachment (list of Attachment, optional): An array of Attachment objects to be set as attachments. 
            Defaults to an empty list if not provided.

        Returns:
        None
        """
        self.attachment = attachment

    def set_metadata(self, metadata={}):
        self.metadata = metadata

    def set_options_attributes(self, attributes=OptionsAttributes()):
        self.options_attributes = attributes

    def to_dict(self):
        return {
            "subject": self.subject,
            "from": self.from_address.to_dict(),
            "replyTo": [address.to_dict() for address in self.reply_to],
            "to": [address.to_dict() for address in self.to],
            "cc": [address.to_dict() for address in self.cc],
            "bcc": [address.to_dict() for address in self.bcc],
            "bodyText": self.body_text,
            "bodyHtml": self.body_html,
            "headers": [header.to_dict() for header in self.headers],
            "attachments": [attachment.to_dict() for attachment in self.attachment],
            "metadata": self.metadata,
            "optionsAttributes": self.options_attributes.to_dict(),
            "templateId": self.template_id,
            "substitutionData": self.substitution_data
        }

    def to_json(self):
        return json.dumps(self.to_dict())
    