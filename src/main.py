from handler import VideoHandler


def main():
    
    input_file_name = input("input file name: ")
    output_file_name = "output.mp4"
    report = "report.csv"
    
    video_handler = VideoHandler()
    video_handler.process_video("../input/"+input_file_name, "../output/"+output_file_name, "../output/"+report)


if __name__ == '__main__':
    main()