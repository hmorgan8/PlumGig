import psycopg2
import psycopg2.extras

import os
from flask import Flask, session, render_template, request, redirect, url_for
from flask.ext.socketio import SocketIO, emit

app=Flask(__name__, static_url_path='')
app.config['SECRET_KEY']='secret!'

socketio=SocketIO(app)

def connectToDB():
    connectionString='dbname=plumgig user=aziz password=PrudentGrape host=localhost'
    print connectionString
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")
        
def refresh_vids():
    conn=connectToDB()
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    query=cur.mogrify("select * from videos order by vid_id desc limit 6")
    cur.execute(query)
    videorows=cur.fetchall()
    #ex. videorows will look like [(1, 100, "abc'def"), (2, None, 'dada'), (3, 42, 'bar')]
    vids=[]
    
    for vid in videorows:
        tmp={'creator':vid[1],'published':vid[2],'URL':vid[3],'title':vid[4],'technique':vid[5],'genre':vid[6]}
        vids.append(tmp)
        
    return vids

# @socketio.on('updatevidlist', namespace='/iss')
# def refresh_vids():
#     conn=connectToDB()
#     cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
#     query=cur.mogrify("select * from videos order by timeposted desc limit 6")
#     cur.execute(query)
#     videorows=cur.fetchall()
#     #ex. videorows will look like [(1, 100, "abc'def"), (2, None, 'dada'), (3, 42, 'bar')]
#     vids=[]
    
#     for vid in videorows:
#         tmp={'creator':vid[1],'published':vid[2],'URL':vid[4],'title':vid[5],'technique':vid[6],'genre':vid[7]}
#         vids.append(tmp)
        
#     emit('loadvids', vids)

# @socketio.on('verifyuser', namespace='/iss')
# def verify(u,p):
#     conn=connectToDB()
#     cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
#     query=cur.mogrify("select * from users where username=%s and password=%s", (u,p))
#     cur.execute(query)
#     rows=cur.fetchall()
    
#     if not rows:
#         emit('badlogin')
#     else:
#         vids=refresh_vids()
#         emit('currentuser',u)
#         #return render_template('index.html', vidlist=vids)
#         return app.send_static_file('index.html', vidlist=vids)

@app.route('/userhome', methods=['GET','POST'])
def userhome():

    if 'currentUser' in session:
        print session['currentUser']
        vids=refresh_vids()

    else:
        return redirect(url_for('mainIndex'))

    return render_template('userhome.html', vidlist=vids)

@app.route('/login', methods=['GET', 'POST'])
def loginpage():
    conn=connectToDB()
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    session.pop('currentUser', None)
    
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        username = request.form['username']
        session['currentUser'] = username

        password = request.form['password']
        query = cur.mogrify("select * from users WHERE username = %s AND password = crypt(%s, password)", (username, password))
        print query
        cur.execute(query)
        if cur.fetchone():
            return redirect(url_for('userhome'))
        else:
            print "bad login"
    
    if 'currentUser' in session:
        currentUser=session['currentUser']
    else:
        currentUser=''
    return render_template('login.html', currentUser=currentUser)

@app.route('/')
def mainIndex():
    print 'in hello world'
    vids=refresh_vids()

    return render_template('home.html', vidlist=vids)

if __name__=='__main__':
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)