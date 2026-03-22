import random
import pygame


class Background:
    def __init__(self, width, height, image_path):
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.meteor_count = 30
        self.min_speed = 4
        self.max_speed = 11
        self.min_length = 12
        self.max_length = 30
        self.meteors = [self._spawn_meteor(initial=True) for _ in range(self.meteor_count)]

    def _spawn_meteor(self, initial=False):
        if initial:
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
        else:
            x = random.uniform(-120, self.width)
            y = random.uniform(-120, -20)

        return {
            "x": x,
            "y": y,
            "speed": random.uniform(self.min_speed, self.max_speed),
            "length": random.randint(self.min_length, self.max_length),
            "thickness": random.randint(1, 2),
        }

    def _update_meteors(self):
        for index, meteor in enumerate(self.meteors):
            meteor["x"] += meteor["speed"] * 0.35
            meteor["y"] += meteor["speed"]

            is_out_of_screen = (
                meteor["y"] - meteor["length"] > self.height
                or meteor["x"] - meteor["length"] > self.width
            )
            if is_out_of_screen:
                self.meteors[index] = self._spawn_meteor()

    def _draw_meteors(self, screen):
        for meteor in self.meteors:
            head = (int(meteor["x"]), int(meteor["y"]))
            tail = (
                int(meteor["x"] - meteor["length"] * 0.6),
                int(meteor["y"] - meteor["length"]),
            )

            pygame.draw.line(screen, (210, 230, 255), head, tail, meteor["thickness"])
            pygame.draw.circle(screen, (255, 255, 255), head, 1 + meteor["thickness"])

    def draw(self, screen):
        # Vẽ nền tĩnh
        screen.blit(self.image, (0, 0))

        # Cập nhật và vẽ hiệu ứng mưa sao băng
        self._update_meteors()
        self._draw_meteors(screen)