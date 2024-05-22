import argparse
from handler import VideoHandler


def main():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-i", "--input",   help="input file name",   default="input.mp4")
    parser.add_argument("-o", "--output",  help="output file name",  default="output.mp4")
    parser.add_argument("-r", "--report",  help="report file name",  default="report.csv")    
    
    args = parser.parse_args()
    
    video_handler = VideoHandler()
    video_handler.process_video("../input/"+args.input, "../output/"+args.output, "../output/"+args.report)
    


if __name__ == '__main__':
    main()