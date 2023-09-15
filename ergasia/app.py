from flask import Flask, render_template, request, make_response,session,request
import  sqlite3

app = Flask(__name__)
app.config['SECRET_KEY']='Omustikoskwdikosmou'
database = 'mybase.db'

def connect_db():
    return sqlite3.connect(database)

def display_db():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user")
    lista = cursor.fetchall()
    for i in lista:
        print(i)

@app.route("/home")
def home():
    return render_template('index.html')



@app.route("/")
def index():
    return render_template('login.html')

@app.route("/login",methods=['POST'])
def login():
    username=request.form['username']
    password=request.form['password']
    db = connect_db()
    cur = db.execute("SELECT userID, username, password FROM admins WHERE username=? and password=?", [username, password])
    rv = cur.fetchall()
    print(rv)
    cur.close()
    if rv:
        user = rv[0]
        if username == user[1] and password == user[2]:
            session['logged_in'] = True
            session['userID'] = user[0]
            return render_template('index.html')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in']=False
    return render_template('login.html')

@app.route("/signup",methods=['POST'])
def signup():
    username = request.form["username"]
    firstname = request.form["firstname"]
    lastname=request.form["lastname"]
    password=request.form["password"]
    db=connect_db()
    sql='INSERT INTO admins(username, firstname, lastname, password) VALUES (?,?,?,?)'
    db.execute(sql, [username, firstname, lastname, password])
    db.commit()
    display_db()
    db.close()
    return render_template('succesfullysignedup.html')

@app.route('/newadminuser')
def newadminuser():
    return render_template('signup.html')


@app.route('/newuserform')
def newuserform():
    return render_template('newuserform.html')

@app.route("/addprofile",methods=['POST'])
def addprofile():
    myname=request.form['myname']
    mylastname=request.form['mylastname']
    myage=request.form['myage']
    myemail=request.form['myemail']
    mydescription=request.form['mydescription']
    db = connect_db()
    sql = 'INSERT INTO user (name, lastname, age, email, description, adminID) VALUES (?,?,?,?,?, ?)'
    db.execute(sql, [myname, mylastname, myage, myemail, mydescription, session['userID']])
    db.commit()
    display_db()
    db.close()
    return render_template('newuser.html', html_page_name = myname, html_page_lastname = mylastname)

@app.route('/displayprofiles')
def displayprofiles():
    db = connect_db()
    profiles=db.execute("SELECT id, name, lastname, age, email, description FROM user WHERE adminID = ?", [session['userID']])
    egrafes=[]
    for row in profiles.fetchall():
        egrafes.append(dict(id=row[0], name=row[1], lastname=row[2],age=row[3], email=row[4],description=row[5]))
    db.close()
    return render_template('Listapelatwn.html',egrafes=egrafes)

@app.route('/displayprofileswithnames')
def displayprofileswithnames():
    print(request.args.get('name'))
    print(request.args.get('lastname'))
    searchname=request.args.get('name')
    searchlastname=request.args.get('lastname')
    db = connect_db()
    cursor = db.cursor()
    profiles=cursor.execute("SELECT id, name, lastname, age, email, description FROM user WHERE name LIKE  ? AND lastname LIKE ? and adminID=?",(str(searchname)+'%',str(searchlastname)+'%',session['userID']))
    egrafes=[]
    for row in profiles.fetchall():
        egrafes.append(dict(id=row[0], name=row[1], lastname=row[2],age=row[3], email=row[4],description=row[5]))
    db.close()
    return render_template('Listapelatwn.html',egrafes=egrafes)

@app.route('/edituser')
def edituser():
    id = request.args.get('id')
    db = connect_db()
    cur= db.execute("SELECT id,  age, email, description FROM user WHERE id=?",[id])
    rv=cur.fetchall()
    print(rv)
    cur.close()
    user = rv[0]
    print(user)
    db.close()
    return render_template('updateuserform.html', user=user)



@app.route('/updateuser',methods=['POST'])
def updateuser():
    id = request.form['id']
    myage = request.form['myage']
    myemail = request.form['myemail']
    mydescription = request.form['mydescription']
    db = connect_db()
    sql = "UPDATE user SET age=?, email=? , description=? WHERE id=?"
    db.execute(sql, [myage , myemail, mydescription, id])
    db.commit()
    db.close()

    return render_template('edituser.html')

@app.route('/deleteuser')
def deleteuser():
    id = request.args.get('id')
    db = connect_db()
    sql = "DELETE FROM user WHERE id=?"
    db.execute(sql, [id])
    db.commit()
    db.close()
    return render_template('index.html')


if __name__=='__main__':
    display_db()
    app.run(debug=True)

