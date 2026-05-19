from pathlib import Path
import pygame

from settings import GRID_SIZE

# image cache is used for loading an image only once
IMAGE_CACHE = {}


def load_grid_image(relative_path: str) -> pygame.Surface | None:
    # base directory: Python's Burden/
    base_dir = Path(__file__).resolve().parent
    image_path = base_dir / relative_path

    if not image_path.exists():
        print(f"Missing image: {image_path}")
        return None

    if relative_path not in IMAGE_CACHE:
        image = pygame.image.load(str(image_path)).convert_alpha()
        image = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
        IMAGE_CACHE[relative_path] = image

    return IMAGE_CACHE[relative_path]

def rotate_snake_image_by_direction(
    image: pygame.Surface,
    direction: tuple[int, int],
) -> pygame.Surface:
    if direction == (1, 0):      # right
        return image
    if direction == (0, -1):     # up
        return pygame.transform.rotate(image, 90)
    if direction == (-1, 0):     # left
        return pygame.transform.rotate(image, 180)
    if direction == (0, 1):      # down
        return pygame.transform.rotate(image, -90)

    return image


def get_snake_tail_direction(
    previous_segment: tuple[int, int],
    tail_segment: tuple[int, int],
) -> tuple[int, int]:
    # vector
    dx = tail_segment[0] - previous_segment[0]
    dy = tail_segment[1] - previous_segment[1]

    # handle quantum transit wrap-around
    if dx > 1:
        dx = -1
    elif dx < -1:
        dx = 1
    if dy > 1:
        dy = -1
    elif dy < -1:
        dy = 1

    return (dx, dy)


def rotate_bullet_image_by_direction(
    image: pygame.Surface | None,
    direction: tuple[int, int],
) -> pygame.Surface | None:
    if image is None:
        return None

    if direction == (0, -1):     # up
        return image

    if direction == (1, 0):      # right
        return pygame.transform.rotate(image, -90)

    if direction == (0, 1):      # down
        return pygame.transform.rotate(image, 180)

    if direction == (-1, 0):     # left
        return pygame.transform.rotate(image, 90)

    return image