CREATE TABLE phone_numbers (
    wapn_id         TEXT PRIMARY KEY,       -- Meta's phone_number_id
    wa_number       TEXT NOT NULL,           -- Display phone number
    label           TEXT                     -- e.g. "support", "sales"
);

CREATE TABLE users (
    user_id         TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    password        TEXT NOT NULL,            -- Hashed password
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active       BOOLEAN DEFAULT TRUE,
    is_admin        BOOLEAN DEFAULT FALSE,
    last_login_at   TIMESTAMP,
    wapn_id         TEXT NOT NULL,
    FOREIGN KEY (wapn_id) REFERENCES phone_numbers(wapn_id)
);

CREATE TABLE conversations (
    conversation_id     TEXT PRIMARY KEY,
    customer_wa_user_id TEXT NOT NULL,       -- Stable WhatsApp user ID unique id for each whatsapp account
    customer_wa_id      TEXT NOT NULL,       -- Customer's current phone number
    customer_name       TEXT,
    wapn_id             TEXT NOT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wapn_id) REFERENCES phone_numbers(wapn_id)
);

CREATE TABLE messages (
    message_id      TEXT PRIMARY KEY,        -- wamid from WhatsApp
    conversation_id TEXT NOT NULL,
    timestamp       INTEGER NOT NULL,        -- Unix timestamp
    message_type    TEXT NOT NULL,            -- text, image, audio, video, etc.
    message         TEXT,                     -- Message content
    direction       TEXT NOT NULL CHECK (direction IN ('in', 'out')),
    status          TEXT DEFAULT 'sent' CHECK (status IN ('sent', 'delivered', 'read')),
    viewed_by       TEXT,                     -- Staff who viewed the message
    viewed_at       TIMESTAMP,               -- When it was viewed
    messaged_by     TEXT,                     -- Who sent it (bot or staff, NULL for incoming)
    reply_msg_id    TEXT,                     -- Quote reply reference
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id),
    FOREIGN KEY (viewed_by) REFERENCES users(user_id),
    FOREIGN KEY (messaged_by) REFERENCES users(user_id),
    FOREIGN KEY (reply_msg_id) REFERENCES messages(message_id)
);

CREATE TABLE message_status (
    message_id      TEXT PRIMARY KEY,
    delivered_at    INTEGER,                 -- Unix timestamp
    read_at         INTEGER,                 -- Unix timestamp
    FOREIGN KEY (message_id) REFERENCES messages(message_id)
);

-- ============================================
-- Indexes for common queries
-- ============================================
CREATE INDEX idx_users_wapn_id ON users(wapn_id);
CREATE INDEX idx_conversations_wapn_id ON conversations(wapn_id);
CREATE INDEX idx_conversations_customer ON conversations(customer_wa_user_id);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_messaged_by ON messages(messaged_by);
CREATE INDEX idx_messages_viewed_by ON messages(viewed_by);
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
CREATE INDEX idx_messages_status ON messages(status);