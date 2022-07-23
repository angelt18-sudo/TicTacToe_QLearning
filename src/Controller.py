import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"   # Hide the welcome message from pygame

import sys
import pygame

import Constants

from TicTacToe import TicTacToe
from Player import Player
from Button import Button
from AgentQLearning import AgentQLearning

def main():
    """Initialize the screen and the pygame module."""
    # Initialize the pygame module
    pygame.init()
    # Load and set the logo
    logo = load_image(Constants.IMAGE_LOGO, 256, 256)
    pygame.display.set_icon(logo)
    pygame.display.set_caption(Constants.TITLE)
     
    # Set size of the screen
    screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))

    # Create the main screen
    main_screen(screen)

def load_image(dir, width, height):
    """Load the image.

    Params:
        ----------
        dir : str
            The direction of the image to load
        width : int
            The width of the image
        height : int
            The height of the image

        Returns
        -------
        img
            The image loaded
    """
    img = pygame.image.load(dir)
    img = pygame.transform.scale(img, (width, height)) # The image is resized
    return img

def get_font(size, font):
    """Loads and gets the font.

    Params:
    ----------
    size : int
        The size of the font
    font : string
        The direction of the font to be load'
    """
    return pygame.font.Font(font, size)

def exit():
    """End the application and the pygame module."""
    pygame.quit()
    sys.exit()

def main_screen(screen):
    """Creates the main menu (main screen).

    Params:
    ----------
    screen :
        The screen where draws the main menu
    """
    # Defines buttons and texts
    center_x = Constants.SCREEN_WIDTH/2

    title_text = get_font(Constants.SIZE_FONT_BIG, font=Constants.FONT_GAMES).render(Constants.TITLE, True, Constants.COLOR_TEXT)
    title_text_rect = title_text.get_rect(center=(center_x, 60))

    play_button = Button(image=load_image(Constants.IMAGE_PLAY_BUTTON, 330, 80), pos=(center_x, 160), 
                        text_input=Constants.PLAY, font=get_font(Constants.SIZE_FONT_BIG, font=Constants.FONT_GAMES), base_color=Constants.COLOR_BUTTON, hovering_color=Constants.WHITE)                
    qlearning_button = Button(image=load_image(Constants.IMAGE_OPTIONS_BUTTON, 420, 80), pos=(center_x, 330), 
                        text_input=Constants.Q_LEARNINNG, font=get_font(Constants.SIZE_FONT_BIG, font=Constants.FONT_GAMES), base_color=Constants.COLOR_BUTTON, hovering_color=Constants.WHITE)
    quit_button = Button(image=load_image(Constants.IMAGE_QUIT_BUTTON, 300, 90), pos=(center_x, 460), 
                        text_input=Constants.QUIT, font=get_font(Constants.SIZE_FONT_BIG, font=Constants.FONT_GAMES), base_color=Constants.COLOR_BUTTON, hovering_color=Constants.WHITE)
    
    mode = 'PLAYER VS PLAYER'
    mode_button = Button(image=load_image(Constants.IMAGE_PLAY_BUTTON, 400, 50), pos=(center_x, 240), 
                        text_input=mode, font=get_font(18, font=Constants.FONT_GAMES), base_color=Constants.COLOR_BUTTON, hovering_color=Constants.WHITE)   

    while True:
        
        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN: # Event click with the mouse
                if play_button.checkForInput(mouse_position):
                    # Starts game
                    if mode == 'PLAYER VS PLAYER':
                        p1 = Player()
                        p2 = Player()
                    elif mode == 'PLAYER (X) VS IA':
                        p1 = Player()
                        p2 = AgentQLearning()
                    elif mode == 'PLAYER (O) VS IA':
                        p1 = AgentQLearning()
                        p2 = Player()

                    retry = True
                    while retry:
                        winner = play_game(screen, p1, p2)
                        pygame.time.wait(1000)
                        retry = winner_screen(screen, winner)

                if mode_button.checkForInput(mouse_position):
                    # Change game mode
                    if mode == 'PLAYER VS PLAYER':
                        mode = 'PLAYER (X) VS IA'
                    elif mode == 'PLAYER (X) VS IA':
                        mode = 'PLAYER (O) VS IA'
                    elif mode == 'PLAYER (O) VS IA':
                        mode = 'PLAYER VS PLAYER'
                    mode_button.changeText(mode)

                if qlearning_button.checkForInput(mouse_position):
                    training_screen(screen, title_text, title_text_rect)
                    # Qlearning
                    train_q_learning(screen)

                if quit_button.checkForInput(mouse_position):
                    # Exit
                    exit()

        # Draws the background image
        screen.blit(Constants.BACKGROUND, (0, 0))
        screen.blit(title_text, title_text_rect)

        # Draws the buttons
        for button in [play_button, qlearning_button, quit_button, mode_button]:
            button.changeColor(mouse_position)
            button.update(screen)
        pygame.display.update()

