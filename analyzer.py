import ast
import re
from typing import Dict, List, Any

class CodeAnalyzer:
    """Analyzes Python code for sustainability and efficiency patterns"""
    
    def __init__(self):
        self.issues = []
    
    def analyze(self, code: str) -> Dict[str, Any]:
        """Main analysis method that returns comprehensive code analysis"""
        self.issues = []
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            raise SyntaxError(f"Invalid Python syntax: {e}")
        
        # Basic statistics
        lines_of_code = len([line for line in code.split('\n') if line.strip() and not line.strip().startswith('#')])
        
        # AST-based analysis
        visitor = CodeVisitor()
        visitor.visit(tree)
        
        # Additional pattern analysis
        inefficient_patterns = self._find_inefficient_patterns(code)
        unused_imports = self._find_unused_imports(code, tree)
        
        # Compile results
        results = {
            'lines_of_code': lines_of_code,
            'function_count': visitor.function_count,
            'import_count': visitor.import_count,
            'while_loop_count': visitor.while_loop_count,
            'for_loop_count': visitor.for_loop_count,
            'inefficient_patterns_count': len(inefficient_patterns),
            'unused_imports_count': len(unused_imports),
            'issues': self._compile_issues(visitor, inefficient_patterns, unused_imports),
            'complexity_score': self._calculate_complexity(visitor)
        }
        
        return results
    
    def _find_inefficient_patterns(self, code: str) -> List[Dict[str, Any]]:
        """Find inefficient coding patterns using regex"""
        patterns = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for range(len(...)) pattern
            if re.search(r'range\s*\(\s*len\s*\(', line):
                patterns.append({
                    'type': 'inefficient_range_len',
                    'line': i,
                    'description': 'Using range(len(...)) instead of direct iteration',
                    'suggestion': 'Consider using "for item in collection:" or enumerate()'
                })
            
            # Check for unnecessary list() calls
            if re.search(r'list\s*\(\s*range\s*\(', line):
                patterns.append({
                    'type': 'unnecessary_list_conversion',
                    'line': i,
                    'description': 'Converting range to list unnecessarily',
                    'suggestion': 'Use range directly in most cases'
                })
        
        return patterns
    
    def _find_unused_imports(self, code: str, tree: ast.AST) -> List[Dict[str, Any]]:
        """Find potentially unused imports"""
        # Get all imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        'name': alias.name,
                        'alias': alias.asname,
                        'line': node.lineno,
                        'type': 'import'
                    })
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append({
                        'name': alias.name,
                        'alias': alias.asname,
                        'module': node.module,
                        'line': node.lineno,
                        'type': 'from_import'
                    })
        
        # Simple unused import detection (basic implementation)
        unused = []
        code_body = ' '.join(code.split('\n')[1:])  # Skip import lines for usage check
        
        for imp in imports:
            import_name = imp['alias'] if imp['alias'] else imp['name']
            if import_name and import_name not in code_body:
                unused.append({
                    'type': 'unused_import',
                    'line': imp['line'],
                    'description': f"Import '{import_name}' appears to be unused",
                    'suggestion': 'Remove unused imports to reduce memory footprint'
                })
        
        return unused
    
    def _compile_issues(self, visitor, inefficient_patterns, unused_imports) -> List[Dict[str, Any]]:
        """Compile all issues into a single list"""
        issues = []
        
        # Add while loop issues
        for line in visitor.while_loops:
            issues.append({
                'type': 'while_loop',
                'line': line,
                'description': 'While loop detected - consider if for-loop or list comprehension is more appropriate',
                'suggestion': 'Replace with for-loop or list comprehension when possible'
            })
        
        # Add inefficient patterns
        issues.extend(inefficient_patterns)
        
        # Add unused imports
        issues.extend(unused_imports)
        
        return sorted(issues, key=lambda x: x['line'])
    
    def _calculate_complexity(self, visitor) -> int:
        """Calculate a simple complexity score"""
        complexity = 0
        complexity += visitor.while_loop_count * 3  # While loops are more complex
        complexity += visitor.for_loop_count * 1
        complexity += visitor.function_count * 2
        complexity += visitor.nested_depth * 2
        return complexity
    
    def calculate_green_score(self, analysis_results: Dict[str, Any]) -> int:
        """Calculate the green score based on analysis results"""
        base_score = 100
        
        # Deduct points for issues
        deductions = 0
        deductions += analysis_results.get('while_loop_count', 0) * 15
        deductions += analysis_results.get('unused_imports_count', 0) * 10
        deductions += analysis_results.get('inefficient_patterns_count', 0) * 12
        
        # Complexity penalty
        complexity = analysis_results.get('complexity_score', 0)
        if complexity > 20:
            deductions += (complexity - 20) * 2
        
        # Calculate final score
        green_score = max(0, base_score - deductions)
        return min(100, green_score)

class CodeVisitor(ast.NodeVisitor):
    """AST visitor to collect code statistics"""
    
    def __init__(self):
        self.function_count = 0
        self.import_count = 0
        self.while_loop_count = 0
        self.for_loop_count = 0
        self.while_loops = []  # Store line numbers
        self.nested_depth = 0
        self.current_depth = 0
    
    def visit_FunctionDef(self, node):
        self.function_count += 1
        self.current_depth += 1
        self.nested_depth = max(self.nested_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1
    
    def visit_AsyncFunctionDef(self, node):
        self.function_count += 1
        self.current_depth += 1
        self.nested_depth = max(self.nested_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1
    
    def visit_Import(self, node):
        self.import_count += len(node.names)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        self.import_count += len(node.names)
        self.generic_visit(node)
    
    def visit_While(self, node):
        self.while_loop_count += 1
        self.while_loops.append(node.lineno)
        self.current_depth += 1
        self.nested_depth = max(self.nested_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1
    
    def visit_For(self, node):
        self.for_loop_count += 1
        self.current_depth += 1
        self.nested_depth = max(self.nested_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1
