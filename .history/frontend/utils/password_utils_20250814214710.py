import re
import string

def calculate_password_strength(password):
    """
    Calculate password strength and return score (0-100) and description
    """
    if not password:
        return 0, "No password"
    
    score = 0
    feedback = []
    
    # Length scoring
    length = len(password)
    if length >= 12:
        score += 25
    elif length >= 8:
        score += 15
    elif length >= 6:
        score += 10
    else:
        feedback.append("Too short (minimum 8 characters)")
    
    # Character variety scoring
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\?]', password))
    
    variety_count = sum([has_lower, has_upper, has_digit, has_special])
    
    if variety_count == 4:
        score += 25
    elif variety_count == 3:
        score += 20
    elif variety_count == 2:
        score += 10
    else:
        feedback.append("Use uppercase, lowercase, numbers, and symbols")
    
    # Pattern scoring
    if not re.search(r'(.)\1{2,}', password):  # No 3+ repeated characters
        score += 15
    else:
        feedback.append("Avoid repeated characters")
    
    if not re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde)', password.lower()):
        score += 15
    else:
        feedback.append("Avoid sequential patterns")
    
    # Common password check (simple)
    common_passwords = ['password', '123456', 'qwerty', 'abc123', 'password123']
    if password.lower() not in common_passwords:
        score += 20
    else:
        feedback.append("Avoid common passwords")
    
    # Determine strength level
    if score >= 80:
        strength = "Very Strong"
        color = "#28a745"  # Green
    elif score >= 60:
        strength = "Strong"
        color = "#28a745"  # Green
    elif score >= 40:
        strength = "Medium"
        color = "#ffc107"  # Yellow
    elif score >= 20:
        strength = "Weak"
        color = "#fd7e14"  # Orange
    else:
        strength = "Very Weak"
        color = "#dc3545"  # Red
    
    return score, strength, color, feedback

def generate_secure_password(length=16, include_symbols=True):
    """Generate a secure password"""
    import random
    
    # Character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?" if include_symbols else ""
    
    # Ensure at least one character from each set
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
    ]
    
    if include_symbols:
        password.append(random.choice(symbols))
    
    # Fill the rest with random characters
    all_chars = lowercase + uppercase + digits + symbols
    remaining_length = length - len(password)
    
    for _ in range(remaining_length):
        password.append(random.choice(all_chars))
    
    # Shuffle the password
    random.shuffle(password)
    
    return ''.join(password)