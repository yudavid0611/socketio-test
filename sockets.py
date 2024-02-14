import socketio
from collections import defaultdict

user_room = defaultdict(str)

# create a Socket.IO server
sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
)

# wrap with ASGI application
sio_app = socketio.ASGIApp(
    sio_server,
    socketio_path='sockets')


# 연결
@sio_server.on('connect')
async def connect(sid, env):
    print(f'{sid} 연결')


# 연결 해제
@sio_server.on('disconnect')
async def disconnect(sid):
    # 채팅방 퇴장
    user_room[sid] = ''
    print(f'{sid} 연결 끊김')


# 채팅방 입장
@sio_server.on('enterRoom')
async def enter_room(sid, data: dict):
    # 이미 해당 방에 입장해 있는 경우
    if user_room[sid] == data['room']:
        return
    
    # 기존 채팅방이 있을 경우 퇴장
    if user_room[sid]:
        sio_server.close_room(sid, user_room[sid])
        user_room[sid] = ''
    
    await sio_server.enter_room(sid, data['room'])
    print(f'{data["user"]}를 {data["room"]}에 배정했습니다.')
    user_room[sid] = data['room']


# 클라이언트가 메시지 전송
@sio_server.on('sendMessage')
async def get_message(sid, data: dict):
    print(f'메시지를 전달 받았습니다. | {data}')
    
    # 채팅방 접속자들에게 메시지 전송
    new_message = {
        'sender': data['sender'],
        'message': data['message']
    }
    
    await sio_server.emit('getNewMessage', new_message, room=user_room[sid])