from apps import createApp, socketio

app = createApp()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=10086, debug=True)
