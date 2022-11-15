import torch
import numpy as np

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
class ChessCNNModel(torch.nn.Module):
    def __init__(self):
        super(ChessCNNModel, self).__init__()

        # Note that the input dimension is (64,13). We want the output dimension to be (1,).
        self.linear1 = torch.nn.Linear(64, 8)

        # Convolution 1
        self.convolution1 = torch.nn.Conv2d(
            in_channels = 1,
            out_channels = 20,
            kernel_size = 5,
            stride = 1,
            padding = 0
        )
        self.elu1 = torch.nn.ELU(alpha = 1.0, inplace = False)

        # Max Pool 1
        self.max_pool1 = torch.nn.MaxPool2d(kernel_size = None)

        # Convolution 2
        self.convolution2 = torch.nn.Conv2d(
            in_channels = 20,
            out_channels = 50,
            kernel_size = 3,
            stride = 1,
            padding = 0
        )
        self.elu2 = torch.nn.ELU(alpha = 1.0, inplace = False)

        # Max Pool 2
        self.max_pool2 = torch.nn.MaxPool2d(kernel_size = None)

        # Fully Connected 1 (Readout)
        self.fully_connected1 = torch.nn.Linear(
            in_features = None,
            out_features = None
        )


    def forward(self, input):
        # Convolution 1
        output = self.convolution1(input)
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
loss_function = torch.nn.CrossEntropyLoss()


# INSTANTIATE HYPERPARAMETERS
learning_rate = 0.01
# optimizer = torch.optim.Adam(params = model.parameters(), lr = learning_rate)
optimizer = torch.optim.SGD(params = model.parameters(), lr = learning_rate)


# TRAIN THE MODEL
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
