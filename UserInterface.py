import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import random
import tkinter as tk
from tkinter import messagebox

def launch_tic_tac_toe():
    # Constantes
    GRID_SIZE = 3
    PLAYER_SYMBOLS = ["X", "O"]
    BUTTON_FONT = ("Arial", 20)
    PLAYER_COLORS = {"X": "red", "O": "green"}

    def check_winner():
        nonlocal winner
        # Vérification des lignes, colonnes et diagonales
        for i in range(GRID_SIZE):
            if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
                winner = buttons[i][0]["text"]
                return True
            if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
                winner = buttons[0][i]["text"]
                return True
        if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
            winner = buttons[0][0]["text"]
            return True
        if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
            winner = buttons[0][2]["text"]
            return True
        return False

    def check_draw():
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if buttons[row][col]["text"] == "":
                    return False
        return True

    def clicked(row, col):
        nonlocal current_player, winner
        if buttons[row][col]["text"] == "" and not winner:
            buttons[row][col]["text"] = current_player
            buttons[row][col]["fg"] = PLAYER_COLORS[current_player]  # Changer la couleur du texte pour le joueur actuel
            if check_winner():
                messagebox.showinfo("Jeu terminé", f"Le joueur {winner} a gagné !")
                reset_game()
            elif check_draw():
                messagebox.showinfo("Jeu terminé", "Match nul !")
                reset_game()
            else:
                current_player = PLAYER_SYMBOLS[(PLAYER_SYMBOLS.index(current_player) + 1) % len(PLAYER_SYMBOLS)]
                label_player.config(text=f"Joueur actuel : {current_player}")

    def reset_game():
        nonlocal current_player, winner
        current_player = PLAYER_SYMBOLS[0]
        winner = ""
        label_player.config(text=f"Joueur actuel : {current_player}")
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                buttons[row][col]["text"] = ""
                buttons[row][col]["fg"] = "black"  # Réinitialiser la couleur du texte

    # Création de la fenêtre principale
    window = tk.Tk()
    window.title("Tic Tac Toe")

    # Initialisation des variables
    current_player = PLAYER_SYMBOLS[0]
    winner = ""

    # Création des boutons du jeu
    buttons = []
    for row in range(GRID_SIZE):
        button_row = []
        for col in range(GRID_SIZE):
            button = tk.Button(window, text="", font=BUTTON_FONT, width=4, height=2,
                               command=lambda row=row, col=col: clicked(row, col), bg="lightgray")
            button.grid(row=row, column=col, padx=5, pady=5)
            button_row.append(button)
        buttons.append(button_row)

    # Étiquette pour afficher le joueur actuel
    label_player = tk.Label(window, text=f"Joueur actuel : {current_player}", font=("Arial", 16))
    label_player.grid(row=GRID_SIZE, column=0, columnspan=GRID_SIZE, pady=10)

    # Bouton de réinitialisation
    reset_button = tk.Button(window, text="Nouvelle partie", font=("Arial", 12), command=reset_game)
    reset_button.grid(row=GRID_SIZE+1, column=0, columnspan=GRID_SIZE, pady=10)

    # Lancement de la boucle principale
    window.mainloop()

# Lancer la fonction pour jouer au jeu du morpion
launch_tic_tac_toe()




