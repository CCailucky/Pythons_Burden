from settings import GRID_WIDTH, GRID_HEIGHT

def move_snake(
    snake_body: list[tuple[int, int]], next_head: tuple[int, int], should_grow: bool
) -> None:
    snake_body.insert(0, next_head)  # insert new head into snake_body[0]
    if not should_grow:
        snake_body.pop()  # pop the tail


def get_next_head_pos(
    snake_body: list[tuple[int, int]], direction: tuple[int, int]
) -> tuple[int, int]:
    head_x, head_y = snake_body[0]
    move_x, move_y = direction

    next_head = (head_x + move_x, head_y + move_y)
    # check whether quantum transit is triggered
    next_head = quantum_transit(next_head)

    return next_head


# transit the snake from one place to another place
def quantum_transit(position: tuple[int, int]) -> tuple[int, int]:
    x, y = position

    if x < 0:
        x = GRID_WIDTH - 1
    elif x >= GRID_WIDTH:
        x = 0
    if y < 0:
        y = GRID_HEIGHT - 1
    elif y >= GRID_HEIGHT:
        y = 0
    return (x, y)
    
def check_self_collision(
    next_head: tuple[int, int], snake_body: list[tuple[int, int]], apple_eaten: bool
) -> bool:
    # tail wont disappear so the tail will be included to check the collision
    if apple_eaten:
        return next_head in snake_body
    # snake_body[:-1] for NO collision with the tail, because the tail will disappear in the next move
    return next_head in snake_body[:-1]


def reset_snake(
    directions: dict[str, tuple[int, int]],
) -> tuple[list[tuple[int, int]], tuple[int, int]]:
    snake_body = [(20, 20), (19, 20), (18, 20), (17, 20), (16, 20)]
    direction = directions["RIGHT"]

    return snake_body, direction