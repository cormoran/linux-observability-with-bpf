from bcc import BPF

bpf_source = """
int trace_bpf_prog_load(struct pt_regs *ctx) {
  char comm[16];
  bpf_get_current_comm(&comm, sizeof(comm));

  bpf_trace_printk("%s is loading a BPF program", comm);
  return 0;
}
"""

bpf = BPF(text = bpf_source)
bpf.attach_tracepoint(tp = "bpf:bpf_prog_load", fn_name = "trace_bpf_prog_load")
bpf.trace_print()

# vagrant@bpfbook:~/linux-observability-with-bpf/code/chapter-4/tracepoints$ sudo python example.py
#          python-24337 [001] .... 1286011.689135: 0x00000001: python is loading a BPF program            bash-24340 [000] .... 1286021.619599: 0x00000001: executing program: bash
#        lesspipe-24343 [000] .... 1286021.622958: 0x00000001: executing program: lesspipe
#            bash-24345 [000] .... 1286021.625673: 0x00000001: executing program: bash

# vagrant@bpfbook:~/linux-observability-with-bpf/code/chapter-4/kprobes$ sudo python example.py
#            bash-24338 [000] .... 1286021.615489: 0x00000001: executing program: bash
#        lesspipe-24341 [001] .... 1286021.620809: 0x00000001: executing program: lesspipe
#            bash-24346 [000] .... 1286034.119760: 0x00000001: executing program: bash

# vagrant@bpfbook:~$ bash
# vagrant@bpfbook:~$ ls
# a  get-pip.py  linux-observability-with-bpf