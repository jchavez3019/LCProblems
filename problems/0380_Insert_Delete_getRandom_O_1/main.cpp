#include <iostream>
#include <algorithm>

class RandomizedSet {

private:

    std::pair<int, int>** table;
    bool* should_probe;
    int elems, size;

    static const size_t primes[];

    size_t findPrime(size_t num);

    size_t hash(int key, size_t size);

    size_t secondary_hash(int key, size_t size);

    int findIndex(int key);

    inline bool shouldResize() const
    {
        return static_cast<double>(elems) / size >= 0.7;
    }

    void resizeTable();

public:
    RandomizedSet() {
        size_t tsize =  17; // set as the first prime number in our table

        size = findPrime(tsize);
        table = new std::pair<int, int>*[size];

        should_probe = new bool[size];
        for (size_t i = 0; i < size; i++) {
            table[i] = nullptr;
            should_probe[i] = false;
        }
        elems = 0;

    }

    ~RandomizedSet() {
        destroy();
    }

    void destroy() {
        for (size_t i = 0; i < size; i++) {
            // deletes every item in the table
            delete table[i];
        }
        // deletes the table of references
        delete[] table; table = nullptr;
        // deletes the probe table
        delete[] should_probe; should_probe = nullptr;
    }

    bool insert(int val) {

        // find the element if it exists
        size_t index = findIndex(val);
        if (index != static_cast<size_t>(-1)) {
            // return false if the item was present
            return false;
        }

        std::pair<int, int> * newPair = new std::pair<int, int>(val, val);

        index = hash(val, size);

        while(should_probe[index]) {
            index = (index + secondary_hash(val, size)) % size;
        }

        table[index] = newPair;
        should_probe[index] = true;
        elems++;
        if (shouldResize()) {
            resizeTable();
        }

        // return true if the item was not present and now inserted
        return true;
    }

    bool remove(int val) {
        size_t index = findIndex(val);

        if (index == static_cast<size_t>(-1)) {
            // return false if the item was not present
            return false;
        }

        if (table[index] != nullptr) {
            delete table[index];
            table[index] = nullptr;
            should_probe[index] = false;
            elems--;
            return true; // element existed and was successfully deleted
        }
        return false; // element did not exist
    }

    int getRandom() {

        size_t index;
        std::pair<int, int>* curr = nullptr;
        while (curr == nullptr) {
            index = std::rand() % size;
            curr = table[index];
        }

        return curr->second;

    }

};

const size_t RandomizedSet::primes[]
        = {17ul,         29ul,         37ul,        53ul,        67ul,
           79ul,         97ul,         131ul,       193ul,       257ul,
           389ul,        521ul,        769ul,       1031ul,      1543ul,
           2053ul,       3079ul,       6151ul,      12289ul,     24593ul,
           49157ul,      98317ul,      196613ul,    393241ul,    786433ul,
           1572869ul,    3145739ul,    6291469ul,   12582917ul,  25165843ul,
           50331653ul,   100663319ul,  201326611ul, 402653189ul, 805306457ul,
           1610612741ul, 3221225473ul, 4294967291ul};

size_t RandomizedSet::findPrime(size_t num) {
    size_t len_primes = sizeof(primes) / sizeof(size_t);

    const size_t* first = primes;
    const size_t* last = primes + len_primes;
    const size_t* prime_ptr = std::upper_bound(first, last, num);

    if (prime_ptr == last) {
        // no prime number upper bounded nums, the ptr is now out of range
        --prime_ptr;
    }

    return *prime_ptr;
}

size_t RandomizedSet::hash(int key, size_t size) {
    // Bernstein Hash
    // unsigned int h = 0;
    // for (size_t i = 0; i < key.length(); ++i)
    // h = 33 * h + key[i];
    return key % size;
}

size_t RandomizedSet::secondary_hash(int key, size_t size) {
    // // a different hash than above
    //     unsigned int h = 5381;
    //     for (size_t i = 0; i < key.length(); ++i)
    //         h = 31 * h + key[i];
    //     // +1 because we don't want our secondary hash to ever be 0
    //     return (h % (size - 1)) + 1;
    return (key % (size - 1)) + 1;
}

int RandomizedSet::findIndex(int key) {
    size_t index = RandomizedSet::hash(key, size);
    size_t startIdx = index;

//    while(should_probe[index]) {
    while(1) {
        if (table[index] != nullptr && table[index]->first == key) {
            return index;
        }

        index = (index + RandomizedSet::secondary_hash(key, size))%size;

        if(startIdx == index)
            break;
    }

    return -1;
}

void RandomizedSet::resizeTable() {
    size_t newSize = RandomizedSet::findPrime(size * 2);
    auto temp = new std::pair<int, int>*[newSize];

    delete [] should_probe;
    should_probe = new bool[newSize];
    for (size_t i = 0; i < newSize; i++) {
        temp[i] = nullptr;
        should_probe[i] = false;
    }

    // updates new table references to already existing elements
    for (size_t slot = 0; slot < size; slot++) {
        if (table[slot] != nullptr) {
            size_t h = RandomizedSet::hash(table[slot]->first, newSize);
            size_t jump = RandomizedSet::secondary_hash(table[slot]->first, newSize);
            size_t i = 0;
            size_t idx = h;
            while (temp[idx] != nullptr) {
                ++i;
                idx = (h + jump*i) % newSize;
            }
            temp[idx] = table[slot];
            should_probe[idx] = true;
        }
    }

    delete [] table; // does not delete the full table, only the outdated references
    table = temp;
    size = newSize;

}

