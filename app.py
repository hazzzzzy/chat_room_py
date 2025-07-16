from flask_wtf.csrf import generate_csrf

from apps import createApp, socketio
from config import HOST, PORT, DEBUG

# logging.basicConfig(
#     level=logging.INFO,
#     format='[%(asctime)s] %(message)s',
#     handlers=[logging.StreamHandler(sys.stdout)]
# )
app = createApp()

if __name__ == '__main__':
    socketio.run(app, host=HOST, port=PORT, debug=DEBUG)
