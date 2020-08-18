import tkinter as tk
import numpy as np
import random

UPDATE_RATE = 150
direct = 'east'
grow = False
snake_pos = np.array([[0,2],[0,1],[0,0]])
board_mat = np.array([])
cell_rc = 0
apple_pos = [1, 1]
grid_top_x = 50
grid_top_y = 50
cell_size = 30
grid_bboxes = np.array([])
changes = {
    "northw": "north",
    "norths": "north",
    "northa": "west",
    "northd": "east",
    "eastw": "north", 
    "easts": "south", 
    "easta": "east",       
    "eastd": "east",
    "southw": "south",
    "souths": "south",
    "southa": "west",
    "southd": "east",
    "westw": "north",
    "wests": "south",
    "westa": "west",
    "westd": "west"
}
move_keys = {
    "Up": "w",
    "Left": "a",
    "Down": "s",
    "Right": "d"
}
started = False

class Application(tk.Canvas):
    def __init__(self, master):
        """Initialize the Frame"""
        #making Application class as a subclass of Canvas
        tk.Canvas.__init__(self, master)
        self.canvas = tk.Canvas(master, width=550, height=500)
        self.canvas.pack()
        self.pack()
        global grid_bboxes
        if grid_bboxes.shape[0] == 0:
            self.grid_mat()

    def _close(self): 
        self.quit()
    
    #these functions move the snake at an interval of 1 second in the direction the snake is pointed(either by user or default)
    def default_move(self):
        global direct
        self.movement()
        #print(direct)
        
    def updater(self):
        self.update_canvas()
        self.default_move()
        self.after(UPDATE_RATE, self.updater)

    def start_game(self):
        self.updater()

    #creating matrix which holds the box positions of the respective grid positions 
    def grid_mat(self):
        global grid_top_x
        global grid_top_y
        global cell_size
        global cell_rc
        global grid_bboxes
        grid_bboxes = np.zeros(cell_rc, dtype=object)
        top_x = grid_top_x
        top_y = grid_top_y
        bot_x = grid_top_x + cell_size
        bot_y = grid_top_x + cell_size
        for i in range(cell_rc[0]):
            for j in range(cell_rc[1]):
                grid_bboxes[i,j] = (top_x, top_y, bot_x, bot_y)
                top_x += cell_size
                bot_x += cell_size
            top_x = 50
            bot_x = 80
            top_y += cell_size
            bot_y += cell_size
        return(grid_bboxes)

    #creating snake grid
    def create_grid(self, canvas, x, y, cell_size, grid_size, board_height, board_width):
        for i in range(0, grid_size + 1, cell_size):
            canvas.create_line(x, y + i, board_width, y + i)
            canvas.create_line(x + i, y, x + i, board_height)

    #functions involving key presses
    def update_direct(self, direct_change='none'):
        global direct
        global changes
        if (direct_change == 'none'):
            print("only  this printed" + direct)
            return

        direct = changes[direct + direct_change]

    def key_press(self, event):
        global started
        global move_keys
        if event.keysym=="space" and not started:
            self.start_game()
            started='True'
            return
        if event.keysym=='Escape':
            self._close()
        if event.keysym in "wasd":
            self.update_direct(event.keysym)
            return

        if event.keysym in move_keys.keys():
            self.update_direct(move_keys[event.keysym])


    #movement functions
    def update_mat_snake(self):
        global board_mat           
        global snake_pos
        global cell_rc
        global apple_pos
        board_mat = np.zeros(cell_rc)
        for i in range(snake_pos.shape[0]):
            if i == 0:
                board_mat[snake_pos[i,0],snake_pos[i,1]] = 2
            else:
                board_mat[snake_pos[i,0],snake_pos[i,1]] = 1

    def update_mat_full(self):
        self.update_mat_snake()
        global board_mat           
        global apple_pos
        if board_mat[apple_pos[0], apple_pos[1]] == 0:
            board_mat[apple_pos[0], apple_pos[1]] = 3

    def apple_picker(self):
        global board_mat
        global apple_pos
        self.canvas.delete('apple')
        open_raw = np.where(board_mat == 0)
        open_pos = list(zip(open_raw[0], open_raw[1]))

        apple_pos = random.choice(open_pos)

    #this is the key for updating the snake position
    def change_pos(self):
        global cell_rc
        global direct
        global snake_pos
        global grow

        #needs more options for whne you go off board
        new_snake = snake_pos
        snake_head = np.array([snake_pos[0,0], snake_pos[0,1]])
        if not grow:
            new_snake = np.delete(new_snake, -1, 0)
        grow = False

        if direct=="north":
            snake_head[0,] -= 1
        elif direct=="east":
            snake_head[1,] += 1
        elif direct=="south":
            snake_head[0,] += 1
        else:
            snake_head[1,] -= 1
        #find a way to optimize this (probably for loop)
        if snake_head[0,]==-1:
            snake_head[0,]=cell_rc[0]-1
        elif snake_head[0,]==cell_rc[0]:
            snake_head[0,]=0
        if snake_head[1,]==-1:
            snake_head[1,]=cell_rc[1]-1
        elif snake_head[1,]==cell_rc[1]:
            snake_head[1,]=0
        
        new_snake = np.insert(new_snake, 0, snake_head, axis = 0)
        snake_pos = new_snake

    def snake_killer(self):
        global snake_pos       
        snake_unique = np.unique(snake_pos, axis=0)
        return snake_pos.shape[0] != snake_unique.shape[0]



    def movement(self):
        global cell_rc
        global direct
        global snake_pos
        global apple_pos
        global grow

        #new_direct = update_direct(direct_change, direct)
        self.change_pos()
        
        if self.snake_killer():
            print("Game over")
            #return "quit"
            self._close()
            #self.destroy()

        self.update_mat_full()

        #growth condition checker
        if (snake_pos[0, 0], snake_pos[0, 1]) == apple_pos:
            grow = True
            self.apple_picker()

    def update_canvas(self):
        global grid_bboxes
        global board_mat
        global apple_pos
        global snake_pos

        self.canvas.delete('snake')
        for i in range(snake_pos.shape[0]):
            bbox = grid_bboxes[snake_pos[i,0], snake_pos[i,1]]
            self.canvas.create_rectangle(bbox, fill="green", tags='snake')
        
        bbox = grid_bboxes[apple_pos[0], apple_pos[1]]
        self.canvas.create_rectangle(bbox, fill="red", tags='apple')


def main():
    global board_mat
    global apple_pos
    global started
    global cell_rc
    global grid_bboxes

    master = tk.Tk()
    master.title("Snake Game")

    
    if not started:
        w = tk.Label(master, text="Press Space to Start\nPress Esc to Close Game", bg="grey", fg="white",font=("Helvetica", 16))
        w.pack()

    board_height = 500
    board_width = 500
    grid_size = 450

    cell_rc = (int(grid_size/cell_size), int(grid_size/cell_size))

    app = Application(master)

    app.create_grid(app.canvas, grid_top_x, grid_top_y, cell_size, grid_size, board_height, board_width)

    master.bind('<Key>', app.key_press)

    # set window size
    master.geometry("550x600")

    app.update_mat_snake()
    app.apple_picker()
    app.update_mat_full()
    app.update_canvas()
    
    master.mainloop()


if __name__ == '__main__':
    main()