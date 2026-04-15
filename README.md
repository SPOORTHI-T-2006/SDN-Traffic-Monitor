# Traffic Monitoring and Statistics Collector (SDN using POX)

## Problem Statement

Build an SDN controller module that collects and displays traffic statistics such as packet count and byte count using Mininet and POX controller.

---

## Objective

* Retrieve flow statistics from switches
* Display packet and byte counts
* Perform periodic monitoring
* Generate simple traffic reports

---

## Tools & Technologies

* Mininet (Network Emulator)
* POX Controller
* OpenFlow Protocol
* Ubuntu

---

## Network Topology

* Single switch (s1)
* Three hosts (h1, h2, h3)
* Remote POX controller

---

## Setup Instructions

### 1. Install Dependencies

```bash
sudo apt update
sudo apt install mininet openvswitch-switch git python3
```

### 2. Clone POX

```bash
git clone https://github.com/noxrepo/pox.git
cd pox
```

### 3. Add Controller File

Place `traffic_monitor.py` inside:

```
pox/pox/
```

---

## Execution Steps

### Step 1: Run Controller

```bash
cd ~/pox
./pox.py log.level --DEBUG openflow.of_01 traffic_monitor
```

### Step 2: Run Mininet

```bash
sudo mn --topo single,3 --controller=remote --switch ovsk
```

---

## Testing

### Connectivity Test

```bash
pingall
```

### Generate Traffic

```bash
h1 ping -c 10 h2
```

OR

```bash
iperf h1 h2
```

---

##  Output

### Flow Statistics (Controller Output)

* Displays:

  * Source IP
  * Destination IP
  * Packet Count
  * Byte Count

Example:

```
Flow: 10.0.0.1 -> 10.0.0.2 | Packets: 10 | Bytes: 840
```

---

##  Flow Table Verification

```bash
sudo ovs-ofctl dump-flows s1
```

---

##  Screenshots

* Controller running
* Mininet topology
* Ping results
* Traffic generation (iperf/ping)
* Flow statistics output
* Flow table

---

##  Working Principle

* Switch sends unknown packets to controller (`packet_in`)
* Controller installs flow rules (match-action)
* Traffic flows through switch
* Controller periodically requests statistics
* Displays packet and byte counts

---

##  Features Implemented

* Learning switch behavior
* Flow rule installation
* Periodic monitoring
* Traffic statistics collection

---

##  Conclusion

This project demonstrates how SDN enables centralized control and monitoring of network traffic using POX controller and OpenFlow protocol.

---

## 📚 References

* POX Documentation
* Mininet Documentation
* OpenFlow Specification
