# TinyCPU: a seminar on processor instructions

This teaching kit connects x86-64 concepts (`RIP`, `RFLAGS`, comparisons, and jumps) to a small 32-bit processor. The CLI and notebook share one execution library. The emulator requires Python 3.11+ and has no third-party runtime dependencies. Polygon generators require `testlib.h`.

## Install and run

From `MSAI_python/W03/tinycpu`:

```bash
python -m pip install -e .
python -m tinycpu run examples/sum.asm --input "2 3"
```

The answer is `5`. On some systems the command is `python3`. After installation, you can also invoke `tinycpu`. If package installation is unavailable, run `PYTHONPATH=src python3 -m tinycpu run examples/sum.asm --input "2 3"` on Linux/macOS, or `$env:PYTHONPATH='src'; python -m tinycpu run examples/sum.asm --input '2 3'` in PowerShell.

For a contest runner, pass the test through standard input:

```bash
python -m tinycpu run examples/sum.asm < input.txt > output.txt
```

On successful execution, stdout contains only values written to `OUTPUT`, one integer per line. Errors go to stderr and return a nonzero exit code. The contest checker compares `output.txt` with the expected answer.

For a standalone contest package, build the standard-library zipapp and place it beside `runner.py`:

```bash
python build_standalone.py
printf '2 3\n' | python runner.py examples/sum.asm
python runner.py examples/sum.asm < input.txt > output.txt
```

The two deployable files are `runner.py` and `tinycpu.pyz`. The runner also works directly from this source tree without building the archive. Use `--instruction-limit N` after the program path to set a problem-specific step limit. The archive itself can run the regular CLI as `python tinycpu.pyz run examples/sum.asm < input.txt`.

```asm
LOAD R0, [INPUT]
LOAD R1, [INPUT]
ADD R0, R1
STORE [OUTPUT], R0
HALT
```

`INPUT` and `OUTPUT` are ports at addresses 240 and 241. Each `LOAD [INPUT]` consumes one integer; each `STORE [OUTPUT]` appends one integer to the answer.

Memory can also be addressed through a register: `STORE [R2], R1` writes `R1` to the address currently in `R2`, and `LOAD R1, [R2]` reads from it. See [architecture](docs/architecture.md) for address and I/O checks.

## Teaching and debugging

```bash
python -m tinycpu trace examples/sum.asm --input "2 3" --max-rows 20
python -m tinycpu debug examples/sum.asm --input "2 3"
python scripts/verify_all.py
```

In `debug`, press Enter to step, `c` to continue, `r` for registers, `f` for flags, `m 0 8` for memory, `o` for output, and `q` to quit. `trace` draws a state table; `run` prints only answer integers. See the [console guide](docs/console_usage.md), [ISA specification](docs/architecture.md), and [Assembly reference](docs/assembly_syntax.md).

The [seminar notebook](notebooks/cpu_instructions_and_tinycpu.ipynb) works from the project root and uses the local package. To execute it with Jupyter, install `python -m pip install -e '.[notebook]'` and run:

```bash
python -m jupyter nbconvert --to notebook --execute notebooks/cpu_instructions_and_tinycpu.ipynb --output /tmp/tinycpu-checked.ipynb
```

On Windows, choose a Windows path for `--output`. Without Jupyter, `verify_all.py` executes every code cell with Python.

## Problems and verification

The [12 problems](problems/README.md) include English statements, `testlib` generators and validators, reference solutions, and instruction limits. `python scripts/verify_all.py` runs unit tests, examples, 103 boundary and random cases per problem, and notebook code cells. You can also run `python -m unittest discover -s tests -v`, or install `.[test]` and run `python -m pytest`.

The [Polygon and Yandex Contest guide](docs/yandex_contest_integration.md) describes the stdin/stdout runner and the administrator setup required for direct `.asm` submissions. The existing Turing machine emulator is unchanged.
