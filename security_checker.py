import re
import ast
from typing import List, Dict, Any

class SecurityChecker:
    """Detects security vulnerabilities and risky patterns in Python code"""
    
    def __init__(self):
        self.security_patterns = {
            'eval_usage': {
                'pattern': r'\beval\s*\(',
                'severity': 'HIGH',
                'description': 'Use of eval() function detected - major security risk',
                'suggestion': 'Avoid eval(). Use literal_eval() for safe evaluation or ast.parse() for code analysis'
            },
            'exec_usage': {
                'pattern': r'\bexec\s*\(',
                'severity': 'HIGH', 
                'description': 'Use of exec() function detected - code injection risk',
                'suggestion': 'Avoid exec(). Consider safer alternatives like importlib for dynamic imports'
            },
            'hardcoded_password': {
                'pattern': r'(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']',
                'severity': 'HIGH',
                'description': 'Hardcoded password detected',
                'suggestion': 'Use environment variables or secure configuration files for credentials'
            },
            'hardcoded_secret': {
                'pattern': r'(secret|token|key|api_key)\s*=\s*["\'][^"\']{8,}["\']',
                'severity': 'HIGH',
                'description': 'Hardcoded secret/token detected',
                'suggestion': 'Store secrets in environment variables or secure vault systems'
            },
            'sql_injection_risk': {
                'pattern': r'\.execute\s*\(\s*["\'].*%.*["\']',
                'severity': 'MEDIUM',
                'description': 'Potential SQL injection vulnerability',
                'suggestion': 'Use parameterized queries instead of string formatting in SQL'
            },
            'shell_injection': {
                'pattern': r'(os\.system|subprocess\.call|subprocess\.run)\s*\([^)]*\+',
                'severity': 'HIGH',
                'description': 'Potential shell injection via command concatenation',
                'suggestion': 'Use subprocess with list arguments instead of string concatenation'
            },
            'pickle_usage': {
                'pattern': r'\bpickle\.loads?\s*\(',
                'severity': 'MEDIUM',
                'description': 'Pickle deserialization can be unsafe with untrusted data',
                'suggestion': 'Use JSON or other safe serialization formats for untrusted data'
            },
            'temp_file_unsafe': {
                'pattern': r'open\s*\(\s*["\']\/tmp\/',
                'severity': 'LOW',
                'description': 'Unsafe temporary file usage',
                'suggestion': 'Use tempfile module for secure temporary file creation'
            },
            'weak_random': {
                'pattern': r'random\.(random|randint|choice)',
                'severity': 'LOW',
                'description': 'Using weak random number generator for security purposes',
                'suggestion': 'Use secrets module for cryptographically strong random numbers'
            },
            'debug_mode': {
                'pattern': r'debug\s*=\s*True',
                'severity': 'MEDIUM',
                'description': 'Debug mode enabled - may expose sensitive information',
                'suggestion': 'Disable debug mode in production environments'
            }
        }
    
    def analyze_security(self, code: str) -> Dict[str, Any]:
        """Analyze code for security vulnerabilities"""
        security_issues = []
        
        # Pattern-based detection
        lines = code.split('\n')
        for line_num, line in enumerate(lines, 1):
            for issue_type, pattern_info in self.security_patterns.items():
                if re.search(pattern_info['pattern'], line, re.IGNORECASE):
                    security_issues.append({
                        'type': 'security_vulnerability',
                        'subtype': issue_type,
                        'line': line_num,
                        'severity': pattern_info['severity'],
                        'description': pattern_info['description'],
                        'suggestion': pattern_info['suggestion'],
                        'code_snippet': line.strip()
                    })
        
        # AST-based analysis for more complex patterns
        try:
            tree = ast.parse(code)
            ast_issues = self._analyze_ast_security(tree)
            security_issues.extend(ast_issues)
        except SyntaxError:
            pass  # Skip AST analysis if code has syntax errors
        
        # Calculate security score
        security_score = self._calculate_security_score(security_issues)
        
        return {
            'security_issues': security_issues,
            'security_score': security_score,
            'risk_level': self._get_risk_level(security_score),
            'total_vulnerabilities': len(security_issues),
            'high_risk_count': len([i for i in security_issues if i.get('severity') == 'HIGH']),
            'medium_risk_count': len([i for i in security_issues if i.get('severity') == 'MEDIUM']),
            'low_risk_count': len([i for i in security_issues if i.get('severity') == 'LOW'])
        }
    
    def _analyze_ast_security(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Perform AST-based security analysis"""
        issues = []
        
        for node in ast.walk(tree):
            # Check for dangerous function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    if func_name in ['eval', 'exec', 'compile']:
                        issues.append({
                            'type': 'security_vulnerability',
                            'subtype': f'dangerous_function_{func_name}',
                            'line': node.lineno,
                            'severity': 'HIGH',
                            'description': f'Dangerous function {func_name}() usage detected',
                            'suggestion': f'Avoid using {func_name}() as it can execute arbitrary code'
                        })
                
                # Check for subprocess with shell=True
                elif isinstance(node.func, ast.Attribute):
                    if (hasattr(node.func.value, 'id') and 
                        node.func.value.id == 'subprocess' and
                        any(keyword.arg == 'shell' and 
                            isinstance(keyword.value, ast.Constant) and 
                            keyword.value.value is True 
                            for keyword in node.keywords)):
                        issues.append({
                            'type': 'security_vulnerability',
                            'subtype': 'subprocess_shell_true',
                            'line': node.lineno,
                            'severity': 'HIGH',
                            'description': 'subprocess called with shell=True - command injection risk',
                            'suggestion': 'Use shell=False and pass command as list of arguments'
                        })
            
            # Check for assert statements (can be disabled in production)
            elif isinstance(node, ast.Assert):
                issues.append({
                    'type': 'security_vulnerability',
                    'subtype': 'assert_statement',
                    'line': node.lineno,
                    'severity': 'LOW',
                    'description': 'Assert statement used - can be disabled with -O flag',
                    'suggestion': 'Use proper exception handling instead of assert for security checks'
                })
        
        return issues
    
    def _calculate_security_score(self, issues: List[Dict[str, Any]]) -> int:
        """Calculate security score based on found issues"""
        base_score = 100
        
        for issue in issues:
            severity = issue.get('severity', 'LOW')
            if severity == 'HIGH':
                base_score -= 25
            elif severity == 'MEDIUM':
                base_score -= 10
            elif severity == 'LOW':
                base_score -= 5
        
        return max(0, base_score)
    
    def _get_risk_level(self, security_score: int) -> str:
        """Get risk level based on security score"""
        if security_score >= 90:
            return 'LOW'
        elif security_score >= 70:
            return 'MEDIUM'
        elif security_score >= 50:
            return 'HIGH'
        else:
            return 'CRITICAL'
    
    def get_security_recommendations(self, security_analysis: Dict[str, Any]) -> List[str]:
        """Get general security recommendations"""
        recommendations = [
            "🔒 Use environment variables for sensitive configuration",
            "🛡️ Validate and sanitize all user inputs",
            "🔐 Use parameterized queries for database operations",
            "🔑 Implement proper authentication and authorization",
            "📝 Keep dependencies updated and scan for vulnerabilities",
            "🚫 Avoid using eval(), exec(), and other dangerous functions",
            "🔍 Use static analysis tools in your CI/CD pipeline",
            "🧪 Implement security testing in your development process"
        ]
        
        risk_level = security_analysis.get('risk_level', 'LOW')
        
        if risk_level == 'CRITICAL':
            recommendations.insert(0, "🚨 URGENT: Address critical security vulnerabilities immediately")
        elif risk_level == 'HIGH':
            recommendations.insert(0, "⚠️ HIGH PRIORITY: Multiple security issues need attention")
        
        return recommendations[:6]  # Return top 6 recommendations