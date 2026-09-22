# TinyCPU Assembly quick reference

Instructions and registers are case-insensitive. A comment starts with `;`. Empty lines are allowed. A label looks like `loop:` and may appear on the same line as an instruction. Separate operands with a comma. Integers are signed decimal values. Write memory operands as `[10]`, `[INPUT]`, `[OUTPUT]`, or `[R0]`–`[R3]`. In `[R2]`, the value currently held in `R2` is the memory address. Jumps can target labels above or below the current instruction.

```asm
; Add two integers
LOAD R0, [INPUT]
LOAD R1, [INPUT]
ADD R0, R1
STORE [OUTPUT], R0
HALT
```

Register-indirect memory access lets a loop move through memory:

```asm
MOV R2, 10
MOV R1, 42
STORE [R2], R1 ; memory[10] = 42
LOAD R0, [R2]  ; R0 = memory[10]
```

The address held in the register is checked at execution time. `[R2+1]` and other address expressions are not supported.

Available instructions: `MOV`, `LOAD`, `STORE`, `ADD`, `SUB`, `CMP`, `JMP`, `JE`, `JNE`, `JL`, `JLE`, `JG`, `JGE`, `JC`, `JNC`, and `HALT`. See the [architecture specification](architecture.md) for operand forms and flag behavior.

Common mistakes: `LOAD R0, INPUT` (missing brackets), `ADD R4, 1` (only `R0..R3` exist), `JMP missing` (undefined label), `LOAD R0, [OUTPUT]` (the output port cannot be read), or omitting `HALT`. Diagnostics report the source line.
