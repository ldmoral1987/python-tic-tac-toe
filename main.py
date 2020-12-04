
# Documentación de la librería easyAI: http://zulko.github.io/easyAI/index.html#
# Manual de referencia de la librería: http://zulko.github.io/easyAI/ref.html
# Otros juegos implementados con easyAI: http://zulko.github.io/easyAI/examples/games.html

# Se importan los paquetes necesarios de la librería easyAI
# Para instalar la librería: pip install easyai
from easyAI import TwoPlayersGame, AI_Player, Negamax
from easyAI.Player import Human_Player

# Se importa time (para dormir la salida por pantalla, útil si solo hay jugadores de IA)
import time


# Clase TicTacToeGame, hereda de TwoPlayersGame
class TicTacToeGame(TwoPlayersGame):
    def __init__(self, players):
        # Se define el número de jugadores y el turno
        self.players = players
        self.nplayer = 1

        # Se define el tablero de juego (vector de 9 casillas inicializadas a 0)
        self.board = [0] * 9

    # Devuelve los movimientos posibles que pueden realizarse
    def possible_moves(self):
        # Devuelve los movimientos posibles en el tablero (siempre y cuando las casillas estén vacías)
        # La casilla vacía se representa como y == 0 (el tablero inicialmente está vacío)
        return [x + 1 for x, y in enumerate(self.board) if y == 0]

    # Movimiento de un jugador
    def make_move(self, move):
        # Almacena el número del jugador en la casilla del tablero
        self.board[int(move) - 1] = self.nplayer

    # Deshacer un movimiento (para agilizar la IA)
    def unmake_move(self, move):
        self.board[int(move) - 1] = 0

    # Condicion de victoria
    def condition_for_lose(self):
        # Esta matriz contiene las posibles combinaciones de victoria
        possible_combinations = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
        return any([all([(self.board[z - 1] == self.nopponent) for z in combination])
                    for combination in possible_combinations])

    # Comprueba si el juego ha finalizado
    def is_over(self):
        return (self.possible_moves() == []) or self.condition_for_lose()

    # Muestra el tablero de juego
    def show(self):
        print('\n'+'\n'.join([' '.join([['.', 'O', 'X'][self.board[3*j + i]] for i in range(3)]) for j in range(3)]))

        # Duerme el proceso 1 segundo para poder ver la salida por pantalla
        time.sleep(1)

    # Calcula la puntuación
    def scoring(self):
        return -100 if self.condition_for_lose() else 0

    # Comprueba quien ha ganado
    def check_winner(self):
        possible_combinations = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]

        for combination in possible_combinations:
            player1, player2 = 0, 0

            # Se toma una combinación de victoria y se comprueba si alguno de los jugadores la cumple
            for i in combination:
                if self.board[i-1] == 1:
                    player1 += 1
                elif self.board[i-1] == 2:
                    player2 += 1

            # Si algún jugador cumple alguna condición de victoria se retorna su identificador
            if player1 == 3:
                return 1
            elif player2 == 3:
                return 2

        # Si ningún jugador cumple ninguna condición de victoria se retorna un 0 (tablas)
        return 0


# Método principal de la aplicación
if __name__ == '__main__':
    # Se inicializa el algoritmo Negamax
    # El 7 significa que la IA anticipa 7 movimientos antes de mover
    algorithm = Negamax(7)

    # Título de la aplicación
    print('TicTacToe con easyAI')

    # Se pregunta al usuario el número de jugadores humanos
    players = -1
    while players < 0 or players > 2:
        players = int(input('Jugadores humanos (0, 1, 2): '))

    # Se configura el juego con el parámetro de número de jugadores
    game = None
    if players == 2:
        # Se inicia el juego con dos jugadores humanos
        game = TicTacToeGame([Human_Player(), Human_Player()])
    elif players == 1:
        # Se inicia el juego con un jugador humano
        game = TicTacToeGame([Human_Player(), AI_Player(algorithm)])
    elif players == 0:
        # Se inicia el juego con cero jugadores humanos (2 IA)
        game = TicTacToeGame([AI_Player(algorithm), AI_Player(algorithm)])

    # Se inicia el juego
    game.play()

    # Se comprueba la condición de victoria
    winner = game.check_winner()

    # Se imprime el ganador (o tablas si no ha ganado nadie)
    if winner == 1:
        print('\nGana el jugador 1')
    elif winner == 2:
        print('\nGana el jugador 2')
    else:
        print('\nTablas')
