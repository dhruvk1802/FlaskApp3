#importing the needed packages and modules
from flask import Flask, render_template, request, redirect
import textwrap
import pymssql
app = Flask(__name__)
 
conn = pymssql.connect('webappdbaccess.eastus.cloudapp.azure.com','sa','Dhruv@18',"EmployeeData")
# cursor = conn.cursor()

# cursor.execute("""select * from Person""")




@app.route('/', methods=['GET','POST'])
def hello():
    if request.method == 'POST':
        #Fetch form data
        userDetails = request.form
        firstName = userDetails['firstName']
        lastName = userDetails['lastName']
        email = userDetails['email']
        phoneNumber = userDetails['phoneNumber']
        try:
            cur = conn.cursor()
            insert_query= textwrap.dedent('''INSERT INTO Employee(firstName, lastName, email, phoneNumber) VALUES(%s, %s, %s, %s);''')
            values = (str(firstName),str(lastName),str(email), str(phoneNumber))
            cur.execute(insert_query,values)
            # cur.executemany('''INSERT INTO Employee(firstName, lastName, email, phoneNumber) VALUES(?, ?, ?, ?);''',str(firstName),str(lastName),str(email), str(phoneNumber))
            conn.commit()
        except Exception as err:
            raise err

        # cur.close()
        return redirect('/')
    return render_template('index.html')
 
@app.route('/users',methods=['GET','POST'])
def users():
    if request.method == 'GET':
        #Fetch form data
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM Employee')
            # for row in cur:
            #     print(row)
    
    
            userDetails = cur.fetchall()
            print(userDetails)
            return render_template('users.html',posted=True, noResult=False,userDetails=userDetails)
        except Exception as err:
            return render_template('users.html',posted=False, noResult=True,userDetails=userDetails)
    else:
        return render_template('users.html',posted=False, noResult=True,userDetails=userDetails)
        
    

if __name__ == '__main__':
    app.run(debug=True)


