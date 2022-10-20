from time import time

class Camera():
    def __init__(self,frames):
        self.frames = [open(f + '.jpeg', 'rb').read() for f in ['test']]

    def get_frame(self):
        return self.frames[int(time()) % 3]