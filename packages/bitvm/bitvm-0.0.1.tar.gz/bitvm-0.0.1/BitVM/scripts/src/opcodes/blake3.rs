#![allow(non_snake_case)]
use std::collections::HashMap;

use crate::opcodes::{
    u32_add::u32_add,
    u32_rrot::{u32_rrot12, u32_rrot16, u32_rrot7, u32_rrot8},
    u32_std::{u32_drop, u32_fromaltstack, u32_push, u32_roll, u32_toaltstack},
    u32_xor::{u8_drop_xor_table, u8_push_xor_table, u32_xor},
    unroll,
};

use super::pushable;
use bitcoin::ScriptBuf as Script;
use bitcoin_script::bitcoin_script as script;

//
// Environment
//

// A pointer to address elements on the stack
#[derive(Eq, Hash, PartialEq, Debug, Clone, Copy)]
pub enum Ptr {
    State(u32),
    Message(u32),
}

pub fn S(i: u32) -> Ptr {
    Ptr::State(i)
}

pub fn M(i: u32) -> Ptr {
    Ptr::Message(i)
}

// An environment to track elements on the stack
type Env = HashMap<Ptr, u32>;

pub fn ptr_init() -> Env {
    // Initial positions for state and message
    let mut env: Env = Env::new();
    for i in 0..16 {
        env.insert(S(i), i);
        // The message's offset is the size of the state
        // plus the u32 size of our XOR table
        env.insert(M(i), i + 16 + 256 / 4);
    }
    env
}

pub fn ptr_init_160() -> Env {
    // Initial positions for state and message
    let mut env: Env = Env::new();
    for i in 0..16 {
        env.insert(S(i), i);
        // The message's offset is the size of the state
        // plus the u32 size of our XOR table
        let value: i32 = i as i32
            + 16
            + 256 / 4
            + match i < 10 {
                true => 6,
                false => -10,
            };
        env.insert(M(i), value as u32);
    }
    env
}

pub trait EnvTrait {
    // Get the position of `ptr`
    fn ptr(&mut self, ptr: Ptr) -> u32;

    /// Get the position of `ptr`, then delete it
    fn ptr_extract(&mut self, ptr: Ptr) -> u32;

    /// Set the position of `ptr` to the top stack ptr
    fn ptr_insert(&mut self, ptr: Ptr);
}

impl EnvTrait for Env {
    fn ptr_insert(&mut self, ptr: Ptr) {
        for (_, value) in self.iter_mut() {
            *value += 1;
        }
        self.insert(ptr, 0);
    }

    fn ptr_extract(&mut self, ptr: Ptr) -> u32 {
        match self.remove(&ptr) {
            Some(index) => {
                for (_, value) in self.iter_mut() {
                    if index < *value {
                        *value -= 1;
                    }
                }
                index
            }
            None => panic!("{:?}", ptr),
        }
    }

    fn ptr(&mut self, ptr: Ptr) -> u32 {
        *self.get(&ptr).unwrap()
    }
}

//
// Blake 3 Algorithm
//

const IV: [u32; 8] = [
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
];

const MSG_PERMUTATION: [u32; 16] = [2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8];

pub fn initial_state(block_len: u32) -> Vec<Script> {
    let mut state = [
        IV[0], IV[1], IV[2], IV[3], IV[4], IV[5], IV[6], IV[7], IV[0], IV[1], IV[2], IV[3], 0, 0,
        block_len, 0b00001011,
    ];
    state.reverse();
    state.iter().map(|x| u32_push(*x)).collect::<Vec<_>>()
}

