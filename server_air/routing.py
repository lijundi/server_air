from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from temperature.consumers import TempConsumer
from server.consumers import AirConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
            URLRouter([
                url(r'^temperature/websocket/$', TempConsumer),
                url(r'^$', AirConsumer),
            ])
    ),
})
