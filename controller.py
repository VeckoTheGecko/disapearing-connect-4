from model import Model
from view import View
import pygame
import sys


class Controller:
    def __init__(self, model=Model(), view=View()):
        self.model = model
        self.view = view
        self.actions = {
            "place": [pygame.K_DOWN, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_s],
            "move_left": [pygame.K_LEFT, pygame.K_a],
            "move_right": [pygame.K_RIGHT, pygame.K_d],
            "move_number": [
                pygame.K_0,
                pygame.K_1,
                pygame.K_2,
                pygame.K_3,
                pygame.K_4,
                pygame.K_5,
                pygame.K_6,
                pygame.K_7,
                pygame.K_8,
                pygame.K_9,
            ],
            "reset": [pygame.K_r],
        }

    def reset_board(self):
        self.model = Model()
        return

    def game_loop(self):
        in_game = True
        turn = "red"
        while True:  # Game is exit using a return statement inside
            placing_token = False

            events = pygame.event.get()
            current_pos = self.model.get_position()
            # Processing events
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key in self.actions["place"]:
                        if self.model.place_token(
                            token=turn, col=current_pos
                        ):  # if its successful
                            placing_token = True

                    elif event.key in self.actions["move_left"]:
                        self.model.move_left()

                    elif event.key in self.actions["move_right"]:
                        self.model.move_right()

                    elif event.key in self.actions["move_number"]:
                        key_pressed = self.actions["move_number"].index(event.key)
                        self.model.set_position(key_pressed)

                    elif event.key in self.actions["reset"]:
                        self.reset_board()
                        in_game = True
                        turn = "red"

                elif event.type == pygame.QUIT:
                    # Exits out the game when the x is pressed.
                    pygame.exit()
                    sys.exit()

            if in_game:
                self.view.render_board(self.model.board)

                if placing_token:
                    self.view.play_click()

                    # checking that the game is still running
                    if self.model.is_win(
                        turn_color=turn, col=self.model.get_position()
                    ):
                        self.view.render_outcome(win=turn)
                        in_game = False

                    if self.model.board_is_full():
                        self.view.render_outcome(win=None)
                        in_game = False
                    # Updating display
                    pygame.display.update()
                    # Switching turns
                    if turn == "yellow":
                        turn = "red"
                    else:
                        turn = "yellow"


if __name__ == "__main__":
    controller = Controller(model=Model(), view=View())
    controller.game_loop()
