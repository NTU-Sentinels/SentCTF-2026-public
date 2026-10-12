#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

//
// $ gcc -static -no-pie -fno-stack-protector -Wno-stringop-overflow -o pivot2gadgets pivot2gadgets.c
//

// global buffer in .bss section (fixed address since its compiled with -no-pie flag)
char global_fake_stack[0x100];

// 'planted' gadget for the players - intended to be the final one to execute system call
// __attribute__((naked)): tells the compiler to omit the function prologue and epologue entirely (eg. push rbp, mov rbp, rsp, etc.)
void __attribute__((naked)) custom_gadget() {
    __asm__(
        "gadget_entry:\n"
        // --- mov 59 into rax (calls system function) ---
        "   mov $59, %rax\n"             // RAX = 59 (execve)

        // --- constraint check 1: r12 == 0xdeadbeef ---
        "   cmpl $0xc001babe, %r12d\n"     // Must pass R12 check!
        "   jne fail\n"

        // --- load value into rdi (to execute shell) ---
        "   lea binsh(%rip), %rdi\n"     // RDI = "/bin/sh"

        // --- check rsp value, else jump to fail subroutine ---
        "   mov (%rsp), %rsi\n"          // move [rsp] into rsi temporarily
        "   cmpq $0x13371337, %rsi\n"     
        "   jne fail\n"

        // --- clear rdi, rdx ---
        "   xor %rsi, %rsi\n"            // Clear RSI to NULL
        "   xor %rdx, %rdx\n"            // Clear RDX to NULL
        "   syscall\n"

        "fail:\n"
        "   ret\n"

        "binsh:\n"
        "   .string \"/usr/bin/bash\"\n"
    );
}


// 'planted' gadget for the players - to load R12
void __attribute__((naked)) gadget() {
    __asm__(
        "pop %r12; ret\n"                // needed to satisfy R12 == 0xdeadbeef
        // "leave; ret\n"                   // needed to jump to next instruction (eg. custom_gadget)
    );
}

void vuln() {
    char buf[0x30];
    
    // Stage 1: load fake stack
    // puts("Stage 1 - Setup your workspace:");
    read(0, global_fake_stack, 0x100);

    // Stage 2: small overflow: exactly 0x40 bytes (0x30 buffer + 0x8 saved rbp)
    // should NOT be able to reach RIP at buf + 0x38
    // puts("Stage 2 - Execute:");
    read(0, buf, 0x38);  // stops overwriting right before RIP
}

int main() {
    volatile char dummy[16]; // forces stack frame allocation (sub rsp, 0x10) - makes the compiler generate explicit 'leave' instruction for stack pivoting to work

    setvbuf(stdout, NULL, _IONBF, 0);
    vuln();
    puts("Exiting normally...");
    return 0;
}



