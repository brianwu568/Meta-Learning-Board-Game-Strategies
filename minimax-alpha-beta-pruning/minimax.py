# Reference: This code is based off of Tony Poer's Implementation of the MiniMax Algorithm.

# Define a Class for the MiniMax Agent:
class MiniMaxAgent:
    # Initialization Function: the class takes in a Game Tree object as input.
    def __init__(self, gametree):
        self.successors_list = []                   # List to hold successor nodes at any point in the tree
        self.gametree = gametree                    # GameTree Object
        self.gametree_root = gametree.root          # GameTree Node Object
        self.current_node = None                    # GameTree Node Object
        self.POSITIVE_INFINITY = float('inf')       # Constant to represent positive infinity
        self.NEGATIVE_INFINITY = -1 * float('inf')  # Constant to represent negative infinity

    # Return the Successors (Children Nodes) of a Node
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

    # Return the value of a current node
    def getValue(self, current_node):
        if current_node == None:
            raise Exception("getValue: Node being passed into function is of type NONE")
        else:
            current_node_value = current_node.value
            return current_node_value

    # Find the maximum value out of a node and its children (A maximizing the chance of A winning)
    def getMaxValue(self, current_node):
        print("MiniMax->MAX: Currently Visiting Node: " + str(current_node.id))

        # If the node is a leaf node, then the maximum value is just the value of the node itself
        if self.isLeaf(current_node) == True:
            maximum_value = self.getValue(current_node)
            return maximum_value

        # Otherwise, we loop through all of the children nodes of the parent node to find the maximum value
        else:
            maximum_value = self.NEGATIVE_INFINITY
            children_nodes_list = self.getChildren(current_node)

            for children_node in children_nodes_list:
                children_node_minimum_value = self.getMinValue(children_node)
                maximum_value = max(maximum_value, children_node_minimum_value)

            return maximum_value

    # Find the minimum value out of a node and its children (B trying to minimize the chance of A winning)
    def getMinValue(self, current_node):
        print("MiniMax->MIN: Currently Visiting Node: " + str(current_node.id))

        # If the node is a leaf node, then the maximum value is just the value of the node itself.
        if self.isLeaf(current_node) == True:
            minimum_value = self.getValue(current_node)
            return minimum_value

        # Otherwise, we loop through all of the children nodes of the parent node to find the minimum value
        else:
            minimum_value = self.POSITIVE_INFINITY
            children_nodes_list = self.getChildren(current_node)

            for children_node in children_nodes_list:
                children_node_maximum_value = self.getMaxValue(children_node)
                minimum_value = min(minimum_value, children_node_maximum_value)

            return minimum_value

    def minimaxBestMove(self, gametree_root_node):
        # Get the current best value (the value of the root node of the tree)
        best_value = self.getMaxValue(gametree_root_node)
        print("MiniMax: Current Best Value (Value of Root Node) is: " + str(best_value))

        # Find the Node in the tree with that best value: propagate all values from nodes up the tree using MiniMax
        root_node_children = self.getChildren(gametree_root_node)
        current_best_move = None

        for child_node in root_node_children:
            child_node_value = self.getValue(child_node)
            if child_node_value == best_value:
                current_best_move = child_node

        return current_best_move
