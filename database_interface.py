#!/usr/bin/env python3
"""
Test psycopg with CockroachDB.
"""

# curl --create-dirs -o $HOME/.postgresql/root.crt -O https://cockroachlabs.cloud/clusters/994be2c3-81d2-4c2d-bc37-05fd579317e7/cert

import time
import random
import logging
from argparse import ArgumentParser, RawTextHelpFormatter
import uuid

import psycopg2
from psycopg2.errors import SerializationFailure

import json



'''
def delete_accounts(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM bank.accounts")
        logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
            

def print_balances(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, balance FROM accounts")
        logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        print(f"Balances at {time.asctime()}:")
        for row in rows:
            print(row)


def transfer_funds(conn, frm, to, amount):
    with conn.cursor() as cur:

        # Check the current balance.
        cur.execute("SELECT balance FROM accounts WHERE id = %s", (frm,))
        from_balance = cur.fetchone()[0]
        if from_balance < amount:
            raise RuntimeError(
                f"Insufficient funds in {frm}: have {from_balance}, need {amount}"
            )

        # Perform the transfer.
        cur.execute(
            "UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, frm)
        )
        cur.execute(
            "UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, to)
        )

    conn.commit()
    logging.debug("transfer_funds(): status message: %s", cur.statusmessage)


def run_transaction(conn, op, max_retries=3):
    """
    Execute the operation *op(conn)* retrying serialization failure.

    If the database returns an error asking to retry the transaction, retry it
    *max_retries* times before giving up (and propagate it).
    """
    # leaving this block the transaction will commit or rollback
    # (if leaving with an exception)
    with conn:
        for retry in range(1, max_retries + 1):
            try:
                op(conn)

                # If we reach this point, we were able to commit, so we break
                # from the retry loop.
                return

            except SerializationFailure as e:
                # This is a retry error, so we roll back the current
                # transaction and sleep for a bit before retrying. The
                # sleep time increases for each failed transaction.
                logging.debug("got error: %s", e)
                conn.rollback()
                logging.debug("EXECUTE SERIALIZATION_FAILURE BRANCH")
                sleep_ms = (2 ** retry) * 0.1 * (random.random() + 0.5)
                logging.debug("Sleeping %s seconds", sleep_ms)
                time.sleep(sleep_ms)

            except psycopg2.Error as e:
                logging.debug("got error: %s", e)
                logging.debug("EXECUTE NON-SERIALIZATION_FAILURE BRANCH")
                raise e

        raise ValueError(f"Transaction did not succeed after {max_retries} retries")


def test_retry_loop(conn):
    """
    Cause a seralization error in the connection.

    This function can be used to test retry logic.
    """
    with conn.cursor() as cur:
        # The first statement in a transaction can be retried transparently on
        # the server, so we need to add a dummy statement so that our
        # force_retry() statement isn't the first one.
        cur.execute("SELECT now()")
        cur.execute("SELECT crdb_internal.force_retry('1s'::INTERVAL)")
    logging.debug("test_retry_loop(): status message: %s", cur.statusmessage)
'''

def add_user(name, uuid, school, email, password, role, classes):
    conn = returnConn()
    with conn.cursor() as cur:
        command = "UPSERT INTO users (id, name, school, email, password, role, classes, scores, exp) VALUES ('" + uuid + "', '" + name + "', '" + school + "', '" + email + "', '" + password + "', '" + role + "', '" + classes + "', '"+ str(0) + "', '"+ str(0) +"')"
        cur.execute(command)
    conn.commit()
    conn.close()

def create_table():
    conn = returnConn()
    with conn.cursor() as cur:
        cur.execute(
<<<<<<< Updated upstream
            "CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, name TEXT, school TEXT, email TEXT, password TEXT, role TEXT, rep INT, classes TEXT)"
=======
            "CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, name TEXT, school TEXT, email TEXT, password TEXT, role TEXT, classes TEXT, scores TEXT, exp INT)"
>>>>>>> Stashed changes
        )
    conn.commit()
    conn.close()

