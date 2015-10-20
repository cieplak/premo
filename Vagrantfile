# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.hostname = "premo-virtualbox"
  config.vm.box = "ubuntu/trusty64"
  config.vm.synced_folder "../premo", "/home/vagrant/premo"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
  end
  config.vm.network "private_network", type: "dhcp"
  config.vm.network "forwarded_port", guest: 15672, host: 15672 
  config.vm.provision "shell", inline: <<-SHELL
        sudo apt-get update
        sudo apt-get install -y git htop ncdu python python-dev python-pip tmux tree vim
        sudo pip install ansible==1.9.2
        cd /home/vagrant/premo/tests/provisioning
        sudo ansible-playbook site.yml -i hosts --connection=local
  SHELL
end
