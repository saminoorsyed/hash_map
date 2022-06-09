# Name: Sami Noor Syed
# OSU Email: Syeds@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date:6/3/22
# Description: implimentation of a hashmap class which handles collisions using open Addressing and has the following methods: put(), get(), remove(), contains_key(), clear(), empty_buckets(), resize_table(), table_load(), get_keys()



from Hash_map_supp import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

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

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key / value pair in the hash map. If the given key already exists in the hash map, its associated value must be replaced with the new value. If the given key is not in the hash map, a key / value pair must be added. For this hash map implementation, the table must be resized to double its current capacity when this method is called and the current load factor of the table is greater than or equal to 0.5.

        """
        # check if the load factor is greater than or = to 0.5. if it is double the capacity until it isn't
        
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity*2)
        
        # find the index for the underlying Dynamic Array
        index = self._hash_function(key) % self._capacity
        #initial variables to start the while loop
        count = 0
        check_index = index
        check_entry = self._buckets.get_at_index(index)
        # quadratic probing until an empty place/ tombstone is found in the hash table or the proper key to replace its value has been found
        while check_entry and check_entry.key != key and not check_entry.is_tombstone:
            count += 1
            check_index = (index + count**2) % self._capacity
            check_entry = self._buckets.get_at_index(check_index)
        # adjust the size so that it reflects whether a value in the table has been amended or a value has been added
        if check_entry and check_entry.key == key and not check_entry.is_tombstone:
            self._size -= 1
        self._size += 1
        # set the proper index to the new hash value
        new_entry = HashEntry(key, value)
        self._buckets.set_at_index(check_index, new_entry)
        

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. All existing key / value pairs must remain in the new hash map, and all hash table links must be rehashed. If new_capacity is less than 1, the method does nothing.
        """
        if new_capacity < 1 or new_capacity < self._size:
            return
    
        # store the old table
        old_table = self._buckets
        # set the new capacity
        self._capacity = new_capacity
        # clear the old table and create a new empty hash table
        self.clear()
        # hash each old value into the hash function
        for index in range(old_table.length()):
            # if there is a hash entry that is not a tombstone hash the entry
            old_entry = old_table.get_at_index(index)
            if old_entry and not old_entry.is_tombstone:
                #find the old key and value and create a new entry
                key = old_table.get_at_index(index).key
                value = old_table.get_at_index(index).value
                self.put(key, value)
                


    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hash map, the method returns None.

        """
        check_index = self.find_key(key)
        check_entry = self._buckets.get_at_index(check_index)
        if check_entry and check_entry.key == key:
            return check_entry.value

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False. An empty hash map does not contain any keys.
        """
        if self._size == 0:
            return False
        # find and assign the index that should be checked against the target key
        check_index = self.find_key(key)
        check_entry = self._buckets.get_at_index(check_index)
        # if an entry at the target index exists, check its key against the target key and return true if there is a match
        if check_entry and check_entry.key == key:
            return True
        return False


    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map. If the key is not in the hash map, the method does nothing (no exception needs to be raised).

        Param: key:str
        return: None
        """
        # an empty hashmap contains no values to remove
        if self._size == 0:
            return
        check_index = self.find_key(key)
        check_entry = self._buckets.get_at_index(check_index)
        # if the Hash entry at the node has a key equal to the target key, set that entry's key and value to None and its is_tombstone value to True
        if  check_entry and check_entry.key == key:
            check_entry.is_tombstone = True
            self._size -= 1

    
    def find_key(self, key: str) -> int:
        """
        finds the index of the target key which is to either be returned, removed or checked

        Param: key:str
        return: int
        """
        # find the appropriate index for the hashtable
        index = self._hash_function(key) % self._capacity
        #conditions to initialize the loop
        count = 0
        check_index = index
        check_entry = self._buckets.get_at_index(index)
        # quadratic probing until an empty place is found in the hash table or the proper key to replace its value has been found, continue iterating through Tombstones
        while (check_entry and check_entry.key != key) or (check_entry and check_entry.is_tombstone):
            count += 1
            check_index = (index + count**2) % self._capacity
            check_entry = self._buckets.get_at_index(check_index)
        
        return check_index

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash table capacity.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys(self) -> DynamicArray:
        """
        This method returns a DynamicArray that contains all the keys stored in the hash map. The order of the keys in the DA does not matter.
        """
        all_keys = DynamicArray()
        for index in range(self._buckets.length()):
            hash_entry = self._buckets.get_at_index(index)
            if hash_entry and not hash_entry.is_tombstone:
                all_keys.append(hash_entry.key)
        return all_keys



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

        if m.table_load() >= 0.5:
            capacity = m._capacity
            size = m._size
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

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
