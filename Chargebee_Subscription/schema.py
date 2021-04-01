import chargebee
import json
import graphene
import extraction
import requests

from chargebee import ChargeBee, Subscription

from testProg import customer

chargebee.configure("test_qqu3aX84uFhM2zJe0qsIoI96NPfkfBtV","rsystems-test")

class Subscription(graphene.ObjectType):
    id = graphene.String()
    planid = graphene.String(required=True)
    planquantity = graphene.Int()
    planunitprice = graphene.Int()
    billingperiod = graphene.Int()
    billingperiodunit = graphene.String()
    autocollection = graphene.String()
    customerid = graphene.String()
    planamount = graphene.Int()
    planfreequantity = graphene.Int()
    status = graphene.String()
    currenttermstart = graphene.Int()
    currenttermend = graphene.Int()
    nextbillingat = graphene.Int()
    createdat = graphene.Int()
    startedat = graphene.Int()
    activatedat = graphene.Int()
    updatedat = graphene.Int()
    hasscheduledchanges = graphene.Boolean()
    resourceversion = graphene.Int()
    deleted = graphene.Boolean()
    object = graphene.String()
    currencycode = graphene.String()
    dueinvoicescount = graphene.Int()
    mrr = graphene.Int()

class BillingAddress(graphene.ObjectType):
    city = graphene.String()
    country = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    line1 = graphene.String()
    object = graphene.String()
    state = graphene.String()
    state_code = graphene.String()
    validation_status = graphene.String()
    zip = graphene.String()

class Customer(graphene.ObjectType):
    allowdirectdebit = graphene.Boolean()
    autocollection = graphene.String()
    cardstatus = graphene.String()
    createdat = graphene.Int()
    deleted = graphene.Boolean()
    email = graphene.String()
    excesspayments = graphene.Int()
    firstname = graphene.String()
    id = graphene.String()
    lastname = graphene.String()
    locale = graphene.String()
    nettermdays = graphene.Int()
    object = graphene.String()
    piicleared = graphene.String()
    preferredcurrencycode = graphene.String()
    promotionalcredits = graphene.Int()
    refundablecredits = graphene.Int()
    resourceversion = graphene.Int()
    taxability = graphene.String()
    unbilledcharges = graphene.Int()
    updatedat = graphene.Int()
    billingaddress = graphene.Field(BillingAddress)

class CreateSubscriptionResponse(graphene.ObjectType):
    card_status=graphene.String()
    created_at=graphene.Int()
    deleted=graphene.Boolean()
    email=graphene.String()



#Mutation Code Start
class CreateSubscription(graphene.Mutation):
    class Arguments:
        plan_id = graphene.String(required=True)
        auto_collection = graphene.String()
        billing_address = graphene.String()
        customer = graphene.String()


    subs = graphene.Field(CreateSubscriptionResponse)
    def mutate(self, info, plan_id, auto_collection, billing_address, customer):
        result = create_subscription(plan_id, auto_collection, billing_address, customer)
        subscription = result.subscription
        customer = result.customer
        card = result.card
        invoice = result.invoice
        unbilled_charges = result.unbilled_charges
        print(customer.card_status)

        subs = CreateSubscriptionResponse(card_status=customer.card_status, created_at=customer.created_at,
                                          deleted=customer.deleted, email=customer.email)
        return CreateSubscription(subs)


class CreateCustomer(graphene.Mutation):
    class Arguments:
        allowdirectdebit = graphene.Boolean()
        autocollection = graphene.String()
        cardstatus = graphene.String()
        createdat = graphene.Int()
        deleted = graphene.Boolean()
        email = graphene.String()
        excesspayments = graphene.Int()
        firstname = graphene.String()
        id = graphene.String()
        lastname = graphene.String()
        locale = graphene.String()
        nettermdays = graphene.Int()
        object = graphene.String()
        piicleared = graphene.String()
        preferredcurrencycode = graphene.String()
        promotionalcredits = graphene.Int()
        refundablecredits = graphene.Int()
        resourceversion = graphene.Int()
        taxability = graphene.String()
        unbilledcharges = graphene.Int()
        updatedat = graphene.Int()

    cust = graphene.Field(Customer)
    def mutate(self, info,firstname,lastname,email,locale):
        result = create_customer(firstname,lastname,email,locale)
        customer=result.customer
        cust=Customer(id=customer.id,firstname=customer.first_name,lastname=customer.last_name,email=customer.email,locale=customer.locale)
        return CreateCustomer(cust)

class Mutations(graphene.ObjectType) :
    createSubscription = CreateSubscription.Field()
    createCustomer = CreateCustomer.Field()


class Query(graphene.ObjectType):
    subscription = graphene.Field(Subscription, plan_id=graphene.String(), auto_collection=graphene.String(), billing_address=graphene.String(), customer=graphene.String())
    #Resolver which generate response for a GraphQL query. Called by GraphQL
    def resolve_subscription(self, info, plan_id, auto_collection, billing_address, customer):
        return Subscription(plan_id = plan_id, auto_collection = auto_collection, billing_address = billing_address, customer = customer)

