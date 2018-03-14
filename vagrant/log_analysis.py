import psycopg2


def db_query(query, db_name, user):
    """
    Connects to the given DB and runs the given query.

    Arguments:
        -query: string, required: the query (or view) to be requested
        -db_name: string, required: the database that will be connected to
        -user: string, required: username to be used when logging into DB
    Returns:
        -unmodified data structure received from psycopg2 library
    """

    # Attempt connection to DB with given parameters
    try:
        conn = psycopg2.connect(dbname=db_name, user=user)
    except psycopg2.Error as e:
        print(e)
        conn.close()
        raise SystemExit

    # Create cursor and try to execute given query
    cur = conn.cursor()
    try:
        cur.execute(query)
    except psycopg2.Error as e:
        print(e)
        conn.close()


#db_query('select * from authors;', 'news', 'vagrant')
