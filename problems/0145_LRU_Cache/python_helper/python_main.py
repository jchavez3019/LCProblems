from typing import *


class KeyNode:
 """
 A key node will be stored in the hash map of the LRU cache. The value of the node is the value associated with the key
 in the hash map. However, we also maintain previous and next pointers in order to maintain a relative ordering
 between keys in the hash map. In particular, the previous key should be more recently used that this node, and the
 next key should be less recently used. The previous key should only be None if this node is the most recently used,
 and the next key should only be None if this node is the least recently used.
 """
 def __init__(self, val: int, prev_key: Union[int, None], next_key: Union[int, None]):
  self.val: int = val
  self.prev: Union[int, None] = prev_key
  self.next: Union[int, None] = next_key


class LRUCache:

 def __init__(self, capacity: int):
  assert capacity > 0
  self.key_map: Dict[int, KeyNode] = {} # hash map holding key nodes
  self.lru = self.mru = None  # holds the most and least recently used keys
  self.capacity = capacity # maximum capacity in the cache

 def _update_existing_element(self, key: int, curr_el: KeyNode):
  """
  Update the hash map so that this key and its corresponding element
  are now the new most recently used element.
  :param key:      Key in the key_map that should be the new mru.
  :param curr_el:  Corresponding value of this key in the key map, i.e., curr_el == self.hash_map[key]
  :return:
  """

  if key == self.mru:
   # is already mru, return
   return

  # The previous node should now point to this current element's next node.
  # Note that the current node is not the mru, thus it is impossible for its previous key to be None. However,
  # its next key may be None.
  self.key_map[curr_el.prev].next = curr_el.next

  if key == self.lru:
   # The previous element should be the new lru. The previous element
   # already had its next pointer set to None
   self.lru = curr_el.prev
   assert self.key_map[curr_el.prev].next is None
  else:
   # This element was not lru, so its next element must exist, and we must update its next pointer.
   self.key_map[curr_el.next].prev = curr_el.prev

  # this element should now point to the current mru
  curr_el.next = self.mru

  # previous mru should point back to this element
  self.key_map[self.mru].prev = key

  # now set this element as the new mru
  self.mru = key

  # as new mru, prev should be None
  curr_el.prev = None

 def _insert_new_element(self, key: int, value: int):
  """
  Assuming the hash map has capacity, inserts a new element into the hash map and updates the relative ordering
  accordingly.
  :param key:   Key to use for the new element.
  :param value: Value associated with the new element.
  """
  # create the new node with next pointing to mru (mru may be None if this is the first element)
  self.key_map[key] = KeyNode(value, None, None)

  # if this is the first new element, we must initialize mru and lru and return
  if len(self.key_map) == 1:
   self.mru = key
   self.lru = key
   return

  # update current mru to point back to this next element
  self.key_map[self.mru].prev = key

  # set the current element to point to old mru
  self.key_map[key].next = self.mru

  # update this element to be the new mru
  self.mru = key

 def get(self, key: int) -> int:
  """
  Gets the value in the cache given a key. Returns -1 if the key does not exist.
  :param key: Key to index in the cache
  :return:    Key's corresponding value or -1
  """
  curr_el = self.key_map.get(key, None)

  # this element does not exist
  if curr_el is None:
   return -1

  # update the hash-map appropriately in case mru and/or lru get updated
  self._update_existing_element(key, curr_el)

  # simple check to ensure this key is the mru and its prev is None
  assert self.mru == key and self.key_map[key].prev is None

  # finally, return the value
  return curr_el.val

 def put(self, key: int, value: int) -> None:
  curr_el = self.key_map.get(key, None)

  if curr_el is not None:
   # this element exists
   curr_el.val = value  # update its value

   # update the hash-map appropriately in case mru and/or lru get updated
   self._update_existing_element(key, curr_el)
  else:
   # this element does not exist

   if len(self.key_map) < self.capacity:
    # we have the capacity to store this element
    self._insert_new_element(key, value)

   else:
    # we must remove the lru element

    # get prev key of the lru element
    lru_prev = self.key_map[self.lru].prev

    # update lru's prev to point to None
    # Note that if the capacity is 1, this lru_prev may be None
    if lru_prev is not None:
     self.key_map[lru_prev].next = None

    # delete the current lru
    del self.key_map[self.lru]

    # update the prev to be the new lru
    if lru_prev is not None:
     self.lru = lru_prev
    else:
     self.lru = self.mru

    # we now have the capacity to store the new element
    self._insert_new_element(key, value)

   # simple check to ensure this key is the mru and its prev is None
   assert self.mru == key and self.key_map[key].prev is None

 def get_keys(self, ordered=False):
  """
  Returns the keys in the LRU Cache as a list
  :param ordered: If true, the hash_map is traversed in order from most recent to least recent.
  :return keys:   List of keys in the LRU cache
  """
  if not ordered:
   # ordering does not matter, can simply return all keys
   return list(self.key_map.keys())
  else:
   # must traverse the hash map in order
   curr_key = self.mru
   keys = []
   while curr_key is not None:
    keys.append(curr_key)
    curr_key = self.key_map[curr_key].next
   return keys

def main():
 # Your LRUCache object will be instantiated and called as such:
 methods = ["LRUCache", "put", "put", "put", "put", "get", "get", "get", "get", "put", "get", "get", "get", "get", "get"]
 parameters = [[3], [1, 1], [2, 2], [3, 3], [4, 4], [4], [3], [2], [1], [5, 5], [1], [2], [3], [4], [5]]
 obj = LRUCache(*parameters[0])
 print(f"i: 0 | method: LRUCache | param: {parameters[0]}")
 for i, method, param in zip(range(len(methods)), methods, parameters):
  if i == 0:
   continue
  print(f"i: {i} | method: {method} | param: {param}")
  method = getattr(obj, method)
  method(*param)
  print(f"mru after method: {obj.mru} | lru after method: {obj.lru}")
  print(f"Keys after operation: {obj.get_keys(False)}")
  print(f"Ordered Keys after operation: {obj.get_keys(True)}")
  print()

if __name__ == "__main__":
 main()