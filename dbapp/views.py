from django.shortcuts import render
from django.http import HttpResponse

import os,sys
import cx_Oracle

# oracle database connection
conn = cx_Oracle.connect('scott', 'tiger','localhost:1521/orcl')
cur = conn.cursor()

# convert str to html string
# tag = html tag && cls = html class
def makeHtml(str,tag,cls):
	if cls!=0:
		return '<'+tag+ 'class="'+ cls +'">'+str+'</'+tag+'>'
	else:
		return '<'+tag+'>'+str+'</'+tag+'>'

# V1: output format is table 
# porb : problem definition
# sql : sql statement
def executeSQL_V1(prob,sql):
	cur.execute(sql)
	rows = cur.fetchall()
	length = len(cur.description)
	count = 0

	result = '<div class="jumbotron">'
	result = result + makeHtml("Q: " + prob, 'p','h2') 	
	result = result + makeHtml("SQL: " + sql,'p','h3')+  '<hr class="my-4">'

	content = '<table class="table table-striped"><thead><tr><th scope="col">#</th>'
	for i in range(0,length):
		content = content + '<th scope="col">' + str(cur.description[i][0]) + '</th>'
	content = content + '</tr><thead><tbody>'
	

	if len(rows) == 0:
		result = "RESULT NOT FOUND\n"
	else:
		for r in rows:
			content = content + '<tr>'
			content = content + '<td>'  + str(count) + '</td>' 
			count = count + 1
			for idx in range(length):
				content = content + '<td>' + str(r[idx]) + '</td>'
			content = content + '</tr>'
		content = content + '</tbody></table>'

	result = result + content + '</div>'
	return result;

# V2: the number of output is signle value
def executeSQL_V2(prob, sql):
	cur.execute(sql)
	rows = cur.fetchall()
	
	result = '<div class="jumbotron">'
	result = result + makeHtml("Q: " + prob, 'p','h2') 	
	result = result + makeHtml("SQL: " + sql,'p','h3')+  '<hr class="my-4">'

	if len(rows) == 0:
		result = "RESULT NOT FOUND\n"
	else:
		for r in rows:
			result = result + makeHtml(str(r[0]),'p','h5') + "<br/>"

	result = result + '</div>'
	return result;


def main(request):
	html_head = """<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <title>Hello, world!</title>
</head>
<body>"""

	html_foot = """<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
  </body>
</html>"""

## MODIFY HERE ! ##
#########################################################################################################################
	
	# EX1
	prob1 = "show  employee whose salary over $3000"
	sql1 = "SELECT empno , job, sal  FROM EMP WHERE sal > 3000"
	result1 = executeSQL_V1(prob1, sql1)

	#EX2
	prob2 = "count the number of all employee in EMP table"
	sql2 ="SELECT COUNT(*) FROM EMP";
	result2 = executeSQL_V2(prob2, sql2);

	html_body = result1 + result2


##########################################################################################################################

	# DO NOT MODIFY
	output = html_head + html_body + html_foot
	return HttpResponse(output)
