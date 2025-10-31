stack_server_config_v2: dict = {
    "host": "172.17.0.1",
    "server": "http",
    "hot": False,
    "liveReload": True,
    "client": {
        "logging": 'verbose',
        "overlay": {
            "errors": True,
            "warnings": False,
            "runtimeErrors": True,
        },
        "webSocketTransport": 'sockjs',
        "webSocketURL": "auto://dev-full-v2.flexio.io/devui-deported/socketjs"
    },
    "proxy": [
        {
            "context": [
                "//[a-z]+/*"
            ],
            "logLevel": "debug",
            "target": "https://dev-full-v2.flexio.io/devui-deported",
            "secure": False,
            "pathRewrite": {
                "^//[a-z]+/*": "/"
            }
        }
    ],
    "webSocketServer": False
}
