names1 = ['A', 'B']
names2 = names1[:]
print (names1[:])
names3 = names2
names2[0] = 'C'
names3[1] = 'E'
print (names1)
print (names2)
print (names3)