// $ sudo apt-get install systemtap-sdt-dev # (for ubuntu)
// $ gcc -o hello_usdt hello_usdt.c
#include <sys/sdt.h>

int main(int argc, char const *argv[]) {
    DTRACE_PROBE(hello - usdt, probe - main);
    return 0;
}

// vagrant@bpfbook:~/linux-observability-with-bpf/code/chapter-4/usdt$ readelf
// -n ./hello_usdt
//
// Displaying notes found in: .note.ABI-tag
//   Owner                 Data size       Description
//   GNU                  0x00000010       NT_GNU_ABI_TAG (ABI version tag)
//     OS: Linux, ABI: 3.2.0
//
// Displaying notes found in: .note.gnu.build-id
//   Owner                 Data size       Description
//   GNU                  0x00000014       NT_GNU_BUILD_ID (unique build ID
//   bitstring)
//     Build ID: 6b40da19093c9fc78accb088043d391a3d8cb034
//
// Displaying notes found in: .note.stapsdt
//   Owner                 Data size       Description
//   stapsdt              0x0000002f       NT_STAPSDT (SystemTap probe
//   descriptors)
//     Provider: hello-usdt
//     Name: probe-main
//     Location: 0x0000000000000605, Base: 0x0000000000000694, Semaphore:
//     0x0000000000000000 Arguments:

// vagrant@bpfbook:~/linux-observability-with-bpf/code/chapter-4/usdt$
// tplist-bpfcc -l ./hello_usdt
// ./hello_usdt hello-usdt:probe-main