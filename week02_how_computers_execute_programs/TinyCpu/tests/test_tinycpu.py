import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from tinycpu import assemble, TinyCPU
from tinycpu.errors import (TinyCPUError, RegisterError, LabelError, MemoryAddressError,
                            InputExhausted, InstructionLimit, NoHalt, IOError as TinyIOError)
ROOT = Path(__file__).resolve().parents[1]

class AssemblerTests(unittest.TestCase):
    def test_case_comments_and_labels(self):
        p=assemble(' ; comment\n start: mov r0, -1 ; hi\n jMp start\n')
        self.assertEqual(len(p.instructions),2)
        self.assertEqual(p.instructions[1].operands,(0,))
    def test_bad_operands_and_lines(self):
        for source in ('MOV R0\nHALT','ADD R0 R1','LOAD R0, INPUT','HALT R0'):
            with self.subTest(source=source),self.assertRaises(TinyCPUError) as e: assemble(source)
            self.assertEqual(e.exception.line,1)
    def test_bad_register_and_labels(self):
        with self.assertRaises(RegisterError): assemble('MOV R4, 1')
        with self.assertRaises(LabelError): assemble('JMP missing')
        with self.assertRaises(LabelError): assemble('x: HALT\nx: HALT')
        with self.assertRaises(MemoryAddressError): assemble('LOAD R0, [242]')
    def test_back_and_forward(self):
        p=assemble('JMP end\nloop: HALT\nend: JMP loop')
        self.assertEqual(p.instructions[0].operands,(2,))
        self.assertEqual(p.instructions[2].operands,(1,))
    def test_indirect_memory_syntax(self):
        p=assemble('STORE [r2], R1\nLOAD R3, [R2]\nHALT')
        self.assertEqual(p.instructions[0].operands,('R2','R1'))
        self.assertEqual(p.instructions[1].operands,('R3','R2'))
        with self.assertRaises(RegisterError) as error: assemble('STORE [R4], R1')
        self.assertEqual(error.exception.line,1)

class CPUTests(unittest.TestCase):
    def run_source(self, source, inputs=()):
        c=TinyCPU(inputs); c.run(assemble(source)); return c
    def test_mov_load_store_and_io(self):
        c=self.run_source('LOAD R0, [INPUT]\nSTORE [10], R0\nMOV R0, 0\nLOAD R0, [10]\nSTORE [OUTPUT], R0\nHALT',[8])
        self.assertEqual(c.outputs,[8]); self.assertEqual(c.memory[10],8)
        self.assertFalse(any(c.flags.values()))
        with self.assertRaises(InputExhausted): self.run_source('LOAD R0, [INPUT]\nHALT')
    def test_indirect_load_store_and_io(self):
        source=('MOV R2, 239\nMOV R1, 37\nSTORE [R2], R1\nLOAD R0, [r2]\n'
                'MOV R2, 241\nSTORE [R2], R0\nHALT')
        c=self.run_source(source)
        self.assertEqual(c.memory[239],37)
        self.assertEqual(c.outputs,[37])
        self.assertFalse(any(c.flags.values()))
        c=self.run_source('MOV R2, 240\nLOAD R0, [R2]\nSTORE [OUTPUT], R0\nHALT',[9])
        self.assertEqual(c.outputs,[9])
        c=self.run_source((ROOT/'examples'/'print.asm').read_text(),[3,10,20,30])
        self.assertEqual(c.outputs,[30,20,10])
    def test_indirect_address_errors(self):
        cases=[(-1,'LOAD',MemoryAddressError,'outside 0..255'),
               (256,'STORE',MemoryAddressError,'outside 0..255'),
               (242,'LOAD',MemoryAddressError,'reserved'),
               (240,'STORE',TinyIOError,'INPUT'),
               (241,'LOAD',TinyIOError,'OUTPUT')]
        for address,operation,error_type,message in cases:
            source=f'MOV R2, {address}\n'+(
                'LOAD R0, [R2]\nHALT' if operation=='LOAD' else
                'STORE [R2], R0\nHALT')
            with self.subTest(address=address,operation=operation), self.assertRaises(error_type) as error:
                self.run_source(source)
            self.assertEqual(error.exception.line,2)
            self.assertIn(message,str(error.exception))
    def test_flags_add_sub_cmp(self):
        cases=[('MOV R0, 2147483647\nADD R0, 1',-2147483648,(False,True,False,True)),
               ('MOV R0, -2147483648\nSUB R0, 1',2147483647,(False,False,False,True)),
               ('MOV R0, -1\nADD R0, 1',0,(True,False,True,False)),
               ('MOV R0, 0\nSUB R0, 1',-1,(False,True,True,False)),
               ('MOV R0, 1\nCMP R0, 1',1,(True,False,False,False))]
        for code,value,flags in cases:
            with self.subTest(code=code):
                c=self.run_source(code+'\nHALT'); self.assertEqual(c.registers[0],value)
                self.assertEqual(tuple(c.flags.values()),flags)
    def test_all_branches(self):
        for op,first,second,expected in [('JE',1,1,1),('JE',1,2,0),('JNE',1,2,1),('JNE',1,1,0),
            ('JL',-2147483648,1,1),('JL',1,-2147483648,0),('JLE',2,2,1),('JLE',3,2,0),
            ('JG',3,2,1),('JG',2,3,0),('JGE',2,2,1),('JGE',-1,1,0),
            ('JC',0,1,1),('JC',2,1,0),('JNC',2,1,1),('JNC',0,1,0)]:
            source=f'MOV R0, {first}\nCMP R0, {second}\n{op} yes\nMOV R1, 0\nJMP done\nyes: MOV R1, 1\ndone: STORE [OUTPUT], R1\nHALT'
            with self.subTest(op=op,first=first,second=second): self.assertEqual(self.run_source(source).outputs,[expected])
    def test_limit_no_halt_step(self):
        c=TinyCPU(instruction_limit=2); c.load(assemble('x: JMP x'))
        c.step(); c.step()
        with self.assertRaises(InstructionLimit): c.step()
        with self.assertRaises(NoHalt): self.run_source('MOV R0, 1')
        c=self.run_source('HALT'); self.assertIsNone(c.step()); self.assertEqual(c.steps,1)

