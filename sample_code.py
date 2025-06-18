SAMPLE_INEFFICIENT_CODE = """# Sample inefficient Python code for testing
import os
import sys
import math
import random
import unused_module  # This import is not used

# Inefficient while loop example
def count_items(items):
    count = 0
    i = 0
    while i < len(items):  # Could use for loop or len() directly
        if items[i] > 0:
            count += 1
        i += 1
    return count

# Inefficient range(len()) pattern
def process_list(data):
    results = []
    for i in range(len(data)):  # Should iterate directly
        if data[i] % 2 == 0:
            results.append(data[i] * 2)
    return results

# Inefficient list creation
def create_squares(n):
    squares = []
    for i in range(n):
        squares.append(i * i)  # Could use list comprehension
    return squares

# Another while loop that could be optimized
def find_first_negative(numbers):
    index = 0
    while index < len(numbers):
        if numbers[index] < 0:
            return index
        index += 1
    return -1

# Main execution
if __name__ == "__main__":
    # Test the inefficient functions
    test_data = [1, -2, 3, -4, 5, 6, 7, 8, 9, 10]
    
    print("Count of positive items:", count_items(test_data))
    print("Processed data:", process_list(test_data))
    print("Squares:", create_squares(5))
    print("First negative index:", find_first_negative(test_data))
    
    # More inefficient patterns
    result = list(range(10))  # Unnecessary list() conversion
    
    # Unused variable
    unused_variable = "This variable is never used"
"""

# Alternative sample codes for different testing scenarios
SAMPLE_CODES = {
    "basic_inefficient": """
import unused_import

def bad_loop(items):
    i = 0
    while i < len(items):
        print(items[i])
        i += 1

for i in range(len([1, 2, 3, 4, 5])):
    print(i)
""",
    
    "moderately_inefficient": """
import sys
import os
import math

def process_data(data):
    result = []
    i = 0
    while i < len(data):
        if data[i] > 0:
            result.append(data[i] * 2)
        i += 1
    return result

def another_function(numbers):
    squares = []
    for i in range(len(numbers)):
        squares.append(numbers[i] ** 2)
    return squares

data = [1, 2, 3, 4, 5]
print(process_data(data))
print(another_function(data))
""",
    
    "efficient_code": """
def process_data(data):
    return [item * 2 for item in data if item > 0]

def calculate_squares(numbers):
    return [num ** 2 for num in numbers]

def main():
    data = [1, 2, 3, 4, 5]
    processed = process_data(data)
    squares = calculate_squares(data)
    
    print(f"Processed: {processed}")
    print(f"Squares: {squares}")

if __name__ == "__main__":
    main()
"""
}

def get_sample_code(code_type: str = "basic_inefficient") -> str:
    """Get sample code by type"""
    return SAMPLE_CODES.get(code_type, SAMPLE_INEFFICIENT_CODE)

def get_all_sample_types() -> list:
    """Get all available sample code types"""
    return list(SAMPLE_CODES.keys())
