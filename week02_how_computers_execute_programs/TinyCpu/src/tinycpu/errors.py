"""Diagnostics with source line numbers."""

class TinyCPUError(Exception):
    kind = "TinyCPU error"

    def __init__(self, message: str, line: int | None = None):
        self.line = line
        self.message = message
        super().__init__(f"{self.kind}{f' (line {line})' if line else ''}: {message}")

class SyntaxError(TinyCPUError): kind = "Syntax error"
class UnknownInstruction(TinyCPUError): kind = "Unknown instruction"
class OperandError(TinyCPUError): kind = "Operand error"
class RegisterError(TinyCPUError): kind = "Unknown register"
class LabelError(TinyCPUError): kind = "Label error"
class MemoryAddressError(TinyCPUError): kind = "Invalid memory address"
class IOError(TinyCPUError): kind = "Invalid I/O operation"
class InputExhausted(TinyCPUError): kind = "Input exhausted"
class PCError(TinyCPUError): kind = "PC out of program"
class InstructionLimit(TinyCPUError): kind = "Instruction limit exceeded"
class NoHalt(TinyCPUError): kind = "Missing HALT"
