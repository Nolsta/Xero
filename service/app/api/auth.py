import requests

from fastapi import APIRouter
from fastapi.security import HTTPBasic
from xero.auth import OAuth2Credentials
from service.app.api.universal_auth import conn
from service.app.api.models import Organisation

security = HTTPBasic()
xAuth = APIRouter()

def get_refresh_token_from_db(org: Organisation):
    global query_results, stud_json

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Xero WHERE client_id='" + org + "'")

        clients = [field[0] for field in cur.description]

        query_results = cur.fetchone()

        row = dict(zip(clients, query_results))

        return row

    except Exception as e:
        print("Database connection failed due to {}".format(e))


def authentication(org: Organisation):
    _token = get_refresh_token_from_db(org=org)
    rfrsh_tkn = _token["refresh_token"]
    clnt_d = _token["client_id"]
    clnt_scrt = _token["client_secret"]
    tnnt_d = _token["tenant_id"]

    cred = {
        "grant_type": "refresh_token",
        "refresh_token": rfrsh_tkn,
        "client_id": clnt_d,
        "client_secret": clnt_scrt
    }

    try:
        response = requests.post('https://identity.xero.com/connect/token', cred)
        token = response.json()

        credentials = OAuth2Credentials(client_id=clnt_d,
                                    client_secret=clnt_scrt,
                                    callback_uri="http://localhost/callback",
                                    tenant_id=tnnt_d, token=token)
        credentials.set_default_tenant()

        ttkn = token["refresh_token"]

        cur = conn.cursor()
        cur.execute("UPDATE ringier_crm.Xero SET refresh_token='" + ttkn + "' WHERE client_id='" + clnt_d + "'")
        conn.commit()

        return credentials

    except Exception as e:
        print("Authentication failed due to {}".format(e))


