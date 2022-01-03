from socket import socket, AF_INET, SOCK_STREAM
from os import getpid
from source.connect import *
import json


class Server:
    def __init__(self, host='localhost', port=1234):
        self._socket = None
        self._host = host
        self._port = port

    def run(self):
        print('Server PID = {}'.format(getpid()))
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self._host, self._port))
        while True:
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            break
                        if data == b'Lessons':
                            self._dataBaseLessonsRequest()
                        elif data == b'Exams':
                            self._dataBaseExamsRequest()
                        elif data == b'Marks':
                            self._dataBaseMarksRequest()
                        elif data == b'Events':
                            self._dataBaseEventsRequest()
                    except ConnectionError:
                        break

    @staticmethod
    def _dataBaseLessonsRequest():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(open('sql_scripts/get_lessons.sql').read().format('Понедельник'))
            db = cur.fetchall()
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                [print(item) for item in db]

    @staticmethod
    def _dataBaseExamsRequest():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(open('sql_scripts/get_exams.sql').read())
            db = cur.fetchall()
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                [print(item) for item in db]

    @staticmethod
    def _dataBaseMarksRequest():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(open('sql_scripts/get_marks.sql').read().format('Тришин', 'Дмитрий', 'Александрович'))
            db = cur.fetchall()
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print(type(db))
                [print(item) for item in db]

    @staticmethod
    def _dataBaseEventsRequest():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(open('sql_scripts/get_events.sql').read())
            db = cur.fetchall()
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                [print(item) for item in db]