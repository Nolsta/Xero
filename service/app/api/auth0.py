import json
import os

import pymysql
import redis
import requests
from fastapi import APIRouter
from fastapi.security import HTTPBasic
from xero.auth import OAuth2Credentials

from service.app.api.models import Organisation
from service.app.api.universal_auth import conn

security = HTTPBasic()

xAuth = APIRouter()

# host = os.getenv("XERO_DB_HOST")
# port = 5439
# dbname = os.getenv("XERO_DB_NAME")
# user = os.getenv("XERO_DB_USERNAME")
# password = os.getenv("XERO_DB_PASSWORD")


host = os.getenv("DB_HOST")
port = 3306
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")


# Redis connection
# r = redis.Redis(host='localhost', db=1, port=6379)


# Gets the refresh token from the database
# Receives the organisation value from the authentication method
# gets the refresh token and credentials from the cache storage

# def get_refresh_token_from_cache(org: Organisation):
#     try:
#         _token = r.hgetall(org)
#         # converts the cache results from byte to string
#         rfrsh_tkn = _token[b'refresh_token'].decode("UTF-8")
#         clnt_d = _token[b'client_id'].decode("UTF-8")
#         clnt_scrt = _token[b'client_secret'].decode("UTF-8")
#         tnnt_d = _token[b'tenant_id'].decode("UTF-8")
#
#         token = {
#             "refresh_token": rfrsh_tkn,
#             "client_id": clnt_d,
#             "client_secret": clnt_scrt,
#             "tenant_id": tnnt_d
#         }
#         return token
#     except Exception as e:
#         print("Was not able to return results".format(e))
#         return {}


# retrieves the refresh token and user credentials from the database
def get_refresh_token_from_db(org):
    global query_results, stud_json

    conn0 = pymysql.connect(host, user, password, dbname)
    try:
        # Gets the refresh token and credentials from a db table
        cur = conn0.cursor()
        cur.execute("SELECT * FROM ringier_crm.Xero WHERE config_id='" + org + "'")

        # Arranges the results of the query into json format

        # Gets the column names returned by the query
        clients = [field[0] for field in cur.description]
        # fetches a single row from the query results
        query_results = cur.fetchone()
        # combines the column names and query results into 1 dict
        row = dict(zip(clients, query_results))
        conn0.close()

        # print("test1")
        # r2 = str(query_results)
        # print(query_results)
        # ds2 = {key: row[key] for key in clients}

        # Sends the results of the query to the cache database
        name = query_results[1]


        # rrr=json.dumps(row).encode('utf-8')
        # writes the method results into the cache
        # r.mset(name, query_results)
        # print(" test 2")


        return row
        # print("Hello1")

    except Exception as e:
        print("Database action failed due to {}".format(e))
        return e


# # If the cache results are empty, get the results from the DB
# def refresh_token_formatting(org: Organisation):
#     _token = get_refresh_token_from_cache(org=org)
#
#     t1 = not bool(_token)
#
#     if t1 == False:
#         _token
#     else:
#         _token = get_refresh_token_from_db(org=org)
#     return _token


# def check_token_expiry():

# Gets the organisation value from the xero method run
# Authenticates each method
# The method that actually gets the access token
def authentication(org):
    try:
        #Runs the method to get refresh token from db
        _token = get_refresh_token_from_db(org)
    except Exception  as e:
        return _token
    if _token != "'NoneType' object is not iterable":
        try:
            rfrsh_tkn = _token['refresh_token']
            clnt_d = _token['client_id']
            clnt_scrt = _token['client_secret']
            tnnt_d = _token['tenant_id']
        except Exception as e:
            return "Could not find matching records for this organisation."
    else:
        return "Could not find matching records for this organisation."


    try:
        #assign values to 0auth credentials
        cred = {
            "grant_type": "refresh_token",
            "refresh_token": rfrsh_tkn,
            "client_id": clnt_d,
            "client_secret": clnt_scrt
        }
        # XERO Link to get access token
        response = requests.post('https://identity.xero.com/connect/token', cred)
        token = response.json()
        print(token)

        # PyXero defined credentials used for authentication
        credentials = OAuth2Credentials(client_id=clnt_d,
                                        client_secret=clnt_scrt,
                                        callback_uri="http://localhost:5000/callback",
                                        tenant_id=tnnt_d, token=token)
        credentials.set_default_tenant()

        # ttkn = token["refresh_token"]
        # print(ttkn)

        #Create DB connection
        conn = pymysql.connect(host, user, password, dbname)

        cur = conn.cursor()
        cur.execute("UPDATE ringier_crm.Xero SET refresh_token='" + ttkn + "' WHERE client_id='" + clnt_d + "'")
        conn.commit()
        # Update the cache with new refresh_token
        new_dict = {
            "client_id": clnt_d,
            "client_secret": clnt_scrt,
            "tenant_id": tnnt_d,
            "refresh_token": ttkn
        }

        # r.expire(org, 1800)
        # r.hmset(clnt_d, new_dict)

        return credentials

    except Exception as e:
        print("Authentication failed due to {}".format(e))


