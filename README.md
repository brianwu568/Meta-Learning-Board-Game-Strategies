# CS330 Fall 2022 Final Project

### OVERALL PLAN
Read through https://medium.com/applied-data-science/how-to-train-ai-agents-to-play-multiplayer-games-using-self-play-deep-reinforcement-learning-247d0b440717.

SIMPLE is basically a deep reinforcement learning framework to learn board games. It's really good so I think for the milestone, at least, we should use it as an oracle.

### EXPERIMENT 1.1- Baseline, Chess (BRIAN- this is your current to-do)
1. Acquire dataset 2 from https://www.ai.rug.nl/~mwiering/GROUP/ARTICLES/ICPRAM_CHESS_DNN_2018.pdf. Transform each position in the database from a chessboard to a 64x1 vector. Each item should be the ID of a piece. There should be 13 IDs in total (Pawn, Knight, Bishop, Rook, Queen, King for both White and Black = 12, plus one more for empty).
2. One-hot encode. This should transform the 64x1 vector into a 64x13 vector. Make sure the empty squares get the ID of 0, this is important for experiment 1.2.
3. Create a neural net with similar architecture to the given paper. Use only Dataset 2- this has an input of a board, and output of a numerical value (called "cp" in the paper) that categorizes into one of 15 different labels, section 3.1 of the paper talks about this. Input should be the 64x13 vector, output should be a number. The key difference here is that we need to first include an initial layer that will transform the 64x13 vector into a 64x8 vector; this is our embedding layer. It should just be a normal Conv2D, I think.
4. Train for however many epochs it takes to get within 10% of the paper's accuracy.
5. SAVE THE MODEL
6. Notify the groupchat when you're done with this.

### EXPERIMENT 1.2- Few-Shot Learning from Chess to All
1. Train SIMPLE on each board game over X iterations (I think 150 seems reasonable right now) and save the policies. 
2. Use SIMPLE to generate a set of 20 random midgame states for each game.
3. Bootstrap SIMPLE to play out the game from each position. Have SIMPLE play out each position 100 times, and calculate the win rate for each position.
4. Normalize the winrate for each position into the range (-3, 3). Bucket them in the same way that the paper from Experiment 1.1 buckets them (read section 3.1 of the paper for explanation). The buckets will be our output. In the end, we should have 20 positions, each with a corresponding numerical evaluation classification. The positions will again get one-hot encoded into a 64x13 vector, with empty squares as ID = 0. Note that we won't be using all 13 IDs for most games, since only chess has that many, but we still need to one-hot encode to this size to maintain the neural net architecture. Overall, 
5. Take the saved model from Experiment 1.1. Freeze every layer but the initial layer (the embedding layer) and the final layer. Train on the small dataset. Record evaluation percentages.
6. Do the same thing, but don't start with the saved model; train from scratch with the same number of data positions.

In Experiments 1.1 and 1.2, for the final project we'll be ablating over the performance metric that we use. Currently, we're using the win rate for each position as the performance metric, but hopefully in the final project we'll be able to change that to something a little more sophisticated.

### EXPERIMENT 1.3 (probably after milestone)- Few-Shot Learning from All to Chess
The idea for this is basically the same as the previous experiments; the difference is that instead of few-shot learning from chess to other games, we'll be many-shot learning from other games to chess, since chess has an abundance of data that we can just abuse. According to Eric, the pre-training on other games should make less and less difference as we increase the number of shots taken to learn chess. Here, since we have a preset performance metric (Stockfish), we don't ablate over the performance metric. Instead, we ablate over the number of shots taken. 



### Other TODOs

1. Train SIMPLE on each board game we have configured. Record training time.
2. Use the learned SIMPLE agent to generate data. For each position we generate, we can have SIMPLE play games itself from that position. The move predicted from that position is the the output of our neural net. 
3. Train neural networks to predict the numerical value given the position. We will try a) training from scratch, and b) transfer learning. For now, we should probably just stick to training from scratch. Inputs will be board state, with pieces encoded as one-hot encoders. As per Eric's advice, each neural net will have an initial layer that's unfrozen, which will act as the encoder/embedding layer. The output for the milestone should be a move. This may be challenging since the action space differs based on the board state. 
4. We only have concrete data on the best move for chess. Therefore, our base neural nets will be trained on (input, output) = (position, SIMPLE prediction) for non-chess games and fine-tuned on chess for testing.
5. Figure out positional encodings? simultaneous task learning? idk at this point i'm out of ideas


### TODO:
- Build game environments (Ian- in progress)
- Talk with TAs aboiut encoding schema (Ian- will do Monday)
- Recreate results from https://www.ai.rug.nl/~mwiering/GROUP/ARTICLES/ICPRAM_CHESS_DNN_2018.pdf (URGENT- needs training time, architecture is relatively simple)
- Find Checkers dataset online (Brian - in progress)
- Reinforcement learning skeleton- URGENT
- Generate data for Connect 4/Stratego- needs RL and game environments to be completed first

### DONE:
- Chess game environment (Ian)
- Checkers game environment (Ian)
- Connect-4 game environment (Ian)
- Minimax + Alpha Beta Pruning skeleton (Brian)
- GameTree Data Structure (Brian)

### NOTES:
- Chess doesn't have en passant or promotion choice enabled (always queen). Isn't super necessary at the moment.
