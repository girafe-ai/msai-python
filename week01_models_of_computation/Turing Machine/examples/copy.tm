q0 0 -> 0 R q0
q0 1 -> 1 R q0
q0 _ -> @ L q1
q1 0 -> 0 L q1
q1 1 -> 1 L q1
q1 _ -> _ R q2
q2 0 -> X R r0
q2 1 -> X R r1

r0 0 -> 0 R r0
r0 1 -> 1 R r0
r0 @ -> @ R r0
r1 0 -> 0 R r1
r1 1 -> 1 R r1
r1 @ -> @ R r1

r0 _ -> 0 L l0
r1 _ -> 1 L l1

l0 0 -> 0 L l0
l0 1 -> 1 L l0
l0 @ -> @ L l0
l1 0 -> 0 L l1
l1 1 -> 1 L l1
l1 @ -> @ L l1

l0 X -> 0 R q2
l1 X -> 1 R q2

q2 @ -> @ S HALT