# SDN Learning Switch Implementation using Mininet and POX Controller

## Project Overview
This project demonstrates a Software-Defined Networking (SDN) based **Layer-2 Learning Switch** using:
- **Mininet** for network topology emulation
- **POX** as the OpenFlow controller

The controller dynamically learns MAC addresses of connected hosts and installs precise flow rules on the switch.

---

## Objective
- Establish controller-switch interaction over OpenFlow 1.0  
- Implement dynamic MAC address learning (packet-in handling)  
- Install explicit match-action flow rules on the switch  
- Observe network behavior and validate correct forwarding  

---

## Topology
A simple tree topology with:
- **1 Open vSwitch** (`s1`)
- **3 Hosts** (`h1`, `h2`, `h3`)

```
        s1
      / | \
    h1  h2  h3
```

---

## Environment & Prerequisites
- **Operating System**: Ubuntu 22.04 (WSL2)
- **Mininet**:
  ```bash
  sudo apt install mininet -y
  ```
- **POX Controller**:
  ```bash
  git clone https://github.com/noxrepo/pox.git
  ```

---

## How to Run

### Step 1: Clone POX Controller
```bash
git clone https://github.com/noxrepo/pox.git
cd pox
```

### Step 2: Start POX Controller (Terminal 1)
```bash
cd ~/pox
./pox.py openflow.of_01 --address=127.0.0.1 --port=6633 forwarding.l2_learning
```

**Expected Output:**
```
INFO:core:POX 0.7.0 (gar) is up.
INFO:openflow.of_01:Listening on 127.0.0.1:6633
INFO:forwarding.l2_learning:Learning switch running.
```

---

### Step 3: Start Mininet Topology (Terminal 2)
```bash
sudo mn --topo single,3 --controller remote --mac --switch ovsk
```

---

### Step 4: Test Connectivity
```bash
mininet> pingall
```

**Expected:**
```
0% dropped (6/6 received)
```

---

### Step 5: View Flow Rules
```bash
mininet> sh ovs-ofctl dump-flows s1
```

---

### Step 6: Exit
```bash
mininet> exit
```

Press `Ctrl + C` in the POX terminal to stop the controller.

---

## Expected Output & Observations

### Pingall Result
```
*** Ping: testing ping reachability
h1 -> h2 h3
h2 -> h1 h3
h3 -> h1 h2
*** Results: 0% dropped (6/6 received)
```

---

### Flow Table Example
```
cookie=0x0, duration=12.3s, table=0, n_packets=3, n_bytes=294, priority=1, in_port=1,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:02 actions=output:2
cookie=0x0, duration=12.3s, table=0, n_packets=3, n_bytes=294, priority=1, in_port=2,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:01 actions=output:1
```

---

### Controller Logs (POX Terminal)
```
INFO:forwarding.l2_learning:Learned 00:00:00:00:00:01 on port 1 of switch 1
INFO:forwarding.l2_learning:Learned 00:00:00:00:00:02 on port 2 of switch 1
```

---

## Performance Note
- First ping has slight delay (due to MAC learning)
- Subsequent pings are faster (flow rules handle forwarding)

---

## Proof of Execution
Screenshots stored in `/screenshots` folder:
- `/screenshots/pox_startup.png` – POX controller running  
- `/screenshots/pingall_result.png` – Successful connectivity  
- `/screenshots/flow_table.png` – Installed flow rules  

---

## Validation
- Controller-switch handshake (OpenFlow 1.0)  
- MAC addresses dynamically learned  
- Flow rules with correct match-action  
- 0% packet loss on pingall  
- Flow table verified via `ovs-ofctl`  

---

## References
- Mininet: http://mininet.org  
- POX: https://github.com/noxrepo/pox  
- OpenFlow 1.0 Spec: https://opennetworking.org/wp-content/uploads/2014/10/openflow-spec-v1.0.0.pdf  

---

## Author
**N Lakshanyaa**  
**PES University**  
Course: Computer Networks / SDN Simulation Project  
