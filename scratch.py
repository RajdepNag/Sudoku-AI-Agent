a = {'1': 'a'}
b = '2'
c = 'b'
d = {}
a[b] = c
print(a)
d = {'3': 'c'}
a.update(d)
print(a.items())