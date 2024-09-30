import csv

def load_lookup_table(filename):
    lookup = {}
    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  
        for row in csv_reader:
            dstport, protocol, tag = row[0], row[1].lower(), row[2] 
            lookup[(dstport, protocol)] = tag
    return lookup


def parse_flow_log(flow_log_line):
    parts = flow_log_line.strip().split()
    if len(parts) < 14:
        return None 
    dstport = parts[5]  
    protocol_num = parts[7]  

    protocol_map = {
        '1': 'icmp',        
        '6': 'tcp',         
        '17': 'udp',        
        '2': 'igmp',        
        '47': 'gre',        
        '50': 'esp',        
        '51': 'ah',         
        '58': 'icmpv6',     
        '89': 'ospf',       
        '132': 'sctp'       
    }
    
    protocol_str = protocol_map.get(protocol_num, 'unknown')

    #print(f"dstport: {dstport}, protocol: {protocol_str}")

    return dstport, protocol_str


def process_logs(flow_log_file, lookup):
    tag_counts = {}
    port_protocol_counts = {}
    untagged_count = 0
    
    with open(flow_log_file, mode='r') as file:
        for line in file:
            result = parse_flow_log(line)
            if not result:
                continue  
            
            dstport, protocol = result
            tag = lookup.get((dstport, protocol), "Untagged")
            
            #print(f"Checking: dstport={dstport}, protocol={protocol}, found_tag={tag}")
            
            if tag == "Untagged":
                untagged_count += 1
            else:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
            port_protocol = (dstport, protocol)
            port_protocol_counts[port_protocol] = port_protocol_counts.get(port_protocol, 0) + 1

    return tag_counts, port_protocol_counts, untagged_count



def write_output(tag_counts, port_protocol_counts, untagged_count, output_file):
    with open(output_file, mode='w') as file:

        file.write("Tag Counts:\n")
        file.write("Tag,Count\n")
        for tag, count in tag_counts.items():
            file.write(f"{tag},{count}\n")
        file.write(f"Untagged,{untagged_count}\n")
        

        file.write("\nPort/Protocol Combination Counts:\n")
        file.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counts.items():
            file.write(f"{port},{protocol},{count}\n")


def main():
    lookup_file = "lookup.csv"  
    flow_log_file = "flow_logs.txt" 
    output_file = "output.txt"  
    
 
    lookup = load_lookup_table(lookup_file)
    
    tag_counts, port_protocol_counts, untagged_count = process_logs(flow_log_file, lookup)
    
    write_output(tag_counts, port_protocol_counts, untagged_count, output_file)


if __name__ == "__main__":
    main()

