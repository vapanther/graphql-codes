import chargebee
import json
chargebee.configure("test_qqu3aX84uFhM2zJe0qsIoI96NPfkfBtV","rsystems-test")
entries = chargebee.Item.list({
    "limit" : 2
    })
for entry in entries:
  item = entry.item
  print(item)