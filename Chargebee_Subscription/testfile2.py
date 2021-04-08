import chargebee
import json
chargebee.configure("test_qqu3aX84uFhM2zJe0qsIoI96NPfkfBtV","rsystems-test")
'''result = chargebee.Plan.create({
    "id" : "silver1",
    "name" : "Silver1",
    "invoice_name" : "sample plan",
    "price" : 5000,
    "cf_usage":"testUsage"
    })
plan = result.plan
print(plan.cf_usage)'''

'''result = chargebee.Plan.retrieve("silver1")
plan = result.plan
print(plan)'''

entries = chargebee.Plan.list({
    "limit" : 18,
    "status[is]" : "active"
    })
for entry in entries:
  plan = entry.plan
  print(plan)