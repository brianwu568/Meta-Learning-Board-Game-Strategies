import torch
import numpy as np

# DEFINE HYPERPARAMETERS FOR THE NEURAL NETWORK
INPUT_SIZE = 2048 #TODO: REMOVE 2048 PLACEHOLDER TO WHATEVER INPUT SIZE WE HAVE
HIDDEN_SIZES = [1048, 500, 50] # same as reference paper
OUTPUT_SIZE = 1 # TODO: CHANGE OUTPUT SIZE OF 1 IF NEEDED, THIS IS THE NUMBER OF CLASSES

# LOAD DATASET
#TODO: Implement this from the chess data and load it in here
train_data = None
test_data = None

# CREATE DATA LOADERS
batch_size = 32
number_of_iterations = 5000
number_of_epochs = int(number_of_iterations / (len(train_data) / batch_size))

train_dataloader = torch.utils.data.DataLoader(dataset=train_data, 
                                           batch_size=batch_size, 
                                           shuffle = True)

test_dataloader = torch.utils.data.DataLoader(dataset = test_data, 
                                          batch_size = batch_size, 
                                          shuffle = False)

# CREATE MODEL CLASS
class ChessMLPModel(torch.nn.Module):
    def __init__(self):
        super(ChessMLPModel, self).__init__()

        ### Define MLP Layers ###

        # Layer 1
        self.layer1 = torch.nn.Linear(INPUT_SIZE, HIDDEN_SIZES[0])
        self.ReLU1 = torch.nn.ReLU()

        # Layer 2
        self.layer2 = torch.nn.Linear(HIDDEN_SIZES[0], HIDDEN_SIZES[1])
        self.ReLU2 = torch.nn.ReLU()

        # Layer 3
        self.layer3 = torch.nn.Linear(HIDDEN_SIZES[1], HIDDEN_SIZES[2])
        self.ReLU3 = torch.nn.ReLU()

        # Layer 4: Output Layer
        self.layer4 = torch.nn.Linear(HIDDEN_SIZES[2], OUTPUT_SIZE)

        # SoftMax
        self.softmax_output = torch.nn.Softmax(dim = 1)

        # Dropout Configuration
        self.dropout = torch.nn.Dropout(0.2)


    # Forward Pass
    def forward(self, input):
        output = torch.flatten(input)

        # Layer 1
        output = self.dropout(self.layer1(output))
        output = self.ReLU1(output)

        # Layer 2
        output = self.dropout(self.layer2(output))
        output = self.ReLU2(output)

        # Layer 3
        output = self.dropout(self.layer3(output))
        output = self.ReLU3(output)

        # Layer 4: Output Layer
        output = self.dropout(self.layer4(output))

        # SoftMax Classifier
        output = self.softmax_output(output)

        return output


# INSTANTIATE MODEL CLASS
if torch.cuda.is_available() == True: # GPU Available
    DEVICE = torch.device("cuda:0")
else: # GPU Not Available, defaulting to CPU
    DEVICE = torch.device("cpu")

model = ChessMLPModel()
model.to(DEVICE)

# INSTANTIATE LOSS FUNCTION
loss_function = torch.nn.CrossEntropyLoss()

# INSTANTIATE HYPERPARAMETERS
learning_rate = 0.001
optimizer = torch.optim.Adam(
    params = model.parameters(), 
    lr = learning_rate,
    betas = (0.90, 0.99),
    eps = 1e-08
    )

# TRAIN THE MODEL
iteration = 0

for epoch in range(number_of_epochs): # loop over all epochs
    for i in range(len(train_dataloader)): # loop over all training examples
        # Set current loss value
        current_loss = 0.0

        # Get the data
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
        current_loss += loss.item()
        if iteration % 500 == 0:
            # Print loss on minibatch, then reset loss
            print('Loss after mini-batch %5d: %.3f' % (iteration + 1, current_loss / 500))
            current_loss = 0.0

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
