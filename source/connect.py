import psycopg2
from source.config import config


def connect(scriptpath : str):
    conn = None
    try:
        # read connection parameters
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        print("Connected.")

        cur.execute(open('sql_scripts/get_marks.sql').read().format('Тришин', 'Дмитрий', 'Александрович'))
        db = cur.fetchall()
        [print(item) for item in db]
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
