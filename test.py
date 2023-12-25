from __future__ import annotations

from typing import Union

import notrandom


def test_seeded_instance(seed: Union[bytes, str, int]) -> None:
    rnd = notrandom.Random(seed)
    print(rnd.getblock().hex())
    print(rnd.randbytes(10).hex())
    print("".join(str(rnd.getrandbits(1)) for _ in range(100)))

    lst = list(range(10))
    for _ in range(10):
        print(rnd.random())
        print(rnd.randint(1, 100))
        rnd.shuffle(lst)
        print(lst)


test_seeded_instance(0)
test_seeded_instance("This is a very long string" * 100)
test_seeded_instance(b"deadbeef")
test_seeded_instance(107804174469117380743351761694252458912307896999095263774861835630573032431634)
