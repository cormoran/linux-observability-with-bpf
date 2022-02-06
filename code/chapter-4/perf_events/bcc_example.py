import ctypes
from bcc import BPF
import ctypes as ct

bpf_source = """
#include <uapi/linux/ptrace.h>

BPF_PERF_OUTPUT(events);

int do_sys_execve(struct pt_regs *ctx) {
  char comm[16];
  bpf_get_current_comm(&comm, sizeof(comm));

  events.perf_submit(ctx, &comm, sizeof(comm));
  return 0;
}
"""

bpf = BPF(text = bpf_source)
# execve_function = bpf.get_syscall_fnname("execve")
bpf.attach_kprobe(event = "sys_execve", fn_name = "do_sys_execve")

from collections import Counter
aggregates = Counter()

def aggregate_programs(cpu, data, size):
  comm = ct.cast(data, ct.POINTER(ct.c_char * 16)).contents.value
  aggregates[comm] += 1

bpf["events"].open_perf_buffer(aggregate_programs)

for i in range(100):
    bpf.kprobe_poll()

for (comm, times) in aggregates.most_common():
    print("Program {} executed {} times".format(comm, times))

# $ sudo python bcc_example.py
# Program xargs executed 329 times
# Program bash executed 2 times

#  seq 100 | xargs -L1 ls
