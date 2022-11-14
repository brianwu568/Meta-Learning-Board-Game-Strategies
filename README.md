# CS330 Fall 2022 Final Project

### OVERALL PLAN
Read through https://medium.com/applied-data-science/how-to-train-ai-agents-to-play-multiplayer-games-using-self-play-deep-reinforcement-learning-247d0b440717.

SIMPLE is basically a deep reinforcement learning framework to learn board games. It's really good so I think for the milestone, at least, we should use it as an oracle. The idea I have in mind is:
1. Train SIMPLE on each board game we have configured. Record training time.
2. Use the learned SIMPLE agent generate data. For each position we generate, we can have SIMPLE play somewhere around 100 games against itself starting from that position. The numerical value of that position (that'll be the output of our neural net) is going to be the normalized number of games it wins against itself from that starting position, mapping from -1 to 1. 
3. Train neural networks to predict the numerical value given the position. We will try a) training from scratch, and b) transfer learning. For now, we should probably just stick to training from scratch.
4. Figure out positional encodings? simultaneous task learning? idk at this point i'm out of ideas


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
