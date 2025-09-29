# 📚 Study Notes

## 📋 Content Summary
This document, "ITN_Module_8.pdf," covers the fundamentals of the Network Layer in computer networking. It details the characteristics of the network layer, focusing on IP protocols (IPv4 and IPv6), packet encapsulation, and the core operations of addressing, encapsulation, routing, and de-encapsulation. The module also delves into the structure and purpose of IPv4 and IPv6 packet headers, how hosts make routing decisions, the role of default gateways, and the mechanics of router routing tables, including static and dynamic routing.

## 🎯 Key Points

*   **Network Layer Core Functions:** The network layer, primarily using IP protocols like IPv4 and IPv6, is responsible for enabling end-to-end data exchange between devices. Its key operations include addressing, encapsulation, routing, and de-encapsulation.
*   **IP Protocol Characteristics:** IP is connectionless, best-effort, and media-independent. This means it doesn't establish a connection before sending, doesn't guarantee delivery, and can operate over various physical media.
*   **IPv4 vs. IPv6:** IPv6 was developed to overcome IPv4's limitations, primarily address depletion and increased network complexity due to NAT. IPv6 offers a vastly larger address space, improved packet handling with a simplified header, and eliminates the need for NAT.
*   **Host Routing Decisions:** A host determines if a destination is itself, on the local network, or a remote network. For remote destinations, it forwards traffic to the default gateway.
*   **Router Routing Tables:** Routers use routing tables to make forwarding decisions. These tables contain information about directly connected networks, remote networks (learned statically or dynamically), and a default route for unknown destinations.

## 💡 Detailed Explanation

### Network Layer Characteristics

*   **Purpose of the Network Layer:**
    *   Provides services to allow end devices to exchange data.
    *   Uses IP version 4 (IPv4) and IP version 6 (IPv6) as the primary communication protocols.
*   **Four Basic Operations:**
    *   **Addressing End Devices:** Assigning unique IP addresses to devices for identification and communication.
    *   **Encapsulation:** The network layer encapsulates transport layer segments into network layer packets (e.g., IP packets). This involves adding an IP header.
    *   **Routing:** The process of selecting paths in a network along which to send network traffic. Routers examine packet headers and consult their routing tables to determine the next hop.
    *   **De-encapsulation:** As packets arrive at the destination, the network layer removes the IP header and passes the payload to the transport layer.

### IP Protocol Characteristics

*   **Connectionless:** IP does not establish a connection with the destination before sending packets. There's no handshake or session establishment. Packets are sent independently.
*   **Best Effort:** IP does not guarantee delivery of packets. Packets can be lost, duplicated, or arrive out of order. The network layer doesn't retransmit lost packets; this responsibility typically falls to higher layers (like TCP).
*   **Media Independent:** IP is unaware of the underlying network media (e.g., Ethernet, Wi-Fi, fiber optics). It can operate over any data link layer protocol and physical medium.

### IPv4 Packet Header

*   **Purpose:** Ensures packets are sent in the correct direction and contains information for network layer processing. This information is used by all Layer 3 devices.
*   **Key Fields:**
    *   **Version:** Identifies the IP version (e.g., 4 for IPv4).
    *   **Internet Header Length (IHL):** Specifies the length of the IPv4 header.
    *   **Differentiated Services (DS)/Type of Service (ToS):** Used for Quality of Service (QoS) to prioritize traffic.
    *   **Total Length:** The entire length of the IP packet, including header and data.
    *   **Identification, Flag, Fragment Offset:** Fields related to packet fragmentation.
    *   **Time to Live (TTL):** A hop count; when it reaches zero, the packet is discarded to prevent infinite loops.
    *   **Protocol:** Identifies the next-level protocol (e.g., ICMP, TCP, UDP).
    *   **Header Checksum:** Used to detect corruption in the IPv4 header.
    *   **Source IP Address:** The 32-bit IP address of the sending device.
    *   **Destination IP Address:** The 32-bit IP address of the intended recipient.

### IPv6 Packet Header

