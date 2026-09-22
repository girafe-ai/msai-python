# TinyCPU: formal architecture, version 1

## State

TinyCPU has four general-purpose registers (`R0`–`R3`), a `PC` (the index of the instruction about to execute), four flags (`ZF`, `SF`, `CF`, `OF`), and 256 memory addresses. Each instruction occupies one program position; TinyCPU does not encode instructions as machine-code bytes. Registers, memory, and flags start at zero. Values are stored modulo 2³². Registers, memory, and output are displayed as signed 32-bit integers (`−2³¹..2³¹−1`). Immediate values must be in this range.

Addresses `0..239` are ordinary memory. `240 = INPUT` is read-only: each `LOAD` consumes the next integer; reading beyond the input stream raises an error. `241 = OUTPUT` is write-only: each `STORE` appends one signed integer to the answer. Addresses `242..255` are reserved and inaccessible. Numeric and symbolic addresses are equivalent. Input integers are interpreted modulo 2³².

## Instructions

| Instruction | Effect | Flags |
|---|---|---|
| `MOV dst, src` | Copy a register or immediate value | Unchanged |
| `LOAD dst, [addr]` | Read memory or `INPUT` | Unchanged |
| `STORE [addr], src` | Write memory or `OUTPUT` | Unchanged |
| `ADD dst, src` | Add modulo 2³² | Update all four |
| `SUB dst, src` | Subtract modulo 2³² | Update all four |
| `CMP lhs, rhs` | Set flags as `SUB` would, without storing the result | Update all four |
| `JMP label` | Unconditional jump | Unchanged |
| `JE`, `JNE`, `JL`, `JLE`, `JG`, `JGE`, `JC`, `JNC` | Conditional jump | Unchanged |
| `HALT` | Stop successfully | Unchanged |

`dst` and `lhs` must be one of `R0..R3`; `src` and `rhs` can be a register or signed decimal integer. A memory operand may contain a constant (`[10]`), a port name (`[INPUT]`, `[OUTPUT]`), or a register (`[R0]`–`[R3]`). With a register, the **current register value** is used as the address at execution time: `STORE [R2], R1` stores `R1` at the address in `R2`, while `LOAD R1, [R2]` reads from that address. This is register-indirect addressing; only a single register is allowed inside the brackets, with no offsets or arithmetic. There is no `MUL`, `DIV`, `MOD`, stack, or function call.

For direct addresses, the assembler checks the address and I/O direction. For register-indirect addresses, the CPU performs the same checks when the instruction executes: `0..239` are ordinary memory, `240` may only be read as `INPUT`, `241` may only be written as `OUTPUT`, and `242..255` are reserved. A negative address or an address above 255 is invalid. Address calculation and `LOAD`/`STORE` do not modify the flags.

## Flags and jumps

Let `r` be the low 32 bits of the result and `a` and `b` the unsigned representations of the operands. `ZF = (r == 0)` and `SF = bit31(r)`. For `ADD`, `CF = (a+b > 2³²−1)` and `OF = (~(a xor b) & (a xor r) & 2³¹) != 0`. For `SUB` and `CMP`, `CF = (a < b)` (borrow) and `OF = ((a xor b) & (a xor r) & 2³¹) != 0`. For example, `2147483647 + 1` produces `−2147483648` and sets `OF=1`. `CMP` does not modify its operands. `MOV`, `LOAD`, `STORE`, and jumps leave the flags unchanged.

| Jump | Condition |
|---|---|
| `JE` | `ZF` |
| `JNE` | `not ZF` |
| `JL` | `SF != OF` |
| `JLE` | `ZF or SF != OF` |
| `JG` | `not ZF and SF == OF` |
| `JGE` | `SF == OF` |
| `JC` | `CF` |
| `JNC` | `not CF` |

`JL/JLE/JG/JGE` perform signed comparisons. `JC/JNC` inspect the unsigned borrow or carry. An ordinary instruction advances `PC` by one; a taken jump sets it to the label's instruction index. `HALT` counts as an executed instruction. Reaching the end without `HALT` is a `NO_HALT` error. The default instruction limit is 10,000.