class CLITests(unittest.TestCase):
    def test_run_from_stdin_prints_only_output(self):
        env={**os.environ,'PYTHONPATH':str(ROOT/'src')}
        command=[sys.executable,'-m','tinycpu']
        help_result=subprocess.run(command+['--help'],capture_output=True,text=True,env=env)
        self.assertEqual(help_result.returncode,0)
        self.assertNotIn('check',help_result.stdout)
        program=str(ROOT/'examples'/'sum.asm')
        result=subprocess.run(command+['run',program],input='2 3\n',capture_output=True,text=True,env=env)
        self.assertEqual((result.returncode,result.stdout,result.stderr),(0,'5\n',''))
        result=subprocess.run(command+['run',program,'--input','2 3'],capture_output=True,text=True,env=env)
        self.assertEqual((result.returncode,result.stdout,result.stderr),(0,'5\n',''))
    def test_multiple_outputs_and_errors(self):
        env={**os.environ,'PYTHONPATH':str(ROOT/'src')}
        command=[sys.executable,'-m','tinycpu','run']
        with tempfile.TemporaryDirectory() as directory:
            program=Path(directory)/'program.asm'
            program.write_text('LOAD R0, [INPUT]\nSTORE [OUTPUT], R0\nLOAD R0, [INPUT]\nSTORE [OUTPUT], R0\nHALT\n')
            result=subprocess.run(command+[str(program)],input='-4 9\n',capture_output=True,text=True,env=env)
            self.assertEqual((result.returncode,result.stdout,result.stderr),(0,'-4\n9\n',''))
            result=subprocess.run(command+[str(program)],input='-4\n',capture_output=True,text=True,env=env)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(result.stdout,'')
            self.assertIn('Input exhausted',result.stderr)
    def test_standalone_runner(self):
        with tempfile.TemporaryDirectory() as directory:
            location=Path(directory)
            archive=location/'tinycpu.pyz'
            subprocess.run([sys.executable,str(ROOT/'build_standalone.py'),'--output',str(archive)],
                           check=True,capture_output=True,text=True)
            runner=location/'runner.py'
            runner.write_bytes((ROOT/'runner.py').read_bytes())
            program=location/'sum.asm'
            program.write_bytes((ROOT/'examples'/'sum.asm').read_bytes())
            result=subprocess.run([sys.executable,str(runner),str(program)],
                                  input='2 3\n',capture_output=True,text=True)
            self.assertEqual((result.returncode,result.stdout,result.stderr),(0,'5\n',''))

if __name__=='__main__': unittest.main()
