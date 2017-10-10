from mitmproxy import io
from mitmproxy.exceptions import FlowReadException
import os


def read_flowfile(flowfile, filename):
    with open(flowfile, 'rb') as capture_traffic:
        freader = io.FlowReader(capture_traffic)

        try:
            for flow in freader.stream():
                if find_search_keyword(str(flow)):
                    print(flowfile)

        except FlowReadException as e:
            print("flow file corrupted: {}".format(e))



def find_search_keyword(flow):

    lines = flow.split('\n')
    for line in lines:
        #print(line)
        if line.find('iphone') >= 0:
            return True
    return False



def search(dirname):
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        read_flowfile(full_filename, filename)




def main():
    #file_path = '/home/hknam/Downloads/170912/result/traffic/'
    file_path = '/home/hknam/flowdump/traffic/'
    search(file_path)


if __name__ == "__main__":
    main()