fn G(env: &mut Env, ap: u32, a: Ptr, b: Ptr, c: Ptr, d: Ptr, m0: Ptr, m1: Ptr) -> Script {
    let script = script! {
        // z = a+b+m0
        {u32_add(env.ptr(b), env.ptr_extract(a))}
        {u32_add(env.ptr(m0) + 1, 0)}
        // Stack:  m1 m0 d c b  |  z

        // y = (d^z) >>> 16
        {u32_xor(0, env.ptr_extract(d) + 1, ap + 1)}
        u32_rrot16
        // Stack:  m1 m0 c b  |  z y


        // x = y+c
        {u32_add(0, env.ptr_extract(c) + 2)}
        // Stack:  m1 m0 b  |  z y x

        // w = (b^x) >>> 12
        {u32_xor(0, env.ptr_extract(b) + 3, ap + 1)}
        u32_rrot12
        // Stack:  m1 m0 |  z y x w


        // v = z+w+m1
        {u32_add(0, 3)}
        {u32_add(env.ptr(m1) + 4, 0)}
        // Stack: m1 m0 |  y x w v

        // u = (y^v) >>> 8
        {u32_xor(0, 3, ap + 1)}
        u32_rrot8
        // Stack: m1 m0 |  x w v u

        // t = x+u
        {u32_add(0, 3)}
        // Stack: m1 m0 |  w v u t

        // s = (w^t) >>> 7
        {u32_xor(0, 3, ap + 1)}
        u32_rrot7
        // Stack: m1 m0 |  v u t s
    };

    env.ptr_insert(a);
    env.ptr_insert(d);
    env.ptr_insert(c);
    env.ptr_insert(b);
    script
}

pub fn round(env: &mut Env, ap: u32) -> Script {
    script! {
        { G(env, ap, S(0), S(4), S(8),  S(12), M(0),  M(1)) }
        { G(env, ap, S(1), S(5), S(9),  S(13), M(2),  M(3)) }
        { G(env, ap, S(2), S(6), S(10), S(14), M(4),  M(5)) }
        { G(env, ap, S(3), S(7), S(11), S(15), M(6),  M(7)) }

        { G(env, ap, S(0), S(5), S(10), S(15), M(8),  M(9)) }
        { G(env, ap, S(1), S(6), S(11), S(12), M(10), M(11)) }
        { G(env, ap, S(2), S(7), S(8),  S(13), M(12), M(13)) }
        { G(env, ap, S(3), S(4), S(9),  S(14), M(14), M(15)) }
    }
}

pub fn permute(env: &mut Env) {
    let mut prev_env = Vec::new();
    for i in 0..16 {
        prev_env.push(env.ptr(M(i)));
    }

    for i in 0..16 {
        env.insert(M(i as u32), prev_env[MSG_PERMUTATION[i] as usize]);
    }
}

fn compress(env: &mut Env, ap: u32) -> Script {
    script! {
        // Perform 7 rounds and permute after each round,
        // except for the last round
        {round(env, ap)}
        {unroll(6, |_| {
            permute(env);
            round(env, ap)
        })}

        // XOR states [0..7] with states [8..15]
        {unroll(8, |i| u32_xor(env.ptr(S(i)) + i, env.ptr_extract(S(i + 8)) + i, ap + 1))}
    }
}

fn compress_160(env: &mut Env, ap: u32) -> Script {
    script! {
        // Perform 7 rounds and permute after each round,
        // except for the last round
        {round(env, ap)}
        {unroll(6, |_| {
            permute(env);
            round(env, ap)
        })}

        // XOR states [0..4] with states [8..12]
        {unroll(5, |i| u32_xor(env.ptr(S(i)) + i, env.ptr_extract(S(i + 8)) + i, ap + 1))}
    }
}

/// Blake3 taking a 64-byte message and returning a 32-byte digest
pub fn blake3() -> Script {
    let mut env = ptr_init();
    script! {
        // Initialize our lookup table
        // We have to do that only once per program
        u8_push_xor_table

        // Push the initial Blake state onto the stack
        {initial_state(64)}

        // Perform a round of Blake3
        {compress(&mut env, 16)}

        // Clean up the stack
        {unroll(32, |_| u32_toaltstack())}
        u8_drop_xor_table
        {unroll(32, |_| u32_fromaltstack())}

        {unroll(24, |i| u32_roll(i + 8))}
        {unroll(24, |_| u32_drop())}
    }
}

/// Blake3 taking a 40-byte message and returning a 20-byte digest
pub fn blake3_160() -> Script {
    let mut env = ptr_init_160();
    script! {
        // Message zero-padding to 64-byte block
        {unroll(6, |_| u32_push(0))}

        // Initialize our lookup table
        // We have to do that only once per program
        u8_push_xor_table

        // Push the initial Blake state onto the stack
        {initial_state(40)}

        // Perform a round of Blake3
        {compress_160(&mut env, 16)}

        // Clean up the stack
        {unroll(5, |_| u32_toaltstack())}
        {unroll(27, |_| u32_drop())}
        u8_drop_xor_table

        {unroll(5, |_| u32_fromaltstack())}
    }
}
