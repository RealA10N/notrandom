"""notrandom: Pseudorandom, 100% reproducible variable generators.

Implementation of the builtin 'random' API, which guarantees 100% deterministic
and reproducible computation of values, regardless of python versions,
operating system or environment (a guarantee that the 'random' module does not
provide). Non randomness guaranteed!

This package is based on the builtin 'random' module and strongly resembles its
API, with only minor adjustments. In particular, all global functions of random
are also available in notrandom, in addition to the notrandom.Random object which
implements the random.Random api. Check out the test.py file for usage examples.

It is important to note that the values computed by the notrandom are actually
not random at all, as the process is 100% deterministic (that is the whole
point!). Obviously, it is not intended to be used cryptographically in any way
or circumstance.

Behind the scenes, notrandom uses the cryptographic hash function SHA256, in a
process that resembles the OFB mode of operation. The algorithm produces blocks
of 256bits ad-hoc, by hashing the previous 256bit block using SHA256, where the
initial block is derived from the key directly. Then using similar technics to
the ones that 'random' uses, random floating point numbers and integers in
range are derived when requested."""

from __future__ import annotations

import random as _random
import typing as _tp
from hashlib import sha256 as _sha256

VERSION = "1.0.0"

__all__ = [
    "Random",
    "NotRandom",
    "betavariate",
    "choice",
    "choices",
    "expovariate",
    "gammavariate",
    "gauss",
    "getrandbits",
    "getstate",
    "lognormvariate",
    "normalvariate",
    "paretovariate",
    "randbytes",
    "randint",
    "random",
    "randrange",
    "sample",
    "seed",
    "setstate",
    "shuffle",
    "triangular",
    "uniform",
    "vonmisesvariate",
    "weibullvariate",
]


_SeedTypes: _tp.TypeAlias = _tp.Union[int, str, bytes]


class UnseededRandomGeneratorError(RuntimeError):
    pass


class Random(_random.Random):
    def __init__(self, seed: _tp.Optional[_SeedTypes] = None) -> None:
        self._seed: _tp.Optional[bytes] = self._convert_to_byteseed(seed)

    def seed(self, seed: _tp.Optional[_SeedTypes]) -> None:
        """Set the set of the reproducible-random generator. Pass in None to
        un-seed the generator."""
        self._seed = None if seed is None else self._convert_to_byteseed(seed)

    def _convert_to_byteseed(self, input_seed: _SeedTypes) -> bytes:
        """Converts any valid input seed into a bytes block, which is used as
        the actual seed."""

        if isinstance(input_seed, str):
            input_seed = input_seed.encode(encoding="utf8")
        if isinstance(input_seed, bytes):
            input_seed = _sha256(input_seed).digest()
        if isinstance(input_seed, int):
            input_seed = input_seed.to_bytes(32, byteorder="big")
        return input_seed

    def getblock(self) -> bytes:
        """Computes the next block of 32 reproducible-random bytes and returns
        them as a bytes object."""

        if self._seed is None:
            raise UnseededRandomGeneratorError(
                "reproducible random generator must be provided with initial"
                " seed using the initializer or the seed() method."
            )

        self._seed = _sha256(self._seed).digest()
        return self._seed

    def randbytes(self, n: int) -> bytes:
        """Computes the next n reproducible-random bytes and returns them as a
        bytes object."""
        blocks = (n + 31) // 32
        return b"".join(self.getblock() for _ in range(blocks))[:n]

    def getrandbits(self, n: int) -> int:
        """Computes the next n reproducible-random bits and returns them as an
        int that consists of n bits."""
        if n < 0:
            raise ValueError("number of bits must be non-negative")

        # compute the number of bytes needed to generate n bits,
        # by dividing by 8 and rounding up. also compute the extra bits.
        # then shift drop the extra bytes out by shifting.
        numbytes = (n + 7) // 8
        extrabits = 8 * numbytes - n
        x = int.from_bytes(self.randbytes(numbytes), byteorder="big")
        return x >> extrabits

    def getstate(self) -> bytes:
        return self._seed

    def setstate(self, state: bytes) -> None:
        if not isinstance(state, bytes) or len(state) != 32:
            raise ValueError("state must be a 32 byte string")
        self._seed = state

    def random(self) -> float:
        # A python float consists of 53bits of precision.
        # Here we generate an integer consisting of 53bits, then divide it
        # to fit in the range [0, 1]. This is a similar implementation to the
        # implementation of the builtin random.random() function.
        return self.getrandbits(53) * (2**-53)


NotRandom = Random  # recommend alias to use for readability
_inst = Random()
seed = _inst.seed
random = _inst.random
uniform = _inst.uniform
triangular = _inst.triangular
randint = _inst.randint
choice = _inst.choice
randrange = _inst.randrange
sample = _inst.sample
shuffle = _inst.shuffle
choices = _inst.choices
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
betavariate = _inst.betavariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getstate = _inst.getstate
setstate = _inst.setstate
getrandbits = _inst.getrandbits
randbytes = _inst.randbytes
