#!/usr/bin/env python3
"""
Test psycopg with CockroachDB.
"""

import time
import random
import logging
from argparse import ArgumentParser, RawTextHelpFormatter
import uuid

import psycopg2
from psycopg2.errors import SerializationFailure





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

def add_user(conn, name, uuid, school, email, password, role, rep, classes):
    with conn.cursor() as cur:
        command = "UPSERT INTO users (id, name, school, email, password, role, rep, classes) VALUES ('" + uuid + "', '" + name + "', '" + school + "', '" + email + "', '" + password + "', '" + role + "', '" + rep + "', '" + classes + "')"
        cur.execute(command)
    conn.commit()

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, name TEXT, school TEXT, email TEXT, password TEXT, role TEXT, rep INT, classes TEXT)"
        )
    conn.commit()

def pull_names(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM users")
        logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        #print(f"names at {time.asctime()}:")
        names = []
        for row in rows:
            names.append(row[1])
        return names

"""
def main():
    conn = psycopg2.connect("postgresql://keshavbabu:IsoON0LSvLsJTznlliHVZw@free-tier11.gcp-us-east1.cockroachlabs.cloud:26257/users?sslmode=verify-full&options=--cluster%3Dfading-serpent-461")
    create_table(conn)
    add_user(conn, "keshav", "0", "MSU", "babukesh@msu.edu", "password", "student", "0", "CSE232-MTH235")
    add_user(conn, "bob", "1", "MSU", "bob@msu.edu", "password", "student", "0", "WRA101")
    print(pull_names(conn))
    conn.close()



if __name__ == "__main__":
    main()
"""