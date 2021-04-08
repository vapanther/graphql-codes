import chargebee
import json
chargebee.configure("test_XLstiV7ahWpqSdxB8V8hXdNKgwFB17QB","tvunetworks-test")
result = chargebee.Subscription.retrieve("169mBRSTrPrsX2P4s")
subscription = result.subscription
customer = result.customer
card = result.card
print(subscription)