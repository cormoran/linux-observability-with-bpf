# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

$bootstrap=<<SCRIPT
sudo grep '^deb ' /etc/apt/sources.list | sed 's/^deb /deb-src /g' | sudo tee /etc/apt/sources.list.d/deb-src.list
sudo apt update -y
sudo apt install build-essential git make libelf-dev clang strace tar bpfcc-tools linux-headers-$(uname -r) gcc-multilib -y dpkg-dev
cd /tmp
sudo apt source linux
sudo mv linux-4.15.0 /kernel-src
cd /kernel-src/tools/lib/bpf
make && sudo make install prefix=/
sudo echo export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/kernel-src/tools/lib/bpf/ >> ~/.bashrc
SCRIPT
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
	ipv4 = "192.168.33.10"
	config.vm.define "bpfbook" do |ubuntu|
		ubuntu.vm.box = "bento/ubuntu-18.04"
		net_index = 1
		ubuntu.vm.hostname = "bpfbook"
		ubuntu.vm.provider "virtualbox" do |vb|
			vb.customize ["modifyvm", :id, "--memory", "1024"]
		end
		ubuntu.vm.provider "libvirt" do |lv|
			lv.memory = 1024
		end
		ubuntu.vm.network :private_network, ip: "#{ipv4}"
		ubuntu.vm.provision :shell, inline: $bootstrap, :args => "#{ipv4}"
		ubuntu.vm.synced_folder ".", "/home/vagrant/linux-observability-with-bpf", owner: "vagrant", group: "vagrant"
	end
end