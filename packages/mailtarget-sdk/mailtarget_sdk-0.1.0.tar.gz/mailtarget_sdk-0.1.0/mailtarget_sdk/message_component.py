class Address:
    def __init__(self, email="", name=""):
        self.email = email
        self.name = name

    def to_dict(self):
        return {
            "email": self.email,
            "name": self.name,
        }
    
class Header:
    def __init__(self, name="", value=""):
        self.name = name
        self.value = value

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value,
        }

class Attachment:
    def __init__(self, mime_type="", filename="", value="", contentId= "", disposition=""):
        self.mime_type = mime_type
        self.filename = filename
        self.value = value
        self.contentId = contentId
        self.disposition = disposition
        

    def to_dict(self):
        return {
            "mimeType": self.mime_type,
            "filename": self.filename,
            "value": self.value,
            "contentId": self.contentId,
            "disposition": self.disposition
        }

class OptionsAttributes:
    def __init__(self, click_tracking=False, open_tracking=False, transactional=True):
        self.click_tracking = click_tracking
        self.open_tracking = open_tracking
        self.transactional = transactional
    
    def to_dict(self):
        return {
            "clickTracking": self.click_tracking,
            "openTracking": self.open_tracking,
            "transactional": self.transactional
        }