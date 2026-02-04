import random
import hashlib
from pwn import *
from z3 import *
from contextlib import contextmanager
from time import perf_counter

@contextmanager
def timeit(task_name):
    print(f"[-] Start - {task_name}")
    start = perf_counter()
    try:
        yield
    finally:
        end = perf_counter()
        print(f"[-] End - {task_name}")
        print(f"[-] Elapsed time: {end - start:.2f} seconds")

N = 624
M = 397
MATRIX_A = 0x9908B0DF
UPPER_MASK = 0x80000000
LOWER_MASK = 0x7FFFFFFF

def random_seed(seed):
    init_key = []
    if isinstance(seed, int):
        while seed != 0:
            init_key.append(seed % 2**32)
            seed //= 2**32
    else:
        init_key = seed
    key = init_key if len(init_key) > 0 else [0]
    keyused = len(init_key) if len(init_key) > 0 else 1
    return init_by_array(key, keyused)


def init_by_array(init_key, key_length):
    s = 19650218
    mt = [0] * N
    mt[0] = s
    for mti in range(1, N):
        if isinstance(mt[mti - 1], int):
            mt[mti] = (1812433253 * (mt[mti - 1] ^ (mt[mti - 1] >> 30)) + mti) % 2**32
        else:
            mt[mti] = 1812433253 * (mt[mti - 1] ^ LShR(mt[mti - 1], 30)) + mti
    i = 1
    j = 0
    k = N if N > key_length else key_length
    while k > 0:
        if isinstance(mt[i - 1], int):
            mt[i] = (
                (mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1664525)) + init_key[j] + j
            ) % 2**32
        else:
            mt[i] = (
                (mt[i] ^ ((mt[i - 1] ^ LShR(mt[i - 1], 30)) * 1664525))
                + init_key[j]
                + j
            )
        i += 1
        j += 1
        if i >= N:
            mt[0] = mt[N - 1]
            i = 1
        if j >= key_length:
            j = 0
        k -= 1
    for k in range(1, N)[::-1]:
        if isinstance(mt[i - 1], int):
            mt[i] = (
                (mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1566083941)) - i
            ) % 2**32
        else:
            mt[i] = (mt[i] ^ ((mt[i - 1] ^ LShR(mt[i - 1], 30)) * 1566083941)) - i
        i += 1
        if i >= N:
            mt[0] = mt[N - 1]
            i = 1
    mt[0] = 0x80000000
    return mt


def update_mt(mt):
    for i in range(N):
        x = (mt[i] & UPPER_MASK) ^ (mt[(i + 1) % N] & LOWER_MASK)
        if isinstance(x, int):
            xA = x >> 1
            if x & 1:
                xA ^= MATRIX_A
        else:
            # xA = LShR(x, 1) ^ If(x & 1 == 1, BitVecVal(MATRIX_A, 32), BitVecVal(0, 32))
            xA = LShR(x, 1)
            x0 = x & 1
            for j in range(32):
                if (MATRIX_A >> j) & 1:
                    xA ^= x0 << j
        mt[i] = mt[(i + M) % N] ^ xA


def temper(state):
    y = state
    if isinstance(y, int):
        y ^= y >> 11
    else:
        y ^= LShR(y, 11)
    y ^= (y << 7) & 0x9D2C5680
    y ^= (y << 15) & 0xEFC60000
    if isinstance(y, int):
        y ^= y >> 18
    else:
        y ^= LShR(y, 18)
    return y


def mt_gen(init_state, *, index=N):
    state = init_state[:]  # copy
    while True:
        index += 1
        if index >= N:
            update_mt(state)
            index = 0
        yield temper(state[index])


def mt_gen_sol(sol, init_state, *, index=N):
    state = init_state[:]  # copy
    twist = 0
    while True:
        index += 1
        if index >= N:
            # replace the new state with new symbolic variables
            # this somehow improve the performance of z3 a lot
            update_mt(state)
            next_state = [BitVec(f"__{twist}_state_{i}", 32) for i in range(N)]
            for x, y in zip(state, next_state):
                sol.add(x == y)
            state = next_state
            twist += 1
            index = 0
        yield temper(state[index])

def seed(s):
    if type(s) == int:
        n = abs(s)
    elif type(s) == str or type(s) == bytes or type(s) == bytearray:
        if type(s) == str:
            s = s.encode()
        n = int.from_bytes(s + hashlib.sha512(s).digest(), "big")
    elif s == None:
        print("NoneType seed leads to random result")
        exit()
    elif type(s) == float:
        raise NotImplementedError 

    uint32_mask = 1 << 32
    mt = [0 for i in range(624)]
    mt[0] = 0x12bd6aa
    for i in range(1, 624):
        mt[i] = (0x6c078965 * (mt[i - 1] ^ (mt[i - 1] >> 30)) + i) % uint32_mask

    keys = []
    while n:
        keys.append(n % uint32_mask)
        n >>= 32
    if len(keys) == 0:
        keys.append(0)

    i, j = 1, 0
    for _ in range(max(624, len(keys))):
        mt[i] = ((mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 30)) * 0x19660d)) + keys[j] + j) % uint32_mask
        i += 1
        j += 1
        if i >= 624:
            mt[0] = mt[623]
            i = 1
        j %= len(keys)

    for _ in range(623):
        mt[i] = ((mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 30)) * 0x5d588b65)) - i) % uint32_mask
        i += 1
        if i >= 624:
            mt[0] = mt[623]
            i = 1
    mt[0] = 0x80000000
    state = (3, tuple(mt + [624]), None)
    return state