*   **Overview:** Developed to overcome IPv4 limitations.
*   **Improvements:**
    *   **Increased Address Space:** Uses 128-bit addresses, providing a vastly larger pool of unique addresses compared to IPv4's 32-bit addresses.
    *   **Simplified Header:** More streamlined header with fewer fields, leading to more efficient packet processing by routers.
    *   **Eliminates NAT:** The abundance of addresses negates the need for Network Address Translation (NAT).
*   **Key Fields:**
    *   **Version:** Identifies the IP version (e.g., 6 for IPv6).
    *   **Traffic Class:** Similar to IPv4's Differentiated Services field for QoS.
    *   **Flow Label:** Allows a device to identify and handle flows of packets that require special treatment.
    *   **Payload Length:** Indicates the length of the data portion of the IPv6 packet.
    *   **Next Header:** Identifies the type of header immediately following the IPv6 header (similar to the Protocol field in IPv4).
    *   **Hop Limit:** Replaces the TTL field in IPv4, functioning as a hop count.
    *   **Source IP Address:** The 128-bit IP address of the sending device.
    *   **Destination IP Address:** The 128-bit IP address of the intended recipient.
*   **Extension Headers (EH):** IPv6 packets can optionally include extension headers that provide additional information for fragmentation, security, mobility, etc. Unlike IPv4, routers do not fragment IPv6 packets.

### Host Routing Decisions

*   **Packets at the Source:** Packets are always created at the source device.
*   **Host Routing Table:** Each host maintains its own routing table.
*   **Destination Determination:** A host determines if the destination is:
    *   **Itself:** Using loopback addresses (127.0.0.1 for IPv4, ::1 for IPv6).
    *   **Local Host:** If the destination IP address falls within the same local network (LAN).
    *   **Remote Host:** If the destination IP address is on a different network.
*   **Local vs. Remote Traffic:**
    *   **Local Traffic:** Handled by an intermediary device (e.g., switch) on the local network.
    *   **Remote Traffic:** Forwarded to the **default gateway**.

### Default Gateway

*   **Definition:** A router or Layer 3 switch on the local network that acts as a "door" to other networks.
*   **Features:**
    *   Must have an IP address in the same subnet as the LAN.
    *   Can accept data from the LAN and forward it off the LAN.
    *   Capable of routing traffic to other networks.
*   **Importance:** If a device lacks a correctly configured default gateway, it cannot communicate with devices outside its local network.
*   **Configuration:** Hosts learn their default gateway either statically or dynamically (e.g., via DHCP for IPv4, Router Solicitation for IPv6).

### Router Routing Tables

*   **Function:** Stores information about network paths, enabling routers to make forwarding decisions for incoming packets.
*   **Types of Routes:**
    *   **Directly Connected:** Routes to networks directly attached to the router's interfaces. These are automatically added when an interface is active and configured with an IP address.
    *   **Remote:** Routes to networks not directly connected to the router. These are learned:
        *   **Manually (Static Routing):** Configured by an administrator.
        *   **Dynamically (Dynamic Routing):** Learned through routing protocols (e.g., OSPF, EIGRP).
    *   **Default Route:** A "catch-all" route (0.0.0.0/0) that directs traffic to a specific next hop when no other matching route is found in the routing table. This is often the default gateway.
*   **Route Selection:** When multiple routes to a destination exist, the router selects the "best" route based on criteria like the longest subnet mask match (most specific route) or administrative distance/metric.
*   **`show ip route` Command:** Used on Cisco devices to display the router's routing table, including route sources (L, C, S, O, D, etc.) and route types.

## 🔑 Key Concepts

*   **Network Layer (Layer 3):** The layer responsible for logical addressing and routing of data packets across networks.
*   **IP (Internet Protocol):** The primary protocol suite used at the network layer for addressing and routing.
*   **IPv4:** The fourth version of the Internet Protocol, using 32-bit addresses.
*   **IPv6:** The sixth version of the Internet Protocol, using 128-bit addresses.
*   **Packet:** The unit of
