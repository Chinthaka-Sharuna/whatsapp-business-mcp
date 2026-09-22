# WhatsApp MCP Server — Data Dictionary

---

## 1. phone_numbers

### Purpose

This table stores the WhatsApp Business phone numbers registered in the system. Each phone number represents a separate business line (e.g. support, sales, billing). It acts as the top-level entity that users and conversations are linked to, enabling the system to manage multiple WhatsApp lines from a single application.

### Columns

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| wapn_id | TEXT | PRIMARY KEY | Meta's unique phone number identifier, obtained from the `phone_number_id` field in the WhatsApp Cloud API webhook metadata. |
| wa_number | TEXT | NOT NULL | The display phone number in international format. |
| label | TEXT | — | A human-readable label describing the purpose of the phone line. |

---

## 2. users

### Purpose

This table stores all accounts that can send messages through the system, including both human agents and bot accounts. By treating bots and humans as the same entity, the system uses a unified flow for message handling. The application layer determines which user is a bot through configuration rather than a database column. Each user is assigned to a specific phone number, defining which business line they operate on.

### Columns

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| user_id | TEXT | PRIMARY KEY | Unique identifier for the user. |
| name | TEXT | NOT NULL | Display name of the user or bot. |
| password | TEXT | NOT NULL | Hashed password used for authentication. Plain text passwords must never be stored. |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When the user account was created. |
| is_active | BOOLEAN | DEFAULT TRUE | Whether the account is currently active. Inactive accounts cannot log in or send messages. |
| is_admin | BOOLEAN | DEFAULT FALSE | Whether the user has admin privileges. |
| last_login_at | TIMESTAMP | — | Timestamp of the user's most recent login. NULL if the user has never logged in. |
| wapn_id | TEXT | FOREIGN KEY → phone_numbers(wapn_id), NOT NULL | The phone number this user is assigned to. |

---

## 3. conversations

### Purpose

This table represents a chat thread between a customer and a business phone number. A new conversation is created for each unique combination of customer and business phone number, meaning one customer can have multiple conversations if they message different business lines. The table stores both the customer's stable user ID and their current phone number. If a customer changes their phone number, the stable user ID remains the same, preserving conversation history, while the phone number field is updated to enable continued communication.

### Columns

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| conversation_id | TEXT | PRIMARY KEY | Unique identifier for the conversation. |
| customer_wa_user_id | TEXT | NOT NULL | The customer's stable WhatsApp user ID. This ID is country-scoped and persists even if the customer changes their phone number. |
| customer_wa_id | TEXT | NOT NULL | The customer's current phone number in international format. Updated if the customer changes their number. Required for sending replies through the API. |
| customer_name | TEXT | — | The customer's WhatsApp profile name, obtained from the webhook payload. |
| wapn_id | TEXT | FOREIGN KEY → phone_numbers(wapn_id), NOT NULL | The business phone number this conversation belongs to. |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When the conversation was first created. |

---

## 4. messages

### Purpose

This table stores every incoming and outgoing message across all conversations. It contains the message content, metadata, and UI-related tracking such as who sent the message, who viewed it, and the current delivery status. The delivery status is stored directly in this table for fast rendering of tick indicators in the frontend without requiring a JOIN. The table also supports quote replies through a self-referencing foreign key, allowing a message to reference another message it is replying to.

### Columns

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| message_id | TEXT | PRIMARY KEY | The unique message ID from WhatsApp (`wamid`). Also used for deduplication since webhooks may fire multiple times. |
| conversation_id | TEXT | FOREIGN KEY → conversations(conversation_id), NOT NULL | The conversation this message belongs to. |
| timestamp | INTEGER | NOT NULL | Unix timestamp of when the message was sent or received. |
| message_type | TEXT | NOT NULL | The type of message content. |
| message | TEXT | — | The message content. For text messages this is the body text. For media messages this may contain a URL or caption. NULL for unsupported message types. |
| direction | TEXT | NOT NULL, CHECK IN ('in', 'out') | `in` — message received from the customer. `out` — message sent by the bot or a human agent. |
| status | TEXT | DEFAULT 'sent', CHECK IN ('sent', 'delivered', 'read') | Current delivery status of the message. Updated via WhatsApp webhook status events. Used directly by the frontend to render tick indicators. |
| viewed_by | TEXT | FOREIGN KEY → users(user_id) | The staff member who viewed this incoming message. NULL if the message has not been viewed yet. |
| viewed_at | TIMESTAMP | — | When the message was viewed by the staff member. NULL if the message has not been viewed yet. |
| messaged_by | TEXT | FOREIGN KEY → users(user_id) | The user (bot or human) who sent the message. NULL for incoming messages where `direction = 'in'`. |
| reply_msg_id | TEXT | FOREIGN KEY → messages(message_id) | References another message in the same conversation if this is a quote reply. NULL if not a reply. |

---

## 5. message_status

### Purpose

This table tracks delivery timestamps for outgoing messages. While the messages table stores the current delivery status for fast UI rendering, this table records when each delivery event occurred. This data is used for analytics such as average delivery time, average time to read, and delivery success rates. The table is kept separate to avoid bloating the messages table with columns that are rarely needed during normal message display.

### Columns

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| message_id | TEXT | PRIMARY KEY, FOREIGN KEY → messages(message_id) | The message this status record belongs to. One-to-one relationship with the messages table. |
| delivered_at | INTEGER | — | Unix timestamp of when the message was delivered to the customer's device. NULL if not yet delivered. |
| read_at | INTEGER | — | Unix timestamp of when the customer read the message. NULL if not yet read. |

---

## Relationships

| Relationship | Type | Description |
|--------------|------|-------------|
| phone_numbers → users | One-to-Many | One phone number can have multiple users (agents and bots) assigned to it. |
| phone_numbers → conversations | One-to-Many | One phone number can have multiple conversations with different customers. |
| conversations → messages | One-to-Many | One conversation contains zero or more messages. |
| users → messages (messaged_by) | One-to-Many | One user can send zero or more outgoing messages. |
| users → messages (viewed_by) | One-to-Many | One user can view zero or more incoming messages. |
| messages → messages | Self-referencing | A message can optionally reference one other message as a quote reply via `reply_msg_id`. |
| messages → message_status | One-to-One | Each message has at most one status tracking record. |

---

## Indexes

| Index Name | Table | Column | Purpose |
|------------|-------|--------|---------|
| idx_users_wapn_id | users | wapn_id | Find all users assigned to a phone number. |
| idx_conversations_wapn_id | conversations | wapn_id | Find all conversations under a phone number. |
| idx_conversations_customer | conversations | customer_wa_user_id | Look up all conversations for a specific customer. |
| idx_messages_conversation | messages | conversation_id | Retrieve all messages in a conversation. |
| idx_messages_messaged_by | messages | messaged_by | Find all messages sent by a specific user. |
| idx_messages_viewed_by | messages | viewed_by | Find all messages viewed by a specific user. |
| idx_messages_timestamp | messages | timestamp | Order and filter messages by time. |
| idx_messages_status | messages | status | Filter messages by delivery status. |

---

## Enum Values

| Column | Table | Allowed Values |
|--------|-------|----------------|
| direction | messages | `in`, `out` |
| status | messages | `sent`, `delivered`, `read` |
| message_type | messages | `text`, `image`, `audio`, `video`, `document`, `sticker`, `location`, `contacts`, `interactive`, `reaction` |