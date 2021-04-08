import chargebee
import json
chargebee.configure("test_qqu3aX84uFhM2zJe0qsIoI96NPfkfBtV","rsystems-test")
result = chargebee.HostedPage.checkout_one_time({
    "billing_address" : {
        "first_name" : "John",
        "last_name" : "Doe",
        "line1" : "PO Box 9999",
        "city" : "Walnut",
        "state" : "California",
        "zip" : "91789",
        "country" : "US"
        },
    "shipping_address" : {
        "first_name" : "John",
        "last_name" : "Mathew",
        "city" : "Walnut",
        "state" : "California",
        "zip" : "91789",
        "country" : "US"
        },
    "customer" : {
        "id" : "__test__3Nl7Oe7SJWjx905b"
        },
    "addons" : [
        {
            "id" : "cbdemo_setuphelp",
            "unit_price" : 2000,
            "quantity" : 2
        }]
    })
hosted_page = result.hosted_page
print(hosted_page)