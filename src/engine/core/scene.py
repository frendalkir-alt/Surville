"""Базовые сцены и менеджер сцен."""


class Scene:
    def __init__(self, game):
        self.game = game

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass


class SceneManager:
    def __init__(self, game):
        self.game = game
        self.scenes = {}
        self.current = None
        self._pending_name = None

    def register(self, name, scene):
        self.scenes[name] = scene

    def switch(self, name):
        self._pending_name = name

    def _apply_pending(self):
        if self._pending_name is None:
            return
        name = self._pending_name
        self._pending_name = None
        if name not in self.scenes:
            raise KeyError(f"Scene '{name}' not registered")
        if self.current:
            self.current.on_exit()
        self.current = self.scenes[name]
        self.current.on_enter()

    def handle_event(self, event):
        if self.current:
            self.current.handle_event(event)

    def update(self, dt):
        self._apply_pending()
        if self.current:
            self.current.update(dt)

    def draw(self, surface):
        if self.current:
            self.current.draw(surface)