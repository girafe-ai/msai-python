# Find the right edge of the binary number.
q0 0 -> 0 R q0
q0 1 -> 1 R q0
q0 _ -> _ L q_carry

# Propagate the carry towards the left.
q_carry 1 -> 0 L q_carry
q_carry 0 -> 1 S HALT
# Overflow: add a new leading one.
q_carry _ -> 1 S HALT

