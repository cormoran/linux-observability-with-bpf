from bcc import BPF

bpf_source = """
#include <uapi/linux/ptrace.h>

int ret_sys_execve(struct pt_regs *ctx) {
  int return_value;
  char comm[16];
  bpf_get_current_comm(&comm, sizeof(comm));
  return_value = PT_REGS_RC(ctx);

  bpf_trace_printk("program: %s, return: %d\\n", comm, return_value);
  return 0;
}
"""

bpf = BPF(text=bpf_source)

# execve_function = bpf.get_syscall_fnname("execve")
bpf.attach_kretprobe(event="sys_execve", fn_name="ret_sys_execve")
bpf.trace_print()

# sudo python example.py
# ls-24239 [000] d... 1284896.761796: 0x00000001: program: ls, return: 0
# ls-24240 [001] d... 1284910.288134: 0x00000001: program: ls, return: 0
# ls-24241 [001] d... 1284916.801520: 0x00000001: program: ls, return: 0
# rm-24242 [001] d... 1284923.607359: 0x00000001: program: rm, return: 0
