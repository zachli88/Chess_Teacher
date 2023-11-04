import chess
import chess.pgn as pgn
import torch
import torch.nn as nn
import ai
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import os

# Define your input size
input_size = 189

# Create a custom neural network class
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init()
        self.hidden_layer = nn.Sequential(
            nn.Linear(input_size, 1),  # One neuron in the hidden layer
            nn.ReLU()
        )
    def forward(self, x):
        x = self.hidden_layer(x)
        return x

def train_net(input_arr, eval_arr):
    input_tensor = torch.tensor(input_arr)
    eval_tensor = torch.tensor(eval_arr)
    criterion = nn.MSELoss()

    dataset = TensorDataset(input_tensor, eval_tensor)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=True)
    num_epochs = 1

    for epoch in range(num_epochs):
        for inputs, targets in dataloader:
            print("finished %s of %s", dataloader.index, len(dataloader))
            optim.zero_grad()  # Zero the gradients
            outputs = SimpleNN(inputs)  # Forward pass
            loss = criterion(outputs, targets)  # Calculate the loss
            loss.backward()  # Backpropagate
            optim.step()  # Update model weights

        # Optionally, you can print the loss for each epoch
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item()}')

    # Save the trained model and optimizer state
    torch.save({
        'epoch': num_epochs,
        'model_state_dict': SimpleNN.state_dict(),
        'optimizer_state_dict': optim.state_dict(),
        'loss': loss
    }, 'model_checkpoint.pth')

# Call the train_net function to start training


def neural_net_input(board):
    piece_index = {"p": 5, "n": 0, "b":1, "r":2, "q":3, "k": 4}
    inputs = [0] * 189
    current_player = board.turn
    for i in range (8):
        for j in range (8):
            square = chess.SQUARES[chess.square(i,j)]
            piece = str(board.piece_at(square))
            color = 1
            if piece == piece.lower():
                color *= -1
            piece = piece.lower()
            rank = j
            if color == -1:
                rank = 7 - j
            file = i
            if file > 3:
                file = 7 - i
            if piece != "none":
                index = len(inputs) - 1 - piece_index[piece]
                inputs[index] += color
                if piece != "p":
                    inputs[piece_index[piece] * 32 + rank * 4 + file] += color
                else:
                    inputs[piece_index[piece] * 32 + (rank - 1) * 4 + file] += color
    return inputs

def main():
    input_params = 0
    pgn_file = open("temp.pgn") 
    game = pgn.read_game(pgn_file)
    pos_list = []
    eval_list = []
    evaluations_file = "evaluations.txt"
    fileFound = os.path.exists(evaluations_file)
    permissions = "r+" if fileFound else "w+"
    with open(evaluations_file, permissions) as f:
        while (game != None) :
            board = chess.Board()
            for number, move in enumerate(game.mainline_moves()):
                board.push(move)
                    # val = str(board)
                    # #first number is file second number is rank (0,0) = A1
                    # square = chess.SQUARES[chess.square(0,0)]
                net_inputs = neural_net_input(board)
                best_move = ai.getMove(board.fen())
                if not fileFound:
                    print("evaluating position ", input_params)
                    board_eval = ai.getEval()
                    print(str(board_eval), file=f)
                else:
                    board_eval = f.readline()


                if str(board_eval)[0] == "m":
                    continue
                pos_list.append(net_inputs)
                eval_list.append(board_eval)

                input_params+=1
            fen = board.fen()
            # print(fen)
            # print(board)
            game = pgn.read_game(pgn_file)

    train_net(pos_list, eval_list)
    



if __name__ == "__main__":
    main()