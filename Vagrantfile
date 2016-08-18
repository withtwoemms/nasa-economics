Vagrant.configure("2") do |config|
  config.vm.box = "debian/jessie64"
  config.vm.network "forwarded_port", host: 8080, guest: 80
  config.vm.synced_folder "./vps/vagrant", "/vagrant"
  config.vm.provision :shell, path: "./vps/vagrant/provision.sh"
end
