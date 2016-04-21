import psycopg2
import psycopg2.extras

import json

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
        
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj
        
def refresh_vids(choice, searchterm):
    conn=connectToDB()
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    print 'refreshing vids'
    
    if(choice=='latest'):
        query=cur.mogrify("select * from videos order by vid_id desc limit 9")
    elif(choice=='toprated'):
        query=cur.mogrify("select v.vid_id, v.username, v.created_at, v.url, v.title, v.technique, v.genre, avg(r.total_score) as score from videos as v inner join reviews as r on v.vid_id=r.vid_id group by v.vid_id order by avg(r.total_score) desc limit 21")
    elif(choice=='animedium'):
        query=cur.mogrify("select * from videos where technique=%s order by vid_id desc", (searchterm,))
    elif(choice=='vidgenre'):
        query=cur.mogrify("select * from videos where genre=%s order by vid_id desc", (searchterm,))
    
    print "successful query creation"
    
    cur.execute(query)
    videorows=cur.fetchall()
    #ex. videorows will look like [(1, 100, "abc'def"), (2, None, 'dada'), (3, 42, 'bar')]
    vids=[]
    
    for vid in videorows:
        tmp={'creator':vid[1],'published':vid[2],'URL':vid[3],'title':vid[4],'technique':vid[5],'genre':vid[6]}
        print tmp
        vids.append(tmp)
    
    #emit('updatevidlist', vids)
        
    return vids

@socketio.on('updatemedia', namespace='/iss')
def refresh_mediumlist():
    conn=connectToDB()
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print "running update media"
    
    query=cur.mogrify("select technique, count(technique) from videos group by technique order by count(technique) desc")
    
    cur.execute(query)
    media_list=cur.fetchall()
    #ex. media_list will look like [(1, 100, "abc'def"), (2, None, 'dada'), (3, 42, 'bar')]
    
    for med in media_list:
        tmp={'quality':med[0],'count':med[1]}
        print tmp
        emit('updatemediumlist', tmp)

@socketio.on('updategenre', namespace='/iss')
def refresh_genrelist():
    conn=connectToDB()
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print "running update genrelist"
    
    query=cur.mogrify("select genre, count(genre) from videos group by genre order by count(genre) desc")
    
    cur.execute(query)
    genre_list=cur.fetchall()
    #ex. genre_list will look like [(1, 100, "abc'def"), (2, None, 'dada'), (3, 42, 'bar')]
    
    for g in genre_list:
        tmp={'quality':g[0],'count':g[1]}
        print tmp
        emit('updategenrelist', tmp)

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
        vids=refresh_vids('latest','')
    else:
        return redirect(url_for('mainIndex'))

    return render_template('userhome.html', vidlist=vids, title="Recent Uploads")

@app.route('/toprated', methods=['GET', 'POST'])
def toprated():
    vids=refresh_vids('toprated','')
    return render_template('home.html', vidlist=vids, title="Top Rated")

@app.route('/animedium', methods=['GET', 'POST'])
def animedium():
    return app.send_static_file('anibrowse.html')

@socketio.on('animationbrowse', namespace='/iss')
def abrowse(term):
    print 'updating videos based on animation medium term'
    vids=refresh_vids('animedium', term)
    
    print 'going into loop'
    for vid in vids:
        obj=json.dumps(vid['published'], default=date_handler)
        tmp={'creator':vid['creator'],'published':obj,'URL':vid['URL'],'title':vid['title'],'technique':vid['technique'],'genre':vid['genre']}
        print tmp
        emit('updatevidlist', tmp)


@app.route('/vidgenre', methods=['GET', 'POST'])
def vidgenre():
    return app.send_static_file('genrebrowse.html')

@socketio.on('genrebrowse', namespace='/iss')
def gbrowse(term):
    print 'updating videos based on genre term'
    vids=refresh_vids('vidgenre', term)
    
    print 'going into loop'
    for vid in vids:
        obj=json.dumps(['published'], default=date_handler)
        tmp={'creator':vid['creator'],'published':obj,'URL':vid['URL'],'title':vid['title'],'technique':vid['technique'],'genre':vid['genre']}
        print tmp
        emit('updatevidlist', tmp)


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
    vids=refresh_vids('latest', '')

    return render_template('home.html', vidlist=vids, title="Recent Uploads")

if __name__=='__main__':
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)