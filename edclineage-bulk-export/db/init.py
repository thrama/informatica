import psycopg2
# Connect to your postgres DB


def create():
    conn = psycopg2.connect(
        "host=localhost dbname=edc_lineages user=postgres password=Milano2003+")

    # Open a cursor to perform database operations
    cur = conn.cursor()
  
    cur.execute("DROP TABLE IF EXISTS edc_lineages")
   
    edc_lineages = '''CREATE TABLE edc_lineages(
        id SERIAL NOT NULL PRIMARY KEY,
        downloaded INT NOT NULL,
        response_code INT NOT NULL,
        response_size CHAR(50) NOT NULL,
        response_time CHAR(50) NOT NULL,
        starting_time TIMESTAMP NOT NULL,
        ending_time TIMESTAMP NOT NULL
    )'''

    cur.execute(edc_lineages)
   

    conn.commit()

    print('databse reset')
    conn.close()


create()
