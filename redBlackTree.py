class Node:
    def __init__(self, data, color='red', parent=None, left=None, right=None):
        self.data = data
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right

class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(data=0, color='black')
        self.root = self.TNULL

    def search_tree_helper(self, node, key):
        if node == self.TNULL or key == node.data:
            return node

        if key < node.data:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    def fix_delete(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 'red':
                    s.color = 'black'
                    x.parent.color = 'red'
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 'black' and s.right.color == 'black':
                    s.color = 'red'
                    x = x.parent
                else:
                    if s.right.color == 'black':
                        s.left.color = 'black'
                        s.color = 'red'
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 'black'
                    s.right.color = 'black'
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 'red':
                    s.color = 'black'
                    x.parent.color = 'red'
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == 'black' and s.right.color == 'black':
                    s.color = 'red'
                    x = x.parent
                else:
                    if s.left.color == 'black':
                        s.right.color = 'black'
                        s.color = 'red'
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 'black'
                    s.left.color = 'black'
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 'black'

    def rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.data == key:
                z = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("Kljuc nije pronadjen u stablu")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.rb_transplant(z, z.right)
        elif (z.right == self.TNULL):
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 'black':
            self.fix_delete(x)

    def fix_insert(self, k):
        while k.parent.color == 'red':
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 'red':
                    u.color = 'black'
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == 'red':
                    u.color = 'black'
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 'black'

    def print_tree_helper(self, node, indent, last):
        if node != self.TNULL:
            print(indent, end='')
            if last:
                print("R----", end='')
                indent += "     "
            else:
                print("L----", end='')
                indent += "|    "

            s_color = "RED" if node.color == 'red' else "BLACK"
            print(str(node.data) + "(" + s_color + ")")
            self.print_tree_helper(node.left, indent, False)
            self.print_tree_helper(node.right, indent, True)

    # preorder obilazak - prvo korijen, pa lijevo podstablo, pa onda desno

    def preorder(self):
        self.preorder_helper(self.root)

    # inorder obilazak - prvo lijevo podstablo, pa korijen cvora, pa desno podstablo

    def inorder(self):
        self.inorder_helper(self.root)

    # postorder obilazak - prvo lijevo podstablo, pa desno, pa korijen cvora

    def postorder(self):
        self.postorder_helper(self.root)

    # search tree - kljuc je 'k', metod avrace cvor sa kljucem ako ga pronadje, ako ne vraca 'None'

    def search_tree(self, k):
        return self.search_tree_helper(self.root, k)
    
    # vraca najmanji cvor u podstablu

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node
    
    # vraca najveci cvor u podstablu

    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node
    
    # successor - vraca cvor u inorder redosledu, ukoliko ne postoji desni 'child' vrace 'None'

    def successor(self, x):
        if x.right != self.TNULL:
            return self.minimum(x.right)

        y = x.parent
        while y != self.TNULL and x == y.right:
            x = y
            y = y.parent
        return y
    
    # predecessor - vraca prethodni cvor u inorder redosledu, ukoliko ne postoji lijevi 'child' vrace 'None'

    def predecessor(self, x):
        if x.left != self.TNULL:
            return self.maximum(x.left)

        y = x.parent
        while y != self.TNULL and x == y.left:
            x = y
            y = y.parent
        return y

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # metoda za dodavanje 

    def insert(self, key):
        node = Node(data=key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 'red'

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 'black'
            return

        if node.parent.parent == None:
            return

        self.fix_insert(node)

    # delete_node - metoda za brisanje cvora

    def delete_node(self, data):
        self.delete_node_helper(self.root, data)

    def print_tree(self):
        self.print_tree_helper(self.root, "", True)

# implementacija red-black stabla

if __name__ == "__main__":
    bst = RedBlackTree()

    # Dodavanje elemenata u stablo

    bst.insert(55)
    bst.insert(40)
    bst.insert(65)
    bst.insert(60)
    bst.insert(75)
    bst.insert(57)

    bst.print_tree()

    print("\nNakon brisanja elemenata:\n")

    # Brisanje elemenata iz stabla

    bst.delete_node(40)
    bst.delete_node(65)

    # Stampa stabla

    bst.print_tree()
