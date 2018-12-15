from collections import Counter

transactions = []

with open('./coffee-shop-data.txt', 'r') as f:
    for line in f:
        items = tuple(sorted(list(set(line[:-1].split(',')))))
        transactions.append(items)

print('Top 20 transactions: ')
for item in Counter(transactions).most_common(20):
    if len(item[0]) > 1:
        print('{} count {}'.format(item[0], item[1]))