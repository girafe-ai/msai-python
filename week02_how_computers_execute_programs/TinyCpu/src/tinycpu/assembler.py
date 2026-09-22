"""Strict two-pass TinyCPU Assembly parser."""
from __future__ import annotations
from dataclasses import dataclass
import re
from .errors import (SyntaxError, UnknownInstruction, OperandError, RegisterError,
                     LabelError, MemoryAddressError, IOError)

REG = re.compile(r"R[0-3]$", re.I)
REG_LIKE = re.compile(r"R\d+$", re.I)
LABEL = re.compile(r"[A-Za-z_][A-Za-z_0-9]*$")
INT = re.compile(r"[+-]?\d+$")
ARITY = {"MOV":2,"LOAD":2,"STORE":2,"ADD":2,"SUB":2,"CMP":2,
         "JMP":1,"JE":1,"JNE":1,"JL":1,"JLE":1,"JG":1,"JGE":1,
         "JC":1,"JNC":1,"HALT":0}
JUMPS = frozenset(k for k, n in ARITY.items() if n == 1)

@dataclass(frozen=True)
class Instruction:
    opcode: str
    operands: tuple[int | str, ...]
    line: int
    source: str

@dataclass(frozen=True)
class Program:
    instructions: tuple[Instruction, ...]
    labels: tuple[tuple[str, int], ...]

def _register(token: str, line: int) -> str:
    if REG.fullmatch(token): return token.upper()
    if REG_LIKE.fullmatch(token): raise RegisterError(f"{token}: valid registers are R0–R3", line)
    raise OperandError(f"expected a register R0–R3, got {token!r}", line)

def _source(token: str, line: int) -> int | str:
    if REG.fullmatch(token): return token.upper()
    if REG_LIKE.fullmatch(token): raise RegisterError(f"{token}: valid registers are R0–R3", line)
    if INT.fullmatch(token):
        n = int(token)
        if not -(1<<31) <= n <= (1<<31)-1:
            raise OperandError("immediate is outside the signed 32-bit range", line)
        return n
    raise OperandError(f"expected a register or decimal integer, got {token!r}", line)

def _address(token: str, line: int, *, writing: bool) -> int | str:
    if not token.startswith('[') or not token.endswith(']'):
        raise OperandError(f"expected an address in [brackets], got {token!r}", line)
    inner = token[1:-1].strip().upper()
    if REG.fullmatch(inner): return inner
    if REG_LIKE.fullmatch(inner): raise RegisterError(f"{inner}: valid registers are R0–R3", line)
    if inner == 'INPUT': addr = 240
    elif inner == 'OUTPUT': addr = 241
    elif INT.fullmatch(inner): addr = int(inner)
    else: raise OperandError(f"unknown address {inner!r}", line)
    if not 0 <= addr <= 255: raise MemoryAddressError(f"address {addr} is outside 0..255", line)
    if addr >= 242: raise MemoryAddressError(f"address {addr} is reserved", line)
    if writing and addr == 240: raise IOError("writing to INPUT is forbidden", line)
    if not writing and addr == 241: raise IOError("reading from OUTPUT is forbidden", line)
    return addr

def assemble(source: str) -> Program:
    labels: dict[str, int] = {}
    rows: list[tuple[str,int,str]] = []
    for number, raw in enumerate(source.splitlines(), 1):
        code = raw.split(';',1)[0].strip()
        while ':' in code:
            prefix, rest = code.split(':',1)
            name = prefix.strip()
            if not LABEL.fullmatch(name): raise SyntaxError("invalid label", number)
            key = name.upper()
            if key in labels: raise LabelError(f"label {name} is defined more than once", number)
            labels[key] = len(rows)
            code = rest.strip()
        if code: rows.append((code, number, raw.strip()))
    instructions = []
    for code, line, raw in rows:
        pieces = code.split(None,1)
        opcode = pieces[0].upper()
        if opcode not in ARITY: raise UnknownInstruction(opcode, line)
        tail = pieces[1].strip() if len(pieces)==2 else ''
        args = [x.strip() for x in tail.split(',')] if tail else []
        if len(args) != ARITY[opcode] or any(not x for x in args):
            raise OperandError(f"{opcode}: expected {ARITY[opcode]} operand(s), separated by a comma", line)
        if opcode in JUMPS:
            key = args[0].upper()
            if not LABEL.fullmatch(key): raise OperandError("expected a jump label", line)
            if key not in labels: raise LabelError(f"label {args[0]} is undefined", line)
            parsed: tuple[int|str,...] = (labels[key],)
        elif opcode == 'HALT': parsed = ()
        elif opcode == 'LOAD': parsed = (_register(args[0],line), _address(args[1],line,writing=False))
        elif opcode == 'STORE': parsed = (_address(args[0],line,writing=True), _register(args[1],line))
        else: parsed = (_register(args[0],line), _source(args[1],line))
        instructions.append(Instruction(opcode, parsed, line, raw))
    return Program(tuple(instructions), tuple(labels.items()))