def winner_screen(screen, winner):
    """Creates the winner screen.

    Params:
    ----------
    screen :
        The screen where draws the main menu
    winner : int or None
        None - tie
        1 - player 1 win
        2 - player 2 win

    Returns
    -------
    boolean
        Indicates if the player wants to play again    
    """
    
    center_x = Constants.SCREEN_WIDTH/2

    title_text = get_font(Constants.SIZE_FONT_BIG, font=Constants.FONT_GAMES).render(Constants.TITLE, True, Constants.COLOR_TEXT)
    title_text_rect = title_text.get_rect(center=(center_x, 60))

    if winner == 1:
        text = 'X WINNER!'
    elif winner == 2:
        text = 'O WINNER!'
    else:
        text = 'TIE!'

    winner_text = get_font(50, font=Constants.FONT_GAMES).render(text, True, Constants.WHITE)
    winner_text_rect = winner_text.get_rect(center=(center_x, 140))

    play_button = Button(image=load_image(Constants.IMAGE_PLAY_BUTTON, 420, 80), pos=(center_x, 250), 
                        text_input=Constants.PLAY_AGAIN, font=get_font(Constants.SIZE_FONT_BIG, font=Constants.FONT_GAMES), base_color=Constants.COLOR_BUTTON, hovering_color=Constants.WHITE)                
    menu_button = Button(image=load_image(Constants.IMAGE_OPTIONS_BUTTON, 420, 80), pos=(center_x, 350), 
                        text_input=Constants.MAIN_MENU, font=get_font(Constants.SIZE_FONT_BIG, font=Constants.FONT_GAMES), base_color=Constants.COLOR_BUTTON, hovering_color=Constants.WHITE)
    quit_button = Button(image=load_image(Constants.IMAGE_QUIT_BUTTON, 300, 90), pos=(center_x, 480), 
                        text_input=Constants.QUIT, font=get_font(Constants.SIZE_FONT_BIG, font=Constants.FONT_GAMES), base_color=Constants.COLOR_BUTTON, hovering_color=Constants.WHITE)
    
    while True:
        
        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN: # Event click with the mouse
                if play_button.checkForInput(mouse_position):
                    return True

                if menu_button.checkForInput(mouse_position):
                    return False

                if quit_button.checkForInput(mouse_position):
                    # Exit
                    exit()

        # Draws the background image
        screen.blit(Constants.BACKGROUND, (0, 0))
        screen.blit(title_text, title_text_rect)
        screen.blit(winner_text, winner_text_rect)

        for button in [play_button, menu_button, quit_button]:
            button.changeColor(mouse_position)
            button.update(screen)
        pygame.display.update()

def training_screen(screen, title_text, title_text_rect):
    """Creates the training screen. It shows a message of training

    Params:
    ----------
    screen :
        The screen where draws the main menu
    title_text : 
        The title of the screen
    title_text_rect :
        Position of the title
    """
    
    center_x = Constants.SCREEN_WIDTH/2
    center_y = Constants.SCREEN_HEIGHT/2

    training_text = get_font(25, font=Constants.FONT_GAMES).render('TRAINING...', True, Constants.WHITE)
    training_text_rect = training_text.get_rect(center=(center_x, center_y))

    # Draws the background image
    screen.blit(Constants.BACKGROUND, (0, 0))
    screen.blit(title_text, title_text_rect)
    screen.blit(training_text, training_text_rect)

    pygame.display.update()

def play_game(screen, p1, p2):
    """Run a complete tic tac toe game.

    Params:
    ----------
    screen :
        The screen where draws the main menu
    p1 :
        Player 1
    p2 :
        Player 2
    Returns
    -------
    int or None
        None - tie
        1 - player 1 win
        2 - player 2 win 
    """

    # Initialize the game
    game = TicTacToe()
    board, turn = game.get_board(), game.get_turn()

    game.render(screen)

    done = False

    while not done:

        if turn:
            action = p1.movement(board)
        else:
            action = p2.movement(board)

        board, done, reward, info = game.step(action)
        turn = info['turn']
        winner = info['winner']
        game.render(screen)

    return winner

def train_q_learning(screen, iterations=100000):
    """Trains the qlearning algorithm to play tic tac toe.

    Params:
    ----------
    screen :
        The screen where draws the main menu
    iterations : int
        Number of iterations of training
    """
    
    player = AgentQLearning()
    greedy = 0.25

    for i in range(iterations):
        alpha = 0.5
        discount_factor = 0.9

        game = TicTacToe()
        state, turn = game.get_board().copy(), game.get_turn()

        action = player.random_movement(state)
        n_state, _, reward, _ = game.step(action)
        done = False
        while not done:

            action2 = player.movement(n_state, greedy)
            n_state2, done, reward2, info = game.step(action2)
            winner = info['winner']

            if done:
                q_value = (1-alpha)*player.get_qvalue(n_state, action2) + alpha*(reward2)
                player.update_qvalue(q_value, n_state, action2)

                if winner != None:
                    reward2 = -reward2
                q_value = (1-alpha)*player.get_qvalue(state, action) + alpha*(reward2)
                player.update_qvalue(q_value, state, action)
            else:
            
                # Update Q
                q_value = (1-alpha)*player.get_qvalue(state, action) + alpha*(reward2 + discount_factor*player.get_qvalue_max(n_state2))
                player.update_qvalue(q_value, state, action)

                state = n_state.copy()
                n_state = n_state2.copy()

                action = action2

                reward = reward2

            #game.render(screen)
            #pygame.time.wait(1000)

    player.write_qtable()
    print('The training has finished')
    #print(player.Q_table)

# Starts the API
if __name__ == "__main__":
    main()

