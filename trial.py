test_list = ({'gfg': 1, 'is': 2, 'good': 3},
             {'gfg': 2}, {'best': 3, 'gfg': 4})

print(test_list)
print()

res=[ sub['gfg'] for sub in test_list ]
print(res)