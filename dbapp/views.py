from django.shortcuts import render

import os
import cx_Oracle

# oracle database connection
conn = cx_Oracle.connect('scott', 'tiger','localhost:1521/orcl')
cur = conn.cursor()


def executeSQL_V1(sql):
	cur.execute(sql);
	



def main(request):
    sql = "SELECT count(*) from emp"
    cur.execute(sql)
    rows = cur.fetchall()

    result = ''
    if len(rows)==0:
        result = "RESULT NOT FOUND\n"
    else:
        for r in rows:
            result = result + str(r) + "\n"

    print(result)

    return render(request, 'dbapp/main.html', {})



def print
