#!/usr/bin/env python

# -*- coding: iso-8859-15 -*-

# Codigo fuente implementando tres en raya con minimax, se utiliza python 2.x (Yo lo construia con python 2.7.13)

# LIBRERIAS
import random, time

Vacio = '-'
Jugador_X = 'x'
Jugador_O = 'o'

# random : Ofrece generadores de numeros pseudo-aleatorios para varias distribuciones.
# time : Proporciona un conjunto de funciones para trabajar con fechas y/o horas.


def todosIguales(list):
    # Retorna si todos los elementos de la lista son iguales o si esta vacia#
    return not list or list == [list[0]] * len(list)


class Board:
    # Esta clase representa al tablero del tres en raya #
    def __init__(self):
        # Inicializa los miembros consecutivos #
        self.pieces = [Vacio] * 9
        self.field_names = '123456789'

    def output(self):
        # Construccion del tablero #
        for line in [self.pieces[0:3], self.pieces[3:6], self.pieces[6:9]]:
            print ' '.join(line)

    def winner(self):
        # Funcion de deteccion de estado final. Returns Jugador_X, Jugador_O or None #
        winning_rows = [[0, 1, 2], [3, 4, 5], [6, 7, 8],  # vertical
                        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # horizontal
                        [0, 4, 8], [2, 4, 6]]  # diagonal
        for row in winning_rows:
            if self.pieces[row[0]] != Vacio and todosIguales([self.pieces[i] for i in row]):
                return self.pieces[row[0]]

    def getValidMoves(self):
        # Lista de movimientos validos. Son validos los vacios. #
        return [pos for pos in range(9) if self.pieces[pos] == Vacio]

    def gameOver(self):
        # Retorna cierto si ganador o no mas movimientos. #
        return self.winner() or not self.getValidMoves()

    def getMoveName(self, move):
        # Movimiento legible #
        return self.field_names[move]

    def makeMove(self, move, jugador):
        # Mueve #
        self.pieces[move] = jugador

    def undoMove(self, move):
        # Deshace un movimiento de tablero #
        self.makeMove(move, Vacio)


def jugadorHumano(board, jugador):
    # Funcion para el jugador humano #
    board.output()
    possible_moves = dict([(board.getMoveName(move), move) for move in board.getValidMoves()])
    move = raw_input("Introduce tu movimiento (%s): " % (', '.join(sorted(possible_moves)))) # <---- Mostramos los n disponibles
    while move not in possible_moves:
        print "'%s' no es valido. Intentalo de nuevo." % move
        move = raw_input("Introduce tu movimiento (%s): " % (', '.join(sorted(possible_moves)))) # <---- Mostramos los n disponibles
    board.makeMove(possible_moves[move], jugador)


def jugadorAzar(board,jugador):
    # Funcion para el jugador maquina al azar #
    board.output()
    possible_moves = dict([(board.getMoveName(move), move) for move in board.getValidMoves()])
    sorted(possible_moves)
    move = random.randint(1,9)
    while move not in possible_moves:
        move = random.randint(1,9)
        print move
        break
    board.makeMove(move, jugador)


def jugadorMaquina(board, jugador):
    # Funcion de seleccion para la maquina #
    t0 = time.time()
    board.output()
    opponent = {Jugador_O: Jugador_X, Jugador_X: Jugador_O}

    # Nodo terminal, evalua valor: 1 gana, 0 nada, -1 pierde #
    def judge(winner):
        if winner == jugador:
            return +1
        if winner == None:
            return 0
        return -1

    def evaluateMove(move, p=jugador):
        try:
            board.makeMove(move, p)
            if board.gameOver():
                return judge(board.winner())
            outcomes = (evaluateMove(next_move, opponent[p]) for next_move in board.getValidMoves())

            if p == jugador:
                # return min(outcomes)
                min_element = 1
                for o in outcomes:
                    if o == -1:
                        return o
                    min_element = min(o, min_element)
                return min_element
            else:
                # return max(outcomes)
                max_element = -1
                for o in outcomes:
                    if o == +1:
                        return o
                    max_element = max(o, max_element)
                return max_element

        finally:
            board.undoMove(move)

    moves = [(move, evaluateMove(move)) for move in board.getValidMoves()]
    random.shuffle(moves)
    moves.sort(key=lambda(move, winner) : winner)
    print "Mueve la IA con una rapidez de: %0.3f ms" % ((time.time() - t0) * 1000)
    print moves
    # realiza movimiento -1 o en 0 por ese orden #
    board.makeMove(moves[-1][0], jugador)


def game():
    # Tres en raya #
    # dibujamos tablero y asignamos el primer turno al humano #
    b = Board()
    turn = 1
    while True:
        print "Turno %i." % turn
        jugadorHumano(b, Jugador_X)
        if b.gameOver():
            break

        jugadorMaquina(b, Jugador_O)
        if b.gameOver():
            break
        turn += 1

    b.output()
    if b.winner():
        print 'EL JUGADOR "%s" GANA' % b.winner()
    else:
        print '*-- ES EMPATE, SIMPLE MORTAL --*'


def game1():
    # Tres en raya #
    # dibujamos tablero y asignamos el primer turno #
    b = Board()
    turn = 1
    while True:
        print "Turno %i." % turn
        jugadorHumano(b, Jugador_X)
        if b.gameOver():
            break

        jugadorHumano(b,Jugador_O)
        if b.gameOver():
            break
        turn += 1
    b.output()
    if b.winner():
        print 'EL JUGADOR "%s" GANA' % b.winner()
    else:
        print '*-- ES EMPATE --*'


def game2():
    # Tres en raya #
    # dibujamos tablero y asigamos el primer turno al humano #
    b = Board()
    turn = 1
    while True:
        print "Turno %i." % turn
        jugadorHumano(b, Jugador_X)
        if b.gameOver():
            break

        jugadorAzar(b, Jugador_O)
        if b.gameOver():
            break
        turn += 1
    b.output()
    if b.winner():
        print 'EL JUGADOR "%s" GANA' % b.winner()
    else:
        print '*-- ES EMPATE --*'


# Funcion principal para activar las demas funciones
if __name__ == "__main__":
    option = int(input('Selecciona el modo de juego:\n1.- Basico (H vs H),\n2.- Intermedio (H vs M)\n3.-Experto (H vs IA)\n Eleccion: '))
    if option == 1:
        print '***** TRES EN RAYA: HUMANO vs HUMANO *****'
        game1()
    elif option == 2:
        print '***** TRES EN RAYA: HUMANO vs MAQUINA *****'
        game2()
    elif option == 3:
        print '***** TRES EN RAYA: HUMANO vs IA *****'
        game()