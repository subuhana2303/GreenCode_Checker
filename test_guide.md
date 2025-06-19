# Green Code Checker - Testing Guide

## How to Test All Features

### 1. Basic Code Analysis
**Steps:**
1. Enter this test code in the main text area:
```python
import os
import sys
import unused_module

def inefficient_function():
    data = []
    for i in range(len([1,2,3,4,5])):
        data.append(i * 2)
    
    counter = 0
    while counter < 10:
        print(f"Count: {counter}")
        counter += 1
    
    return data

result = inefficient_function()
```

2. Click "Analyze Code"
3. **Expected Results:**
   - Green Score should be around 40-60/100
   - Should detect: unused imports, range(len()) pattern, while loop
   - Should show security score of 100/100

### 2. Dashboard Tab Features
**What to verify:**
- Green score gauge displays correctly
- Environmental impact metrics show energy usage
- Code statistics chart shows bars for different metrics
- Issues pie chart displays found problems
- Complexity radar chart shows multiple dimensions

### 3. Details Tab
**What to verify:**
- Expandable issue sections with line numbers
- Specific suggestions for each issue
- Clear descriptions of problems found

### 4. Security Tab
**Test with this code:**
```python
import subprocess
password = "hardcoded123"
user_input = input("Enter command: ")
subprocess.call(user_input, shell=True)
eval("print('dangerous')")
```

**Expected Results:**
- Security score should be low (20-40/100)
- Should detect: hardcoded credentials, shell injection, eval usage
- Security recommendations should appear

### 5. Achievements Tab
**How to test:**
1. Complete multiple analyses with different scores
2. Try to get scores of 80+ and 100
3. **Expected Results:**
   - Level progression should update
   - Achievement badges should unlock
   - LinkedIn sharing button should work
   - Progress bars should show advancement

### 6. History Tab
**How to test:**
1. Analyze several different code samples
2. **Expected Results:**
   - Interactive chart showing score progression
   - List of recent analyses with expandable details
   - Export CSV button should work
   - Code previews should display

### 7. Carbon Impact Tab
**What to verify:**
- Energy consumption metrics in microjoules
- Carbon emissions calculations
- Efficiency rating (A+ to F scale)
- Environmental equivalents (smartphone charges, etc.)
- Pie chart showing energy breakdown

### 8. Database Tab
**What to verify:**
- Platform statistics (total users, analyses)
- Global leaderboard showing rankings
- User analytics charts if you're logged in as non-default user

### 9. AI Refactoring (Enhanced Feature)
**How to test:**
1. Use the inefficient code sample above
2. Check the "Details" tab for refactoring suggestions
3. **Expected Results:**
   - Before/after code comparisons
   - Specific improvement descriptions
   - Performance impact metrics

### 10. Sample Code Testing
**Steps:**
1. Use sidebar "Load Sample Code" dropdown
2. Try different sample types:
   - Basic Inefficient
   - Moderate Issues
   - Good Code
3. Analyze each to see different score ranges

## Quick Verification Checklist

- [ ] Code analysis completes without errors
- [ ] Green score appears (0-100)
- [ ] All 7 tabs load and display content
- [ ] Visualizations render (charts, gauges, graphs)
- [ ] Database connection works (check Database tab)
- [ ] Achievement system responds to good scores
- [ ] LinkedIn sharing generates proper URLs
- [ ] History tracking works across sessions
- [ ] Security analysis detects vulnerabilities
- [ ] AI refactoring shows optimization suggestions

## Troubleshooting

### If achievements don't work:
- Complete at least 2-3 analyses
- Try achieving scores above 80
- Check Database tab for user statistics

### If LinkedIn sharing doesn't work:
- The button generates a URL - clicking opens LinkedIn
- Copy the generated URL manually if needed

### If charts don't display:
- Refresh the page
- Try analyzing code again
- Check browser console for errors

### If database features are limited:
- Some features depend on PostgreSQL connection
- Basic functionality works with local storage fallback

## Expected Performance Benchmarks

**Code Quality Scores:**
- Efficient code: 85-100/100
- Average code: 60-84/100  
- Inefficient code: 0-59/100

**Security Scores:**
- Secure code: 90-100/100
- Minor issues: 70-89/100
- Major vulnerabilities: 0-69/100

The application should handle all test cases gracefully and provide meaningful feedback for code improvement.