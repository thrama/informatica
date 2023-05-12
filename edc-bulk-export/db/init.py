import psycopg2
# Connect to your postgres DB


def create():
    conn = psycopg2.connect(
        "host=localhost dbname=edc user=postgres password=Milano2003+")

    # Open a cursor to perform database operations
    cur = conn.cursor()
    # cur.execute("DROP TABLE IF EXISTS all_resources")
    # cur.execute("DROP TABLE IF EXISTS data_domain_resources")
    # cur.execute("DROP TABLE IF EXISTS data_file_resources")
    # cur.execute("DROP TABLE IF EXISTS rdbms_resources")
    # cur.execute("DROP TABLE IF EXISTS reference_resources")
    cur.execute("DROP TABLE IF EXISTS all_edc")
    cur.execute("DROP TABLE IF EXISTS general_data")

    # edc all resources
    # all_resources = '''CREATE TABLE all_resources(
    #     id SERIAL NOT NULL PRIMARY KEY,
    #     downloaded INT NOT NULL,
    #     response_code INT NOT NULL,
    #     response_size CHAR(50) NOT NULL,
    #     response_time CHAR(50) NOT NULL,
    #     starting_time TIMESTAMP NOT NULL,
    #     ending_time TIMESTAMP NOT NULL
    # )'''
    # # edc data domain
    # data_domain_resources = '''CREATE TABLE data_domain_resources(
    #     id SERIAL NOT NULL PRIMARY KEY,
    #     downloaded INT NOT NULL,
    #     response_code INT NOT NULL,
    #     response_size CHAR(50) NOT NULL,
    #     response_time CHAR(50) NOT NULL,
    #     starting_time TIMESTAMP NOT NULL,
    #     ending_time TIMESTAMP NOT NULL
    # )'''

    # # edc datafile
    # data_file_resources = '''CREATE TABLE data_file_resources(
    #     id SERIAL NOT NULL PRIMARY KEY,
    #     downloaded INT NOT NULL,
    #     response_code INT NOT NULL,
    #     response_size CHAR(50) NOT NULL,
    #     response_time CHAR(50) NOT NULL,
    #     starting_time TIMESTAMP NOT NULL,
    #     ending_time TIMESTAMP NOT NULL
    # )'''
    # # edc datafile
    # data_file_resources_extra = '''CREATE TABLE data_file_resources_extra(
    #     id SERIAL NOT NULL PRIMARY KEY,
    #     downloaded INT NOT NULL,
    #     response_code INT NOT NULL,
    #     response_size CHAR(50) NOT NULL,
    #     response_time CHAR(50) NOT NULL,
    #     starting_time TIMESTAMP NOT NULL,
    #     ending_time TIMESTAMP NOT NULL
    # )'''
    # # edc datafile
    # data_file_resources_lookup = '''CREATE TABLE data_file_resources_lookup(
    #     id SERIAL NOT NULL PRIMARY KEY,
    #     downloaded INT NOT NULL,
    #     response_code INT NOT NULL,
    #     response_size CHAR(50) NOT NULL,
    #     response_time CHAR(50) NOT NULL,
    #     starting_time TIMESTAMP NOT NULL,
    #     ending_time TIMESTAMP NOT NULL
    # )'''
    # # edc rdbms
    # rdbms_resources = '''CREATE TABLE rdbms_resources(
    #     id SERIAL NOT NULL PRIMARY KEY,
    #     downloaded INT NOT NULL,
    #     response_code INT NOT NULL,
    #     response_size CHAR(50) NOT NULL,
    #     response_time CHAR(50) NOT NULL,
    #     starting_time TIMESTAMP NOT NULL,
    #     ending_time TIMESTAMP NOT NULL
    # )'''
    # # edc references

    # reference_resources = '''CREATE TABLE reference_resources(
    #     id SERIAL NOT NULL PRIMARY KEY,
    #     downloaded INT NOT NULL,
    #     response_code INT NOT NULL,
    #     response_size CHAR(50) NOT NULL,
    #     response_time CHAR(50) NOT NULL,
    #     starting_time TIMESTAMP NOT NULL,
    #     ending_time TIMESTAMP NOT NULL
    # )'''

    all_edc = '''CREATE TABLE all_edc(
        id SERIAL NOT NULL PRIMARY KEY,
        resource_name CHAR(50) NOT NULL,
        resource_type CHAR(50) NOT NULL,
        downloaded INT NOT NULL,
        response_code INT NOT NULL,
        response_size CHAR(50) NOT NULL,
        response_time CHAR(50) NOT NULL,
        starting_time TIMESTAMP NOT NULL,
        ending_time TIMESTAMP NOT NULL
    )'''

    # general table
    general = '''CREATE TABLE general_data(
        id SERIAL NOT NULL PRIMARY KEY,
        last_update TIMESTAMP NOT NULL,
        updated_edc_quantity INT NOT NULL,
        run_time CHAR(50) NOT NULL
    )'''

    # cur.execute(all_resources)
    # cur.execute(data_domain_resources)
    # cur.execute(data_file_resources)
    # cur.execute(data_file_resources_extra)
    # cur.execute(data_file_resources_lookup)
    # cur.execute(rdbms_resources)
    # cur.execute(reference_resources)
    cur.execute(all_edc)
    cur.execute(general)

    conn.commit()

    print('databse reset')
    conn.close()


create()
