# SDN Learning Switch with Mininet and POX

## Objective
Implement an SDN-based learning switch using Mininet and POX controller that dynamically learns MAC addresses and installs flow rules.

## Setup
- Mininet installed via `sudo apt install mininet`
- POX cloned from `https://github.com/noxrepo/pox`

## Execution Steps

### 1. Start POX Controller
```bash
cd ~/pox
./pox.py openflow.of_01 --address=127.0.0.1 --port=6633 forwarding.l2_learning# SDN-Mininet-learning-switch
