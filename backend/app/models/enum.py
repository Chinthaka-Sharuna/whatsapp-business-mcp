from enum import Enum

class PhoneNumberLables(str,Enum):
    SUPPORT = "support"
    SALES = "sales"
    CHATBOT = "chatbot"

class MessageDirection(str,Enum):
    IN = "in"
    OUT = "out"

class MessageStatus(str,Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"