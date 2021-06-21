import sys
import tkinter
import tkinter.messagebox
import pygame
import board

darkcolor = (0, 0, 0)
lightcolor = (54, 5, 69)
cyan = (0, 190, 197)
magenta = (255, 11, 235)

class Pane:
    def __init__(self, row_count, column_count, square_size):
        self.board = board.Board(row_count, column_count)
        self.square_size = square_size
        self.radius = square_size // 2 - 5
        self.width = column_count * square_size
        self.height = (row_count + 1) * square_size  
        self.offset = square_size  
        self.circle_offset = square_size // 2 
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_background(self):
        for r in range(self.board.row_count):
            for c in range(self.board.column_count):
                left = c * self.square_size
                top = r * self.square_size + self.offset
                pygame.draw.rect(self.screen, lightcolor, (left, top, self.square_size, self.square_size))
                pygame.draw.circle(self.screen, darkcolor, (left + self.circle_offset, top + self.circle_offset), self.radius)
        pygame.display.update()

    def fill_in_pieces(self):
        for r in range(self.board.row_count):
            for c in range(self.board.column_count):
                if self.board.grid[r, c] == 1:
                    current_color = cyan
                elif self.board.grid[r, c] == 2:
                    current_color = magenta
                else:
                    current_color = darkcolor
                x_position = c * self.square_size + self.circle_offset
                y_position = self.height - (r * self.square_size + self.circle_offset)  
                pygame.draw.circle(self.screen, current_color, (x_position, y_position), self.radius)
        pygame.display.update()

    def track_mouse_motion(self, x_position, current_color):
        pygame.draw.rect(self.screen, darkcolor, (0, 0, self.width, self.square_size)) 
        pygame.draw.circle(self.screen, current_color, (x_position, self.circle_offset), self.radius)
        pygame.display.update()

    def try_drop_piece(self, x_position, turn):
        column_selection = x_position // self.square_size
        if self.board.is_valid_location(column_selection):
            row = self.board.get_next_open_row(column_selection)
            self.board.drop_piece(row, column_selection, turn)
            return True
        return False

    def reset(self):
        self.screen = pygame.display.set_mode((self.width, self.height))  # Gives Pygame focus again
        self.board.reset()
        self.draw_background()
        self.fill_in_pieces()


def prompt_player(winner = False):
    title = 'Game Over!'
    if winner:
        message = f'Player {winner} wins! Would you like to start again?'
    else:
        message = 'The match was a draw. Would you like to start again?'
    return tkinter.messagebox.askyesno(title=title, message=message)

def main():
    tkinter.Tk().wm_withdraw()
    pygame.init()
    pygame.display.set_caption('Connect 4')
    pane = Pane(6, 7, 90)
    pane.draw_background()
    continue_playing = True
    turn = 1
    current_color = cyan

    while continue_playing:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                pane.track_mouse_motion(event.pos[0], current_color)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pane.try_drop_piece(event.pos[0], turn):
                    pane.fill_in_pieces()
                    if pane.board.has_four_in_a_row(turn): 
                        continue_playing = prompt_player(turn)
                        pane.reset()
                    elif pane.board.is_full():  
                        continue_playing = prompt_player()
                        pane.reset()
                    else:  
                        turn = 1 if turn == 2 else 2  
                        current_color = cyan if turn == 1 else magenta 
                        pane.track_mouse_motion(event.pos[0], current_color) 


if __name__ == "__main__":
    main()