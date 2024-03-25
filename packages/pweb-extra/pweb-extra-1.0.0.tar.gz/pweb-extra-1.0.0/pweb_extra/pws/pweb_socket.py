from flask_socketio import SocketIO
from ppy_common import Console
from pweb_extra.pws.pweb_socket_conf import PwebSocketConf


class PWebSocket:
    web_socket: SocketIO = None
    config: PwebSocketConf = None

    @staticmethod
    def register(pweb_app, config: PwebSocketConf = None):
        if not config:
            config = PwebSocketConf()
        PWebSocket.web_socket = SocketIO(
            app=pweb_app,
            path=config.register_end_point,
            cors_allowed_origins=config.cors_allowed_origins
        )
        PWebSocket().__init_configuration(PWebSocket.web_socket, config=config)
        Console.info("Registered PWebSocket", system_log=True)

    def __init_configuration(self, web_socket: SocketIO, config: PwebSocketConf = None):
        self.config = config

        # Manage Errors
        web_socket.default_exception_handler = self.on_unhandled_error
        web_socket.exception_handlers["/"] = self.on_slash_error
        self.register_error(web_socket.exception_handlers)

        # Register Event
        web_socket.on_event("connect", self.on_connect)
        web_socket.on_event("disconnect", self.on_disconnect)

    def on_unhandled_error(self, errors):
        Console.error(f"PWebSocket Unhandled Errors: {errors}")
        if self.config and self.config.on_unhandled_error:
            self.config.on_unhandled_error(errors)

    def on_slash_error(self, errors):
        Console.error(f"PWebSocket Slash Errors: {errors}")
        if self.config and self.config.on_slash_error:
            self.config.on_slash_error(errors)

    def register_error(self, exception_handlers):
        pass

    def on_connect(self):
        if self.config and self.config.on_connect:
            self.config.on_connect()

    def on_disconnect(self):
        if self.config and self.config.on_disconnect:
            self.config.on_disconnect()

    @staticmethod
    def notify(event: str, send_str_dict, feedback_func=None, namespace=None, broadcast=False):
        if PWebSocket.web_socket:
            kwargs = {}

            if feedback_func:
                kwargs["callback"] = feedback_func

            if namespace:
                kwargs["namespace"] = namespace

            if broadcast:
                kwargs["broadcast"] = broadcast

            PWebSocket.web_socket.emit(event, send_str_dict, **kwargs)

    @staticmethod
    def notify_message(send_str_dict, feedback_func=None, namespace=None, to=None):
        if PWebSocket.web_socket:
            kwargs = {}
            PWebSocket.web_socket.send(send_str_dict, namespace=namespace, callback=feedback_func, to=to, **kwargs)

    @staticmethod
    def register_event(event: str, handler_func=None, namespace=None):
        if PWebSocket.web_socket:
            PWebSocket.web_socket.on_event(message=event, handler=handler_func, namespace=namespace)
