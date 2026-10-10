from enum import Enum

class PhoneNumberLabels(str,Enum):
    SUPPORT = "support"
    SALES = "sales"
    CHATBOT = "chatbot"

class MessageDirection(str,Enum):
    IN = "in"
    OUT = "out"

class MessageStatus(str,Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    RECEIVED = "received"

class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    STICKER = "sticker"
    LOCATION = "location"
    CONTACTS = "contacts"
    INTERACTIVE = "interactive"
    BUTTON = "button"
    REACTION = "reaction"
    TEMPLATE = "template"
    UNSUPPORTED = "unsupported"