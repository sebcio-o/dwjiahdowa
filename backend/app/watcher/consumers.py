from channels.generic.websocket import WebsocketConsumer

class WatcherConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive_json(self, content, **kwargs):
        print(content)
        return super().receive_json(content, **kwargs)

    def disconnect(self):
        self.close()