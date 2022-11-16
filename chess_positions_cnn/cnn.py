import torch
import numpy as np
from torch.utils.data import Dataset

# LOAD DATASET

with open("chess_train.txt", "r") as fd:
    content = fd.readlines()
    # each row is split into a list of string representing float numbers
    # then each string is converted to a float with map(float, ...)
    values_train = [list(map(float, row.strip().split(" "))) for row in content]
values_train = torch.tensor(values_train)
boards_train = values_train[:, :-1]
evals_train = values_train[:, -1]
boards_train = boards_train.long()

with open("chess_test.txt", "r") as fd:
    content = fd.readlines()
    # each row is split into a list of string representing float numbers
    # then each string is converted to a float with map(float, ...)
    values_test = [list(map(float, row.strip().split(" "))) for row in content]
values_test = torch.tensor(values_test)
boards_test = values_test[:, :-1]
evals_test = values_test[:, -1]
boards_test = boards_test.long()

# CREATE DATA LOADERS
batch_size = 8
number_of_iterations = 5000
number_of_epochs = int(number_of_iterations / (values_train.shape[0] / batch_size))


class ChessBoardDataset(Dataset):
    def __init__(self, boards, evals):
        self.boards = boards
        self.evals = evals


    def __len__(self):
        return self.boards.shape[0]

    def __getitem__(self, idx):
        # Return Category
        def return_category(x: float) -> int:
            if x < -5.5:
                return 1
            elif -5.5 <= x < -4.5:
                return 2
            elif -4.5 <= x < -3.5:
                return 3
            elif -3.5 <= x < -2.5:
                return 4
            elif -2.5 <= x < -1.5:
                return 5
            elif -1.5 <= x < -0.5:
                return 6
            elif -0.5 <= x < 0.5:
                return 7
            elif 0.5 <= x < 1.5:
                return 8
            elif 1.5 <= x < 2.5:
                return 9
            elif 2.5 <= x < 3.5:
                return 10
            elif 3.5 <= x < 4.5:
                return 11
            elif 4.5 <= x < 5.5:
                return 12
            else: # x >= 5.5
                return 13


        one_hot = torch.eye(13) # 13x13 identity matrix
        board = self.boards[idx]
        board = one_hot[board]
        # label = self.evals[idx]
        label = return_category(idx)
        
        return board, label
    
train_data = ChessBoardDataset(boards_train, evals_train)
test_data = ChessBoardDataset(boards_test, evals_test)


train_dataloader = torch.utils.data.DataLoader(dataset=train_data, 
                                           batch_size=batch_size, 
                                           shuffle = True)

test_dataloader = torch.utils.data.DataLoader(dataset = test_data, 
                                          batch_size = batch_size, 
                                          shuffle = False)

# CREATE CUSTOM CLASS FOR CATEGORICAL CROSS ENTROPY LOSS
class CategoricalCrossEntropyLoss(torch.nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, y_hat, y):
        return torch.nn.functional.nll_loss(y_hat.log(), y.argmax(dim = 1))


# CREATE MODEL CLASS
class ChessCNNModel(torch.nn.Module):
    def __init__(self):
        super(ChessCNNModel, self).__init__()

        # Note that the input dimension is (64,13). We want the output dimension to be (1,).
        self.linear1 = torch.nn.Linear(13, 8)

        # Convolution 1
        self.convolution1 = torch.nn.Conv2d(
            in_channels = 1,
            out_channels = 20,
            kernel_size = 3,
            stride = 1,
            padding = 1
        )
        self.elu1 = torch.nn.ELU(alpha = 1.0, inplace = None)

        # Max Pool 1
        self.max_pool1 = torch.nn.MaxPool2d(kernel_size = 2)

        # Convolution 2
        self.convolution2 = torch.nn.Conv2d(
            in_channels = 20,
            out_channels = 50,
            kernel_size = 3,
            stride = 1,
            padding = 1
        )
        self.elu2 = torch.nn.ELU(alpha = 1.0, inplace = False)

        # Max Pool 2
        self.max_pool2 = torch.nn.MaxPool2d(kernel_size = 2)

        # Fully Connected 1 (Readout)
        self.fully_connected1 = torch.nn.Linear(
            in_features = 50*16*2,
            out_features = 1
        )


    def forward(self, input):
        # Linear 1
        output = self.linear1(input)

        # Convolution 1
        output = output[:, None, :, :]
        output = self.convolution1(output)
        output = self.elu1(output)

        # Max Pool 1
        output = self.max_pool1(output)
        # Convolution 2
        output = self.convolution2(output)
        output = self.elu2(output)

        # Max Pool 2
        output = self.max_pool2(output)
        # Resize
        output = output.view(output.size(0), -1)

        # Fully Connected Layer
        output = self.fully_connected1(output)

        return output


