Vagrant.configure(2) do |config|

  # ... your existing config
  
    # Custom configuration for docker
    config.vm.provider "docker" do |docker, override|
      # docker doesnt use boxes
      override.vm.box = nil

      #config.vm.network :public_network, type: "dhcp", bridge: "eth0", docker_network__ip_range: "192.168.1.252/30"
      #config.vm.network :private_network,
      #  ip: "192.168.1.22"

      config.vm.network "private_network", :ip => "172.16.42.43"
      config.vm.network "forwarded_port", guest: 5000, host: 5000
  
      # this is where your Dockerfile lives
      docker.build_dir = "."
  
      # Make sure it sets up ssh with the Dockerfile
      # Vagrant is pretty dependent on ssh
      override.ssh.insert_key = true
      docker.has_ssh = true
  
      # Configure Docker to allow access to more resources
      docker.privileged = true
    end
  
  # ...
  
  end