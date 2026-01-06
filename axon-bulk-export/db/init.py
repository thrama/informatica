import psycopg2

# Connect to your postgres DB


def create():
    conn = psycopg2.connect("host=localhost dbname=python-test user=postgres password=ChangeMe123!")

    # Open a cursor to perform database operations
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS axon_facets")
    cur.execute("DROP TABLE IF EXISTS axon_with_relations")
    cur.execute("DROP TABLE IF EXISTS general_data")
    cur.execute("DROP TABLE IF EXISTS server_data")

    # axon table without relations
    axon_facets = """CREATE TABLE axon_facets(
        id SERIAL NOT NULL PRIMARY KEY,
        facet_name CHAR(150) NOT NULL,
        downloaded BOOLEAN NOT NULL,
        response_code INT NOT NULL,
        response_size CHAR(50) NOT NULL,
        response_time CHAR(50) NOT NULL,
        starting_time TIMESTAMP NOT NULL,
        ending_time TIMESTAMP NOT NULL
    )"""
    # axon table with relations
    axon_with_relations = """CREATE TABLE axon_with_relations(
        id SERIAL NOT NULL PRIMARY KEY,
        facet_name CHAR(150) NOT NULL,
        downloaded BOOLEAN NOT NULL,
        response_code INT NOT NULL,
        response_size CHAR(50) NOT NULL,
        response_time CHAR(50) NOT NULL,
        starting_time TIMESTAMP NOT NULL,
        ending_time TIMESTAMP NOT NULL
    )"""

    # general table
    general = """CREATE TABLE general_data(
        id SERIAL NOT NULL PRIMARY KEY,
        last_update TIMESTAMP NOT NULL,
        updated_axon_quantity INT NOT NULL,
        updated_edc_quantity INT NOT NULL,
        run_time CHAR(50) NOT NULL
    )"""

    # server table
    server = """CREATE TABLE server_data(
        id SERIAL NOT NULL PRIMARY KEY,
        created_at TIMESTAMP NOT NULL,
        response_code INT NOT NULL
    )"""

    cur.execute(axon_facets)
    cur.execute(axon_with_relations)
    cur.execute(general)
    cur.execute(server)

    conn.commit()

    print("databse reset")
    conn.close()


create()
