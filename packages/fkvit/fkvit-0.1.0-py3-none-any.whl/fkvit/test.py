import sys

def main():
    # Read input from stdin until EOF (Ctrl+D or Ctrl+Z)
    input_string = sys.stdin.read()
    input()
    process_input(input_string)

def process_input(input_string):
    # Process the input here
    print("Input string length:", len(input_string))
    print("Input string:")
    print(input_string)

if __name__ == "__main__":
    main()