"""Terminal visualization in the style of the educational Turing machine."""
from __future__ import annotations
import sys
from .cpu import TinyCPU, StepInfo

def trace_line(info: StepInfo, *, changes: bool = False, previous: StepInfo | None = None) -> str:
    regs = ' '.join(f'R{i}={v:>11}' for i,v in enumerate(info.registers))
    flags = ' '.join(f'{name}={int(value)}' for name,value in zip(('ZF','SF','CF','OF'),info.flags))
    if changes and previous:
        regs = ' '.join(f'R{i}={v}' for i,v in enumerate(info.registers) if v != previous.registers[i]) or '—'
        flags = ' '.join(f'{n}={int(v)}' for i,(n,v) in enumerate(zip(('ZF','SF','CF','OF'),info.flags)) if v != previous.flags[i]) or '—'
    output = f" → OUT: {' '.join(map(str,info.new_outputs))}" if info.new_outputs else ''
    return f'{info.number:>5} │ {info.pc:>3} │ {info.instruction.source:<28.28} │ {regs} │ {flags}{output}'

def trace(cpu: TinyCPU, *, max_rows: int = 100, changes: bool = False, stream=None) -> None:
    stream = stream or sys.stdout
    print(' Step │ PC  │ Instruction                  │ Registers │ Flags / output',file=stream)
    print('──────┼─────┼──────────────────────────────┼───────────┼──────────────',file=stream)
    previous = None
    while not cpu.halted:
        info = cpu.step()
        if info.number <= max_rows: print(trace_line(info,changes=changes,previous=previous),file=stream)
        previous = info
    if cpu.steps > max_rows: print(f'… hidden steps: {cpu.steps-max_rows}',file=stream)
    print(f'Output: {" ".join(map(str,cpu.outputs)) or "—"}; steps: {cpu.steps}',file=stream)

def _next(cpu: TinyCPU) -> str:
    if cpu.halted: return 'HALT: program stopped'
    if cpu.program and cpu.pc < len(cpu.program.instructions):
        return f'PC {cpu.pc:03}: {cpu.program.instructions[cpu.pc].source}'
    return f'PC {cpu.pc:03}: end of program'

def debug(cpu: TinyCPU) -> None:
    print('┏━ TinyCPU · debugger ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
    print('┃ Enter/s: step · c: continue · r/f/m/o: state · h: help        ┃')
    print('┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')
    print(_next(cpu))
    while True:
        try: command = input('tinycpu> ').strip().lower()
        except EOFError: return
        if command in ('q','quit','exit'): return
        if command in ('','s','step'):
            if cpu.halted: print('Program has already halted'); continue
            info = cpu.step(); print(trace_line(info)); print(_next(cpu))
        elif command in ('c','continue'):
            previous = None
            while not cpu.halted:
                info = cpu.step(); previous = info
            if previous: print(trace_line(previous))
            print(_next(cpu))
        elif command in ('r','registers'): print(' '.join(f'R{i}={v}' for i,v in enumerate(cpu.registers)),f'PC={cpu.pc}')
        elif command in ('f','flags'): print(' '.join(f'{k}={int(v)}' for k,v in cpu.flags.items()))
        elif command.startswith(('m','memory')):
            parts = command.split()
            try:
                address = int(parts[1]) if len(parts)>1 else 0
                count = int(parts[2]) if len(parts)>2 else 8
                if not 0 <= address < 240 or not 1 <= count <= 240-address: raise ValueError
                print(' '.join(f'[{i}]={cpu.memory[i]}' for i in range(address,address+count)))
            except ValueError: print('Enter an address in 0..239 and a valid cell count')
        elif command in ('o','output'): print('Output:',*cpu.outputs)
        elif command in ('h','help','?'): print('step/s/Enter, continue/c, registers/r, flags/f, memory/m [address] [count], output/o, help/h, quit/q')
        else: print('Unknown command; type help for a list')
