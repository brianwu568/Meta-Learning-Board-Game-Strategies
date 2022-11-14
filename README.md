# CS330 Fall 2022 Final Project

### OVERALL PLAN
Read through https://medium.com/applied-data-science/how-to-train-ai-agents-to-play-multiplayer-games-using-self-play-deep-reinforcement-learning-247d0b440717.

SIMPLE is basically a deep reinforcement learning framework to learn board games. It's really good so I think for the milestone, at least, we should use it as an oracle. The idea I have in mind is:

### EXPERIMENT 1- Baseline, Chess to Other (BRIAN- this is your current to-do)
1. Acquire dataset 2 from https://www.ai.rug.nl/~mwiering/GROUP/ARTICLES/ICPRAM_CHESS_DNN_2018.pdf. Transform each position in the database from a chessboard to a 64x1 vector. Each item should be the ID of a piece. There should be 13 IDs in total (Pawn, Knight, Bishop, Rook, Queen, King for both White and Black = 12, plus 1 for empty).
2. One-hot encode. This should transform the 64x1 vector into a 64x13 vector. 
3. Create a neural net with similar architecture to the given paper. Use only Dataset 2- this has an input of a board, and output of a numerical value (called "cp" in the paper) that categorizes into one of 15 different labels, section 3.1 of the paper talks about this. Input should be the 64x13 vector, output should be a number. The key difference here is that we need to first include an initial layer that will transform the 64x13 vector into a 64x8 vector; this is our embedding layer. It should just be a normal Conv2D, I think.
4. Train for however many epochs it takes to get within 10% of the accuracy.
5. Notify the groupchat when you're done with this.



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
