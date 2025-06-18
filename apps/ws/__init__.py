def register_ws(app, ws):
    from . import server
    ws.init_app(app)
