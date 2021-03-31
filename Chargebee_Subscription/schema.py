"""
GraphQL schema for extracting results from a website.
"""
import graphene
import extraction
import requests
import chargebee
import json

class Company(graphene.ObjectType):
    name = graphene.String()
    address = graphene.String()
    detail =graphene.String()
    id = graphene.String()
    pincode= graphene.String()

class Subscription(graphene.ObjectType):
    id = graphene.String()
    planid = graphene.String()
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

#Mutation Code Start

#Mutation Code End
    
class Query(graphene.ObjectType):
    getsubscription = graphene.Field(Subscription, subsid=graphene.String())
    # Resolver which generate response for a GraphQL query. Called by GraphQL
    def resolve_getsubscription(self, info, subsid):
        result=getValue(subsid)
        subscription = result.subscription
        customer = result.customer
        return Subscription(
            planid=subscription.plan_id,
            currencycode=subscription.currency_code,
            customerid=subscription.customer_id,
            id=subscription.id
        )

def getValue(subsid):
    chargebee.configure("test_qqu3aX84uFhM2zJe0qsIoI96NPfkfBtV","rsystems-test")
    result = chargebee.Subscription.retrieve(subsid)
    subscription = result.subscription
    customer = result.customer
    card = result.card
    print(subscription.id)
    return result

schema = graphene.Schema(query=Query)
#schema = graphene.Schema(query=Query, mutation=Mutations)
