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
        raise SystemExit

    # Create cursor and try to execute given query
    # and return fetched data
    cur = conn.cursor()
    try:
        cur.execute(query)
    except psycopg2.Error as e:
        print(e)
        conn.close()
    else:
        return cur.fetchall()
        cur.close()
        conn.close()


# Output results of query for the most popular articles of all time
q1 = db_query('select * from view_select_popular_articles',
              'news', 'vagrant')

print('\nMost popular articles of all time:\n')
for entry in q1:
    print('{} - {} views'.format(entry[0], entry[1]))


# Output results of query for most popular authors of all time
q2 = db_query('select * from view_select_popular_authors',
              'news', 'vagrant')

print('\nMost popular authors of all time:\n')
for entry in q2:
    print('{} - {} views'.format(entry[0], entry[1]))


# Output results of query for days with error % greather than 1
q3 = db_query('select * from view_select_error_percent',
              'news', 'vagrant')

print('\nDays with error count over 1%:\n')
for entry in q3:
    print('{} - {}%'.format(entry[0], entry[1]))
