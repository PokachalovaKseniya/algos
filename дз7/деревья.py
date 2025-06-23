class TreeNode:
    def __init__(self, key=None, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.size = 1  

def split_tree(root, k):
    if root is None:
        return (None, None)
    
    left_size = root.left.size if root.left else 0
    
    if k == left_size:
        right_tree = root.right
        root.right = None
        update_size(root)
        return (root, right_tree)
    elif k < left_size:
        left_tree, right_tree = split_tree(root.left, k)
        root.left = right_tree
        update_size(root)
        return (left_tree, root)
    else:
        left_tree, right_tree = split_tree(root.right, k - left_size - 1)
        root.right = left_tree
        update_size(root)
        return (root, right_tree)

def update_size(node):
    if node is None:
        return 0
    left_size = update_size(node.left)
    right_size = update_size(node.right)
    node.size = left_size + right_size + 1
    return node.size

def build_tree():
    root = TreeNode(50)
    root.left = TreeNode(30)
    root.right = TreeNode(70)
    root.left.left = TreeNode(20)
    root.left.right = TreeNode(40)
    root.right.left = TreeNode(60)
    root.right.right = TreeNode(80)
    update_size(root)
    return root

def print_tree(node, level=0, prefix="Root: "):
    if node is not None:
        print(" " * (level * 4) + prefix + str(node.key) + f" (size={node.size})")
        print_tree(node.left, level + 1, "L--- ")
        print_tree(node.right, level + 1, "R--- ")

root = build_tree()
print("Original tree:")
print_tree(root)

k = 3
left_tree, right_tree = split_tree(root, k)
print("\nLeft tree (first", k, "elements):")
print_tree(left_tree)
print("\nRight tree (remaining elements):")
print_tree(right_tree)