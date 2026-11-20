class TypewriterText:
    def __init__(self, text, characters_per_second=20, max_width=None, lifetime=None, centered=False, align="left", rotation=0, color=(255,255,255)):
        self.text = text
        self.characters_per_second = characters_per_second
        self.elapsed = 0.0
        self.max_width = max_width
        self.visible = True
        self.time_since_finish = 0.0
        self.lifetime = lifetime
        self.centered = centered
        self.align = align
        self.rotation = rotation
        self.color = color

    def update(self, delta_time):
        self.elapsed += delta_time
        if self.finished:
            self.time_since_finish += delta_time

    @property
    def visible_text(self):
        count = int(self.elapsed * self.characters_per_second)
        return self.text[:count]

    @property
    def finished(self):
        return len(self.visible_text) >= len(self.text)

    @property
    def expired(self):
        return self.lifetime is not None and self.time_since_finish >= self.lifetime