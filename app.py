from flask import Flask
from flask import request
from flask_mysqldb import MySQL
from flask_cors import CORS
import json
mysql = MySQL()
app = Flask(__name__)
CORS(app)
# My SQL Instance configurations
# Change these details to match your instance configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Lab5'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
mysql.init_app(app)

@app.route("/add") #Add Student
def add():
  name = request.args.get('name')
  email = request.args.get('email')
  cur = mysql.connection.cursor() #create a connection to the SQL instance
  s='''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name,email) # kludge - use stored proc or params
  cur.execute(s)
  result = '{"Result":"Failure1"}'
  try:
    mysql.connection.commit();
    result = '{"Result":"Success"}' 
  except Exception as e:
    result = '{"Result":"Failure2"}'

  return result

@app.route("/delete") #Delete Student
def delete():
  id = request.args.get('studentid')
  cur = mysql.connection.cursor() #create a connection to the SQL instance
  s='''DELETE FROM students WHERE studentID = ('{}');'''.format(id) # kludge - use stored proc or params
  cur.execute(s)
  result = '{"Result":"Failure"}'
  try:
    mysql.connection.commit();
    result = '{"Result":"Success"}' 
  except Exception as e:
    result = '{"Result":"Failure"}'

  return result
  
@app.route("/") #Default - Show Data
def read(): # Name of the method
  cur = mysql.connection.cursor() #create a connection to the SQL instance
  cur.execute('''SELECT * FROM students''') # execute an SQL statment
  rv = cur.fetchall() #Retreive all rows returend by the SQL statment
  Results=[]
  for row in rv: #Format the Output Results and add to return string
    Result={}
    Result['Name']=row[0].replace('\n',' ')
    Result['Email']=row[1]
    Result['ID']=row[2]
    Results.append(Result)
  response={'Results':Results, 'count':len(Results)}
  ret=app.response_class(
    response=json.dumps(response),
    status=200,
    mimetype='application/json'
  )
  return ret #Return the data in a string format
if __name__ == "__main__":
  app.run(host='0.0.0.0',port='8080') #Run the flask app at port 8080

