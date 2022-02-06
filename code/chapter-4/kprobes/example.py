from bcc import BPF

bpf_source = """
#include <uapi/linux/ptrace.h>

int do_sys_execve(struct pt_regs *ctx) {
  char comm[16];
  bpf_get_current_comm(&comm, sizeof(comm));
  // Populates the first argument address with the current process name.
  // It should be a pointer to a char array of at least size TASK_COMM_LEN, which is defined in linux/sched.h.
  // https://github.com/iovisor/bcc/blob/63de4c502aad2371542f647dbd03b6a7689ef86b/docs/reference_guide.md#6-bpf_get_current_comm
  bpf_trace_printk("executing program: %s\\n", comm);
  return 0;
}
"""

bpf = BPF(text=bpf_source)
# execve_function = bpf.get_syscall_fnname("execve")
# get_syscall_fnname and get_syscall_prefix was introduced in newer version
# https://github.com/iovisor/bcc/commit/83b49ad6cd9efba88f922c2e7b892fc275208514#diff-a2ae791d9876879bf1288479649a032f00e9acc61c1f9e2132eadc4855d421e5R526
bpf.attach_kprobe(event="sys_execve", fn_name="do_sys_execve")
bpf.trace_print()

# $ sudo python example.py
# # execute command in another terminal
# bash-24229 [001] .... 1283990.509109: 0x00000001: executing program: bash
# bash-24230 [000] .... 1283999.051030: 0x00000001: executing program: bash