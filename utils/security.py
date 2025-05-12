import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Test
if __name__ == "__main__":
    hashed = hash_password("test123")
    print("Hashed:", hashed)
    print("Check:", check_password("test123", hashed))