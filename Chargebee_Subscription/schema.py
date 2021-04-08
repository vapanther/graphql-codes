from datetime import datetime

import chargebee
import json
import graphene
import extraction
import requests
import json

from chargebee import ChargeBee

chargebee.configure("test_XLstiV7ahWpqSdxB8V8hXdNKgwFB17QB","tvunetworks-test")

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


class Addon(graphene.ObjectType):
    chargeType = graphene.String()
    enabledPortal = graphene.Boolean()
    id = graphene.String()
    invoiceName = graphene.String()
    name = graphene.String()
    object = graphene.String()
    period = graphene.Int()
    periodUnit = graphene.String()
    price = graphene.Int()
    status = graphene.String()
    taxable = graphene.Boolean()
    type = graphene.String()


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

class CardResponse(graphene.ObjectType):
    brand = graphene.String()
    expiry_month = graphene.Int()
    expiry_year = graphene.String()
    funding_type = graphene.String()
    iin = graphene.String()
    last4 = graphene.String()
    masked_number = graphene.String()
    object = graphene.String()


class BillingInfoResponse(graphene.ObjectType):
    card = graphene.Field(CardResponse)
    created_at = graphene.String()
    customer_id = graphene.String()
    deleted = graphene.Boolean()
    gateway = graphene.String()
    gateway_account_id = graphene.String()
    id = graphene.String()
    issuing_country = graphene.String()
    object = graphene.String()
    reference_id = graphene.String()
    resource_version = graphene.String()
    status = graphene.String()
    type = graphene.String()
    updated_at = graphene.String()

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

class ListPlans(graphene.ObjectType):
    list = graphene.String()

class CreateSubscriptionResponse(graphene.ObjectType):
    customer = graphene.String()
    invoice = graphene.String()
    subscription = graphene.String()

class InvoiceOneTimeChargeResponse(graphene.ObjectType):
		invoice = graphene.String()

class CreatePlanResponse(graphene.ObjectType):
    addon_applicability = graphene.String()
    charge_model = graphene.String()
    currency_code = graphene.String()
    enabled_in_hosted_pages = graphene.Boolean()
    enabled_in_portal = graphene.Boolean()
    free_quantity = graphene.Int()
    giftable = graphene.Boolean()
    id = graphene.String()
    invoice_name = graphene.String()
    is_shippable = graphene.Boolean()
    name = graphene.String()
    object = graphene.String()
    period = graphene.Int()
    period_unit = graphene.String()
    price = graphene.Int()
    pricing_model = graphene.String()
    resource_version = graphene.String()
    show_description_in_invoices = graphene.Boolean()
    show_description_in_quotes = graphene.Boolean()
    status = graphene.String()
    taxable = graphene.Boolean()
    updated_at = graphene.Date()
    Usage = graphene.String()


# Mutation Code Start
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
        subs = CreateSubscriptionResponse(customer=customer, invoice=invoice,
                                          subscription=subscription)
        return CreateSubscription(subs)


class CreateAddon(graphene.Mutation):
    class Arguments:
        chargeType = graphene.String()
        enabledPortal = graphene.Boolean()
        id = graphene.String()
        invoiceName = graphene.String()
        name = graphene.String()
        object = graphene.String()
        period = graphene.Int()
        periodUnit = graphene.String()
        price = graphene.Int()
        status = graphene.String()
        taxable = graphene.Boolean()
        type = graphene.String()

    addonvalue = graphene.Field(Addon)

    def mutate(self, info, id, name):
        result = create_Addon(id, name)
        addon = result.addon
        add_on = Addon(chargeType=addon.charge_type, enabledPortal=addon.enabled_in_portal, id=addon.id,
                       invoiceName=addon.invoice_name, name=addon.name, object=addon.object, period=addon.period,
                       periodUnit=addon.period_unit, price=addon.price, status=addon.status, taxable=addon.taxable,
                       type=addon.type)
        return CreateAddon(add_on)


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

    def mutate(self, info, firstname, lastname, email, locale):
        result = create_customer(firstname, lastname, email, locale)
        customer = result.customer
        cust = Customer(id=customer.id, firstname=customer.first_name, lastname=customer.last_name,
                        email=customer.email, locale=customer.locale)
        return CreateCustomer(cust)


