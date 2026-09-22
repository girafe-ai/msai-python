"""Execution model independent of the console interface."""
from __future__ import annotations
from dataclasses import dataclass
from .assembler import Program, Instruction
from .errors import InputExhausted, PCError, InstructionLimit, NoHalt, IOError, MemoryAddressError

MASK = (1 << 32)-1
SIGN = 1 << 31
def signed(n: int) -> int:
    n &= MASK
    return n - (1<<32) if n & SIGN else n

@dataclass(frozen=True)
class StepInfo:
    number: int
    pc: int
    instruction: Instruction
    registers: tuple[int,int,int,int]
    flags: tuple[bool,bool,bool,bool]
    new_outputs: tuple[int,...]

@dataclass(frozen=True)
class RunResult:
    outputs: list[int]
    steps: int
    registers: tuple[int,int,int,int]
    flags: tuple[bool,bool,bool,bool]

class TinyCPU:
    def __init__(self, inputs=(), instruction_limit: int = 10_000):
        if instruction_limit < 1: raise ValueError("instruction_limit must be positive")
        self.inputs = list(inputs)
        self.instruction_limit = instruction_limit
        self.registers = [0]*4
        self.memory = [0]*240
        self.flags = {'ZF':False,'SF':False,'CF':False,'OF':False}
        self.pc = self.steps = self.input_position = 0
        self.outputs: list[int] = []
        self.halted = False
        self.program: Program | None = None

    def load(self, program: Program) -> None:
        self.program = program

    def _value(self, operand: int|str) -> int:
        return self.registers[int(operand[1])] if isinstance(operand,str) else operand

    def _address(self, operand: int | str, *, writing: bool, line: int) -> int:
        address = self._value(operand)
        if not 0 <= address <= 255:
            raise MemoryAddressError(f"address {address} is outside 0..255", line)
        if address >= 242:
            raise MemoryAddressError(f"address {address} is reserved", line)
        if writing and address == 240:
            raise IOError("writing to INPUT is forbidden", line)
        if not writing and address == 241:
            raise IOError("reading from OUTPUT is forbidden", line)
        return address

    def _arithmetic(self, left: int, right: int, subtract: bool) -> int:
        a,b = left & MASK, right & MASK
        raw = a-b if subtract else a+b
        result = raw & MASK
        self.flags.update(ZF=result==0, SF=bool(result&SIGN),
                          CF=(a<b if subtract else raw>MASK),
                          OF=(bool(((a^b)&(a^result)&SIGN)) if subtract
                              else bool((~(a^b)&(a^result)&SIGN))))
        return signed(result)

    def step(self, program: Program | None = None) -> StepInfo | None:
        if program is not None: self.load(program)
        if self.program is None: raise ValueError("load a program first")
        if self.halted: return None
        p = self.program
        if self.pc == len(p.instructions): raise NoHalt("program ended without HALT", p.instructions[-1].line if p.instructions else None)
        if self.pc < 0 or self.pc > len(p.instructions): raise PCError(f"PC={self.pc}")
        ins = p.instructions[self.pc]
        if self.steps >= self.instruction_limit: raise InstructionLimit(f"limit {self.instruction_limit}", ins.line)
        op, args = ins.opcode, ins.operands
        before = len(self.outputs)
        old_pc = self.pc
        self.pc += 1
        if op == 'MOV': self.registers[int(args[0][1])] = signed(self._value(args[1]))
        elif op == 'LOAD':
            addr = self._address(args[1], writing=False, line=ins.line)
            if addr == 240:
                if self.input_position >= len(self.inputs): raise InputExhausted("no more input integers", ins.line)
                value = self.inputs[self.input_position]
                self.input_position += 1
            else: value = self.memory[addr]
            self.registers[int(args[0][1])] = signed(value)
        elif op == 'STORE':
            addr = self._address(args[0], writing=True, line=ins.line)
            reg = args[1]
            value = self.registers[int(reg[1])]
            if addr == 241: self.outputs.append(value)
            else: self.memory[addr] = value
        elif op in ('ADD','SUB','CMP'):
            reg = int(args[0][1]); value = self._arithmetic(self.registers[reg],self._value(args[1]),op != 'ADD')
            if op != 'CMP': self.registers[reg] = value
        elif op == 'HALT': self.halted = True
        else:
            f = self.flags
            take = {'JMP':True,'JE':f['ZF'],'JNE':not f['ZF'],
                    'JL':f['SF']!=f['OF'],'JLE':f['ZF'] or f['SF']!=f['OF'],
                    'JG':not f['ZF'] and f['SF']==f['OF'],'JGE':f['SF']==f['OF'],
                    'JC':f['CF'],'JNC':not f['CF']}[op]
            if take: self.pc = args[0]
        self.steps += 1
        return StepInfo(self.steps, old_pc, ins, tuple(self.registers), tuple(self.flags.values()), tuple(self.outputs[before:]))

    def run(self, program: Program | None = None) -> RunResult:
        if program is not None: self.load(program)
        while not self.halted: self.step()
        return RunResult(self.outputs.copy(),self.steps,tuple(self.registers),tuple(self.flags.values()))
