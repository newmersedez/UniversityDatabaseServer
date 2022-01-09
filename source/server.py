from socket import socket, AF_INET, SOCK_STREAM
from os import getpid
from source.request import *
import psycopg2
from source.config import config
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
                        recvBytes = conn.recv(1024)
                        if not recvBytes:
                            break
                        data = recvBytes.decode("utf-8")
                        print('RECV = {}'.format(data))
                        request = Request(data)
                        if request.request_name == 'Auth':
                            json_string = self._dataBaseUserAuthentication(request)
                            print('SEND = {}'.format(json_string))
                            conn.send(json_string.encode())
                        elif request.request_name == 'Lessons':
                            json_string = self._dataBaseLessonsRequest(request)
                            print('SEND = {}'.format(json_string))
                            conn.send(json_string.encode())
                        elif request.request_name == 'Exams':
                            json_string = self._dataBaseExamsRequest(request)
                            print('SEND = {}'.format(json_string))
                            conn.send(json_string.encode())
                        elif request.request_name == 'Marks':
                            json_string = self._dataBaseMarksRequest(request)
                            print('SEND = {}'.format(json_string))
                            conn.send(json_string.encode())
                        elif request.request_name == 'Events':
                            json_string = self._dataBaseEventsRequest()
                            print('SEND = {}'.format(json_string))
                            conn.send(json_string.encode())
                        elif request.request_name == 'AdminStudents':
                            json_string = self._dataBaseAdminStudentsRequest(request)
                            print('SEND = {}'.format(json_string))
                            conn.send(json_string.encode())
                        elif request.request_name == 'AdminLecturers':
                            json_string = self._dataBaseAdminLecturersRequest()
                            print('SEND = {}'.format(json_string))
                            conn.send(json_string.encode())
                        elif request.request_name == 'AdminChangeLogin':
                            self._dataBaseChangeStudentLoginRequest(request)
                        elif request.request_name == 'AdminChangePassword':
                            self._dataBaseChangeStudentPasswordRequest(request)
                    except ConnectionError:
                        break

    @staticmethod
    def _dataBaseUserAuthentication(request: Request):
        conn = None
        json_text = ""
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            columns = ('StudentLastname',
                       'StudentName',
                       'StudentPatronymic',
                       'StudentGroup',
                       'StudentDegree',
                       'StudentFormOfEducation',
                       'SpecialtyNumber',
                       'SpecialtyName')
            cur.execute(open('sql_scripts/student_auth.sql').read().format(
                request.args[0],
                request.args[1]))
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
    def _dataBaseLessonsRequest(request: Request):
        conn = None
        json_text = ""
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            columns = ('LessonDay',
                       'LessonTime',
                       'LessonType',
                       'ClassroomName',
                       'SubjectName')
            cur.execute(open('sql_scripts/get_lessons.sql').read().format(request.args[0]))
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
    def _dataBaseExamsRequest(request: Request):
        conn = None
        json_text = ""
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            columns = ('SubjectName',
                       'GroupName',
                       'ExamDate',
                       'ExamTime',
                       'ClassroomName')
            cur.execute(open('sql_scripts/get_exams.sql').read().format(request.args[0]))
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
    def _dataBaseMarksRequest(request: Request):
        conn = None
        json_text = ""
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            columns = ('StudentLastname',
                       'StudentName',
                       'StudentPatronymic',
                       'SubjectName',
                       'Grade')
            cur.execute(open('sql_scripts/get_marks.sql').read().format(
                request.args[0],
                request.args[1],
                request.args[2]))
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
            columns = ('EventName',
                       'EventDate',
                       'EventTime',
                       'ClassroomName',
                       'GroupName')
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

    @staticmethod
    def _dataBaseAdminStudentsRequest(request: Request):
        conn = None
        json_text = ""
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            columns = ('StudentID',
                       'StudentLastname',
                       'StudentName',
                       'StudentPatronymic',
                       'StudentLogin',
                       'StudentPassword')
            cur.execute(open('sql_scripts/admin_get_students.sql').read())
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
    def _dataBaseAdminLecturersRequest():
        conn = None
        json_text = ""
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            columns = ('LecturerID',
                       'LecturerLastname',
                       'LecturerName',
                       'LecturerPatronymic',
                       'SubjectName')
            cur.execute(open('sql_scripts/admin_get_lecturers.sql').read())
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
    def _dataBaseChangeStudentLoginRequest(request: Request):
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(open('sql_scripts/admin_change_login.sql').read().format(
                str(request.args[1]),
                request.args[0]))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def _dataBaseChangeStudentPasswordRequest(request: Request):
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(open('sql_scripts/admin_change_password.sql').read().format(
                str(request.args[1]),
                request.args[0]))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

