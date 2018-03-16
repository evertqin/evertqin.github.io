---
title: Disjoint-set data structure
date: 10/20/2015
tags: 
- Technology
- C++
---

An interesting problem, given some numbers, group them into individual sets based on certain rules. For example, for numbers between, we group them into sets (0, 0), [1, 5), [10, 30), [30, 60), [60, 100]. I found this [article](https://www.topcoder.com/community/data-science/data-science-tutorials/disjoint-set-data-structures/) on topcode is very helpful. Below is an implementation in C++.

<!--more-->

~~~~{.cpp}
#include <iostream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <set>
#include <algorithm>
#include <climits>
#include <stack>
#include <queue>
#include <map>
#include <iterator>
#include <assert.h>

using namespace std;

struct Node {
  int rank;
  int value;
  Node * parent;
};

class DisjointSets{
private:
  int _count;
  int _numElements;
  int _numSets;
  unordered_map<int, Node *> _nodes;
public:
  DisjointSets(): _numElements(0), _numSets(0){}

  ~DisjointSets(){
    for(auto it = _nodes.begin(); it != _nodes.end(); ++it){
      delete it->second;
    }
    _nodes.clear();
  }

  int find_set(int element) {
    if(!_nodes.count(element)){
      return -1;
    }
    Node * curr = _nodes[element];

    while(curr->parent){
      curr = curr->parent;
    }
    Node * root = curr;

    // update the parents along the way
    curr = _nodes[element];
    while(curr != root){
      Node * next = curr->parent;
      curr->parent = root;
      curr = next;
    }

    return root->value;
  }

  void make_union(int setId1, int setId2){
    if(setId1 == setId2){
      return;
    }

    if(!_nodes.count(setId1)){
      return;
    }
    Node* set1 = _nodes[setId1];
    if(!_nodes.count(setId2)){
      return;
    }
    Node* set2 = _nodes[setId2];

    if(set1->rank > set2->rank){
      set2->parent = set1;
    } else if(set1->rank < set2->rank){
      set1->parent = set2;
    } else {
      set2->parent = set1;
      set1->rank++;
    }
    --_numSets;
  }

  void add_element(int element) {
    _nodes[element] = new Node();
    _nodes[element]->parent = NULL;
    _nodes[element]->value = element;
    _nodes[element]->rank = 0;

    _numElements++;;
    _numSets++;
  }

  int get_num_elements() const {
    return _numElements;
  }

  int get_num_sets() const {
    return _numSets;
  }
};

void printElementSets(DisjointSets & s, const vector<int>& nums)
{
  assert(nums.size() <= s.get_num_elements());
  for (int i = 0; i < nums.size(); ++i) {
    cout << s.find_set(nums[i]) << "  ";
  }
  cout << endl;
}

void groupTogether(DisjointSets& s, const vector<int>& nums, map<int, vector<int>>& groups){
  assert(nums.size() <= s.get_num_elements());
  for (int i = 0; i < nums.size() && i < s.get_num_elements(); ++i) {
    groups[s.find_set(nums[i])].push_back(nums[i]);
  }
}

void prettyPrintGroups(const map<int, vector<int>>& groups){
  for(auto it = groups.begin(); it != groups.end(); ++it){
    std::cout << "Group " << it->first << " -------------"<< std::endl;
    for(int i = 0; i <  it->second.size(); ++i){
      std::cout << it->second[i] << "  ";
    }
    std::cout <<  std::endl;
  }
}

void testGenerator(int size){
  vector<pair<int, int>> rules{{0, 0}, {1, 5}, {10, 30}, {30, 60}, {60, 100}};
  vector<int> randoms;
  for(int i = 0; i < size; ++i){
    randoms.push_back(random() % 100);
  }

  DisjointSets s;

  for_each(randoms.begin(), randoms.end(), [&](int num){s.add_element(num); });

  std::cout << "Orginal data:" << std::endl;
  printElementSets(s, randoms);

  for(int i = 0; i < rules.size(); ++i){
    int rep = rules[i].first;
    // push representative to DisjointSets
    s.add_element(rep);
    for(int j = rules[i].first + 1 ; j < rules[i].second; ++j){
      s.make_union(s.find_set(rep), s.find_set(j));
    }
  }
  std::cout << "After union find, group representative:" << std::endl;
  printElementSets(s, randoms);
  std::cout  << std::endl;

  // group together
  map<int, vector<int>> groups;
  groupTogether(s, randoms, groups);
  prettyPrintGroups(groups);
}

int main(int argc, char *argv[])
{
  const int DATA_SIZE = 10;
  testGenerator(DATA_SIZE);
  return 0;
}
~~~~
Sample Output:
Orginal data:
83  86  77  15  93  35  86  92  49  21  
After union find, group representative:
60  60  60  10  60  30  60  60  30  10  

Group 10 -------------
15  21  
Group 30 -------------
35  49  
Group 60 -------------
83  86  77  93  86  92
~~~~
