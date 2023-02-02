from slack_cleaner2 import *


s = SlackCleaner('xxxxxxxx')
# list of users
users = s.users
print(users)
# list of all kind of channels
conversations = s.conversations
print("conversations")
print(s.conversations)

# delete all messages in -bots channels
for msg in s.msgs(filter(match('.*securitybot'), s.conversations)):
  # delete messages, its files, and all its replies (thread)
    print("messages")
    print(msg)
    msg.delete(replies=True, files=True)

# delete all general messages and also iterate over all replies
for msg in s.c.general.msgs(with_replies=True):
    msg.delete()
