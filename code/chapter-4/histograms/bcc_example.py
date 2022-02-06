import sys
import signal
from time import sleep

from bcc import BPF


def signal_ignore(signal, frame):
    print()


bpf_source = """
#include <uapi/linux/ptrace.h>

BPF_HASH(cache, u64, u64);
BPF_HISTOGRAM(histogram);

int trace_bpf_prog_load_start(void *ctx) {
  u64 pid = bpf_get_current_pid_tgid();
  u64 start_time_ns = bpf_ktime_get_ns();
  cache.update(&pid, &start_time_ns);
  return 0;
}
"""

bpf_source += """
int trace_bpf_prog_load_return(void *ctx) {
  u64 *start_time_ns, delta;
  u64 pid = bpf_get_current_pid_tgid();
  start_time_ns = cache.lookup(&pid);
  if (start_time_ns == 0)
    return 0;
  delta = bpf_ktime_get_ns() - *start_time_ns;
  histogram.increment(bpf_log2l(delta));
  return 0;
}
"""

bpf = BPF(text=bpf_source)
bpf.attach_kprobe(event="bpf_prog_load", fn_name="trace_bpf_prog_load_start")
bpf.attach_kretprobe(event="bpf_prog_load",
                     fn_name="trace_bpf_prog_load_return")


try:
    sleep(300)
except KeyboardInterrupt:
    signal.signal(signal.SIGINT, signal_ignore)

bpf["histogram"].print_log2_hist("msecs")


# bash run.sh

# $ sudo python bcc_example.p
# ^C     msecs               : count     distribution
#          0 -> 1          : 0        |                                        |
#          2 -> 3          : 0        |                                        |
#          4 -> 7          : 0        |                                        |
#          8 -> 15         : 0        |                                        |
#         16 -> 31         : 0        |                                        |
#         32 -> 63         : 0        |                                        |
#         64 -> 127        : 0        |                                        |
#        128 -> 255        : 0        |                                        |
#        256 -> 511        : 0        |                                        |
#        512 -> 1023       : 0        |                                        |
#       1024 -> 2047       : 0        |                                        |
#       2048 -> 4095       : 0        |                                        |
#       4096 -> 8191       : 0        |                                        |
#       8192 -> 16383      : 0        |                                        |
#      16384 -> 32767      : 0        |                                        |
#      32768 -> 65535      : 0        |                                        |
#      65536 -> 131071     : 0        |                                        |
#     131072 -> 262143     : 37       |****************************************|
#     262144 -> 524287     : 2        |**                                      |