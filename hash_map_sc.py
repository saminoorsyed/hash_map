# Name: Sami Noor Syed
# OSU Email: Syeds@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date:6/3/22
# Description: implimentation of a hashmap class which handles collisions using chaining and has the following methods: put(), get(), remove(), contains_key(), clear(), empty_buckets(), resize_table(), table_load(), get_keys() this file also contains a function to find the mode of a Hash table



from Hash_map_supp import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    #------------------------------------------------------------------ #
   
    def put(self, key: str, value: object) -> None:
        """
        This method updates the key / value pair in the hash map. If the given key already exists in the hash map, its associated value must be replaced with the new value. If the given key is not in the hash map, a key / value pair must be added.

        Param: key: str
        value: object

        """

        # feed the key into the hash function and find the remainder when the hash is divided by the capacity of the dynamic array
        index = self._hash_function(key) % self._capacity

        
        # if the key already exists in the hash table, assign the node in question to "node"
        node = self._buckets.get_at_index(index).contains(key)
        #assign the new value
        if node:
            node.value = value
        # if the node was not in the hash table, insert it
        else:
            self._size += 1
            self._buckets.get_at_index(index).insert(key,value)

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.

        Param: None
        return: int

        """
        #loop through the Dynamic array structure and see how many buckets are full
        filled_buckets = 0
        for index in range(self._buckets.length()):
            if self._buckets.get_at_index(index)._head:
                filled_buckets+=1
        # the difference of the capacity and the number of filled buckets should be the number of empty buckets

        return self._capacity - filled_buckets

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.

        Param: None
        return: float
        """
        return self._size/self._capacity
        

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash table capacity.
        
        Param: None
        return: None
        """

        self._buckets = DynamicArray()
        self._size = 0
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. All existing key / value pairs must remain in the new hash map, and all hash table links must be rehashed. If new_capacity is less than 1, the method does nothing.

        Param: new_capacity: int
        return: None

        """
    
        if new_capacity < 1:
            return
        # store the old hash table
        old_table = self._buckets
        #set the capacity to the new_capacity value
        self._capacity = new_capacity
        #clear and resize the underlying data structure
        self.clear()
        # for each index in the old Dynamic array loop through and hash each item into a new hash table
        for index in range(old_table.length()):
            node = old_table.get_at_index(index)._head
            while node:
                self.put(node.key, node.value)
                node = node.next

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hash map, the method returns None.
        
        Param: key: str
        return: object
        """
        index = self._hash_function(key)% self._capacity
        node = self._buckets.get_at_index(index).contains(key)
        if node:
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False. An empty hash map does not contain any keys.

        Param: key: str
        return: bool
        """
        index = self._hash_function(key)% self._capacity
        if self._buckets.get_at_index(index).contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map. If the key is not in the hash map, the method does nothing (no exception needs to be raised).

        Param: key: str
        return: None
        """
        index = self._hash_function(key) % self._capacity
        result = self._buckets.get_at_index(index).remove(key)
        if result:
            self._size -= 1
            

    def get_keys(self) -> DynamicArray:
        """
        This method returns a DynamicArray that contains all the keys stored in the hash map.

        Param: None
        return: DynamicArray
        """
        #initialize the DynamicArray object to be returned
        key_array = DynamicArray()
        #append each key to the new DynamicArray
        for linked_list in range(self._buckets.length()):
            for node in self._buckets.get_at_index(linked_list):
                key_array.append(node.key)
        return key_array



def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    This function receives a DynamicArray (that is not guaranteed to be sorted). This function will return a tuple containing, in this order, a DynamicArray comprising the mode (most occurring) value/s of the array, and an integer that represents the highest frequency (how many times they appear).
    
    If there is more than one value with the highest frequency, all values at that frequency should be included in the array being returned (the order does not matter). If there is only one mode, return a DynamicArray comprised of only that value. 
    
    Param: da: DynamicArray
    return: (DynamicArray, int)
    """
    map = HashMap(da.length() // 3, hash_function_1)
    # create a hashmap in which each item in the input Dynamic array is a key in the hashmap. The value associated with the key in the hashmap will correspond to the frequency of that value in the original array
    for index in range(da.length()):
        # assign the key to the current element
        key = da.get_at_index(index)
        # if the element is in the hash table, increment its value by one
        if map.contains_key(key):
            freq = map.get(key)
            freq += 1
            #insert the new value in place of the old one
            map.put(key, freq)
        #if the element is not in the hash table put it in the hash table with a value of one
        else:
            map.put(key, 1)
    # set the freq and mode to initial values before looping through hashmap
    freq = 0
    mode_da = DynamicArray()
    # check each item in the hashtable
    for item in range(map._buckets.length()):
        node = map._buckets.get_at_index(item)._head
        # check any nodes that may have been chained into that index of the hashmap starting at the head of the linked list
        while node:
            # if the node value is greater than the current freq then clear the mode_da and insert that value, set the freq to the new val
            if node.value > freq:
                mode_da = DynamicArray()
                mode_da.append(node.key)
                freq = node.value
            # if the node val is = the freq, append the node's key to the mode_da
            elif node.value == freq:
                mode_da.append(node.key)
            # check the next node in the linked list 
            node = node.next
    return mode_da, freq
            
    



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
