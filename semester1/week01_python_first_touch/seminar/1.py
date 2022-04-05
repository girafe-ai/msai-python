db = [
    {
        'author': 'Mike',
        'text': 'Hello abc',
        'date': 123456789,
        'seen': ['Mike2', 'John']
    },
    {
        'author': 'Mike',
        'text': 'Hello def',
        'date': 123456789,
        'seen': ['Mike2', 'John']
    }
]
db.append({
    'author': 'Mike2',
    'text': 'Hello 2 and 3',
    'date': 1234567890,
    'seen': []
})
# print(db)

words = set()
for message in db:
    words |= set(message['text'].lower().split())

print(words)