# authentication('21ea5c49-e3de-48ed-90a8-90495030cf4d1')

# conn0 = pymysql.connect(host, user=user, port=port,
#                         passwd=password, db=dbname)
#
# cur = conn0.cursor()
# cur.execute("UPDATE ringier_crm.Xero SET refresh_token='" + ttkn + "' WHERE client_id='" + clnt_d + "'")
# conn0.commit()
# conn0.close()
#     # scope = "openid profile email accounting.contacts accounting.settings "
#     # redirect_Uri =
#     # state = "123"
#     # url="https://login.xero.com/identity/connect/authorize?response_type=code&client_id=YOURCLIENTID&redirect_uri=YOURREDIRECTURI&scope=openid profile email accounting.transactions&state=123"
#
#
# #Uses the authentication links declared by Xero to get codes
#         else:
#             try:
#                 rfrsh_tkn = _token['refresh_token']
#                 clnt_d = _token['client_id']
#                 clnt_scrt = _token['client_secret']
#                 tnnt_d = _token['tenant_id']
#
#                 print(rfrsh_tkn, clnt_d, clnt_scrt, tnnt_d)
#
#                 cred = {
#                     "grant_type": "refresh_token",
#                     "refresh_token": rfrsh_tkn,
#                     "client_id": clnt_d,
#                     "client_secret": clnt_scrt
#                 }
#                 response = requests.post('https://identity.xero.com/connect/token', cred)
#                 token = response.json()
#                 print(token)
#
#                 credentials = OAuth2Credentials(client_id=clnt_d,
#                                         client_secret=clnt_scrt,
#                                         callback_uri="http://localhost:5000/callback",
#                                         tenant_id=tnnt_d, token=token)
#                 credentials.set_default_tenant()
#
#                 ttkn = token["refresh_token"]
#                 print(ttkn)
#                 conn0 = pymysql.connect(host, user=user, port=port,
#                                     passwd=password, db=dbname)
#
#                 cur = conn0.cursor()
#                 cur.execute("UPDATE ringier_crm.Xero SET refresh_token='" + ttkn + "' WHERE client_id='" + clnt_d + "'")
#                 conn0.commit()
#                 conn0.close()
#                 return credentials
#
#             except Exception as e:
#                 print("Authentication failed due to {}".format(e))
#                 return e


# host = os.getenv("DB_HOST")
# port = 3306
# dbname = os.getenv("DB_NAME")
# user = os.getenv("DB_USERNAME")
# password = os.getenv("DB_PASSWORD")
# host = os.environ["DB_HOST"]
# port = 3306
# dbname = os.environ["DB_NAME"]
# user = os.environ["DB_USERNAME"]
# password = os.environ["DB_PASSWORD"]


# conn = pymysql.connect(host, user=user, port=port,
#                        passwd=password, db=dbname)


# def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
#     cur = conn.cursor()
#     cur.execute("SELECT Username, Password FROM ringier_crm.Cube WHERE Username='" + credentials.username + "'")
#
#     cube = [field[0] for field in cur.description]
#     query_results = cur.fetchone()
#     row = dict(zip(cube, query_results))
#
#     correct_username = secrets.compare_digest(credentials.username, row["Username"])
#     correct_password = secrets.compare_digest(credentials.password, row["Password"])
#
#     if not (correct_username and correct_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return correct_password + correct_username
