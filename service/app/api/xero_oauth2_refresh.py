import requests

from xero.auth import OAuth2Credentials

from service.app.api.auth import conn

try:
    cur = conn.cursor()
    cur.execute("SELECT * FROM Xero")

    orgs = []
    for i in range(len(cur.description)):
        orgs.append(i)

    query_results = cur.fetchall()

    row = dict(zip(orgs, query_results))
    p = -1
    for org in row:
        p = p + 1

        clnt_d = row[p][1]
        clnt_scrt = row[p][2]
        refresh_token = row[p][3]
        tnnt_d = row[p][4]

        cred = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": clnt_d,
            "client_secret": clnt_scrt
        }

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
        print(ttkn)

except Exception as e:
    print("Database connection failed due to {}".format(e))
