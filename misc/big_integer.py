class BigInt:
    from typing import Union

    CHUNK_SIZE = 9
    MOD = 10 ** 9
    NTT_MOD = 998244353
    NTT_G = 3

    def __init__(self, val: Union[int, str, "BigInt"] = 0):
        self.neg = False
        self.arr = []

        if isinstance(val, BigInt):
            self.neg = val.neg
            self.arr = val.arr[:]
        elif isinstance(val, int):
            self._from_int(val)
        elif isinstance(val, str):
            self._from_str(val)

    def _from_int(self, val: int):
        if val == 0:
            return
        if val < 0:
            self.neg = True
            val = -val
        while val > 0:
            val, rem = divmod(val, self.MOD)
            self.arr.append(rem)

    def _from_str(self, s: str):
        s = s.strip()
        if not s or s == "0":
            return
        if s[0] == "-":
            self.neg = True
            s = s[1:]
        elif s[0] == "+":
            s = s[1:]

        C = self.CHUNK_SIZE
        self.arr = [
            int(s[max(0, i - C) : i]) for i in range(len(s), 0, -C)
        ]
        self._shrink()

    def _shrink(self):
        while self.arr and self.arr[-1] == 0:
            self.arr.pop()
        if not self.arr:
            self.neg = False

    def is_zero(self) -> bool:
        return not self.arr

    def __str__(self) -> str:
        if self.is_zero():
            return "0"
        res = ["-"] if self.neg else []
        res.append(str(self.arr[-1]))
        for x in reversed(self.arr[:-1]):
            res.append(f"{x:09d}")
        return "".join(res)

    __repr__ = __str__

    def _abs_lt(self, other: "BigInt") -> bool:
        if len(self.arr) != len(other.arr):
            return len(self.arr) < len(other.arr)
        for a, b in zip(reversed(self.arr), reversed(other.arr)):
            if a != b:
                return a < b
        return False

    def __eq__(self, other: "BigInt") -> bool:
        return self.neg == other.neg and self.arr == other.arr

    def __lt__(self, other: "BigInt") -> bool:
        if self.neg != other.neg:
            return self.neg
        return self._abs_lt(other) if not self.neg else other._abs_lt(self)

    def __add__(self, other: "BigInt") -> "BigInt":
        if not isinstance(other, BigInt):
            other = BigInt(other)

        if self.neg == other.neg:
            res = BigInt()
            res.neg = self.neg
            res.arr = self._raw_add(self.arr, other.arr)
            return res

        if self._abs_lt(other):
            res = BigInt()
            res.neg = other.neg
            res.arr = self._raw_sub(other.arr, self.arr)
            return res
        else:
            res = BigInt()
            res.neg = self.neg
            res.arr = self._raw_sub(self.arr, other.arr)
            return res

    def __sub__(self, other: "BigInt") -> "BigInt":
        if not isinstance(other, BigInt):
            other = BigInt(other)
        other_neg = BigInt(other)
        other_neg.neg = not other_neg.neg if not other_neg.is_zero() else False
        return self + other_neg

    @classmethod
    def _raw_add(cls, a: list, b: list) -> list:
        c = []
        carry = 0
        n = max(len(a), len(b))
        for i in range(n):
            val = carry + (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
            carry, val = divmod(val, cls.MOD)
            c.append(val)
        if carry:
            c.append(carry)
        return c

    @classmethod
    def _raw_sub(cls, a: list, b: list) -> list:
        c = a[:]
        borrow = 0
        for i in range(len(a)):
            val = c[i] - borrow - (b[i] if i < len(b) else 0)
            if val < 0:
                val += cls.MOD
                borrow = 1
            else:
                borrow = 0
            c[i] = val
        while c and c[-1] == 0:
            c.pop()
        return c

    @classmethod
    def _schoolbook_mul(cls, a: list, b: list) -> list:
        c = [0] * (len(a) + len(b))
        for i in range(len(a)):
            ai = a[i]
            if ai == 0:
                continue
            carry = 0
            for j in range(len(b)):
                val = c[i + j] + ai * b[j] + carry
                carry, val = divmod(val, cls.MOD)
                c[i + j] = val
            if carry:
                c[i + len(b)] += carry
        while c and c[-1] == 0:
            c.pop()
        return c

    def __mul__(self, other: "BigInt") -> "BigInt":
        if not isinstance(other, BigInt):
            other = BigInt(other)
        if self.is_zero() or other.is_zero():
            return BigInt(0)

        res = BigInt()
        res.neg = self.neg ^ other.neg

        if len(self.arr) + len(other.arr) < 150:
            res.arr = self._schoolbook_mul(self.arr, other.arr)
        else:
            res.arr = self._ntt_mul(self.arr, other.arr)
        return res

    @classmethod
    def _ntt(cls, a, invert):
        n = len(a)
        j = 0
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                a[i], a[j] = a[j], a[i]
        len_step = 2
        while len_step <= n:
            wlen = pow(cls.NTT_G, (cls.NTT_MOD - 1) // len_step, cls.NTT_MOD)
            if invert:
                wlen = pow(wlen, cls.NTT_MOD - 2, cls.NTT_MOD)
            for i in range(0, n, len_step):
                w = 1
                for j in range(len_step // 2):
                    u, v = a[i + j], (a[i + j + len_step // 2] * w) % cls.NTT_MOD
                    a[i + j] = (u + v) % cls.NTT_MOD
                    a[i + j + len_step // 2] = (u - v) % cls.NTT_MOD
                    w = (w * wlen) % cls.NTT_MOD
            len_step <<= 1
        if invert:
            n_inv = pow(n, cls.NTT_MOD - 2, cls.NTT_MOD)
            for i in range(n):
                a[i] = (a[i] * n_inv) % cls.NTT_MOD

    @classmethod
    def _to_base10(cls, arr: list) -> list:
        res = []
        for x in arr:
            for _ in range(9):
                res.append(x % 10)
                x //= 10
        while res and res[-1] == 0:
            res.pop()
        return res

    @classmethod
    def _ntt_mul(cls, a_arr: list, b_arr: list) -> list:
        A_b10 = cls._to_base10(a_arr)
        B_b10 = cls._to_base10(b_arr)

        n = 1
        while n < len(A_b10) + len(B_b10):
            n <<= 1

        A = A_b10 + [0] * (n - len(A_b10))
        B = B_b10 + [0] * (n - len(B_b10))

        cls._ntt(A, False)
        cls._ntt(B, False)
        C = [(A[i] * B[i]) % cls.NTT_MOD for i in range(n)]
        cls._ntt(C, True)

        res_b10 = []
        carry = 0
        for x in C:
            val = x + carry
            carry, val = divmod(val, 10)
            res_b10.append(val)
        while carry:
            carry, val = divmod(carry, 10)
            res_b10.append(val)

        res_arr = []
        for i in range(0, len(res_b10), 9):
            chunk = 0
            end = min(i + 9, len(res_b10))
            for j in reversed(range(i, end)):
                chunk = chunk * 10 + res_b10[j]
            res_arr.append(chunk)

        while res_arr and res_arr[-1] == 0:
            res_arr.pop()
        return res_arr

    def is_prime(self) -> bool:
        if self.neg or not self.arr:
            return False
        if len(self.arr) > 2:
            return False

        n = 0
        for x in reversed(self.arr):
            n = n * self.MOD + x

        if n < 2:
            return False
        bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
        for p in bases:
            if n == p:
                return True
            if n % p == 0:
                return False
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        for a in bases:
            x = pow(a, d, n)
            if x in (1, n - 1):
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True
