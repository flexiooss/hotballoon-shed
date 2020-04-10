stack_server_config: dict = {
    "host": "172.17.0.1",
    "disableHostCheck": True,
    "publicPath": "/",
    "public": "https://dev.flexio.io/devui",
    "sockPath": "/socketjs",
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
