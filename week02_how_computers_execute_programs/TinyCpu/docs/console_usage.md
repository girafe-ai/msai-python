# Console guide

From the project directory after `python -m pip install -e .`:

```bash
python -m tinycpu run examples/sum.asm --input "2 3"
python -m tinycpu trace examples/sum.asm --input "2 3" --max-rows 20
python -m tinycpu trace examples/sum.asm --input "2 3" --changes-only
python -m tinycpu debug examples/sum.asm --input "2 3"
python -m tinycpu run examples/sum.asm < input.txt > output.txt
```

`run` prints only the answer, one integer per line. To read standard input, omit `--input`; alternatively, use `--input-file`. `trace` shows the step number, `PC`, source instruction, registers, flags, and newly produced output. With `--changes-only`, rows after the first list only changed fields. `--max-rows` limits the displayed table, while the whole program still runs. In `debug`, use Enter/`step`, `continue`, `registers`, `flags`, `memory [address] [count]`, `output`, `help`, and `quit` to inspect state between steps.

Instructors can demonstrate execution with `trace`; students can investigate programs with `debug`. `--instruction-limit N` stops long-running loops. In a contest, `run` reads test data from stdin and writes only the program's output values to stdout. The platform checker compares that output with the answer. `run` returns 0 after `HALT`; errors return code 2 with a diagnostic on stderr and no answer on stdout.
