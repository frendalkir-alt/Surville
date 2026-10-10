"""Таймеры и кулдауны для геймплея."""


class Timer:
    def __init__(self, duration, auto_reset=False):
        self.duration = duration
        self.auto_reset = auto_reset
        self.elapsed = 0.0
        self.running = False

    def start(self):
        self.elapsed = 0.0
        self.running = True

    def stop(self):
        self.running = False

    def reset(self):
        self.elapsed = 0.0

    def update(self, dt):
        if not self.running:
            return False
        self.elapsed += dt
        if self.elapsed >= self.duration:
            if self.auto_reset:
                self.elapsed = 0.0
            else:
                self.running = False
            return True
        return False

    @property
    def finished(self):
        return self.elapsed >= self.duration

    @property
    def progress(self):
        if self.duration == 0:
            return 1.0
        return min(1.0, self.elapsed / self.duration)


class Cooldown:
    def __init__(self, duration):
        self.duration = duration
        self.remaining = 0.0

    def trigger(self):
        self.remaining = self.duration

    def update(self, dt):
        if self.remaining > 0:
            self.remaining = max(0.0, self.remaining - dt)

    @property
    def ready(self):
        return self.remaining <= 0.0