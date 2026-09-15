# Turing Machine

A small educational emulator for a deterministic single-tape Turing Machine.
The CLI, visualizer, tests, and headless Yandex Contest checker all use the same
execution engine. The tape uses a sparse representation and is infinite in both
directions.

## Installation

Python 3.11 or newer is required. Run the following from the project directory:

```bash
python -m pip install .
```

Install the optional `rich` dependency to enable animation:

```bash
python -m pip install '.[visual]'
```

For development and running tests:

```bash
python -m pip install -e '.[visual,test]'
pytest
```


Both invocation methods are available after a regular or editable installation:

```bash
tm --help
python -m turing_machine --help
```

## Transition Language

Each line describes one transition:

```text
STATE READ_SYMBOL -> WRITE_SYMBOL MOVE NEXT_STATE
```

`L`, `R`, and `S` mean move left, move right, and stay in place, respectively.
A tape symbol must consist of exactly one character. `_` is the default blank
symbol. `HALT`, `ACCEPT`, and `REJECT` are terminal states. Empty lines, lines
beginning with `#`, and text following `#` on a line are ignored.

```text
q0 0 -> 0 R q0
q0 1 -> 1 R q0
q0 _ -> _ L q_carry  # start carrying
```

Only one transition may be defined for each `(state, read symbol)` pair.

## CLI

Validate the syntax and run a program:

```bash
tm validate examples/binary_increment.tm
tm run examples/binary_increment.tm 1011
```

Example output:

```text
Initial tape: 1011
Final tape:   1100
Final state:  HALT
Steps:        8
Status:       halted
```

Enable a concise execution trace and configure the visible tape-window width:

```bash
tm run examples/binary_increment.tm 1011 --trace --window 11
```

Enable animation (`rich` gracefully falls back to plain text if unavailable):

```bash
tm run examples/binary_increment.tm 1011 --visual --delay 0.2
```

In interactive mode, Enter executes one step, `r` continues automatically, and
`q` ends the session.

```bash
tm run examples/binary_increment.tm 1011 --visual --interactive
```

You can limit execution and add visualizer breakpoints:

```bash
tm run program.tm 1011 --max-steps 10000 --max-nonblank-cells 1000
tm run program.tm 1011 --visual --break-state q_add --break-step 20
```

Use `--initial-state`, `--head`, `--input-start`, and `--blank` to change the
initial state, head position, input starting position, and blank symbol.

## Debugging and Common Errors

- `duplicate transition` — two lines define the same state and symbol pair;
- `invalid move` — a direction other than `L`, `R`, or `S` was specified;
- `No transition defined` — the machine read a symbol for which the current
  state has no rule; the message includes the step and head position;
- `Step limit ... exceeded` — the program has probably entered an infinite loop;
- an empty result is valid and represents a completely blank tape.

The regular CLI hides Python tracebacks. For internal diagnostics, place the
global debug flag before the command: `tm --debug run program.tm input`.

## Python API

The primary API for loading a program file is:

```python
from turing_machine import load_machine

machine = load_machine(
    "examples/binary_increment.tm",
    max_states=20,
    allowed_symbols={"0", "1", "_"},
)
result = machine.run(
    input_data="1011",
    initial_state="q0",
    max_steps=10_000,
    max_nonblank_cells=1_000,
)
assert result.halted
assert result.output == "1100"
```

`result.output` is a normalized string with blank cells trimmed from both ends.
The complete interval between the outermost non-blank cells is available as
`result.tape_contents`, and its left coordinate is available as
`result.tape_start`. Internal `_` symbols are preserved.

For manual debugging, call `machine.reset(input_data)` followed by
`machine.step()`. Each step returns a `StepInfo` object without printing anything
to stdout.

## Yandex Contest

Checker code should import `check_solution` or `load_machine` from
`turing_machine`. The headless execution path does not import `rich`, print
anything, or introduce delays. All tests still execute through the same
`TuringMachine.step()` implementation.

```python
from turing_machine import check_solution

report = check_solution(
    submitted_text,
    tests=hidden_tests,
    max_steps=10_000,
    max_nonblank_cells=1_000,
    max_states=20,
    allowed_symbols={"0", "1", "_"},
    expected_final_state="HALT",
)
```

`TestResult.error_type` distinguishes between `wrong_output`, `invalid_program`,
`missing_transition`, `step_limit_exceeded`, `resource_limit_exceeded`,
`invalid_alphabet`, and `incorrect_final_state`. The object itself contains the
input and expected output, so it must not be printed in full to a contestant. A
short ready-to-use example that reports only the test number and error category
is available in
[`examples/yandex_checker.py`](examples/yandex_checker.py).

## Examples

- `invert_bits.tm`: `001101` → `110010`;
- `binary_increment.tm`: `1011` → `1100`, `111` → `1000`;
- `unary_addition.tm`: `111+11` → `11111`.
