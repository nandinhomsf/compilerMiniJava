.text
.globl main
main:
li $t0, 1
li $t1, 10
move $a0, $t1
jal ComputeFac
move $t0, $v0
li $v0, 1
move $a0, $t0
syscall
li $v0, 11
li $a0, 10
syscall
jr $ra
ComputeFac:
addiu $sp, $sp, -4
beq $zero, 10, label1
li $t2, 1
move 4($sp), $t2
j label2
label1:
move 4($sp), 1
label2:
jr $ra