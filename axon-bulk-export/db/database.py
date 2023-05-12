import psycopg2
from props.paramsAxon import db_url


# Insert axon data into database
def axon_facets(facet_name, response_code, response_size, response_time, downloaded, starting_time, ending_time):
    conn = psycopg2.connect(db_url)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    query = ''' INSERT INTO axon_facets (facet_name, response_code, response_size,response_time,downloaded,starting_time,ending_time) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id;'''
    datas = (facet_name, int(response_code), response_size,
             response_time, downloaded, starting_time, ending_time)
    cur.execute(query, datas)

    conn.commit()

# Insert axon relations data into database


def axon_with_relations(facet_name, response_code, response_size, response_time, downloaded, starting_time, ending_time):
    conn = psycopg2.connect(db_url)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    query = ''' INSERT INTO axon_with_relations (facet_name, response_code, response_size,response_time,downloaded,starting_time,ending_time) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id;'''
    datas = (facet_name, int(response_code), response_size,
             response_time, downloaded, starting_time, ending_time)
    cur.execute(query, datas)

    conn.commit()

# Insert general runtime for full script data into database


def dbGeneral(last_update, updated_axon_quantity, updated_edc_quantity, run_time):
    conn = psycopg2.connect(db_url)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    query = ''' INSERT INTO general_data (last_update, updated_axon_quantity, updated_edc_quantity, run_time) VALUES (%s, %s, %s, %s);'''
    datas = (last_update, updated_axon_quantity,
             updated_edc_quantity, run_time)

    cur.execute(query, datas)

    conn.commit()


    conn.close()

# Insert first run server data into database


def dbServer(created_at, response_code):
    conn = psycopg2.connect(db_url)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    query = ''' INSERT INTO server_data (created_at, response_code) VALUES (%s, %s);'''
    datas = (created_at, response_code)

    cur.execute(query, datas)

    conn.commit()


    conn.close()
