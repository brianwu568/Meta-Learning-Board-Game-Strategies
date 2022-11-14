# CS330 Fall 2022 Final Project

### OVERALL PLAN
Read through https://medium.com/applied-data-science/how-to-train-ai-agents-to-play-multiplayer-games-using-self-play-deep-reinforcement-learning-247d0b440717.

SIMPLE is basically a deep reinforcement learning framework to learn board games. It's really good so I think for the milestone, at least, we should use it as an oracle. The idea I have in mind is:
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
