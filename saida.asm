.text
.globl main
main:
li $t0, 1
li $v0, 1
move $a0, $t0
syscall
li $v0, 11
li $a0, 10
syscall
jr $ra