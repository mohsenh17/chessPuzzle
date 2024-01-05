class ChessBoard:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = [[' ' for _ in range(8)] for _ in range(8)]

        self.place_initial_pieces(board)

        return board

    def place_initial_pieces(self, board):
        # not Implemented it should come from puzzles
        # currently just plain set
        for i in range(8):
            board[1][i] = Pawn('white')
            board[6][i] = Pawn('black')
        
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i in range(8):
            board[0][i] = piece_order[i]('white')
            board[7][i] = piece_order[i]('black')

    def display_board(self):
        for row in self.board:
            print(' '.join(str(piece) for piece in row))

class ChessPiece:
    def __init__(self, color):
        self.color = color
    def __str__(self):
        # Override the string representation for better display
        return f'{self.color[0].upper()}{self.__class__.__name__[0]}'

class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
    def move():
        raise NotImplementedError

class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
    def move():
        raise NotImplementedError

class Knight(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
    def move():
        raise NotImplementedError

class Bishop(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
    def move():
        raise NotImplementedError
    
class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
    def move():
        raise NotImplementedError
    
class King(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
    def move():
        raise NotImplementedError

if __name__ == "__main__":
    # You can add some test code here to check if your classes work as expected
    chess_board = ChessBoard()
    chess_board.display_board()
