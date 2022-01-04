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
            json_string = ''
            with conn:
                print('Connected by', addr)
                while True:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            break
                        print('RECV = {}'.format(data))
                        if data == b'Lessons' or data == b'Lessons\r\n':
                            json_string = self._dataBaseLessonsRequest()
                        elif data == b'Exams' or data == b'Exams\r\n':
                            json_string = self._dataBaseExamsRequest()
                        elif data == b'Marks' or data == b'Marks\r\n':
                            json_string = self._dataBaseMarksRequest()
                        elif data == b'Events' or data == b'Events\r\n':
                            json_string = self._dataBaseEventsRequest()
                        print('SEND = {}'.format(json_string.encode()))
                        conn.send(json_string.encode())
                    except ConnectionError:
                        break

    @staticmethod
    def _dataBaseLessonsRequest():
        conn = None
        json_text = ""
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            columns = ('lesson_day', 'lesson_time', 'lesson_type', 'classroom_name', 'subject_name')
            cur.execute(open('sql_scripts/get_lessons.sql').read())
            results = []

            for row in cur.fetchall():
                results.append(dict(zip(columns, row)))
            json_text = json.dumps(results, ensure_ascii=False, default=str).encode('utf8').decode()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return json_text

    @staticmethod
    def _dataBaseExamsRequest():
        conn = None
        json_text = ""
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            columns = ('subject_name', 'group_name', 'exam_date', 'exam_time', 'classroom_name')
            cur.execute(open('sql_scripts/get_exams.sql').read())
            results = []

            for row in cur.fetchall():
                results.append(dict(zip(columns, row)))
            json_text = json.dumps(results, ensure_ascii=False, default=str).encode('utf8').decode()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return json_text

    @staticmethod
    def _dataBaseMarksRequest():
        conn = None
        json_text = ""
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            columns = ('student_lastname', 'student_name', 'student_patronymic', 'subject_name', 'mark')
            cur.execute(open('sql_scripts/get_marks.sql').read().format('Тришин', 'Дмитрий', 'Александрович'))
            results = []

            for row in cur.fetchall():
                results.append(dict(zip(columns, row)))
            json_text = json.dumps(results, ensure_ascii=False, default=str).encode('utf8').decode()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return json_text

    @staticmethod
    def _dataBaseEventsRequest():
        conn = None
        json_text = ""
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            columns = ('event_name', 'event_date', 'event_time', 'classroom_name', 'group_name')
            cur.execute(open('sql_scripts/get_events.sql').read())
            results = []

            for row in cur.fetchall():
                results.append(dict(zip(columns, row)))
            json_text = json.dumps(results, ensure_ascii=False, default=str).encode('utf8').decode()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return json_text
