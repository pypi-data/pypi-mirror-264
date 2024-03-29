def prompt_for_file_path():
    return input("Enter the file path: ")

def search_method_1(file_path, search_string):
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if search_string in line:
                print(f"Found '{search_string}' in line {line_number}: {line.strip()}")

def search_method_2(file_path, search_string):
    # This method assumes lines are structured with numbers separated by semicolons
    # and that the search string is also a number. Adjust as necessary.
    lines = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            lines.append((line_number, line))
    
    # Sort lines based on the first number in each line
    lines.sort(key=lambda x: int(x[1].split(';')[0]))
    
    # Perform a binary search on the sorted lines
    low = 0
    high = len(lines) - 1
    while low <= high:
        mid = (low + high) // 2
        line_number, line = lines[mid]
        if search_string in line:
            print(f"Found '{search_string}' in line {line_number}: {line.strip()}")
            return
        elif search_string < line:
            high = mid - 1
        else:
            low = mid + 1
    print("Search string not found.")

if __name__ == "__main__":
    file_path = prompt_for_file_path()
    
    search_string = input("Enter the search string: ")
    
    print("Searching with method 1...")
    search_method_1(file_path, search_string)
    
    print("\nSearching with method 2...")
    search_method_2(file_path, search_string)
