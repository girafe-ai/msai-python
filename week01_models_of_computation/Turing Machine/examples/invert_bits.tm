# Invert every bit while scanning from left to right.
q0 0 -> 1 R q0
q0 1 -> 0 R q0
# Stop on the first blank after the input.
q0 _ -> _ S HALT