def pull_names():
    conn = returnConn()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        #print(rows)
        conn.commit()
        #print(f"names at {time.asctime()}:")
        items = []
        for row in rows:
            items.append(row)
            #print(row)
        conn.close()
        return items

def returnConn():
    conn = psycopg2.connect("postgresql://keshavbabu:IsoON0LSvLsJTznlliHVZw@free-tier11.gcp-us-east1.cockroachlabs.cloud:26257/users?sslmode=verify-full&options=--cluster%3Dfading-serpent-461")
    return conn

def isIDAvalible(idm):
<<<<<<< Updated upstream
=======
    conn = returnConn()
    with conn.cursor() as cur:
        cmd = "SELECT * FROM users WHERE id = "+str(idm)
        cur.execute(cmd)
        output = cur.fetchall()
        conn.commit()
        conn.close()
        return not output

def getTutorsWithForm(form_data):
    classs = form_data.getlist("class")[0]
    conn = returnConn()
    with conn.cursor() as cur:
        cmd = "SELECT * FROM users WHERE role = 'Tutor' AND classes LIKE '%" + classs + "%'"
        cur.execute(cmd)
        rows = cur.fetchall()
        conn.commit()
        items = []
        for row in rows:
            items.append(row)
        conn.close()
        return items

def createReview(form_data):
    rating = form_data.getlist("rating")[0]
    name = form_data.getlist("tutor")[0]
    scores = getScores(name)+"-"+str(rating)
    exp = int(getExp(name)) + 5
    conn = returnConn()
    with conn.cursor() as cur:
        command = "UPDATE users set scores='"+scores+"', exp='"+str(exp)+"' WHERE name='"+name+"';"
        cur.execute(command)
    conn.commit()
    conn.close()

def getExp(name):
>>>>>>> Stashed changes
    conn = returnConn()
    with conn.cursor() as cur:
        cmd = "SELECT exp FROM users WHERE name = '"+name+"'"
        cur.execute(cmd)
        scores = cur.fetchall()
        conn.commit()
        conn.close()
        items = []
        value = {
            "scores": scores
        }
        items.append(json.dumps(value))
        return json.loads(items[0]).get("scores")[0][0]

def getScores(name):
    conn = returnConn()
    with conn.cursor() as cur:
        cmd = "SELECT scores FROM users WHERE name = '"+name+"'"
        cur.execute(cmd)
        scores = cur.fetchall()
        conn.commit()
        conn.close()
        items = []
        value = {
            "scores": scores
        }
        items.append(json.dumps(value))
        return json.loads(items[0]).get("scores")[0][0]

def getTutors():
    conn = returnConn()
    with conn.cursor() as cur:
        cmd = "SELECT * FROM users WHERE role = 'Tutor'"
        cur.execute(cmd)
        rows = cur.fetchall()
        conn.commit()
        items = []
        for row in rows:
            items.append(row)
        conn.close()
        return items

def createUser(form_data):
    school = form_data.getlist("school")[0]
    name = form_data.getlist("name")[0]
    role = form_data.getlist("role")[0]
    classes = form_data.getlist("classes")[0]
    email = form_data.getlist("email")[0]
    uuid = 0
    while(not isIDAvalible(str(uuid))):
        uuid += 1
    uuid = str(uuid)
    add_user(name, uuid, school, email, "password", role, classes)
    
def testDB():
    conn = returnConn()
    print(pull_names())
    conn.close()

def main():
    conn = returnConn()
    #print(getTutors("CSE232"))
    create_table()
    '''
    add_user("keshav", "0", "MSU", "keshavjbabu@gmail.com", "password", "student", "0", "CSE232-MTH235")
    add_user("bob", "1", "MSU", "bob@msu.edu", "password", "student", "0", "WRA101")
    print(pull_names())
    '''
    #print(pull_names())
    conn.close()



if __name__ == "__main__":
    main()
