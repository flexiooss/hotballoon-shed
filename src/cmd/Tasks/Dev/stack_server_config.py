stack_server_config: dict = {
    "host": "172.17.0.1",
    # "disableHostCheck": True,
    "static": {"publicPath": "/"},
    "public": "https://dev.flexio.io/devui",
    "client": {
        "logging": 'info',
        "overlay": False,
        "webSocketTransport": 'sockjs',
        "webSocketURL": "https://dev.flexio.io/devui/socketjs"
    },
    "proxy": [
        {
            "context": [
                "//[a-z]+/*"
            ],
            "logLevel": "debug",
            "target": "https://dev.flexio.io/devui",
            "secure": False,
            "pathRewrite": {
                "^//[a-z]+/*": "/"
            }
        }
    ]
}
