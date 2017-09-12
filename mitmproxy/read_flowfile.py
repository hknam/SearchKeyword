from mitmproxy import io
from mitmproxy.exceptions import FlowReadException

def read_flowfile(flowfile):
    with open(flowfile, 'rb') as capture_traffic:
        freader = io.FlowReader(capture_traffic)
        try:
            for flow in freader.stream():
                find_search_keyword(str(flow))

        except FlowReadException as e:
            print("flow file corrupted: {}".format(e))

def find_search_keyword(flow):
    lines = flow.split('\n')
    for line in lines:
        if line.find('iphone') >= 0:
            print(line)






def main():
    file_path = '/home/hknam/Documents/flowdump/flowdump/traffic/www.gjicp.or.kr'
    read_flowfile(file_path)


if __name__ == "__main__":
    main()

