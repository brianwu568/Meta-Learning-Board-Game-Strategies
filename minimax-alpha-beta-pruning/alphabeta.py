# Reference: This code is based off of Tony Poer's Implementation of the Alpha-Beta Pruning Algorithm.

class AlphaBetaAgent:
    def __init__(self, gametree):
        self.gametree = gametree                    # GameTree Object
        self.gametree_root = gametree.root          # GameTree Node Object
        self.alpha = 0                              # The Alpha constant in Alpha-Beta Pruning
        self.beta = 0                               # The Beta constant in Alpha-Beta Pruning
        self.POSITIVE_INFINITY = float('inf')       # Constant to represent positive infinity
        self.NEGATIVE_INFINITY = -1 * float('inf')  # Constant to represent negative infinity


    # Return the Successors of a Node
    def getChildren(self, current_node):
        if current_node == None:
            raise Exception("getSuccessors: Node being passed into function is of type NONE")
        else:
            children_node_list = list(current_node.children)
            return children_node_list


    # Return whether or not a Node is a leaf node (has no children)
    def isLeaf(self, current_node):
        if current_node == None:
            raise Exception("isLeaf: Node being passed into function is of type NONE")
        else:
            current_node_children = self.getChildren(current_node)
            if len(current_node_children) == 0: # There are no children, so this is a leaf node
                return True
            else: # There are children, so this is not a leaf node
                return False


    # Return the current value of a node
    def getValue(self, current_node):
        if current_node == None:
            raise Exception("getValue: Node being passed into function is of type NONE")
        else:
            current_node_value = current_node.value
            return current_node_value


    # Find the maximum value out of a node and its children (A maximizing the chance of A winning) using Beta
    def getMaxValue(self, current_node, alpha, beta):
        print("AlphaBetaPruning->MAX: Currently Visiting Node: " + str(current_node.id))

        # If the node is a leaf node, then the maximum value is just the value of the node itself
        if self.isLeaf(current_node) == True:
            maximum_value = self.getValue(current_node)
            return maximum_value

        # Otherwise, we loop through all of the children nodes of the parent node to find the maximum value
        else:
            maximum_value = self.NEGATIVE_INFINITY
            children_nodes_list = self.getChildren(current_node)

            for child_node in children_nodes_list:
                child_node_minimum_value = self.getMinValue(child_node, alpha, beta)
                maximum_value = max(maximum_value, child_node_minimum_value)

                # If the maximum value is ever greater than or equal to beta, we terminate and return the max value
                if maximum_value >= beta:
                    return maximum_value
                
                # Otherwise, we reset alpha to be the maximum of the current alpha and the maximum value.
                alpha = max(alpha, maximum_value)

            return maximum_value


    # Find the minimum value out of a node and its children (B minimizing the chance of A winning) using Alpha
    def getMinValue(self, current_node, alpha, beta):
        print("AlphaBetaPruning->MIN: Currently Visiting Node: " + str(current_node.id))

        # If the node is a leaf node, then the minimum value is just the value of the node itself
        if self.isLeaf(current_node) == True:
            minimum_value = self.getValue(current_node)
            return minimum_value

        # Otherwise, we loop through all of the children nodes of the parent node to find the minimum value
        else:
            minimum_value = self.POSITIVE_INFINITY
            children_nodes_list = self.getChildren(current_node)

            for child_node in children_nodes_list:
                child_node_maximum_value = self.getMaxValue(child_node, alpha, beta)
                minimum_value = min(minimum_value, child_node_maximum_value)

                # If the minimum value is less than or equal to alpha, we terminate and return the min value
                if minimum_value <= alpha:
                    return minimum_value

                # Otherwise, we reset beta to be the minimum of the current beta and the minimum value
                beta = min(beta, minimum_value)

            return minimum_value


    # Compute the next best move using the Alpha-Beta Pruning Algorithm
    def alphaBetaPruningBestMove(self, gametree_root_node):
        # Initialize constants for best value (alpha) and beta to -inf and +inf, respectively
        best_value = self.NEGATIVE_INFINITY
        beta = self.POSITIVE_INFINITY

        # Find the Node in the tree with that best value: Remove unnecessary branches using Alpha-Beta Pruning
        root_node_children = self.getChildren(gametree_root_node)
        current_best_move = None

        # Loop over all children nodes and update best_value and beta accordingly
        for child_node in root_node_children:
            current_value = self.getMinValue(child_node, alpha = best_value, beta = beta)
            if current_value > best_value:
                best_value = current_value
                current_best_move = child_node

        print("Alpha-Beta Pruning: Current Best Value (Value of Root Node) is: " + str(best_value))
        print("Alpha-Beta Pruning: Current Best Move (next node to move to) is: " + str(current_best_move.id))

        return current_best_move