class Query(graphene.ObjectType):
    getsubscription = graphene.Field(Subscription, subscription_id=graphene.String())
    def resolve_getsubscription(self, info, subscription_id):
        result=getSubscriptionDetail(subscription_id)
        subscription = result.subscription
        return Subscription(id = subscription.id,
            planid = subscription.plan_id,
            planquantity = subscription.plan_quantity,
            planunitprice = subscription.plan_unit_price,
            billingperiod = subscription.billing_period,
            billingperiodunit = subscription.billing_period_unit,
            autocollection = subscription.auto_collection,
            customerid = subscription.customer_id,
            planamount = subscription.plan_amount,
            planfreequantity = subscription.plan_free_quantity,
            status = subscription.status,
            currenttermstart = subscription.current_term_start,
            currenttermend = subscription.current_term_end,
            nextbillingat = subscription.next_billing_at,
            createdat = subscription.created_at,
            startedat = subscription.started_at,
            activatedat = subscription.activated_at,
            updatedat = subscription.updated_at,
            hasscheduledchanges = subscription.has_scheduled_changes,
            resourceversion = subscription.resource_version,
            deleted = subscription.deleted,
            object = subscription.object,
            currencycode = subscription.currency_code,
            dueinvoicescount = subscription.due_invoices_count,
            mrr = subscription.mrr)

    getcustomer = graphene.Field(Customer, customer_id=graphene.String())
    def resolve_getcustomer(self, info, customer_id):
        result = getCustomerDetail(customer_id)
        customer = result.customer
        return Customer(
            allowdirectdebit=customer.allow_direct_debit,
            autocollection = customer.auto_collection,
            cardstatus = customer.card_status,
            createdat = customer.created_at,
            deleted = customer.deleted,
            email = customer.email,
            excesspayments = customer.excess_payments,
            firstname = customer.first_name,
            id = customer.id,
            lastname = customer.last_name,
            locale = customer.locale,
            nettermdays = customer.net_term_days,
            object = customer.object,
            piicleared = customer.pii_cleared,
            preferredcurrencycode = customer.preferred_currency_code,
            promotionalcredits = customer.promotional_credits,
            refundablecredits = customer.refundable_credits,
            resourceversion = customer.resource_version,
            taxability = customer.taxability,
            unbilledcharges = customer.unbilled_charges,
            updatedat = customer.updated_at,
            billingaddress = customer.billing_address
        )

def getSubscriptionDetail(subscription_id):
    result = chargebee.Subscription.retrieve(subscription_id)
    return result

def getCustomerDetail(customer_id):
    result = chargebee.Customer.retrieve(customer_id)
    return result

def create_subscription(plan_id, auto_collection, billing_address, customer):
    chargebee.configure("test_qqu3aX84uFhM2zJe0qsIoI96NPfkfBtV", "rsystems-test")
    result = chargebee.Subscription.create({
        "plan_id" : plan_id,
        "auto_collection" : "off",
        "billing_address" : {
            "first_name" : "John",
            "last_name" : "Doe",
            "line1" : "PO Box 9999",
            "city" : "Walnut",
            "state" : "California",
            "zip" : "91789",
            "country" : "US"
            },
        "customer" : {
            "first_name" : "John",
            "last_name" : "Doe",
            "email" : "john@user.com"
            }
        })
    return result

def create_customer(fname,lname,email,locale):
    result = chargebee.Customer.create({
        "first_name": fname,
        "last_name": lname,
        "email": email,
        "locale": locale,
        "billing_address" : {
        "first_name" : "Test",
        "last_name" : "Test",
        "line1" : "PO Box 9999",
        "city" : "Walnut",
        "state" : "California",
        "zip" : "91789",
        "country" : "US"
        }
    })
    return result


def list_subscription():
    entries = chargebee.Subscription.list({
        "limit": 2,
        "plan_id[in]": "['basic','no_trial']"
    })
    for entry in entries:
        subscription = entry.subscription
        customer = entry.customer
        card = entry.card

def crete_custom_field_subscription(plan_id, auto_collection, cf_gender, meta_data):
    result = chargebee.Subscription.create({
        "plan_id": "no_trial",
        "auto_collection": "off",
        "cf_gender": "Male",
        "meta_data": '{"features":{"usage-limit":"5GB","speed-within-quota":"2MBbps","post-usage-quota":"512kbps"}}'
    })
    subscription = result.subscription
    customer = result.customer
    card = result.card
    invoice = result.invoice
    unbilled_charges = result.unbilled_charges

def retrieve_subscription():
    chargebee.configure("{site_api_key}", "{site}")
    result = chargebee.Subscription.retrieve("__test__KyVnHhSBWkv9J2YH")
    subscription = result.subscription
    customer = result.customer
    card = result.card

def update_subscription():
    chargebee.configure("{site_api_key}", "{site}")
    result = chargebee.Subscription.update("__test__KyVnHhSBWkvzp2Yd", {
        "plan_id": "plan1",
        "end_of_term": True,
        "addons": [
            {
                "id": "sub_monitor",
                "quantity": 2
            },
            {
                "id": "sub_ssl"
            }]
    })
    subscription = result.subscription
    customer = result.customer
    card = result.card
    invoice = result.invoice
    unbilled_charges = result.unbilled_charges
    credit_notes = result.credit_notes


def create_addon():
    result = chargebee.Addon.create({
        "id": "sms_pack",
        "name": "Sms Pack",
        "invoice_name": "sample data pack",
        "charge_type": "recurring",
        "price": 200,
        "period": 1,
        "pricing_model": "flat_fee",
        "period_unit": "month"
    })
    addon = result.addon

def update_addon():
    result = chargebee.Addon.update("sub_reports", {
        "invoice_name": "sample data pack",
        "price": 100
    })
    addon = result.addon

def retrieve_addon():
    result = chargebee.Addon.retrieve("sub_reports")
    addon = result.addon

def list_addon():
    entries = chargebee.Addon.list({
        "limit": 3,
        "status[is]": "active"
    })
    for entry in entries:
        addon = entry.addon

def delete_addon():
    result = chargebee.Addon.delete("test")
    addon = result.addon

schema = graphene.Schema(query=Query, mutation=Mutations)
