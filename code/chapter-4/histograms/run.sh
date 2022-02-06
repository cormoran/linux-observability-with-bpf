for t in $(shuf -i 1-1000 -n 100); do
    sudo python $HOME/linux-observability-with-bpf/code/chapter-4/kprobes/example.py &
    sleep $(perl -e "print ${t} / 1000")
    sudo kill $(pgrep -fx "python $HOME/linux-observability-with-bpf/code/chapter-4/kprobes/example.py")
    echo "next"
done