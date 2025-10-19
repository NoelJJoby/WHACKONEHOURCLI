import curses
import random


MAP_WIDTH = 40
MAP_HEIGHT = 20



def create_map():
    """Create a simple map with walls and floors."""
    game_map = [['#' if x == 0 or y == 0 or x == MAP_WIDTH - 1 or y == MAP_HEIGHT - 1 else '.' 
                 for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]

    
    for _ in range(60):
        x = random.randint(1, MAP_WIDTH - 2)
        y = random.randint(1, MAP_HEIGHT - 2)
        game_map[y][x] = '#'
    return game_map

def draw_map(stdscr, game_map, player_x, player_y, enemies):
    for y, row in enumerate(game_map):
        for x, ch in enumerate(row):
            stdscr.addch(y, x, ch)
    
    
    
    for e in enemies:
        stdscr.addch(e["y"], e["x"], e["char"])
        
    stdscr.addch(player_y, player_x, '@') 



def move_enemies(enemies, player_x, player_y, game_map):
    for e in enemies:
        dx = 0
        dy = 0
        if e["x"] < player_x: dx = 1
        elif e["x"] > player_x: dx = -1
        if e["y"] < player_y: dy = 1
        elif e["y"] > player_y: dy = -1

        new_x = e["x"] + dx
        new_y = e["y"] + dy

        
        if game_map[new_y][new_x] == '.':
            e["x"], e["y"] = new_x, new_y


def check_combat(player_x, player_y, enemies):
    for e in enemies:
        if e["x"] == player_x and e["y"] == player_y:
            enemies.remove(e)
            return True
    return False



def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    game_map = create_map()
    player_x, player_y = MAP_WIDTH // 2, MAP_HEIGHT // 2

    enemies = [
        {"x": 10, "y": 5, "char": "E"},
        {"x": 25, "y": 1, "char": "E"},
        {"x": 30, "y": 9, "char": "E"},
        {"x": 20, "y": 8, "char": "E"},
        {"x": 18, "y": 7, "char": "E"},
    ]
    message = ""

    while True:
        stdscr.clear()
        draw_map(stdscr, game_map, player_x, player_y, enemies)
        stdscr.addstr(MAP_HEIGHT, 0, message[:40])  # display message
        stdscr.refresh()

        key = stdscr.getch()
        if key in [ord('q'), 27]: break

        new_x, new_y = player_x, player_y
        if key in [ord('w'), curses.KEY_UP]: new_y -= 1
        elif key in [ord('s'), curses.KEY_DOWN]: new_y += 1
        elif key in [ord('a'), curses.KEY_LEFT]: new_x -= 1
        elif key in [ord('d'), curses.KEY_RIGHT]: new_x += 1

        if game_map[new_y][new_x] == '.':
            if check_combat(new_x, new_y, enemies):
                message = "💥 You defeated an enemy!"
            else:
                player_x, player_y = new_x, new_y
                message = ""
                
        move_enemies(enemies, player_x, player_y, game_map)

        if not enemies:
            message = "🎉 You defeated all enemies! You win!"
            stdscr.clear()
            draw_map(stdscr, game_map, player_x, player_y, enemies)
            stdscr.addstr(MAP_HEIGHT + 1, 0, message)
            stdscr.refresh()
            stdscr.getch()  # wait for a key press
            break
                

if __name__ == "__main__":
    curses.wrapper(main)