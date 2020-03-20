from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

from Rehabilitation.consumers import MassagesConsumer

# self.scope['type']获取协议类型
# channels routing 是scope 级别的 ,一个连接只能由一个consumer接受和处理


application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('ws/<str:id>/', MassagesConsumer)
            ])
        )
    )
})

# AllowedHostsOriginValidator 防止通过websocket 进行CSRF 攻击
# AuthMiddlewareStack 用于 WebSocket 集成了 CookieMiddleWare, SessionMiddleWare, AuthMiddleWare,
