import re

file1 = open('file2.txt')
numbers = []
for l in file1:
	numbers.append(re.findall('[0-9]+',l))
print (numbers)

total = 0
count = 0

for list1 in numbers:
	for string in list1:
		number_str = int(string)
		count += 1
		total += number_str

print (total)
print (count)
print (total)