def pure_mt_solver():
    return Then("bit-blast", "sat").solver()

def state2seed(target_state, prefix_bytes, suffix_bytes):
    N = 624
    uint32_mask = 0xFFFFFFFF
    
    def bytes_to_key_chunks(b):
        val = int.from_bytes(b, "big")
        if val == 0: 
            if len(b) == 0: return []
        num_chunks = (len(b) * 8 + 31) // 32
        chunks = []
        for _ in range(num_chunks):
            chunks.append(val & uint32_mask)
            val >>= 32
        return chunks

    suffix_keys = bytes_to_key_chunks(suffix_bytes)
    prefix_keys = bytes_to_key_chunks(prefix_bytes)
    
    middle_len = 624 
    total_len = len(suffix_keys) + middle_len + len(prefix_keys)
    if total_len < 624:
        middle_len = 624 - len(suffix_keys) - len(prefix_keys)
        total_len = 624

    state = list(target_state[1][:-1])
    assert state[0] == 0x80000000
    
    state[0] = state[623]

    curr_i = 1
    for _ in range(total_len):
        curr_i += 1
        if curr_i >= 624: curr_i = 1
    phase2_end_i = curr_i

    curr_i = phase2_end_i
    for _ in range(623):
        curr_i += 1
        if curr_i >= 624: curr_i = 1
    
    mt = state[:]
    idx = curr_i
    for _ in range(623):
        if idx == 1:
            idx = 624 
        idx -= 1
        
        prev_idx = idx - 1
        x = mt[prev_idx]
        x = (x ^ (x >> 30)) * 0x5d588b65
        x &= uint32_mask
        
        val = (mt[idx] + idx) & uint32_mask
        mt[idx] = val ^ x
        
        if idx == 623:
            mt[0] = mt[623]

    prefix_start_j = len(suffix_keys) + middle_len
    prefix_len = len(prefix_keys)
    
    sim_i = 1
    sim_j = 0
    history = [] 
    for step in range(total_len):
        history.append((sim_i, sim_j))
        sim_i += 1
        sim_j += 1
        if sim_i >= 624: sim_i = 1
        sim_j %= total_len
        
    prefix_steps = history[-prefix_len:]
    
    for (step_i, step_j) in reversed(prefix_steps):
        key_val = prefix_keys[step_j - prefix_start_j]
        prev_idx = step_i - 1
        x = mt[prev_idx]
        x = (x ^ (x >> 30)) * 0x19660d
        x &= uint32_mask
        
        tmp = (mt[step_i] - key_val - step_j) & uint32_mask
        mt[step_i] = tmp ^ x
        
        if step_i == 623:
            mt[0] = mt[623]

    origin = [0] * N
    origin[0] = 19650218
    for i in range(1, N):
        origin[i] = (1812433253 * (origin[i-1] ^ (origin[i-1] >> 30)) + i) & uint32_mask
        
    suffix_steps = history[:len(suffix_keys)]
    for (step_i, step_j) in suffix_steps:
        key_val = suffix_keys[step_j]
        x = origin[step_i-1]
        x = (x ^ (x >> 30)) * 0x19660d
        x &= uint32_mask
        
        origin[step_i] = (origin[step_i] ^ x) + key_val + step_j
        origin[step_i] &= uint32_mask
        
        if step_i == 623: origin[0] = origin[623]
        
    middle_steps = history[len(suffix_keys) : len(suffix_keys)+middle_len]
    middle_keys_solved = [0] * middle_len
    
    for k, (step_i, step_j) in enumerate(middle_steps):
        remaining_steps = len(middle_steps) - k
        
        if remaining_steps > 623:
            needed_key = 0
            middle_keys_solved[k] = needed_key
            
            x = origin[step_i-1]
            x = (x ^ (x >> 30)) * 0x19660d
            x &= uint32_mask
            origin[step_i] = (origin[step_i] ^ x) + needed_key + step_j
            origin[step_i] &= uint32_mask
            
        else:
            target_val = mt[step_i]
            
            x = origin[step_i-1]
            x = (x ^ (x >> 30)) * 0x19660d
            x &= uint32_mask
            
            term1 = (origin[step_i] ^ x) & uint32_mask
            
            needed_key = (target_val - term1 - step_j) & uint32_mask
            middle_keys_solved[k] = needed_key
            origin[step_i] = target_val
            
        if step_i == 623: origin[0] = origin[623]

    final_keys = suffix_keys + middle_keys_solved + prefix_keys
    seed_int = 0
    for k in reversed(final_keys):
        seed_int <<= 32
        seed_int |= k
        
    return seed_int