# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # PROXY
  # vagrant box add --insecure hashicorp/centos/7
  # vagrant plugin install --plugin-source http://rubygems.org vagrant-proxyconf
  # config.proxy.http     = "http://something.org:80"
  # config.proxy.https    = "http://something.org:80"
  # config.proxy.no_proxy = "localhost,127.0.0.1,.example.com"

  # Default Hashi corp CentOS 7 box.
  config.vm.box = "centos7"

  # Fixes changes from https://github.com/mitchellh/vagrant/pull/4707
  config.ssh.insert_key = false

  config.vm.provider :virtualbox do |vb|
    host = RbConfig::CONFIG['host_os']
    # Give VM 1/4 system memory 
    if host =~ /darwin/
      # sysctl returns Bytes and we need to convert to MB
      mem = `sysctl -n hw.memsize`.to_i / 1024
    elsif host =~ /linux/
      # meminfo shows KB and we need to convert to MB
      mem = `grep 'MemTotal' /proc/meminfo | sed -e 's/MemTotal://' -e 's/ kB//'`.to_i
    elsif host =~ /mswin|mingw|cygwin/
      # Windows code via https://github.com/rdsubhas/vagrant-faster
      mem = `wmic computersystem Get TotalPhysicalMemory`.split[1].to_i / 1024
    end

    mem = mem / 1024 / 4
    # vb.customize ["modifyvm", :id, "--memory", mem]
    vb.customize ["modifyvm", :id, "--memory", 3072] # RAM allocated to each VM
    vb.gui = false
    vb.cpus = 2
  end

  # Red Hat Registration
  # vagrant plugin install vagrant-registration
  # if Vagrant.has_plugin?('vagrant-registration')
  #   config.registration.username = ''
  #   config.registration.password = ''
  #   config.registration.pools    = ''
  # end

  # Ansible 
  config.vm.provision "ansible" do |ansible|
    ansible.inventory_path = "inventory/hosts"
    ansible.limit          = "vagrant"
    ansible.playbook       = "2_configure.yml"
    ansible.raw_arguments  = "--user=vagrant"
    ansible.raw_arguments  = "--private-key=~/.vagrant.d/insecure_private_key"
    ansible.ask_vault_pass = false
  end

  # RHEL 7.2
  config.vm.define :rhel7.0 do |rhel7.0|
    rhel7.0.vm.hostname = "rhel7.0.local"
    rhel7.0.vm.network :private_network, ip: "192.168.70.101"
    rhel7.0.vm.network :forwarded_port, guest: 8888, host: 8888
    rhel7.0.vm.synced_folder ".", "/vagrant", nfs: true #type: "nfs" 
  end

  # config.vm.define :rhel7.1 do |rhel7.1|
  #   rhel7.1.vm.hostname = "rhel7.1.local"
  #   rhel7.1.vm.network :private_network, ip: "192.168.70.102"
  #   rhel7.1.vm.network :forwarded_port, guest: 8888, host: 8888
  #   rhel7.1.vm.synced_folder ".", "/vagrant", nfs: true #type: "nfs" 
  # end


end

