
date: Jun 2, 2020

# Building unix system for development in docker and kubernetes

## Build VirtualBox template
```
Linux
Ubuntu (64bit)

8192 Mb
Create a virtual harddisk
E:\kube\kube.vdi

500GB
VDI (or VMDK)


Settings

Advanced
shared clip : bi-directional
dragndrop: bi-directional  

System
Base memory: 8192
Processor: 2 CPU

Display: 
Video Memory: 64 MB
Enable 3D Acceleration

Storage:
put in ISO into Empty CD
(using ubuntu-20.04-desktop)

Network:
switch to bridged (ona private home network)

NOTE: I haven't bothered with a shared disk.

Click OK
```

## Install OS
```
Start the VM

Install Ubuntu
Continue
[x] Install third-party
Continue
Install Now
Continue

Thunder Bay
Continue

Steve Falcigno
kube
steve
<password>
<password>
Continue

... wait while files get copied ...
Restart
CD should auto eject
Enter
```

## Final Install Setup
```
Login with the account

Skip
Skip
[x] No, don't send system info
Next
Next
Done

There may be a popup to get updated software.
Install Now
Authorize with password
... this happens in background. Go get a coffee anyway ...
```

## Guest Additions
```
Devices - Insert Guest Additions
Run
<password>
Observe that the screen is resizeable
reboot
```

## Misc tools 

### Terminal Setup
```
rclick - open a terminal
hamburger - preferences
click on Unnamed
[x] Custom font, size 18, select
Colours - Built-in schemes, uncheck use colors from system theme, Solarized light, close the window
```

### Some software I like
```
sudo apt install nethack-x11
sudo apt install bsdgames
sudo apt install vim
sudo snap install --classic code
sudo apt install curl
sudo apt install net-tools
sudo apt install node   # not sure that I "like" this, but I need it for the demo.

Notes:
- python3 (3.8.2) comes with
- gcc 9.3.0
- no java or javac
- no link to python, and no python2
```

### Install Docker
```
sudo apt install docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker steve
sudo usermod -aG sudo steve
... if you try to run now, you will get a sock error ; rebooting will fix
docker run hello-world
should work fine.
```

### Install kubernetes ctl and minikube

link: https://computingforgeeks.com/how-to-install-minikube-on-ubuntu-debian-linux/


#### Update the OS
```
sudo apt-get update
sudo apt-get install apt-transport-https
sudo apt-get upgrade
```

#### Install VirtualBox
```
sudo apt install virtualbox virtualbox-ext-pack
(I think you can get away without this now - it appears to be running in a docker now? Need online confirmation)
```

#### Download minikube
```
wget https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
chmod +x minikube-linux-amd64 
sudo mv minikube-linux-amd64 /usr/local/bin/minikube
$ minikube version
minikube version: v1.11.0
commit: 57e2f55f47effe9ce396cea42a1e0eb4f611ebb
```

#### Install kubectl
```
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version -o json 
{
  "clientVersion": {
    "major": "1",
    "minor": "18",
    "gitVersion": "v1.18.3",
    "gitCommit": "2e7996e3e2712684bc73f0dec0200d64eec7fe40",
    "gitTreeState": "clean",
    "buildDate": "2020-05-20T12:52:00Z",
    "goVersion": "go1.13.9",
    "compiler": "gc",
    "platform": "linux/amd64"
  }
}
```

#### Starting minikube
```
$ minikube start
😄  minikube v1.11.0 on Ubuntu 20.04
✨  Automatically selected the docker driver
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
💾  Downloading Kubernetes v1.18.3 preload ...
    > preloaded-images-k8s-v3-v1.18.3-docker-overlay2-amd64.tar.lz4: 526.01 MiB
🔥  Creating docker container (CPUs=2, Memory=2200MB) ...
🐳  Preparing Kubernetes v1.18.3 on Docker 19.03.2 ...
    ▪ kubeadm.pod-network-cidr=10.244.0.0/16
🔎  Verifying Kubernetes components...
🌟  Enabled addons: default-storageclass, storage-provisioner
🏄  Done! kubectl is now configured to use "minikube"

```

### Basic Operations
```
$ kubectl cluster-info
Kubernetes master is running at https://172.17.0.3:8443
KubeDNS is running at https://172.17.0.3:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

Note that Minikube configuration file is located under ~/.minikube/machines/minikube/config.json
$ kubectl config view
apiVersion: v1
clusters:
- cluster:
    certificate-authority: /home/steve/.minikube/ca.crt
    server: https://172.17.0.3:8443
  name: minikube
contexts:
- context:
    cluster: minikube
    user: minikube
  name: minikube
current-context: minikube
kind: Config
preferences: {}
users:
- name: minikube
  user:
    client-certificate: /home/steve/.minikube/profiles/minikube/client.crt
    client-key: /home/steve/.minikube/profiles/minikube/client.key

$ kubectl get nodes
NAME       STATUS   ROLES    AGE    VERSION
minikube   Ready    master   3m1s   v1.18.3

$ minikube ssh
docker@minikube:~$ exit
logout

To stop a running local kubernetes cluster, run:
$ minikube stop

To delete a local kubernetes cluster, use:
$ minikube delete

 minikube addons list
|-----------------------------|----------|--------------|
|         ADDON NAME          | PROFILE  |    STATUS    |
|-----------------------------|----------|--------------|
| ambassador                  | minikube | disabled     |
| dashboard                   | minikube | disabled     |
| default-storageclass        | minikube | enabled ✅   |
| efk                         | minikube | disabled     |
| freshpod                    | minikube | disabled     |
| gvisor                      | minikube | disabled     |
| helm-tiller                 | minikube | disabled     |
| ingress                     | minikube | disabled     |
| ingress-dns                 | minikube | disabled     |
| istio                       | minikube | disabled     |
| istio-provisioner           | minikube | disabled     |
| logviewer                   | minikube | disabled     |
| metallb                     | minikube | disabled     |
| metrics-server              | minikube | disabled     |
| nvidia-driver-installer     | minikube | disabled     |
| nvidia-gpu-device-plugin    | minikube | disabled     |
| olm                         | minikube | disabled     |
| registry                    | minikube | disabled     |
| registry-aliases            | minikube | disabled     |
| registry-creds              | minikube | disabled     |
| storage-provisioner         | minikube | enabled ✅   |
| storage-provisioner-gluster | minikube | disabled     |
|-----------------------------|----------|--------------|

$ minikube dashboard
🔌  Enabling dashboard ...
🤔  Verifying dashboard health ...
🚀  Launching proxy ...
🤔  Verifying proxy health ...
🎉  Opening http://127.0.0.1:32889/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/ in your default browser...

```

## Going forward. I have a 002-kubernetes_tutorial to check out as well.