class CreatePlan(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        name = graphene.String()
        invoice_name = graphene.String()
        price = graphene.Int()

    plan_details = graphene.Field(CreatePlanResponse)

    def mutate(self, info, id, name, invoice_name, price):
        result = create_plan(id, name, invoice_name, price)
        plan = result.plan
        dt_object = datetime.fromtimestamp(plan.updated_at)
        plan_response = CreatePlanResponse(addon_applicability=plan.addon_applicability, charge_model=plan.charge_model,
                                           currency_code=plan.currency_code,Usage=plan.cf_usage,
                                           enabled_in_hosted_pages=plan.enabled_in_hosted_pages,
                                           enabled_in_portal=plan.enabled_in_portal, free_quantity=plan.free_quantity,
                                           giftable=plan.giftable, id=plan.id, invoice_name=plan.invoice_name,
                                           is_shippable=plan.is_shippable, name=plan.name, object=plan.object,
                                           period=plan.period, period_unit=plan.period_unit, price=plan.price,
                                           pricing_model=plan.pricing_model, resource_version=plan.resource_version,
                                           show_description_in_invoices=plan.show_description_in_invoices,
                                           show_description_in_quotes=plan.show_description_in_quotes,
                                           status=plan.status, taxable=plan.taxable, updated_at=dt_object)
        return CreatePlan(plan_response)


class CreateSubscriptionWithCustomFields(graphene.Mutation):
    class Arguments:
        plan_id = graphene.String(required=True)
        auto_collection = graphene.String()
        cf_gender = graphene.String()
        meta_data = graphene.String()

    subs = graphene.Field(Subscription)

    def mutate(self, info, plan_id, auto_collection, cf_gender, meta_data):
        return CreateSubscriptionWithCustomFields(plan_id=plan_id, auto_collection=auto_collection,
                                                  cf_gender=cf_gender, meta_data=meta_data)


def create_customer(fname, lname, email, locale):
    result = chargebee.Customer.create({
        "first_name": fname,
        "last_name": lname,
        "email": email,
        "locale": locale,
        "billing_address": {
            "first_name": "Test",
            "last_name": "Test",
            "line1": "PO Box 9999",
            "city": "Walnut",
            "state": "California",
            "zip": "91789",
            "country": "US"
        }
    })
    return result

class CreateInvoiceOneTimeCharge(graphene.Mutation):
    class Arguments:
        subscription_id = graphene.String()
        amount = graphene.Int()
        description = graphene.String()

    invoice_data = graphene.Field(InvoiceOneTimeChargeResponse)
    def mutate(self, info, subscription_id, amount, description):
        result = create_invoice_one_time_charge(subscription_id, amount, description)
        invoice = InvoiceOneTimeChargeResponse(invoice=result.invoice)
        return CreateInvoiceOneTimeCharge(invoice)

class Query(graphene.ObjectType):
    # Query to get Subscription
    getsubscription = graphene.Field(Subscription, subscription_id=graphene.String())
    def resolve_getsubscription(self, info, subscription_id):
        result = getSubscriptionData(subscription_id)
        subscription = result.subscription
        customer = result.customer
        return Subscription(id=subscription.id,
                            planid=subscription.plan_id,
                            planquantity=subscription.plan_quantity,
                            planunitprice=subscription.plan_unit_price,
                            billingperiod=subscription.billing_period,
                            billingperiodunit=subscription.billing_period_unit,
                            autocollection=subscription.auto_collection,
                            customerid=subscription.customer_id,
                            planamount=subscription.plan_amount,
                            planfreequantity=subscription.plan_free_quantity,
                            status=subscription.status,
                            currenttermstart=subscription.current_term_start,
                            currenttermend=subscription.current_term_end,
                            nextbillingat=subscription.next_billing_at,
                            createdat=subscription.created_at,
                            startedat=subscription.started_at,
                            activatedat=subscription.activated_at,
                            updatedat=subscription.updated_at,
                            hasscheduledchanges=subscription.has_scheduled_changes,
                            resourceversion=subscription.resource_version,
                            deleted=subscription.deleted,
                            object=subscription.object,
                            currencycode=subscription.currency_code,
                            dueinvoicescount=subscription.due_invoices_count,
                            mrr=subscription.mrr
                            )

    getaddon = graphene.Field(Addon, addon_id=graphene.String())
    def resolve_getaddon(self, info, addon_id):
        result = getAddonDetail(addon_id)
        addon = result.addon
        return Addon(
            chargeType=addon.charge_type,
            enabledPortal=addon.enabled_in_portal,
            id=addon.id,
            invoiceName=addon.invoice_name,
            name=addon.name,
            object=addon.object,
            period=addon.period,
            periodUnit=addon.period_unit,
            price=addon.price,
            status=addon.status,
            taxable=addon.taxable,
            type=addon.type
        )

    # Query to get Plan List
    get_plan_list = graphene.Field(ListPlans, limit=graphene.Int(), status=graphene.String())
    def resolve_get_plan_list(self, info, limit, status):
        result = list_plans(limit, status)
        return ListPlans(list=result.response)

    getcustomer = graphene.Field(Customer, customer_id=graphene.String())
    def resolve_getcustomer(self, info, customer_id):
        result = getCustomerDetail(customer_id)
        customer = result.customer
        return Customer(
            allowdirectdebit=customer.allow_direct_debit,
            autocollection=customer.auto_collection,
            cardstatus=customer.card_status,
            createdat=customer.created_at,
            deleted=customer.deleted,
            email=customer.email,
            excesspayments=customer.excess_payments,
            firstname=customer.first_name,
            id=customer.id,
            lastname=customer.last_name,
            locale=customer.locale,
            nettermdays=customer.net_term_days,
            object=customer.object,
            piicleared=customer.pii_cleared,
            preferredcurrencycode=customer.preferred_currency_code,
            promotionalcredits=customer.promotional_credits,
            refundablecredits=customer.refundable_credits,
            resourceversion=customer.resource_version,
            taxability=customer.taxability,
            unbilledcharges=customer.unbilled_charges,
            updatedat=customer.updated_at,
            billingaddress=customer.billing_address
        )

    get_billing_info = graphene.Field(BillingInfoResponse, cust_payment_source_id=graphene.String())
    def resolve_get_billing_info(self, info, cust_payment_source_id):
        payment_source = billing_information(cust_payment_source_id)
        return BillingInfoResponse(
            card=payment_source.card,
            created_at=payment_source.created_at,
            customer_id=payment_source.customer_id,
            deleted=payment_source.deleted,
            gateway=payment_source.gateway,
            gateway_account_id=payment_source.gateway_account_id,
            id=payment_source.id,
            issuing_country=payment_source.issuing_country,
            object=payment_source.object,
            reference_id=payment_source.reference_id,
            resource_version=payment_source.resource_version,
            status=payment_source.status,
            type=payment_source.type,
            updated_at=payment_source.updated_at

        )


def getSubscriptionData(subscription_id):
    result = chargebee.Subscription.retrieve(subscription_id)
    subscription = result.subscription
    customer = result.customer
    card = result.card
    print(subscription.id)
    return result


def create_subscription(plan_id, auto_collection, billing_address, customer):
    result = chargebee.Subscription.create({
        "plan_id": plan_id,
        "auto_collection": "off",
        "billing_address": {
            "first_name": "John",
            "last_name": "Doe",
            "line1": "PO Box 9999",
            "city": "Walnut",
            "state": "California",
            "zip": "91789",
            "country": "US"
        },
        "customer": {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@user.com"
        }
    })
    return result


def create_plan(id, name, invoice_name, price):
    result = chargebee.Plan.create({
        "id": id,
        "name": name,
        "invoice_name": invoice_name,
        "price": price
    })
    return result


def getCustomerDetail(customer_id):
    result = chargebee.Customer.retrieve(customer_id)
    return result

def billing_information(cust_payment_source_id):
    result = chargebee.PaymentSource.retrieve(cust_payment_source_id)
    payment_source = result.payment_source
    return payment_source

def list_plans(limit, status):
    entries = chargebee.Plan.list({
        "limit": limit,
        "status[is]": status
    })
    return entries


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

def create_invoice_one_time_charge(subscription_id, amount, description):
    #chargebee.configure("test_XLstiV7ahWpqSdxB8V8hXdNKgwFB17QB", "tvunetworks-test")
    result = chargebee.Invoice.charge({
        "subscription_id": subscription_id,
        "amount": amount,
        "description": description
    })
    return result

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


def create_Addon(id, name):
    result = chargebee.Addon.create({
        "id": id,
        "name": name,
        "invoice_name": "sample data pack",
        "charge_type": "recurring",
        "price": 200,
        "period": 1,
        "pricing_model": "flat_fee",
        "period_unit": "month"
    })
    return result


def getAddonDetail(id):
    result = chargebee.Addon.retrieve(id)
    return result


class Mutations(graphene.ObjectType):
    createSubscription = CreateSubscription.Field()
    ceratePlan = CreatePlan.Field()
    createCustomer = CreateCustomer.Field()
    createAddon = CreateAddon.Field()
    invoiceOneTimeCharge = CreateInvoiceOneTimeCharge.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)





