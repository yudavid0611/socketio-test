from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sockets import sio_app


app = FastAPI()
app.mount('/sockets', sio_app)

templates = Jinja2Templates(directory='templates')


@app.get('/chat', response_class=HTMLResponse)
def chat(request: Request, user: str):
    return templates.TemplateResponse('chat.html', {'request': request, 'user': user})