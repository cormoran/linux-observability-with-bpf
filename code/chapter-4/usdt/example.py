from bcc import BPF, USDT

bpf_source = """
#include <uapi/linux/ptrace.h>
int trace_binary_exec(struct pt_regs *ctx) {
  u64 pid = bpf_get_current_pid_tgid();
  bpf_trace_printk("New hello_usdt process running with PID: %d\\n", pid);
}
"""

usdt = USDT(path = "./hello_usdt")
usdt.enable_probe(probe = "probe-main", fn_name = "trace_binary_exec")
bpf = BPF(text = bpf_source, usdt_contexts = [usdt])
bpf.trace_print()

# $ sudo python example.py
# /virtual/main.c:7:1: warning: control reaches end of non-void function [-Wreturn-type]
# }
# ^
# 1 warning generated.
#       hello_usdt-25405 [001] .... 1290284.415810: 0x00000001: New hello_usdt process running with PID: 25405

# $ ./hello_usdt