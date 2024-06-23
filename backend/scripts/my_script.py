import sys

def main():
    # Check the length of command-line arguments
    print("Processing:", sys.argv[1], '- At path:', sys.argv[2])
    if len(sys.argv) > 3:
        print('Prompt:', sys.argv[3])

if __name__ == "__main__":
    main()