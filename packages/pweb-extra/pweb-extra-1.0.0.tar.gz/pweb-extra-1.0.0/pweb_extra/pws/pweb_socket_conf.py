from abc import ABC


class PwebSocketConf(ABC):
    register_end_point: str = "pweb-socket"
    cors_allowed_origins: str = '*'

    def on_unhandled_error(self, errors):
        pass

    def on_slash_error(self, errors):
        pass

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass
