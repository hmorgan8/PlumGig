#import psycopg2
#import psycopg2.extras

import os
from flask import Flask, session
from flask.ext.socketio import SocketIO, emit

app=Flask(__name__, static_url_path='')
app.config['SECRET_KEY']='secret!'

socketio=SocketIO(app)

@app.route('/')
def mainIndex():
    print 'in hello world'
    return app.send_static_file('login.html')

if __name__=='__main__':
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)