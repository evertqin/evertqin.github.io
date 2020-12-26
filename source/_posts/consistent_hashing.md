---
title: Consistent Hashing
date: 05/20/2018
tags: 
- Technology
- Programming
---

What is hash? According to vocabulary.com, hash is "chopped meat mixed with potatoes and browned". In computer world, hashing bears similar meaning, objects come in with different format disparate content and it's the job of hashing to chop them, mix with necessary other ingredients then finally present them in a uniform way, a.k.a, fixed length value.

One prominent usage of hashing is hashtable. A hash table is as simple as: given an arbitrary key can be uniquely mapped to a value. Fitting a small hashtable in memory on a single machine is trivial, but on a larger scale, when the size of the hashtable stretches beyond the limitation of a physical machine, we need to resort to something called consistent hashing.

Consistent hashing is a way of breaking a giant hashtable into manageable smaller hashatables which fit into single physical machine. Imagine it as a round canal with water moving in one direction. Boats (or hash keys) are tossed randomly into the canal and move along with the current and. Ultimately, the boats need to be loaded with goodies (or hash values), before they can exit the canal. This can only be done when boats arrive at the next closest station (or physical machines). In this sense, consistent hashing solves the following problems:

1. Toss a boat and you will get a boatload of goodies
2. Stations can be added and removed freely, if too many boats are in some parts of the canal, it might be wise to add more stations; whereas stations can be suspended if boat traffic is light. The following code snippets demonstrate how these two scenarios work:

The above-mentioned functions can be abstracted into the following class interface

```python
class ConsistentHashing:
    def add_node(self, node_id):
        pass

    def remove_node(self, node_id):
        pass

    def get(self, key):
        pass

    def add(self, key, value):
        pass
```

To lay the ground for this data structure, we need to first construct a <code>Ring</code> class that add or override the following functions:

```python
class Ring(dict):
    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value):
        """
        For constistent hashing ring, we probably don't want to allow adding duplidate nodes into the ring
        We want to find the next availabe node and insert the key value into there
        """
        pass

    def __delitem__(self, key):
        pass

    def override_node(self, key, value):
        pass

    def get_next_node(self, key):
        """
        The next node following the given key will strictly be the "next node" regardless if the key exists on the ring or not
        """
        pass

```

The full code will look like this, I put comments inline:

```python
from collections import OrderedDict
from bisect import bisect_right, insort_left


class Ring(dict):
    def __init__(self, **kwargs):
        super(Ring, self).__init__(**kwargs)
        self.__sorted_keys = [key for key, _ in self.items()]
        self.__sorted_keys.sort()

    def __getitem__(self, key):
        if key in self:
            return super(Ring, self).__getitem__(key)

        index = bisect_right(self.__sorted_keys, key)
        if index >= len(self.__sorted_keys):
            raise "The given key: {key} does not exist".format(key=key)

        return self[self.__sorted_keys[index]]

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
```

How does this work?
1. We start with a ring containing 4 nodes (an extra inf node to handle boundary condition)

{% asset_img Slide1.PNG [Starting Ring] %}

2. Key value pairs are added accordingly, for example, key 1 is tosses onto the ring and it follows the downsteam to node 5

{% asset_img Slide2.PNG [Adding Initial Nodes] %}

3. The result of the ring can be seen below

{% asset_img Slide3.PNG [The Initialized Ring] %}

4. A new node 3 enters the ring, so the key 1 and its value gets moved to node 3

{% asset_img Slide4.PNG [Added Node 3] %}

5. Node 3, 10, 20 leave the ring, the key value pairs are shuffled accordingly.

{% asset_img Slide5.PNG [Removed nodes 3, 10, 20] %}

To demonstrate, we start from the interface, a consistent hashing data structure should be able to do the following