def launch_snake_game():
    # Initialize Pygame
    pygame.init()

    # Screen settings
    WIDTH, HEIGHT = 640, 480
    FPS = 10
    GRID_SIZE = 20
    GRID_WIDTH = WIDTH // GRID_SIZE
    GRID_HEIGHT = HEIGHT // GRID_SIZE

    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)

    # Create window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    # Function to draw obstacles
    def draw_obstacles(obstacles):
        for obstacle in obstacles:
            pygame.draw.rect(screen, WHITE, (obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Main game function
    def game():
        snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        snake_direction = (1, 0)  # Initial direction: right
        apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        score = 0
        game_over = False

        # Distribute obstacles systematically with some spacing
        obstacles = []
        spacing = 4  # Adjust spacing as needed
        for x in range(0, GRID_WIDTH, spacing):
            for y in range(0, GRID_HEIGHT, spacing):
                # Exclude the initial snake position and apple position
                if (x, y) not in snake and (x, y) != apple:
                    obstacles.append((x, y))

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake_direction != (0, 1):
                        snake_direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                        snake_direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                        snake_direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                        snake_direction = (1, 0)

            snake_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])

            # Collision with screen edges
            if (snake_head[0] < 0 or snake_head[0] >= GRID_WIDTH or
                    snake_head[1] < 0 or snake_head[1] >= GRID_HEIGHT):
                game_over = True

            # Collision with itself or obstacles
            if snake_head in snake[1:] or snake_head in obstacles:
                game_over = True

            # Move the snake
            snake.insert(0, snake_head)

            # Collision with apple and update score
            if snake_head == apple:
                score += 1
                apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            else:
                snake.pop()

            # Display
            screen.fill(BLACK)  # Clear the screen

            # Draw obstacles
            draw_obstacles(obstacles)

            # Draw snake
            for segment in snake:
                pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # Draw apple
            pygame.draw.rect(screen, RED, (apple[0] * GRID_SIZE, apple[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # Display score
            font = pygame.font.Font(None, 36)
            text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(text, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

    # Launch the game
    game()

# Lancer la fonction pour jouer au jeu Snake
if __name__ == "__main__":
    launch_snake_game()



def launch_guess_the_number():
    # Initialisation de Pygame
    pygame.init()

    # Paramètres de l'écran
    WIDTH, HEIGHT = 420, 300
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (220, 220, 220)
    GREEN = (0, 200, 0)
    FPS = 60

    # Charger l'image de fond
    background = pygame.image.load('background.jpg')  # Remplacez 'background_image.jpg' par le chemin de votre image
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Fenêtre de configuration
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Guess the Number Game")
    clock = pygame.time.Clock()

    # Variables du jeu
    number_to_guess = random.randint(0, 100)
    guesses = 0
    user_input = ""
    font = pygame.font.Font(None, 36)

    # Textes
    instruction_text = font.render("Guess a number between 0 and 100", True, BLACK)
    result_text = None
    success = False

    # Boucle principale du jeu
    running = True
    while running:
        screen.blit(background, (0, 0))  # Afficher l'image de fond

        # Affichage des éléments textuels
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, 20))
        if result_text:
            screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 100))

        # Création du bouton stylisé
        pygame.draw.rect(screen, GRAY, (150, 200, 100, 50))
        submit_text = font.render("Submit", True, BLACK)
        screen.blit(submit_text, (175, 210))

        # Affichage de la zone de saisie utilisateur
        input_rect = pygame.Rect(20, 150, 360, 30)
        pygame.draw.rect(screen, WHITE, input_rect, 2)  # Rectangle pour l'entrée utilisateur
        input_text = font.render(user_input, True, BLACK)
        screen.blit(input_text, (input_rect.x + 5, input_rect.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not success:
                    if event.key == pygame.K_RETURN:
                        guesses += 1
                        try:
                            user_guess = int(user_input)
                            if user_guess == number_to_guess:
                                success = True
                                result_text = font.render(
                                    f"Congratulations! You guessed it in {guesses} tries. The number was {number_to_guess}.",
                                    True, GREEN)
                            elif user_guess < number_to_guess:
                                result_text = font.render("The number is higher", True, BLACK)
                            else:
                                result_text = font.render("The number is lower", True, BLACK)
                        except ValueError:
                            result_text = font.render("Please enter a valid number!", True, BLACK)
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        # Vérifie si la touche pressée est un chiffre et ajoute au texte utilisateur
                        if event.unicode.isdigit() and len(user_input) < 3:  # Limite à 3 chiffres
                            user_input += event.unicode

                elif event.key == pygame.K_RETURN:
                    # Réinitialiser le jeu
                    number_to_guess = random.randint(0, 100)
                    guesses = 0
                    user_input = ""
                    result_text = None
                    success = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 150 < mouse_pos[0] < 250 and 200 < mouse_pos[1] < 250 and not success:
                    guesses += 1
                    try:
                        user_guess = int(user_input)
                        if user_guess == number_to_guess:
                            success = True
                            result_text = font.render(
                                f"Congratulations! You guessed it in {guesses} tries. The number was {number_to_guess}.",
                                True, GREEN)
                        elif user_guess < number_to_guess:
                            result_text = font.render("The number is higher", True, BLACK)
                        else:
                            result_text = font.render("The number is lower", True, BLACK)
                    except ValueError:
                        result_text = font.render("Please enter a valid number!", True, BLACK)
                    user_input = ""

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Lancer la fonction pour jouer au jeu Guess the Number
if __name__ == "__main__":
    launch_guess_the_number()

def launch_rock_paper_scissors():
    def get_computer_choice():
        choices = ['pierre', 'papier', 'ciseaux']
        return random.choice(choices)

    def determine_winner(user_choice, computer_choice):
        if user_choice == computer_choice:
            return "Égalité !"
        elif (user_choice == 'pierre' and computer_choice == 'ciseaux') or \
             (user_choice == 'papier' and computer_choice == 'pierre') or \
             (user_choice == 'ciseaux' and computer_choice == 'papier'):
            return "Vous avez gagné !"
        else:
            return "L'ordinateur a gagné !"

    def play_game(user_choice):
        computer_choice = get_computer_choice()
        result = determine_winner(user_choice, computer_choice)
        result_label.config(text=result)
        computer_choice_label.config(text=f"L'ordinateur a choisi : {computer_choice}")

    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Jeu Pierre-Papier-Ciseaux")

    # Configuration du style
    root.configure(bg="#f0f0f0")  # Couleur de fond de la fenêtre principale
    button_bg_color = "#4caf50"  # Couleur de fond des boutons
    button_fg_color = "white"  # Couleur du texte des boutons
    font_style = ("Arial", 12)  # Style de police

    # Affichage du choix de l'utilisateur
    user_choice_label = tk.Label(root, text="Votre choix :", font=font_style, bg="#f0f0f0")
    user_choice_label.pack()

    # Affichage du choix de l'ordinateur
    computer_choice_label = tk.Label(root, text="Choix de l'ordinateur :", font=font_style, bg="#f0f0f0")
    computer_choice_label.pack()

    # Affichage du résultat
    result_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f0f0")
    result_label.pack(pady=20)

    # Fonction appelée lors du clic sur les boutons
    def on_choice_click(choice):
        play_game(choice)

    # Création des boutons pour les choix
    choices_frame = tk.Frame(root, bg="#f0f0f0")
    choices_frame.pack(padx=20, pady=10)

    rock_button = tk.Button(choices_frame, text="Pierre", command=lambda: on_choice_click('pierre'), bg=button_bg_color, fg=button_fg_color, font=font_style)
    rock_button.pack(side=tk.LEFT, padx=5)

    paper_button = tk.Button(choices_frame, text="Papier", command=lambda: on_choice_click('papier'), bg=button_bg_color, fg=button_fg_color, font=font_style)
    paper_button.pack(side=tk.LEFT, padx=5)

    scissors_button = tk.Button(choices_frame, text="Ciseaux", command=lambda: on_choice_click('ciseaux'), bg=button_bg_color, fg=button_fg_color, font=font_style)
    scissors_button.pack(side=tk.LEFT, padx=5)

    # Lancement de la boucle principale
    root.mainloop()

# Lancer le jeu
if __name__ == "__main__":
    launch_rock_paper_scissors()


def hangman():
    def check_guess():
        nonlocal attempts_left
        nonlocal guessed_letters
        nonlocal guessed_word
        nonlocal game_over

        user_guess = entry.get().lower()
        entry.delete(0, tk.END)

        if user_guess == chosen_word:
            message_label.config(text="Félicitations ! Vous avez deviné le mot correctement.")
            game_over = True
        elif len(user_guess) == 1 and user_guess.isalpha():
            if user_guess in guessed_letters:
                message_label.config(text="Vous avez déjà deviné cette lettre.")
            elif user_guess not in chosen_word:
                message_label.config(text=f"La lettre '{user_guess}' n'est pas dans le mot.")
                guessed_letters.append(user_guess)
                attempts_left -= 1
                attempts_label.config(text=f"Essais restants : {attempts_left}")
                if attempts_left == 0:
                    message_label.config(text=f"Vous avez utilisé tous vos essais. Le mot était: {chosen_word}")
                    game_over = True
            else:
                message_label.config(text=f"Bonne devinette ! La lettre '{user_guess}' est dans le mot.")
                guessed_letters.append(user_guess)
                for i in range(word_length):
                    if chosen_word[i] == user_guess:
                        guessed_word[i] = user_guess
                if '_' not in guessed_word:
                    message_label.config(text="Félicitations ! Vous avez deviné le mot correctement.")
                    game_over = True
        else:
            message_label.config(text="Veuillez entrer une lettre valide ou devinez le mot complet.")

        if game_over:
            entry.config(state='disabled')
            button.config(state='disabled')

        word_label.config(text=' '.join(guessed_word))
        guessed_label.config(text=f"Lettres devinées: {' '.join(guessed_letters)}")

    window = tk.Tk()
    window.title("Jeu du pendu")

    words = ['python', 'programmation', 'ordinateur', 'jeu', 'apprentissage', 'développement', 'openai', 'intelligence']
    chosen_word = random.choice(words)
    word_length = len(chosen_word)
    attempts_left = 6
    guessed_letters = []
    guessed_word = ['_'] * word_length
    game_over = False

    word_label = tk.Label(window, text=' '.join(guessed_word), font=('Arial', 18))
    word_label.pack(pady=10)

    guessed_label = tk.Label(window, text=f"Lettres devinées: {' '.join(guessed_letters)}", font=('Arial', 12))
    guessed_label.pack()

    attempts_label = tk.Label(window, text=f"Essais restants : {attempts_left}", font=('Arial', 12))
    attempts_label.pack()

    entry = tk.Entry(window, font=('Arial', 14), width=10)
    entry.pack(pady=10)

    button = tk.Button(window, text="Devinez", font=('Arial', 14), command=check_guess)
    button.pack()

    message_label = tk.Label(window, text="", font=('Arial', 12))
    message_label.pack()

    window.mainloop()
# Lancer le jeu
if __name__ == "__main__":
    hangman()
def choose_game():
    def launch_selected_game(game):
        if game == "Tic Tac Toe":
            launch_tic_tac_toe()
        elif game == "Snake Game":
            launch_snake_game()
        elif game == "Guess the Number":
            launch_guess_the_number()
        elif game == "Rock-Paper-Scissors":
            launch_rock_paper_scissors()
        elif game == "Hangman":
            hangman()

    game_window = tk.Tk()
    game_window.title("Choisir un jeu")

    game_window.configure(bg="#FFFFFF")  # Couleur de fond de la fenêtre

    # Marge entre les boutons
    padx, pady = 10, 5

    games = [
        {"name": "Tic Tac Toe", "icon": "tic_tac_toe_icon.png", "color": "#FF6347"},
        {"name": "Snake Game", "icon": "snake_game_icon.png", "color": "#3CB371"},
        {"name": "Guess the Number", "icon": "number_guess_icon.png", "color": "#9370DB"},
        {"name": "Rock-Paper-Scissors", "icon": "rock_paper_scissors_icon.png", "color": "#FFA500"},
        {"name": "Hangman", "icon": "hangman_icon.png", "color": "#4169E1"},
    ]

    for game in games:
        icon_path = game["icon"]
        color = game["color"]

        # Charger l'image spécifique pour chaque jeu
        img = Image.open(icon_path)
        img = img.resize((80, 80), Image.LANCZOS)  # Ajuster la taille de l'icône
        img = ImageTk.PhotoImage(img)

        # Création d'un cadre pour chaque bouton de jeu avec une bordure arrondie et une couleur de fond différente
        game_frame = tk.Frame(game_window, bg=color, highlightbackground="black", highlightthickness=2, bd=0, borderwidth=2, relief=tk.RAISED)
        game_frame.pack(padx=padx, pady=pady)

        # Bouton de jeu
        game_button = tk.Button(game_frame, text=game["name"], command=lambda chosen_game=game["name"]: launch_selected_game(chosen_game), image=img, compound=tk.TOP, bg=color)
        game_button.image = img  # Conserver une référence à l'image pour éviter la suppression par le garbage collector
        game_button.pack(padx=padx, pady=pady)
        
    game_window.mainloop()

# Lancer la fonction pour choisir un jeu
if __name__ == "__main__":
    choose_game()
