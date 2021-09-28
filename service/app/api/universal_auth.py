import os
import secrets
import pymysql

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

host = os.getenv("DB_HOST")
port = 3306
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")


conn = pymysql.connect(host, user, password, dbname)


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    cur = conn.cursor()
    cur.execute("SELECT Username, Password FROM ringier_crm.Cube WHERE Username='" + credentials.username + "'")

    cube = [field[0] for field in cur.description]
    query_results = cur.fetchone()
    row = dict(zip(cube, query_results))

    correct_username = secrets.compare_digest(credentials.username, row["Username"])
    correct_password = secrets.compare_digest(credentials.password, row["Password"])

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return correct_password + correct_username
