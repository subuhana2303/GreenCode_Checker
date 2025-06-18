from typing import List, Dict, Any

class SuggestionEngine:
    """Generates eco-friendly coding suggestions based on analysis results"""
    
    def __init__(self):
        self.suggestions = []
    
    def generate_suggestions(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate suggestions based on analysis results"""
        suggestions = []
        
        # General efficiency suggestions
        suggestions.extend(self._get_general_suggestions(analysis_results))
        
        # Specific issue-based suggestions
        suggestions.extend(self._get_issue_specific_suggestions(analysis_results))
        
        # Best practices suggestions
        suggestions.extend(self._get_best_practices_suggestions(analysis_results))
        
        return suggestions
    
    def _get_general_suggestions(self, results: Dict[str, Any]) -> List[str]:
        """Generate general efficiency suggestions"""
        suggestions = []
        
        if results.get('lines_of_code', 0) > 100:
            suggestions.append(
                "📦 Consider breaking large files into smaller, focused modules for better maintainability and reduced memory usage."
            )
        
        if results.get('function_count', 0) == 0:
            suggestions.append(
                "🔧 Consider organizing your code into functions to improve reusability and reduce code duplication."
            )
        
        if results.get('complexity_score', 0) > 30:
            suggestions.append(
                "🎯 High complexity detected. Consider simplifying logic and reducing nesting levels to improve performance."
            )
        
        return suggestions
    
    def _get_issue_specific_suggestions(self, results: Dict[str, Any]) -> List[str]:
        """Generate suggestions for specific issues found"""
        suggestions = []
        
        if results.get('while_loop_count', 0) > 0:
            suggestions.append(
                "🔄 Replace while loops with for loops or list comprehensions when possible. "
                "For loops are generally more efficient and less prone to infinite loops."
            )
        
        if results.get('unused_imports_count', 0) > 0:
            suggestions.append(
                "🧹 Remove unused imports to reduce memory footprint and improve startup time. "
                "Every import consumes resources even when not used."
            )
        
        if results.get('inefficient_patterns_count', 0) > 0:
            suggestions.append(
                "⚡ Replace range(len(collection)) with direct iteration or enumerate(). "
                "Direct iteration is more Pythonic and efficient."
            )
        
        return suggestions
    
    def _get_best_practices_suggestions(self, results: Dict[str, Any]) -> List[str]:
        """Generate best practices suggestions"""
        suggestions = [
            "🌱 Use list comprehensions instead of loops where appropriate - they're more efficient and readable.",
            "⚙️ Consider using built-in functions like map(), filter(), and reduce() for functional programming approaches.",
            "💾 Use generators for large datasets to save memory and improve performance.",
            "🔧 Profile your code with tools like cProfile to identify actual bottlenecks before optimizing.",
            "📚 Use appropriate data structures: sets for membership testing, deques for frequent insertions/deletions.",
            "🎯 Avoid premature optimization - write clear code first, then optimize where needed based on profiling.",
            "🔄 Use context managers (with statements) for resource management to prevent memory leaks.",
            "⚡ Consider using NumPy for numerical computations - it's significantly faster than pure Python for math operations."
        ]
        
        # Return a subset of suggestions to avoid overwhelming the user
        return suggestions[:4]  # Return first 4 suggestions
    
    def get_optimization_examples(self) -> Dict[str, Dict[str, str]]:
        """Get code optimization examples"""
        return {
            "range_len_optimization": {
                "inefficient": """
# Inefficient
for i in range(len(items)):
    print(items[i])
                """,
                "efficient": """
# Efficient
for item in items:
    print(item)

# Or with index
for i, item in enumerate(items):
    print(f"{i}: {item}")
                """
            },
            "while_to_for": {
                "inefficient": """
# Inefficient
i = 0
while i < len(items):
    process(items[i])
    i += 1
                """,
                "efficient": """
# Efficient
for item in items:
    process(item)
                """
            },
            "list_comprehension": {
                "inefficient": """
# Inefficient
result = []
for item in items:
    if condition(item):
        result.append(transform(item))
                """,
                "efficient": """
# Efficient
result = [transform(item) for item in items if condition(item)]
                """
            }
        }