/**
 * Your RandomizedSet object will be instantiated and called as such:
 * RandomizedSet* obj = new RandomizedSet();
 * bool param_1 = obj->insert(val);
 * bool param_2 = obj->remove(val);
 * int param_3 = obj->getRandom();
 */

const int testSamples[] = {
        1, 2, 3, 4, 5
};

int main() {
    std::cout << "Hello, World!" << std::endl;
    printf("Initializing RandomizedSet\n");
//    RandomizedSet testSet = RandomizedSet();
//    int lenSamples = sizeof(testSamples) / sizeof(int);
//    int currSample;
//    bool successful;
//    for (int i = 0; i < lenSamples; i++) {
//        currSample = testSamples[i];
//        printf("Inserting %d into the set\n", currSample);
//        successful = testSet.insert(currSample);
//        printf("Insertion was %s\n", successful ? "successful" : "unsuccessful");
//    }
//    for (int i = 0; i < lenSamples; i++) {
//        currSample = testSamples[i];
//        printf("Getting random from the set\n");
//        currSample = testSet.getRandom();
//        printf("Random was %d\n", currSample);
//    }
//    for (int i = 0; i < lenSamples; i++) {
//        currSample = testSamples[i];
//        printf("Deleting %d into the set\n", currSample);
//        testSet.remove(currSample);
//        printf("Deletion was %s\n", successful ? "successful" : "unsuccessful");
//    }

//    RandomizedSet randomizedSet = RandomizedSet();
//    randomizedSet.insert(1); // Inserts 1 to the set. Returns true as 1 was inserted successfully.
//    randomizedSet.remove(2); // Returns false as 2 does not exist in the set.
//    randomizedSet.insert(2); // Inserts 2 to the set, returns true. Set now contains [1,2].
//    randomizedSet.getRandom(); // getRandom() should return either 1 or 2 randomly.
//    randomizedSet.remove(1); // Removes 1 from the set, returns true. Set now contains [2].
//    randomizedSet.insert(2); // 2 was already in the set, so return false.
//    randomizedSet.getRandom(); // Since 2 is the only number in the set, getRandom() will always return

//    randomizedSet.insert(-1);
//    randomizedSet.remove(-2);
//    randomizedSet.insert(-2);
//    randomizedSet.getRandom();
//    randomizedSet.remove(-1);
//    randomizedSet.insert(-2);

//    RandomizedSet randomizedSet = RandomizedSet();
//    randomizedSet.insert(1000000000);
//    randomizedSet.insert(1000000001);
//    randomizedSet.insert(1000000002);
//    randomizedSet.insert(1000000003);
//    randomizedSet.insert(1000000004);
//    randomizedSet.insert(1000000005);
//    randomizedSet.insert(1000000006);
//    randomizedSet.insert(1000000007);
//    randomizedSet.insert(1000000008);
//    randomizedSet.insert(1000000009);
//    randomizedSet.insert(1000000010);
//    randomizedSet.insert(1000000011);
//    randomizedSet.insert(1000000012);
//    randomizedSet.insert(1000000013);
//    randomizedSet.insert(1000000014);
//    randomizedSet.insert(1000000015);
//    randomizedSet.insert(1000000016);
//    randomizedSet.insert(1000000017);
//    randomizedSet.insert(1000000018);
//    randomizedSet.insert(1000000019);
//    randomizedSet.insert(1000000020);
//    randomizedSet.insert(1000000021);
//    randomizedSet.insert(1000000022);
//    randomizedSet.insert(1000000023);
//    randomizedSet.insert(1000000024);
//    randomizedSet.insert(1000000025);
//    randomizedSet.insert(1000000026);
//    randomizedSet.insert(1000000027);
//    randomizedSet.insert(1000000028);
//    randomizedSet.insert(1000000029);
//    randomizedSet.insert(1000000030);
//    randomizedSet.insert(1000000031);
//    randomizedSet.insert(1000000032);
//    randomizedSet.insert(1000000033);
//    randomizedSet.insert(1000000034);
//    randomizedSet.insert(1000000035);
//    randomizedSet.insert(1000000036);
//    randomizedSet.insert(1000000037);
//    randomizedSet.insert(1000000038);
//    randomizedSet.insert(1000000039);
//    randomizedSet.insert(1000000040);
//    randomizedSet.insert(1000000041);
//    randomizedSet.insert(1000000042);
//    randomizedSet.insert(1000000043);
//    randomizedSet.insert(1000000044);
//    randomizedSet.insert(1000000045);
//    randomizedSet.insert(1000000046);
//    randomizedSet.insert(1000000047);
//    randomizedSet.insert(1000000048);
//    randomizedSet.insert(1000000049);
//    randomizedSet.insert(1000000050);
//    randomizedSet.insert(1000000051);
//    randomizedSet.insert(1000000052);
//    randomizedSet.insert(1000000053);
//    randomizedSet.insert(1000000054);
//    randomizedSet.insert(1000000055);
//    randomizedSet.insert(1000000056);
//    randomizedSet.insert(1000000057);
//    randomizedSet.insert(1000000058);
//    randomizedSet.insert(1000000059);
//    randomizedSet.insert(1000000060);
//    randomizedSet.insert(1000000061);
//    randomizedSet.insert(1000000062);
//    randomizedSet.insert(1000000063);
//    randomizedSet.insert(1000000064);
//    randomizedSet.insert(1000000065);
//    randomizedSet.insert(1000000066);
//    randomizedSet.insert(1000000067);
//    randomizedSet.insert(1000000068);
//    randomizedSet.insert(1000000069);
//    randomizedSet.insert(1000000070);
//    randomizedSet.insert(1000000071);
//    randomizedSet.insert(1000000072);
//    randomizedSet.insert(1000000073);
//    randomizedSet.insert(1000000074);
//    randomizedSet.insert(1000000075);
//    randomizedSet.insert(1000000076);
//    randomizedSet.insert(1000000077);
//    randomizedSet.insert(1000000078);
//    randomizedSet.insert(1000000079);
//    randomizedSet.insert(1000000080);
//    randomizedSet.insert(1000000081);
//    randomizedSet.insert(1000000082);
//    randomizedSet.insert(1000000083);
//    randomizedSet.insert(1000000084);
//    randomizedSet.insert(1000000085);
//    randomizedSet.insert(1000000086);
//    randomizedSet.insert(1000000087);
//    randomizedSet.insert(1000000088);
//    randomizedSet.insert(1000000089);
//    randomizedSet.insert(1000000090);
//    randomizedSet.insert(1000000091);
//    randomizedSet.insert(1000000092);
//    randomizedSet.insert(1000000093);
//    randomizedSet.insert(1000000094);
//    randomizedSet.insert(1000000095);
//    randomizedSet.insert(1000000096);
//    randomizedSet.insert(1000000097);
//    randomizedSet.insert(1000000098);
//    randomizedSet.insert(1000000099);
//    randomizedSet.insert(-1000000000);
//    randomizedSet.insert(-1000000001);
//    randomizedSet.insert(-1000000002);
//    randomizedSet.insert(-1000000003);
//    randomizedSet.insert(-1000000004);
//    randomizedSet.insert(-1000000005);
//    randomizedSet.insert(-1000000006);
//    randomizedSet.insert(-1000000007);
//    randomizedSet.insert(-1000000008);
//    randomizedSet.insert(-1000000009);
//    randomizedSet.insert(-1000000010);
//    randomizedSet.insert(-1000000011);
//    randomizedSet.insert(-1000000012);
//    randomizedSet.insert(-1000000013);
//    randomizedSet.insert(-1000000014);
//    randomizedSet.insert(-1000000015);
//    randomizedSet.insert(-1000000016);
//    randomizedSet.insert(-1000000017);
//    randomizedSet.insert(-1000000018);
//    randomizedSet.insert(-1000000019);
//    randomizedSet.insert(-1000000020);
//    randomizedSet.insert(-1000000021);
//    randomizedSet.insert(-1000000022);
//    randomizedSet.insert(-1000000023);
//    randomizedSet.insert(-1000000024);
//    randomizedSet.insert(-1000000025);
//    randomizedSet.insert(-1000000026);
//    randomizedSet.insert(-1000000027);
//    randomizedSet.insert(-1000000028);
//    randomizedSet.insert(-1000000029);
//    randomizedSet.insert(-1000000030);
//    randomizedSet.insert(-1000000031);
//    randomizedSet.insert(-1000000032);
//    randomizedSet.insert(-1000000033);
//    randomizedSet.insert(-1000000034);
//    randomizedSet.insert(-1000000035);
//    randomizedSet.insert(-1000000036);
//    randomizedSet.insert(-1000000037);
//    randomizedSet.insert(-1000000038);
//    randomizedSet.insert(-1000000039);
//    randomizedSet.insert(-1000000040);
//    randomizedSet.insert(-1000000041);
//    randomizedSet.insert(-1000000042);
//    randomizedSet.insert(-1000000043);
//    randomizedSet.insert(-1000000044);
//    randomizedSet.insert(-1000000045);
//    randomizedSet.insert(-1000000046);
//    randomizedSet.insert(-1000000047);
//    randomizedSet.insert(-1000000048);
//    randomizedSet.insert(-1000000049);
//    randomizedSet.insert(-1000000050);
//    randomizedSet.insert(-1000000051);
//    randomizedSet.insert(-1000000052);
//    randomizedSet.insert(-1000000053);
//    randomizedSet.insert(-1000000054);
//    randomizedSet.insert(-1000000055);
//    randomizedSet.insert(-1000000056);
//    randomizedSet.insert(-1000000057);
//    randomizedSet.insert(-1000000058);
//    randomizedSet.insert(-1000000059);
//    randomizedSet.insert(-1000000060);
//    randomizedSet.insert(-1000000061);
//    randomizedSet.insert(-1000000062);
//    randomizedSet.insert(-1000000063);
//    randomizedSet.insert(-1000000064);
//    randomizedSet.insert(-1000000065);
//    randomizedSet.insert(-1000000066);
//    randomizedSet.insert(-1000000067);
//    randomizedSet.insert(-1000000068);
//    randomizedSet.insert(-1000000069);
//    randomizedSet.insert(-1000000070);
//    randomizedSet.insert(-1000000071);
//    randomizedSet.insert(-1000000072);
//    randomizedSet.insert(-1000000073);
//    randomizedSet.insert(-1000000074);
//    randomizedSet.insert(-1000000075);
//    randomizedSet.insert(-1000000076);
//    randomizedSet.insert(-1000000077);
//    randomizedSet.insert(-1000000078);
//    randomizedSet.insert(-1000000079);
//    randomizedSet.insert(-1000000080);
//    randomizedSet.insert(-1000000081);
//    randomizedSet.insert(-1000000082);
//    randomizedSet.insert(-1000000083);
//    randomizedSet.insert(-1000000084);
//    randomizedSet.insert(-1000000085);
//    randomizedSet.insert(-1000000086);
//    randomizedSet.insert(-1000000087);
//    randomizedSet.insert(-1000000088);
//    randomizedSet.insert(-1000000089);
//    randomizedSet.insert(-1000000090);
//    randomizedSet.insert(-1000000091);
//    randomizedSet.insert(-1000000092);
//    randomizedSet.insert(-1000000093);
//    randomizedSet.insert(-1000000094);
//    randomizedSet.insert(-1000000095);
//    randomizedSet.insert(-1000000096);
//    randomizedSet.insert(-1000000097);
//    randomizedSet.insert(-1000000098);
//    randomizedSet.insert(-1000000099);
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.getRandom();
//    randomizedSet.remove(1000000000);
//    randomizedSet.remove(1000000001);
//    randomizedSet.remove(1000000002);
//    randomizedSet.remove(1000000003);
//    randomizedSet.remove(1000000004);
//    randomizedSet.remove(1000000005);
//    randomizedSet.remove(1000000006);
//    randomizedSet.remove(1000000007);
//    randomizedSet.remove(1000000008);
//    randomizedSet.remove(1000000009);
//    randomizedSet.remove(1000000010);
//    randomizedSet.remove(1000000011);
//    randomizedSet.remove(1000000012);
//    randomizedSet.remove(1000000013);
//    randomizedSet.remove(1000000014);
//    randomizedSet.remove(1000000015);
//    randomizedSet.remove(1000000016);
//    randomizedSet.remove(1000000017);
//    randomizedSet.remove(1000000018);
//    randomizedSet.remove(1000000019);
//    randomizedSet.remove(1000000020);
//    randomizedSet.remove(1000000021);
//    randomizedSet.remove(1000000022);
//    randomizedSet.remove(1000000023);
//    randomizedSet.remove(1000000024);
//    randomizedSet.remove(1000000025);
//    randomizedSet.remove(1000000026);
//    randomizedSet.remove(1000000027);
//    randomizedSet.remove(1000000028);
//    randomizedSet.remove(1000000029);
//    randomizedSet.remove(1000000030);
//    randomizedSet.remove(1000000031);
//    randomizedSet.remove(1000000032);
//    randomizedSet.remove(1000000033);
//    randomizedSet.remove(1000000034);
//    randomizedSet.remove(1000000035);
//    randomizedSet.remove(1000000036);
//    randomizedSet.remove(1000000037);
//    randomizedSet.remove(1000000038);
//    randomizedSet.remove(1000000039);
//    randomizedSet.remove(1000000040);
//    randomizedSet.remove(1000000041);
//    randomizedSet.remove(1000000042);
//    randomizedSet.remove(1000000043);
//    randomizedSet.remove(1000000044);
//    randomizedSet.remove(1000000045);
//    randomizedSet.remove(1000000046);
//    randomizedSet.remove(1000000047);
//    randomizedSet.remove(1000000048);
//    randomizedSet.remove(1000000049);
//    randomizedSet.remove(1000000050);
//    randomizedSet.remove(1000000051);
//    randomizedSet.remove(1000000052);
//    randomizedSet.remove(1000000053);
//    randomizedSet.remove(1000000054);
//    randomizedSet.remove(1000000055);
//    randomizedSet.remove(1000000056);
//    randomizedSet.remove(1000000057);
//    randomizedSet.remove(1000000058);
//    randomizedSet.remove(1000000059);
//    randomizedSet.remove(1000000060);
//    randomizedSet.remove(1000000061);
//    randomizedSet.remove(1000000062);
//    randomizedSet.remove(1000000063);
//    randomizedSet.remove(1000000064);
//    randomizedSet.remove(1000000065);
//    randomizedSet.remove(1000000066);
//    randomizedSet.remove(1000000067);
//    randomizedSet.remove(1000000068);
//    randomizedSet.remove(1000000069);
//    randomizedSet.remove(1000000070);
//    randomizedSet.remove(1000000071);
//    randomizedSet.remove(1000000072);
//    randomizedSet.remove(1000000073);
//    randomizedSet.remove(1000000074);
//    randomizedSet.remove(1000000075);
//    randomizedSet.remove(1000000076);
//    randomizedSet.remove(1000000077);
//    randomizedSet.remove(1000000078);
//    randomizedSet.remove(1000000079);
//    randomizedSet.remove(1000000080);
//    randomizedSet.remove(1000000081);
//    randomizedSet.remove(1000000082);
//    randomizedSet.remove(1000000083);
//    randomizedSet.remove(1000000084);
//    randomizedSet.remove(1000000085);
//    randomizedSet.remove(1000000086);
//    randomizedSet.remove(1000000087);
//    randomizedSet.remove(1000000088);
//    randomizedSet.remove(1000000089);
//    randomizedSet.remove(1000000090);
//    randomizedSet.remove(1000000091);
//    randomizedSet.remove(1000000092);
//    randomizedSet.remove(1000000093);
//    randomizedSet.remove(1000000094);
//    randomizedSet.remove(1000000095);
//    randomizedSet.remove(1000000096);
//    randomizedSet.remove(1000000097);
//    randomizedSet.remove(1000000098);
//    randomizedSet.remove(1000000099);
//    randomizedSet.remove(-1000000000);
//    randomizedSet.remove(-1000000001);
//    randomizedSet.remove(-1000000002);
//    randomizedSet.remove(-1000000003);
//    randomizedSet.remove(-1000000004);
//    randomizedSet.remove(-1000000005);
//    randomizedSet.remove(-1000000006);
//    randomizedSet.remove(-1000000007);
//    randomizedSet.remove(-1000000008);
//    randomizedSet.remove(-1000000009);
//    randomizedSet.remove(-1000000010);
//    randomizedSet.remove(-1000000011);
//    randomizedSet.remove(-1000000012);
//    randomizedSet.remove(-1000000013);
//    randomizedSet.remove(-1000000014);
//    randomizedSet.remove(-1000000015);
//    randomizedSet.remove(-1000000016);
//    randomizedSet.remove(-1000000017);
//    randomizedSet.remove(-1000000018);
//    randomizedSet.remove(-1000000019);
//    randomizedSet.remove(-1000000020);
//    randomizedSet.remove(-1000000021);
//    randomizedSet.remove(-1000000022);
//    randomizedSet.remove(-1000000023);
//    randomizedSet.remove(-1000000024);
//    randomizedSet.remove(-1000000025);
//    randomizedSet.remove(-1000000026);
//    randomizedSet.remove(-1000000027);
//    randomizedSet.remove(-1000000028);
//    randomizedSet.remove(-1000000029);
//    randomizedSet.remove(-1000000030);
//    randomizedSet.remove(-1000000031);
//    randomizedSet.remove(-1000000032);
//    randomizedSet.remove(-1000000033);
//    randomizedSet.remove(-1000000034);
//    randomizedSet.remove(-1000000035);
//    randomizedSet.remove(-1000000036);
//    randomizedSet.remove(-1000000037);
//    randomizedSet.remove(-1000000038);
//    randomizedSet.remove(-1000000039);
//    randomizedSet.remove(-1000000040);
//    randomizedSet.remove(-1000000041);
//    randomizedSet.remove(-1000000042);
//    randomizedSet.remove(-1000000043);
//    randomizedSet.remove(-1000000044);
//    randomizedSet.remove(-1000000045);
//    randomizedSet.remove(-1000000046);
//    randomizedSet.remove(-1000000047);
//    randomizedSet.remove(-1000000048);
//    randomizedSet.remove(-1000000049);
//    randomizedSet.remove(-1000000050);
//    randomizedSet.remove(-1000000051);
//    randomizedSet.remove(-1000000052);
//    randomizedSet.remove(-1000000053);
//    randomizedSet.remove(-1000000054);
//    randomizedSet.remove(-1000000055);
//    randomizedSet.remove(-1000000056);
//    randomizedSet.remove(-1000000057);
//    randomizedSet.remove(-1000000058);
//    randomizedSet.remove(-1000000059);
//    randomizedSet.remove(-1000000060);
//    randomizedSet.remove(-1000000061);
//    randomizedSet.remove(-1000000062);
//    randomizedSet.remove(-1000000063);
//    randomizedSet.remove(-1000000064);
//    randomizedSet.remove(-1000000065);
//    randomizedSet.remove(-1000000066);
//    randomizedSet.remove(-1000000067);
//    randomizedSet.remove(-1000000068);
//    randomizedSet.remove(-1000000069);
//    randomizedSet.remove(-1000000070);
//    randomizedSet.remove(-1000000071);
//    randomizedSet.remove(-1000000072);
//    randomizedSet.remove(-1000000073);
//    randomizedSet.remove(-1000000074);
//    randomizedSet.remove(-1000000075);
//    randomizedSet.remove(-1000000076);
//    randomizedSet.remove(-1000000077);
//    randomizedSet.remove(-1000000078);
//    randomizedSet.remove(-1000000079);
//    randomizedSet.remove(-1000000080);
//    randomizedSet.remove(-1000000081);
//    randomizedSet.remove(-1000000082);
//    randomizedSet.remove(-1000000083);
//    randomizedSet.remove(-1000000084);
//    randomizedSet.remove(-1000000085);
//    randomizedSet.remove(-1000000086);
//    randomizedSet.remove(-1000000087);
//    randomizedSet.remove(-1000000088);
//    randomizedSet.remove(-1000000089);
//    randomizedSet.remove(-1000000090);
//    randomizedSet.remove(-1000000091);
//    randomizedSet.remove(-1000000092);
//    randomizedSet.remove(-1000000093);
//    randomizedSet.remove(-1000000094);
//    randomizedSet.remove(-1000000095);
//    randomizedSet.remove(-1000000096);
//    randomizedSet.remove(-1000000097);
//    randomizedSet.remove(-1000000098);
//    randomizedSet.remove(-1000000099);

    RandomizedSet randomSet = RandomizedSet();
    randomSet.insert(1000000000);
    randomSet.insert(1000000001);
    randomSet.insert(1000000002);
    randomSet.insert(1000000003);
    randomSet.insert(1000000004);
    randomSet.insert(1000000005);
    randomSet.insert(1000000006);
    randomSet.insert(1000000007);
    randomSet.insert(1000000008);
    randomSet.insert(1000000009);
    randomSet.insert(1000000010);
    randomSet.insert(1000000011);
    randomSet.insert(1000000012);
    randomSet.insert(1000000013);
    randomSet.insert(1000000014);
    randomSet.insert(1000000015);
    randomSet.insert(1000000016);
    randomSet.insert(1000000017);
    randomSet.insert(1000000018);
    randomSet.insert(1000000019);
    randomSet.insert(1000000020);
    randomSet.insert(1000000021);
    randomSet.insert(1000000022);
    randomSet.insert(1000000023);
    randomSet.insert(1000000024);
    randomSet.insert(1000000025);
    randomSet.insert(1000000026);
    randomSet.insert(1000000027);
    randomSet.insert(1000000028);
    randomSet.insert(1000000029);
    randomSet.insert(1000000030);
    randomSet.insert(1000000031);
    randomSet.insert(1000000032);
    randomSet.insert(1000000033);
    randomSet.insert(1000000034);
    randomSet.insert(1000000035);
    randomSet.insert(1000000036);
    randomSet.insert(1000000037);
    randomSet.insert(1000000038);
    randomSet.insert(1000000039);
    randomSet.insert(1000000040);
    randomSet.insert(1000000041);
    randomSet.insert(1000000042);
    randomSet.insert(1000000043);
    randomSet.insert(1000000044);
    randomSet.insert(1000000045);
    randomSet.insert(1000000046);
    randomSet.insert(1000000047);
    randomSet.insert(1000000048);
    randomSet.insert(1000000049);
    randomSet.insert(1000000050);
    randomSet.insert(1000000051);
    randomSet.insert(1000000052);
    randomSet.insert(1000000053);
    randomSet.insert(1000000054);
    randomSet.insert(1000000055);
    randomSet.insert(1000000056);
    randomSet.insert(1000000057);
    randomSet.insert(1000000058);
    randomSet.insert(1000000059);
    randomSet.insert(1000000060);
    randomSet.insert(1000000061);
    randomSet.insert(1000000062);
    randomSet.insert(1000000063);
    randomSet.insert(1000000064);
    randomSet.insert(1000000065);
    randomSet.insert(1000000066);
    randomSet.insert(1000000067);
    randomSet.insert(1000000068);
    randomSet.insert(1000000069);
    randomSet.insert(1000000070);
    randomSet.insert(1000000071);
    randomSet.insert(1000000072);
    randomSet.insert(1000000073);
    randomSet.insert(1000000074);
    randomSet.insert(1000000075);
    randomSet.insert(1000000076);
    randomSet.insert(1000000077);
    randomSet.insert(1000000078);
    randomSet.insert(1000000079);
    randomSet.insert(1000000080);
    randomSet.insert(1000000081);
    randomSet.insert(1000000082);
    randomSet.insert(1000000083);
    randomSet.insert(1000000084);
    randomSet.insert(1000000085);
    randomSet.insert(1000000086);
    randomSet.insert(1000000087);
    randomSet.insert(1000000088);
    randomSet.insert(1000000089);
    randomSet.insert(1000000090);
    randomSet.insert(1000000091);
    randomSet.insert(1000000092);
    randomSet.insert(1000000093);
    randomSet.insert(1000000094);
    randomSet.insert(1000000095);
    randomSet.insert(1000000096);
    randomSet.insert(1000000097);
    randomSet.insert(1000000098);
    randomSet.insert(1000000099);
    randomSet.insert(-1000000000);
    randomSet.insert(-1000000001);
    randomSet.insert(-1000000002);
    randomSet.insert(-1000000003);
    randomSet.insert(-1000000004);
    randomSet.insert(-1000000005);
    randomSet.insert(-1000000006);
    randomSet.insert(-1000000007);
    randomSet.insert(-1000000008);
    randomSet.insert(-1000000009);
    randomSet.insert(-1000000010);
    randomSet.insert(-1000000011);
    randomSet.insert(-1000000012);
    randomSet.insert(-1000000013);
    randomSet.insert(-1000000014);
    randomSet.insert(-1000000015);
    randomSet.insert(-1000000016);
    randomSet.insert(-1000000017);
    randomSet.insert(-1000000018);
    randomSet.insert(-1000000019);
    randomSet.insert(-1000000020);
    randomSet.insert(-1000000021);
    randomSet.insert(-1000000022);
    randomSet.insert(-1000000023);
    randomSet.insert(-1000000024);
    randomSet.insert(-1000000025);
    randomSet.insert(-1000000026);
    randomSet.insert(-1000000027);
    randomSet.insert(-1000000028);
    randomSet.insert(-1000000029);
    randomSet.insert(-1000000030);
    randomSet.insert(-1000000031);
    randomSet.insert(-1000000032);
    randomSet.insert(-1000000033);
    randomSet.insert(-1000000034);
    randomSet.insert(-1000000035);
    randomSet.insert(-1000000036);
    randomSet.insert(-1000000037);
    randomSet.insert(-1000000038);
    randomSet.insert(-1000000039);
    randomSet.insert(-1000000040);
    randomSet.insert(-1000000041);
    randomSet.insert(-1000000042);
    randomSet.insert(-1000000043);
    randomSet.insert(-1000000044);
    randomSet.insert(-1000000045);
    randomSet.insert(-1000000046);
    randomSet.insert(-1000000047);
    randomSet.insert(-1000000048);
    randomSet.insert(-1000000049);
    randomSet.insert(-1000000050);
    randomSet.insert(-1000000051);
    randomSet.insert(-1000000052);
    randomSet.insert(-1000000053);
    randomSet.insert(-1000000054);
    randomSet.insert(-1000000055);
    randomSet.insert(-1000000056);
    randomSet.insert(-1000000057);
    randomSet.insert(-1000000058);
    randomSet.insert(-1000000059);
    randomSet.insert(-1000000060);
    randomSet.insert(-1000000061);
    randomSet.insert(-1000000062);
    randomSet.insert(-1000000063);
    randomSet.insert(-1000000064);
    randomSet.insert(-1000000065);
    randomSet.insert(-1000000066);
    randomSet.insert(-1000000067);
    randomSet.insert(-1000000068);
    randomSet.insert(-1000000069);
    randomSet.insert(-1000000070);
    randomSet.insert(-1000000071);
    randomSet.insert(-1000000072);
    randomSet.insert(-1000000073);
    randomSet.insert(-1000000074);
    randomSet.insert(-1000000075);
    randomSet.insert(-1000000076);
    randomSet.insert(-1000000077);
    randomSet.insert(-1000000078);
    randomSet.insert(-1000000079);
    randomSet.insert(-1000000080);
    randomSet.insert(-1000000081);
    randomSet.insert(-1000000082);
    randomSet.insert(-1000000083);
    randomSet.insert(-1000000084);
    randomSet.insert(-1000000085);
    randomSet.insert(-1000000086);
    randomSet.insert(-1000000087);
    randomSet.insert(-1000000088);
    randomSet.insert(-1000000089);
    randomSet.insert(-1000000090);
    randomSet.insert(-1000000091);
    randomSet.insert(-1000000092);
    randomSet.insert(-1000000093);
    randomSet.insert(-1000000094);
    randomSet.insert(-1000000095);
    randomSet.insert(-1000000096);
    randomSet.insert(-1000000097);
    randomSet.insert(-1000000098);
    randomSet.insert(-1000000099);
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.getRandom();
    randomSet.remove(1000000000);
    randomSet.remove(1000000001);
    randomSet.remove(1000000002);
    randomSet.remove(1000000003);
    randomSet.remove(1000000004);
    randomSet.remove(1000000005);
    randomSet.remove(1000000006);
    randomSet.remove(1000000007);
    randomSet.remove(1000000008);
    randomSet.remove(1000000009);
    randomSet.remove(1000000010);
    randomSet.remove(1000000011);
    randomSet.remove(1000000012);
    randomSet.remove(1000000013);
    randomSet.remove(1000000014);
    randomSet.remove(1000000015);
    randomSet.remove(1000000016);
    randomSet.remove(1000000017);
    randomSet.remove(1000000018);
    randomSet.remove(1000000019);
    randomSet.remove(1000000020);
    randomSet.remove(1000000021);
    randomSet.remove(1000000022);
    randomSet.remove(1000000023);
    randomSet.remove(1000000024);
    randomSet.remove(1000000025);
    randomSet.remove(1000000026);
    randomSet.remove(1000000027);
    randomSet.remove(1000000028);
    randomSet.remove(1000000029);
    randomSet.remove(1000000030);
    randomSet.remove(1000000031);
    randomSet.remove(1000000032);
    randomSet.remove(1000000033);
    randomSet.remove(1000000034);
    randomSet.remove(1000000035);
    randomSet.remove(1000000036);
    randomSet.remove(1000000037);
    randomSet.remove(1000000038);
    randomSet.remove(1000000039);
    randomSet.remove(1000000040);
    randomSet.remove(1000000041);
    randomSet.remove(1000000042);
    randomSet.remove(1000000043);
    randomSet.remove(1000000044);
    randomSet.remove(1000000045);
    randomSet.remove(1000000046);
    randomSet.remove(1000000047);
    randomSet.remove(1000000048);
    randomSet.remove(1000000049);
    randomSet.remove(1000000050);
    randomSet.remove(1000000051);
    randomSet.remove(1000000052);
    randomSet.remove(1000000053);
    randomSet.remove(1000000054);
    randomSet.remove(1000000055);
    randomSet.remove(1000000056);
    randomSet.remove(1000000057);
    randomSet.remove(1000000058);
    randomSet.remove(1000000059);
    randomSet.remove(1000000060);
    randomSet.remove(1000000061);
    randomSet.remove(1000000062);
    randomSet.remove(1000000063);
    randomSet.remove(1000000064);
    randomSet.remove(1000000065);
    randomSet.remove(1000000066);
    randomSet.remove(1000000067);
    randomSet.remove(1000000068);
    randomSet.remove(1000000069);
    randomSet.remove(1000000070);
    randomSet.remove(1000000071);
    randomSet.remove(1000000072);
    randomSet.remove(1000000073);
    randomSet.remove(1000000074);
    randomSet.remove(1000000075);
    randomSet.remove(1000000076);
    randomSet.remove(1000000077);
    randomSet.remove(1000000078);
    randomSet.remove(1000000079);
    randomSet.remove(1000000080);
    randomSet.remove(1000000081);
    randomSet.remove(1000000082);
    randomSet.remove(1000000083);
    randomSet.remove(1000000084);
    randomSet.remove(1000000085);
    randomSet.remove(1000000086);
    randomSet.remove(1000000087);
    randomSet.remove(1000000088);
    randomSet.remove(1000000089);
    randomSet.remove(1000000090);
    randomSet.remove(1000000091);
    randomSet.remove(1000000092);
    randomSet.remove(1000000093);
    randomSet.remove(1000000094);
    randomSet.remove(1000000095);
    randomSet.remove(1000000096);
    randomSet.remove(1000000097);
    randomSet.remove(1000000098);
    randomSet.remove(1000000099);
    randomSet.remove(-1000000000);
    randomSet.remove(-1000000001);
    randomSet.remove(-1000000002);
    randomSet.remove(-1000000003);
    randomSet.remove(-1000000004);
    randomSet.remove(-1000000005);
    randomSet.remove(-1000000006);
    randomSet.remove(-1000000007);
    randomSet.remove(-1000000008);
    randomSet.remove(-1000000009);
    randomSet.remove(-1000000010);
    randomSet.remove(-1000000011);
    randomSet.remove(-1000000012);
    randomSet.remove(-1000000013);
    randomSet.remove(-1000000014);
    randomSet.remove(-1000000015);
    randomSet.remove(-1000000016);
    randomSet.remove(-1000000017);
    randomSet.remove(-1000000018);
    randomSet.remove(-1000000019);
    randomSet.remove(-1000000020);
    randomSet.remove(-1000000021);
    randomSet.remove(-1000000022);
    randomSet.remove(-1000000023);
    randomSet.remove(-1000000024);
    randomSet.remove(-1000000025);
    randomSet.remove(-1000000026);
    randomSet.remove(-1000000027);
    randomSet.remove(-1000000028);
    randomSet.remove(-1000000029);
    randomSet.remove(-1000000030);
    randomSet.remove(-1000000031);
    randomSet.remove(-1000000032);
    randomSet.remove(-1000000033);
    randomSet.remove(-1000000034);
    randomSet.remove(-1000000035);
    randomSet.remove(-1000000036);
    randomSet.remove(-1000000037);
    randomSet.remove(-1000000038);
    randomSet.remove(-1000000039);
    randomSet.remove(-1000000040);
    randomSet.remove(-1000000041);
    randomSet.remove(-1000000042);
    randomSet.remove(-1000000043);
    randomSet.remove(-1000000044);
    randomSet.remove(-1000000045);
    randomSet.remove(-1000000046);
    randomSet.remove(-1000000047);
    randomSet.remove(-1000000048);
    randomSet.remove(-1000000049);
    randomSet.remove(-1000000050);
    randomSet.remove(-1000000051);
    randomSet.remove(-1000000052);
    randomSet.remove(-1000000053);
    randomSet.remove(-1000000054);
    randomSet.remove(-1000000055);
    randomSet.remove(-1000000056);
    randomSet.remove(-1000000057);
    randomSet.remove(-1000000058);
    randomSet.remove(-1000000059);
    randomSet.remove(-1000000060);
    randomSet.remove(-1000000061);
    randomSet.remove(-1000000062);
    randomSet.remove(-1000000063);
    randomSet.remove(-1000000064);
    randomSet.remove(-1000000065);
    randomSet.remove(-1000000066);
    randomSet.remove(-1000000067);
    randomSet.remove(-1000000068);
    randomSet.remove(-1000000069);
    randomSet.remove(-1000000070);
    randomSet.remove(-1000000071);
    randomSet.remove(-1000000072);
    randomSet.remove(-1000000073);
    randomSet.remove(-1000000074);
    randomSet.remove(-1000000075);
    randomSet.remove(-1000000076);
    randomSet.remove(-1000000077);
    randomSet.remove(-1000000078);
    randomSet.remove(-1000000079);
    randomSet.remove(-1000000080);
    randomSet.remove(-1000000081);
    randomSet.remove(-1000000082);
    randomSet.remove(-1000000083);
    randomSet.remove(-1000000084);
    randomSet.remove(-1000000085);
    randomSet.remove(-1000000086);
    randomSet.remove(-1000000087);
    randomSet.remove(-1000000088);
    randomSet.remove(-1000000089);
    randomSet.remove(-1000000090);
    randomSet.remove(-1000000091);
    randomSet.remove(-1000000092);
    randomSet.remove(-1000000093);
    randomSet.remove(-1000000094);
    randomSet.remove(-1000000095);
    randomSet.remove(-1000000096);
    randomSet.remove(-1000000097);
    randomSet.remove(-1000000098);
    randomSet.remove(-1000000099);

    return 0;
}
