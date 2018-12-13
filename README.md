# NSX-T-Public
Scripts for NSX-T

Scripts made for public use.  These scripts should be used with care.  

If you break your environment, I will not support you!! It is up to you to fix your problems :-)


## switchport.py
Script to query all logical switches configured in an NSX-T Manager.  Will find all VMs plugged into the switch along with how many MAC addresses in the logical switch table.
  
### Example Readout:
```
 transport-ls
        Port (Admin status: UP): LB/LB.vmx@70eb9f5b-4776-43da-b3be-c4f8c226ebc9
          Total ports in use: 1
          Total MAC Addresses on switch: 0
          Total MAC Addresses left (max 2048): 2048


virtSw
        Port (Admin status: UP): LB/LB.vmx@70eb9f5b-4776-43da-b3be-c4f8c226ebc9
        Port (Admin status: UP): tiny1/tiny1.vmx@70eb9f5b-4776-43da-b3be-c4f8c226ebc9
        Port (Admin status: UP): tiny2/tiny2.vmx@70eb9f5b-4776-43da-b3be-c4f8c226ebc9
        Port (Admin status: UP): tiny3/tiny3.vmx@48d37f4a-ec2c-41b3-941b-8177f0bb9dbf
          Total ports in use: 4
          Total MAC Addresses on switch: 2
          Total MAC Addresses left (max 2048): 2046


vlan-uplink-sw
          Total ports in use: 0
          Total MAC Addresses on switch: 0
          Total MAC Addresses left (max 2048): 2048
 
 ```
