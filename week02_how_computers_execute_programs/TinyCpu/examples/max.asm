; get maximum of two numbers
LOAD R0, [INPUT]
LOAD R1, [INPUT]
CMP R0, R1
JGE done
MOV R0, R1
done: STORE [OUTPUT], R0
HALT
