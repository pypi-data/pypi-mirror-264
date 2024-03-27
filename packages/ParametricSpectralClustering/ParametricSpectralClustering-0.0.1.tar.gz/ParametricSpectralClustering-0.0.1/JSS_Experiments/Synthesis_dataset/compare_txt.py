import filecmp

f1 = "y_pred_varied.txt"
f2 = "y_pred_varied2.txt"

result = filecmp.cmp(f1, f2)
print(result)
