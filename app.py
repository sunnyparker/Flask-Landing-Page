from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app=Flask(__name__)
# code for connection with MySQL
# MySQL host
app.config['MYSQL_HOST']='localhost'
# MySQL username
app.config['MYSQL_USER']='root'
# MySQL password
app.config['MYSQL_PASSWORD']=''
# MySQL Database name
app.config['MYSQL_DB']='ezetechdb'

mysql=MySQL(app)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=''
    if request.method == 'POST' and 'uname' in request.form and 'pwd' in request.form:
        un=request.form['uname']
        pwd=request.form['pwd']
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("select * from admin where username=%s and password=%s", (un, pwd,))
        account = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if account:
            msg='Logged in Successfully'
            # After login if you want to call a new page then use the below line
            return render_template("index.html")
        else:
            msg='Wrong username or password!'
    return render_template("admin.html", msg=msg)


@app.route('/projectlist',methods=['GET','POST'])
def projectlist():
    #creating variable for connection
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #executing query
    cursor.execute("select * from reg_pro")
    #fetching all records from database
    data=cursor.fetchall()
    #returning back to projectlist.html with all records from MySQL which are stored in variable data
    return render_template("projectlist.html",data=data)


@app.route('/projectreg',methods=['GET','POST'])
def projectreg():
    msg=''
    #applying empty validation
    if request.method == 'POST' and 'name' in request.form and 'tech' in request.form and 'desc' in request.form and 'gname' in request.form:
        #passing HTML form data into python variable
        n = request.form['name']
        t = request.form['tech']
        d = request.form['desc']
        g = request.form['gname']
        #creating variable for connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #query to check given data is present in database or no
        cursor.execute('SELECT * FROM reg_pro WHERE PRO_NAME = % s', (n,))
        #fetching data from MySQL
        result = cursor.fetchone()
        if result:
            msg = 'Project already exists !'
        else:
            #executing query to insert new data into MySQL
            cursor.execute('INSERT INTO REG_PRO VALUES (NULL, % s, % s, % s,% s,% s)', (n, t, d, g,'Pending',))
            mysql.connection.commit()
            #displaying message
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('projectreg.html', msg=msg)

if __name__ == '__main__':
    app.run(port=5000, debug=True)