# INSTANTIATE MODEL CLASS
if torch.cuda.is_available() == True: # GPU Available
    DEVICE = torch.device("cuda:0")
else: # GPU Not Available, defaulting to CPU
    DEVICE = torch.device("cpu")

model = ChessCNNModel()
model.to(DEVICE)


# INSTANTIATE LOSS FUNCTION
# loss_function = torch.nn.MSELoss() # Numerical
loss_function = torch.nn.CrossEntropyLoss() # Categorical
# loss_function = CategoricalCrossEntropyLoss() # Categorical, manually implemented (only forward prop, no backprop yet)

# INSTANTIATE HYPERPARAMETERS
learning_rate = 0.01
# optimizer = torch.optim.Adam(params = model.parameters(), lr = learning_rate)
optimizer = torch.optim.SGD(params = model.parameters(), lr = learning_rate)


# TRAIN THE MODEL: Numerical
# iteration = 0
# for epoch in range(number_of_epochs): # loop over all epochs
#     print("Epoch", epoch)
#     print(len(train_dataloader))
#     input()
#     for i, data in enumerate(train_dataloader, 0): # loop over all training examples
#         train_inputs, train_labels = data

#         # Clear gradients with respect to parameters
#         optimizer.zero_grad()

#         # Load data as tensors with gradient accumulation abilities
#         train_inputs = train_inputs.requires_grad_()

#         # Forward pass to get output/logits
#         train_outputs = model(train_inputs)

#         # Calculate Loss: softmax --> cross entropy loss
#         loss = loss_function(train_outputs, train_labels)

#         # Getting gradients with respect to parameters: backward propagation, then update parameters
#         loss.backward()
#         optimizer.step()

#         # Increment iteration counter

#         # Calculate Accuracy Every 500 iterations
#         if i % 100 == 99:
#             # initialize counters
#             number_correct = 0
#             number_total = 0

#             # Loop over test data
#             for j, test_data in enumerate(train_dataloader, 0):
#                 test_inputs, test_labels = test_data

#                 # Get total number of labels
#                 number_total += test_labels.shape[0]

#                 # Load boards to tensors with gradient accumulation abilities
#                 test_inputs = test_inputs.requires_grad_()

#                 # Forward pass only to get logits/output
#                 test_outputs = model(test_inputs)
#                 # Get number of correct predictions
#                 test_labels = test_labels.view(-1)
#                 test_outputs = test_outputs.view(-1)
#                 running_sum = (abs(test_outputs)/test_outputs == abs(test_labels)/test_labels).sum()
#                 number_correct += running_sum
            
#             # Compute accuracy
#             accuracy = 100 * (number_correct / number_total)

#             # Print Loss to Terminal
#             print('Iteration: {}. Loss: {}. Accuracy: {}'.format(iteration, loss.item(), accuracy))

# model.save()

# TRAIN THE MODEL: Categorical
iteration = 0
for epoch in range(number_of_epochs): # loop over all epochs
    for i in range(len(train_dataloader)): # loop over all training examples
        combined_example = train_dataloader[i]
        current_example_boards = combined_example[0]
        current_example_labels = combined_example[1]

        # Clear gradients with respect to parameters
        optimizer.zero_grad()

        # Load data as tensors with gradient accumulation abilities
        current_example_boards = current_example_boards.requires_grad_()

        # Forward pass to get output/logits
        outputs = model(current_example_boards)

        # Calculate Loss: softmax --> cross entropy loss
        loss = loss_function(outputs, current_example_labels)

        # Getting gradients with respect to parameters: backward propagation, then update parameters
        loss.backward()
        optimizer.step()

        # Increment iteration counter
        iteration += 1

        # Calculate Accuracy Every 500 iterations
        if iteration % 500 == 0:
            # initialize counters
            number_correct = 0
            number_total = 0

            # Loop over test data
            for i in range(len(test_dataloader)):
                current_test_boards = test_dataloader[i][0]
                current_test_labels = test_dataloader[i][1]

                # Get total number of labels
                number_total = current_test_labels.size(0)

                # Load boards to tensors with gradient accumulation abilities
                current_test_boards = current_test_boards.requires_grad_()

                # Forward pass only to get logits/output
                outputs = model(current_test_boards)

                # Get predictions using torch.max
                _, predictions = torch.max(outputs.data, 1)

                # Get number of correct predictions
                running_sum = (predictions == current_test_labels).sum()
                number_correct += running_sum

            # Compute accuracy
            accuracy = 100 * (number_correct / number_total)

            # Print Loss to Terminal
            print('Iteration: {}. Loss: {}. Accuracy: {}'.format(iteration, loss.item(), accuracy))
model.save()
