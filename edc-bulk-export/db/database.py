import psycopg2
from props.paramsEdc import db_url

# Insert all_resources data into database
def all_edc(resource_name, resource_type, downloaded, response_code, response_size, response_time, starting_time, ending_time):
    conn = psycopg2.connect(db_url)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    query = ''' INSERT INTO all_edc (resource_name,resource_type,downloaded, response_code, response_size,response_time,starting_time,ending_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;'''
    datas = (resource_name, resource_type, downloaded, int(response_code), response_size,
             response_time, starting_time, ending_time)
    cur.execute(query, datas)

    
    conn.commit()