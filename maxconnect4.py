import sys

class Game:
    def __init__(self,board=0):
        if board == 0:
            self.board = [[0 for i in range(7)] for ii in range(6)]
        else:
            self.board = board
        self.next_player = 1
        self.cpu = 2
        s = self.calc_score()
        self.scores = [s[0],s[1]]
    def __str__(self):
        s = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                s += str(self.board[row][col])
            s += "\n"
        s += str(self.next_player)
        return s
    def print_state(self):
        print(str(self)[:-2])
        print(f"{self.scores[0]} - {self.scores[1]}")
    def over(self):
        for row in self.board:
            if row.count(0) > 0:
                return False
        return True
    def calc_score(self,board=self.board):
        tempscores = [0,0]
        #horizontal
        for r in range(len(self.board)):
            for c in range(3,len(self.board[r])):
                if (board[r][c] == board[r][c-1] == board[r][c-2] == board[r][c-3]) and board[r][c] != 0:
                    tempscores[board[r][c]-1] += 1
        #vertical
        for r in range(3,len(self.board)):
            for c in range(len(self.board[r])):
                if (board[r][c] == board[r-1][c] == board[r-2][c] == board[r-3][c]) and board[r][c] != 0:
                    tempscores[board[r][c]-1] += 1
        #diagonal
        for r in range(len(self.board)-3):
            for c in range(len(self.board[r])-3):
                if (board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3]) and board[r][c] != 0:
                    tempscores[board[r][c]-1] += 1
                if (board[r+3][c] == board[r+2][c+1] == board[r+1][c+2] == board[r][c+3]) and board[r+3][c] != 0:
                    tempscores[board[r][c]-1] += 1
        return tempscores
    def get_open_space(self,col):
        try:
            for r in range(len(self.board)-1,0,-1):
                for c in range(len(self.board[r])):
                    if c+1 == col and self.board[r][c] == 0:
                        return r
            return -1
        except IndexError:
            return -1
    def valid_move(self,col):
        if self.get_open_space(col) == -1:
            return False
        return True
    def move(self,col):
        self.board[self.get_open_space(col)][col] = self.next_player
        self.next_player = ((self.next_player+2) % 2) + 1
        s = self.calc_score()
        self.scores = [s[0],s[1]]

def minimax(node,depth,maximizingPlayer):
    if depth == 0 or node:
        return 

## MAIN ##
#Open input file if exists
try:
    #mode = sys.argv[1]
    mode = 'interactivef'
    #filename = sys.argv[2]
    filename = "input3.txt"
    #depth = int(sys.argv[4])
    depth = 5
    with open(filename,'r') as f:
        game = Game()
        lines = f.readlines()
        game.next_player = int(lines[-1])
        for row in range(6):
            for col in range(len(lines[row].strip())):
                game.board[row][col] = int(lines[row][col])
except FileNotFoundError:
    game = Game()

#Running loop
if mode == 'interactive':
    if sys.argv[3] == 'computer-next':
        game.cpu = game.next_player
    else:
        game.cpu = ((game.next_player+2) % 2) + 1
    #"skip" ahead in loop if human next
    if game.next_player != game.cpu:
        game.print_state()
        if game.over():
            sys.exit()
        usermove = 100
        while not game.valid_move(usermove):
            usermove = int(input("Enter a valid column to place your piece: ").strip())
        game.move(usermove)
        with open('human.txt','w') as f:
            f.write(game)
    #enter main loop
    while not game.over():
        game.print_state()
        if game.over():
            break
        #computer choose move
        game.move(computer_move(game.cpu,game.board,depth))
        with open('computer.txt','w') as f:
            f.write(game)
        game.print_state()
        if game.over():
            break
        usermove = 100
        while not game.valid_move(usermove):
            usermove = int(input("Enter a valid column to place your piece: ").strip())
        game.move(usermove)
        with open('human.txt','w') as f:
            f.write(game)
elif mode == "one-move":
    outfile = sys.argv[3]
    game.print_state()
    game.move(computer_move(game.next_player,game.board,depth))
    game.print_state()
    with open(outfile,'w') as f:
        f.write(game)
