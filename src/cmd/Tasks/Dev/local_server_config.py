local_server_config: dict = {
    # 'host': 'localhost',
    'host': '0.0.0.0',
    "static": {"publicPath": "/"},
    "client": {
        "logging": 'info',
        "overlay": False,
        "webSocketTransport": 'ws'
    },
    # "disableHostCheck": True,
}
