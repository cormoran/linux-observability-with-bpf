// $ wget https://go.dev/dl/go1.17.6.linux-amd64.tar.gz
// $ sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.17.6.linux-amd64.tar.gz
// $ export PATH=$PATH:/usr/local/go/bin
// $ go build -o hello-bpf main.go
// $ nm hello-bpf | grep main000000000050dee0 D main..inittask
// 000000000047e260 T main.main
// 0000000000431e40 T runtime.main
// 00000000004560e0 T runtime.main.func1
// 00000000004321a0 T runtime.main.func2
// 0000000000524ec0 B runtime.main_init_done
// 00000000004b1038 R runtime.mainPC
// 0000000000553d30 B runtime.mainStarted
//
// objdump -d hello-bpf  > hello-bpf.asm
package main

import (
	"fmt"
	"strconv"
)

func foo(i int) {
	fmt.Println("start foo " + strconv.Itoa(i))
	// time.Sleep(10 * time.Second)
	var x = 0.0
	for i := 0; i < 1000000; i++ {
		x *= x
	}
	fmt.Println("end foo " + strconv.Itoa(i))
}

func main() {
	fmt.Println("Hello, BPF")
	for i := 0; i < 2; i++ {
		go foo(i)
	}
	// time.Sleep(15 * time.Second)
	for i := 0; i < 1000000; i++ {
		foo(100 + i)
	}
}
