a = [1,2,3,4,5,'hey','friend']


def count(lst):
    q = 0
    for num in lst:
        q += 1
    #print(f'Number of items in list: {q}')
    return q

count(a)
b = 23 + count(a)

print(b)
