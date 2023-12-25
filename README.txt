notrandom: Pseudorandom, 100% reproducible variable generators.

Implementation of the builtin 'random' API, which guarantees 100% deterministic and reproducible computation of values, regardless of python versions, operating system or environment (a guarantee that the 'random' module does not provide). Non randomness guaranteed!

For example, when seeding the generator with the integer 0, the those are the first 3 floating numbers, across all systems, Python implement and versions. Try it yourself!

>> from notrandom import random, seed
>> seed(0)
>> print(random(), random(), random())
0.40003172633476936 0.16874476805609495 0.07212944838504431

This package is based on the builtin 'random' module and strongly resembles its API, with only minor adjustments. In particular, all global functions of random are also available in notrandom, in addition to the notrandom.Random object which implements the random.Random api. Check out the test.py file for usage examples.

It is important to note that the values computed by the notrandom are actually not random at all, as the process is 100% deterministic (that is the whole point!). Obviously, it is not intended to be used cryptographically in any way or circumstance.

Behind the scenes, notrandom uses the cryptographic hash function SHA256, in a process that resembles the OFB mode of operation. The algorithm produces blocks of 256bits ad-hoc, by hashing the previous 256bit block using SHA256, where the initial block is derived from the key directly. Then using similar technics to the ones that 'random' uses, random floating point numbers and integers in range are derived when requested.