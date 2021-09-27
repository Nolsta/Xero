from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from xero import Xero

from service.app.api.auth0 import authentication
from service.app.api.universal_auth import get_current_username
from service.app.api.models import Organisation, Invoices, Invoice, CCube

xMethods = APIRouter()

security = HTTPBasic()


@xMethods.post('/')
async def print_Hello_World():
    print("This is a xero service developed by Ringier SA.")
    return "This is a xero service developed by Ringier SA."


# @xMethods.get('/contacts')
# async def add_contacts(org: Organisation, credentials: HTTPBasicCredentials = Depends(security)):
#     get_current_username(credentials=credentials)
#     xero = authentication(payload=org)
#     xeero = Xero(xero)
#     return (xeero.contacts.all())
#
#
# @xMethods.get('/invoices')
# async def get_invoices(org: Organisation, credentials: HTTPBasicCredentials = Depends(security)):
#     get_current_username(credentials=credentials)
#     xero = authentication(payload=org)
#     xeero = Xero(xero)
#     return (xeero.invoices.all())


@xMethods.post('/invoices')
async def create_invoice(payload: CCube, credentials: HTTPBasicCredentials = Depends(security)):#, authx: Ringier):
    # print(payload)
    #gets the venture config ID from the payload
    sc1 = payload.venture_config_id

    # sc2 = sc1["config"]
    # sc3 = sc1["organisation"]
    try:
        #Authenticates bus using basic auth
        get_current_username(credentials=credentials)
        # Xero oauth authenticating current user
        # Returns the tokens
        xero = authentication(sc1)
        #Uses tokens returned by authentication method
        xeero = Xero(xero)
        # return xero

    except Exception as e:
        return "Could not authenticate user due to ".format(e),xero

    #Gets the invoice values from the bus payload
    p1 = payload.payload
    p2 = p1["invoice"]

    #assigns invoice values
    c = {
        "Type": p2["type"],
        "Contact": p2["contact"],
        "LineAmountTypes": p2["line_amount_types"],
        "LineItems": [p2["line_items"]]
    }

    # print(p2["line_items"])
    # xeero.invoices.put(c)
    # return (xeero.invoices.all()), payload
    try:
        xeero.invoices.put(c)
        return "Invoice created."
    except Exception as e:
        return "Could not create invoice due to ".format(e)
    finally:
        print(p2["line_items"])



# @xMethods.put('/invoices')
# def update_invoice(inv: Invoice, org: Organisation, credentials: HTTPBasicCredentials = Depends(security)):#, authx: Ringier):
#     get_current_username(credentials=credentials)
#     xero = authentication(payload=org)
#     xeero = Xero(xero)
#
#     u = xeero.invoices.get(inv.InvoiceID)

