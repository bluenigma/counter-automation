a = ['hello', 'there', 'my', 'dearest', 'friends', 'and', 'fiends']
print(a)

def find_word(feed):
    word = str(input('Word to search for: '))
    if word in feed:
        print('Found it!')
    else:
        print('Not found')

find_word(a)    
