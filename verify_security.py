"""Security verification script for StandardsGPT.
Run this before pushing to GitHub to verify no sensitive data is exposed.
"""
import os
import sys

def check_file_tracking():
    """Check if sensitive files are being tracked by Git."""
    sensitive_files = ['.env', 'config.py']
    tracked_files = os.popen('git ls-files').read().splitlines()
    
    issues = []
    for file in sensitive_files:
        if file in tracked_files:
            issues.append(f"❌ {file} is being tracked by Git!")
        else:
            print(f"✅ {file} is not tracked by Git")
    
    return issues

def check_env_file():
    """Check if .env file exists and contains sensitive data."""
    issues = []
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            content = f.read()
            if 'OPENROUTER_API_KEY' in content:
                issues.append("❌ .env file contains API key (this is fine locally, but don't commit it!)")
    else:
        print("ℹ️  No .env file found (this is fine if you're using config.py)")
    
    return issues

def main():
    print("🔒 Running security checks...\n")
    
    all_issues = []
    all_issues.extend(check_file_tracking())
    all_issues.extend(check_env_file())
    
    if all_issues:
        print("\n⚠️  Security issues found:")
        for issue in all_issues:
            print(f"- {issue}")
        print("\n❌ Please fix these issues before pushing to GitHub!")
        return 1
    else:
        print("\n✅ All security checks passed!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
