import random
import time
import copy

# create players of different classes
class Player:
    def __init__(self,letter):
        self.letter = letter
    def get_move(self,game):
        pass

class Computer(Player):
    def __init__(self,letter):
        super().__init__(letter)
    def get_move(self,game):
        # print(f"{self.letter}'s turn")
        move = random.choice(game.available_moves())
        return move
    
class Human(Player):
    def __init__(self,letter):
        super().__init__(letter)
    def get_move(self,game):
        move = ""
        while move not in game.available_moves():
            try:
                move = int(input(f"{self.letter}'s turn\npick ur move: "))
                if move in game.available_moves():
                    return move
                print("moves already taken")
            except:
                print("Invalid Input!!!")

class Capable_Computer(Player):
    def __init__(self,letter):
        super().__init__(letter)
    def get_move(self,game):
        # take a random move at first if all of the board is empty
        if len(game.available_moves()) == 9:
            return random.choice(game.available_moves())
        # else: get the move based on the minimax algorithm
        move = self.minimax(game,self.letter)["position"]
        return move

    def minimax(self,state,player):
        max_player = "x"
        other_player = "o" if player == "x" else "x"

        # base cases bfore u recurse
        if state.current_winner == other_player:
            # need to return position and score of the winner if there is one. as a dictionary
            return {"position":None, 
                    "score":1*(state.num_empty_spots()+1) if other_player==max_player else -1*(state.num_empty_spots()+1)
                    }
        elif not state.num_empty_spots():
            return {"position":None, "score":0}
        
        # after handling the base cases create dictionaries specifying the best possible moves for players
        if player==max_player:
            best_move = {"position":None, "score":float("-inf")}
        else:
            best_move = {"position":None, "score":float("inf")}
        
        # after handling our base cases of evaluating if there was a winner on the last move and returning
        # their scores we can move on to the recursive part of the minmax algorithm where we loop thorugh
        # all possible moves and assign the players with the most optimal ones
        for every_move in state.available_moves():
            # every_move = int(every_move)
            new_state = copy.deepcopy(state)
            # make some state-copies
            # state_copy = Tic_Tac_Toe()
            # state_copy.board = state.board.copy()
            # state_copy.current_winner = state.current_winner

            # make a move
            new_state.make_move(player,every_move)
            # make a copy of the original game state to pass that to the recursive part, so that the original game state stays uneffected
            # recurse using minimax to simulate a score after every move
            sim_score = self.minimax(new_state,other_player) #we pass minimax the state of the board/game and alternate between players to evaluate the best move for the capable computer player based on the move from the next player
            # restore state of the game to what it was bfore recursing
            # undoing all the moves
            # new_state.board[every_move] = " "
            # new_state.current_winner = None
            # keepin track of the position of the moves that were made when we were recusing to know which move resulted from which position
            sim_score["position"] = every_move

            # updating dictionaries if necessary
            if player==max_player:
                if sim_score["score"] > best_move["score"]:
                    best_move = sim_score
            else:
                if sim_score["score"] < best_move["score"]:
                    best_move = sim_score
        return best_move

# create a class for the functions tic-tac-toe
class Tic_Tac_Toe:
    def __init__(self):
        # initalize the board
        self.board = [" "]*9
        # initalize winner
        self.current_winner = None

    def print_board(self):
        # extract rows
        for row in [self.board[i*3:(i+1)*3]for i in range(3)]:
            print("| " + " | ".join(row) + " |")

    def print_board_nums(self):
        board_nums = [[str(i)for i in range(k*3,(k+1)*3)] for k in range(3)]
        for nums in board_nums:
            print("| " + " | ".join(nums) + " |")

    def available_moves(self):
        return [idx for idx,spot in enumerate(self.board) if spot == " "]
    #     moves = []
    #     for idx,spot in enumerate(self.board):
    #         if spot == " ":
    #             moves.append(idx)
    #     return moves

    def empty_spots(self):
        return " " in self.board
    
    def num_empty_spots(self):
        return self.board.count(" ")
    
    def make_move(self,letter,move):
        if self.board[move] == " ":
            self.board[move] = letter
            if self.winner(letter,move):
                self.current_winner = letter
            return True
        return False
    
    def winner(self,letter,move):
        row_idx = move // 3
        row = self.board[row_idx*3:(row_idx+1)*3]
        if all(spot==letter for spot in row):
            return True
        col_idx = move % 3
        col = [self.board[col_idx+(i*3)] for i in range(3)]
        if all(spot==letter for spot in col):
            return True
        if move % 2 == 0:
            diagnol1 = [self.board[i] for i in [0,4,8]]
            if all(spot==letter for spot in diagnol1):
                return True
            diagnol2 = [self.board[i] for i in [2,4,6]]
            if all(spot==letter for spot in diagnol2):
                return True
            return False

def play(game,x_player,o_player,print_game=False):
    if print_game:
        game.print_board_nums()
    
    letter = "x"
    while game.empty_spots():
        if letter == "x":
            move = x_player.get_move(game)
        else:
            move = o_player.get_move(game)
        if game.make_move(letter,move):
            if print_game:
                print(f"{letter} moved to {move}")
                game.print_board()
                print("")
        if game.current_winner:
            if print_game:
                print(f"{letter} has won")
            return letter

        letter = "o" if letter == "x" else "x"
        # if print_game:
        #     time.sleep(0.89)
    if print_game:
        print("it's a tie")
    
if __name__=="__main__":
    x_wins = 0
    o_wins = 0
    ties = 0
    for _ in range(10):
        x_player = Computer("x")
        o_player = Capable_Computer("o")
        game = Tic_Tac_Toe()
        match = play(game,x_player,o_player,print_game=False)
        if match=="x":
            x_wins += 1
        elif match=="o":
            o_wins += 1
        else:
            ties += 1
    print(f"x_won {x_wins} times, o_won {o_wins} times, it tied {ties} times")