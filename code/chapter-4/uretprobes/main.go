// $ go build -o parallel parallel.go
package main

import (
	"fmt"
	"strconv"
	"time"
)

func foo(i int) {
	fmt.Println("start foo " + strconv.Itoa(i))
	time.Sleep(10 * time.Second)
	fmt.Println("end foo " + strconv.Itoa(i))
}

func main() {
	fmt.Println("Hello, BPF")
	for i := 0; i < 10; i++ {
		go foo(i)
	}
	time.Sleep(15 * time.Second)
}
