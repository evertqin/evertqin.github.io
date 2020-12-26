from collections import OrderedDict
from bisect import bisect_right, insort_left


class Ring(dict):
    def __init__(self, **kwargs):
        super(Ring, self).__init__(**kwargs)
        self.__sorted_keys = [key for key, _ in self.items()]
        self.__sorted_keys.sort()

    def __setitem__(self, key, value):
        """
        For constistent hashing ring, we probably don't want to allow adding duplidate nodes into the ring
        We want to find the next availabe node and insert the key value into there
        """
        if key in self:
            raise Exception("Key: " + str(key) + " already exists")
        super(Ring, self).__setitem__(key, value)
        insort_left(self.__sorted_keys, key)

    def __repr__(self):
        return "Ring: {" + ", ".join(str(key) + " : " + str(self[key]) for key in self.__sorted_keys) + "}"

    def __str__(self):
        return self.__repr__()

    def __delitem__(self, key):
        super(Ring, self).__delitem__(key)

        if key in self.__sorted_keys:
            self.__sorted_keys.remove(key)

    def override_node(self, key, value):
        super(Ring, self).__setitem__(key, value)
        if key not in self:
            insort_left(self.__sorted_keys, key)

    def get_next_node(self, key):
        """
        The next node following the given key will strictly be the "next node" regardless if the key exists on the ring or not
        """
        index = bisect_right(self.__sorted_keys, key + 1 if key in self else key)
        if index >= len(self.__sorted_keys):
            raise "The given key: {key} does not exist".format(key=key)

        return self.__sorted_keys[index]

    def __getitem__(self, key):
        if key in self:
            return super(Ring, self).__getitem__(key)

        index = bisect_right(self.__sorted_keys, key)
        if index >= len(self.__sorted_keys):
            raise "The given key: {key} does not exist".format(key=key)

        return self[self.__sorted_keys[index]]


class ConsistentHashing:
    def __init__(self, num_nodes, initial_space):
        """
        To demonstrate, I used even spacing to initialize the ring. A node with key equals infinite number is added to handle boundary condition.
        The node is prepresented as a dictionary, so we have a dictionary (ring) of dictionaries (node)
        """
        self.__num_nodes = num_nodes
        self.__nodes = Ring()

        for i in range(self.__num_nodes):
            self.__nodes[(i + 1) * initial_space] = {}

        self.__nodes[float("inf")] = {}

    def add_node(self, node_id):
        """
        Adding node involves the following two actions:
        1. Create a new node on the ring
        2. Move the appropriate key value pairs from the downstream node to this new node
        """
        self.__nodes[node_id] = {}
        next_node = self.__nodes.get_next_node(node_id)
        org_node_content = {}
        for key, value in self.__nodes[next_node].items():
            if key <= node_id:
                self.__nodes[node_id][key] = value
            else:
                org_node_content[key] = value

        self.__nodes.override_node(next_node, org_node_content)

    def __repr__(self):
        return self.__nodes.__repr__()

    def remove_node(self, node_id):
        """
        Removing node involves the follow tow actions:
        1. Move all the key value pairs to the downstream node
        2. Delete the current node
        """
        next_node = self.__nodes.get_next_node(node_id)
        for key, value in self.__nodes[node_id].items():
            self.__nodes[next_node][key] = value

        del self.__nodes[node_id]

    def get(self, key):
        return self.__nodes[key][key]

    def add(self, key, value):
        self.__nodes[key][key] = value


if __name__ == '__main__':
    h = ConsistentHashing(num_nodes=4, initial_space=5)
    h.add(1, "apple")
    h.add(5, "orange")
    h.add(7, "pear")
    h.add(15, "watermelon")
    h.add(19, "chia")
    h.add_node(3)
    print(h)
    print(h.get(5))
    h.remove_node(3)
    h.remove_node(10)
    h.remove_node(20)
    print(h)
    print(h.get(1))
