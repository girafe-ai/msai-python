"""Single entry point; run writes only the answer to stdout."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
from . import assemble, TinyCPU, TinyCPUError
from .debugger import trace, debug

def parser() -> argparse.ArgumentParser:
    p=argparse.ArgumentParser(prog='tinycpu',description='Educational 32-bit TinyCPU processor')
    sub=p.add_subparsers(dest='command',required=True)
    for name in ('run','trace','debug'):
        cmd=sub.add_parser(name,help={'run':'print the answer only','trace':'show execution trace','debug':'step-by-step debugger'}[name])
        cmd.add_argument('program',type=Path)
        inp=cmd.add_mutually_exclusive_group()
        inp.add_argument('--input',default=None,help='space-separated input integers')
        inp.add_argument('--input-file',type=Path)
        cmd.add_argument('--instruction-limit',type=int,default=10_000)
        if name=='trace':
            cmd.add_argument('--max-rows',type=int,default=100)
            cmd.add_argument('--changes-only',action='store_true')
    return p

def main(argv: list[str] | None = None) -> int:
    args=parser().parse_args(argv)
    try:
        source=args.program.read_text(encoding='utf-8')
        input_text=(args.input_file.read_text(encoding='utf-8') if args.input_file else
                    args.input if args.input is not None else
                    '' if args.command == 'debug' and sys.stdin.isatty() else sys.stdin.read())
        try: inputs=[int(token) for token in input_text.split()]
        except ValueError as exc: raise ValueError(f'input must contain integers: {exc}') from exc
        cpu=TinyCPU(inputs,args.instruction_limit)
        cpu.load(assemble(source))
        if args.command=='run':
            for value in cpu.run().outputs: print(value)
        elif args.command=='trace': trace(cpu,max_rows=args.max_rows,changes=args.changes_only)
        else: debug(cpu)
        return 0
    except (TinyCPUError,OSError,ValueError) as exc:
        print(exc,file=sys.stderr)
        return 2

if __name__=='__main__': raise SystemExit(main())
