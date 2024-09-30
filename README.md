# Illumio-Online-Assessment-

Illumio Online Assessment Python Code

Requirements:
Python 3.x (Tested with Python 3.12.1)
No external dependencies (only standard Python libraries)

Assumptions:
The protocol number in the flow log is mapped to the following:
1 → icmp
6 → tcp
17 → udp

If a destination port and protocol combination is not found in the lookup table, the log entry is tagged as Untagged.

The matching of protocols is case-insensitive.

Testing:
You can test the program with the provided flow_logs.txt and lookup.csv files or modify them to test additional
cases. Edge cases such as missing or unmatched logs will be marked as Untagged.

Run the program: python log_parser.py -
The program will generate an output.txt file containing:

Tag Counts: The number of log entries mapped to each tag.
Port/Protocol Combination Counts: The count of unique destination port and protocol combinations.
