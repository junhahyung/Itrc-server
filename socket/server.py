import eventlet
import socketio

from pymongo import MongoClient


sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})
client = MongoClient('localhost', 27017)
db = client["database"]
col = db["storage"]

def init():
    for i in range(3):
        n_dest = str(i+1)
        cur = list(col.find({'dest': n_dest}))
        if len(cur) == 0:
            _init = {'dest':n_dest, 'red':0, 'green':0, 'blue':0}
            col.insert_one(_init)
            print(f'inserted initial {n_dest} dict')

    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8080)), app)

@sio.event
def connect(sid, environ):
    print('connected!! ', sid)
    #my_message(sid, {'Test': 'Message'})


@sio.event
def initialize_database(sid, environ):
    x = col.delete_many({})
    print('database initialized', sid)

@sio.event
def my_message(sid, data):
    #sio.send(data)
    print(f'received: {data}')

    dest = data['dest']
    color = data['color']
    _dict = list(col.find({'dest': str(dest)}))[0]

    print('before update: ')
    print(_dict)

    col.delete_one({'dest': str(dest)})
    _dict[color] += 1
    col.insert_one(_dict)

    _dict = list(col.find({'dest': str(dest)}))[0]
    print(f'updated: {_dict}')


@sio.event
def disconnect(sid):
    print('disconnect ', sid)

'''
@sio.event
def on_my_message(self, data):
    print('receivced event')
    print(data)
'''


if __name__ == '__main__':
    init()
