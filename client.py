import socketio
import asyncio


sio_client = socketio.AsyncClient()


@sio_client.event
async def connect():
    print('I am connected.')


@sio_client.event
async def disconnect():
    print('I am disconnected.')
    

async def main():
    await sio_client.connect(url='http://localhost:8000', socketio_path='sockets')
    await sio_client.disconnect()
    

if __name__ == '__main__':
    # 단순 연결 테스트용 모듈
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())