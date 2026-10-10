"""Покадровая анимация."""


class Animation:
    def __init__(self, frames, frame_duration=0.1, loop=True):
        if not frames:
            raise ValueError("Animation needs at least one frame")
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.time = 0.0
        self.index = 0
        self.finished = False

    def reset(self):
        self.time = 0.0
        self.index = 0
        self.finished = False

    def update(self, dt):
        if self.finished and not self.loop:
            return
        self.time += dt
        while self.time >= self.frame_duration:
            self.time -= self.frame_duration
            self.index += 1
            if self.index >= len(self.frames):
                if self.loop:
                    self.index = 0
                else:
                    self.index = len(self.frames) - 1
                    self.finished = True
                    break

    @property
    def current_frame(self):
        return self.frames[self.index]


class Animator:
    def __init__(self):
        self.animations = {}
        self.current_name = None
        self.current = None

    def add(self, name, animation):
        self.animations[name] = animation
        if self.current is None:
            self.current_name = name
            self.current = animation

    def play(self, name, restart=False):
        if name not in self.animations:
            return
        if name == self.current_name and not restart:
            return
        self.current_name = name
        self.current = self.animations[name]
        self.current.reset()

    def update(self, dt):
        if self.current:
            self.current.update(dt)

    @property
    def frame(self):
        return self.current.current_frame if self.current else None

    @property
    def finished(self):
        return self.current.finished if self.current else True