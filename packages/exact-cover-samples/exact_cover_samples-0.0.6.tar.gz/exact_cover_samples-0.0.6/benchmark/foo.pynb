import time

NUMBA = True

if NUMBA:
    import numba as nb
    from numba.experimental import jitclass

    node_type = nb.types.deferred_type()
    spec = dict(
        value=nb.types.int32,
        next=nb.types.optional(node_type),
    )

class Node:
    """
    just like a list, a car and a cdr
    """
    def __init__(self, value):
        self.value = 1
        self.next = None

    def scan(self):
        """
        apply a function to each node
        """
        head = self
        while head is not None:
            # fun(head)
            head = head.next

    @staticmethod
    def create(size: int):
        """
        create a linked list of size
        """
        head = Node(0)
        current = head
        for i in range(1, size):
            current.next = Node(i)
            current = current.next
        return head

if NUMBA:
    print("JIT")
    Node = (jitclass(spec))(Node)
    print("JIT done")
    node_type.define(Node.class_type.instance_type)


def nop(x):
    pass

def to_measure():
    """
    create a linked list from a file
    """
    print("Creating")
    node = Node.create(1_000_000)
    print("Scanning")
    # node.scan(id)
    node.scan()


from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument("-r", "--runs", action='store', type=int, default=3)
    args = parser.parse_args()

    for run in range(args.runs):
        print(f"Run {run + 1} .. ", end="")
        beg = time.process_time()
        to_measure()
        end = time.process_time()
        print(f"{(end - beg):.3f} seconds")

main()
