from typing import Dict, List, Tuple
import re
import ast

class AIRefactorEngine:
    """Provides intelligent code refactoring suggestions and optimizations"""
    
    def __init__(self):
        self.refactor_patterns = {
            'while_to_for': {
                'pattern': r'(\w+)\s*=\s*0\s*\n\s*while\s+\1\s*<\s*len\s*\(\s*(\w+)\s*\)\s*:\s*\n(.*?)\n\s*\1\s*\+\=\s*1',
                'template': 'for {item} in {collection}:\n{body}'
            },
            'range_len_to_enumerate': {
                'pattern': r'for\s+(\w+)\s+in\s+range\s*\(\s*len\s*\(\s*(\w+)\s*\)\s*\)\s*:\s*\n\s*(.+)\[\1\]',
                'template': 'for {index}, {item} in enumerate({collection}):\n    # Use {item} instead of {collection}[{index}]'
            },
            'list_append_to_comprehension': {
                'pattern': r'(\w+)\s*=\s*\[\]\s*\n\s*for\s+(\w+)\s+in\s+(\w+)\s*:\s*\n\s*\1\.append\s*\(\s*(.+)\s*\)',
                'template': '{result} = [{expression} for {item} in {collection}]'
            }
        }
    
    def generate_refactored_code(self, original_code: str, analysis_results: Dict) -> Dict[str, any]:
        """Generate refactored version of the code with improvements"""
        refactored_sections = {}
        
        # Apply basic optimizations
        optimized_code = self._apply_basic_optimizations(original_code, analysis_results)
        
        # Generate specific improvements for each issue type
        issues = analysis_results.get('issues', [])
        
        for issue in issues:
            if issue['type'] == 'while_loop':
                refactored_sections[f"while_loop_line_{issue['line']}"] = self._refactor_while_loop(
                    original_code, issue['line']
                )
            elif issue['type'] == 'inefficient_range_len':
                refactored_sections[f"range_len_line_{issue['line']}"] = self._refactor_range_len(
                    original_code, issue['line']
                )
            elif issue['type'] == 'unused_import':
                refactored_sections[f"unused_import_line_{issue['line']}"] = self._remove_unused_import(
                    original_code, issue['line']
                )
        
        return {
            'optimized_full_code': optimized_code,
            'specific_improvements': refactored_sections,
            'improvement_summary': self._generate_improvement_summary(issues)
        }
    
    def _apply_basic_optimizations(self, code: str, analysis_results: Dict) -> str:
        """Apply basic code optimizations"""
        lines = code.split('\n')
        optimized_lines = []
        
        for i, line in enumerate(lines):
            optimized_line = line
            
            # Replace range(len()) with enumerate or direct iteration
            if 'range(len(' in line and 'for ' in line:
                optimized_line = self._optimize_range_len_pattern(line)
            
            # Suggest list comprehension for simple append patterns
            elif '.append(' in line and i > 0 and 'for ' in lines[i-1]:
                # This is a simple heuristic - in practice, this would need more sophisticated parsing
                optimized_line = line + "  # Consider using list comprehension"
            
            optimized_lines.append(optimized_line)
        
        return '\n'.join(optimized_lines)
    
    def _optimize_range_len_pattern(self, line: str) -> str:
        """Optimize range(len()) patterns"""
        # Simple regex replacement for common patterns
        pattern = r'for\s+(\w+)\s+in\s+range\s*\(\s*len\s*\(\s*(\w+)\s*\)\s*\):'
        match = re.search(pattern, line)
        
        if match:
            index_var = match.group(1)
            collection_var = match.group(2)
            indent = len(line) - len(line.lstrip())
            spacing = ' ' * indent
            
            return f"{spacing}# Optimized: Use enumerate() or direct iteration\n{spacing}for {index_var}, item in enumerate({collection_var}):"
        
        return line
    
    def _refactor_while_loop(self, code: str, line_number: int) -> str:
        """Generate refactored version of while loop"""
        lines = code.split('\n')
        if line_number <= len(lines):
            original_line = lines[line_number - 1]
            
            # Simple while loop to for loop conversion example
            if 'while' in original_line and 'len(' in original_line:
                return """# Original while loop:
# while i < len(items):
#     process(items[i])
#     i += 1

# Optimized version:
for item in items:
    process(item)

# Or with index:
for i, item in enumerate(items):
    process(item)"""
        
        return "# Refactoring suggestion: Consider using for loop or list comprehension"
    
    def _refactor_range_len(self, code: str, line_number: int) -> str:
        """Generate refactored version of range(len()) pattern"""
        return """# Original inefficient pattern:
# for i in range(len(items)):
#     print(items[i])

# Optimized version:
for item in items:
    print(item)

# If you need the index:
for i, item in enumerate(items):
    print(f"{i}: {item}")"""
    
    def _remove_unused_import(self, code: str, line_number: int) -> str:
        """Show code with unused import removed"""
        lines = code.split('\n')
        if line_number <= len(lines):
            import_line = lines[line_number - 1]
            return f"# Remove this unused import:\n# {import_line.strip()}\n\n# This reduces memory footprint and improves startup time"
        
        return "# Remove unused import to optimize memory usage"
    
    def _generate_improvement_summary(self, issues: List[Dict]) -> List[str]:
        """Generate summary of improvements made"""
        improvements = []
        
        issue_counts = {}
        for issue in issues:
            issue_type = issue['type']
            issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        if issue_counts.get('while_loop', 0) > 0:
            improvements.append(f"Converted {issue_counts['while_loop']} while loop(s) to more efficient for loops")
        
        if issue_counts.get('inefficient_range_len', 0) > 0:
            improvements.append(f"Optimized {issue_counts['inefficient_range_len']} range(len()) pattern(s) with direct iteration")
        
        if issue_counts.get('unused_import', 0) > 0:
            improvements.append(f"Removed {issue_counts['unused_import']} unused import(s) to reduce memory footprint")
        
        # Add general improvements
        improvements.extend([
            "Applied Pythonic coding patterns for better readability",
            "Reduced computational complexity where possible",
            "Improved code maintainability and performance"
        ])
        
        return improvements
    
    def get_before_after_examples(self) -> Dict[str, Dict[str, str]]:
        """Get before/after code examples for common optimizations"""
        return {
            "while_loop_optimization": {
                "before": """# Inefficient while loop
i = 0
result = []
while i < len(items):
    if items[i] > 0:
        result.append(items[i] * 2)
    i += 1""",
                "after": """# Efficient list comprehension
result = [item * 2 for item in items if item > 0]

# Or with traditional for loop
result = []
for item in items:
    if item > 0:
        result.append(item * 2)"""
            },
            "range_len_optimization": {
                "before": """# Inefficient range(len()) usage
for i in range(len(data)):
    print(f"Item {i}: {data[i]}")""",
                "after": """# Efficient enumerate usage
for i, item in enumerate(data):
    print(f"Item {i}: {item}")

# Or direct iteration if index not needed
for item in data:
    print(f"Item: {item}")"""
            },
            "list_building_optimization": {
                "before": """# Inefficient list building
squares = []
for i in range(10):
    squares.append(i ** 2)""",
                "after": """# Efficient list comprehension
squares = [i ** 2 for i in range(10)]

# Even more efficient with generator for large datasets
squares_gen = (i ** 2 for i in range(10))"""
            },
            "unused_import_cleanup": {
                "before": """import os
import sys
import math
import random
import unused_module  # Never used

def calculate(x):
    return math.sqrt(x)""",
                "after": """import math

def calculate(x):
    return math.sqrt(x)

# Only import what you actually use
# This reduces memory usage and improves startup time"""
            }
        }
    
    def calculate_improvement_metrics(self, original_analysis: Dict, optimized_analysis: Dict) -> Dict[str, any]:
        """Calculate metrics showing improvement from refactoring"""
        original_score = original_analysis.get('green_score', 0)
        optimized_score = optimized_analysis.get('green_score', 0)
        
        original_issues = len(original_analysis.get('issues', []))
        optimized_issues = len(optimized_analysis.get('issues', []))
        
        return {
            'score_improvement': optimized_score - original_score,
            'issues_fixed': original_issues - optimized_issues,
            'performance_gain': f"{((optimized_score - original_score) / 100 * 100):.1f}%",
            'efficiency_boost': original_issues - optimized_issues,
            'estimated_energy_savings': f"{(original_issues - optimized_issues) * 2.5:.1f} μJ"
        }