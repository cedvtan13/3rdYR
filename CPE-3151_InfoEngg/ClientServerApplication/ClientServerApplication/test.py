# Test import
try:
    import cryptography
    print(f"Cryptography version: {cryptography.__version__}")
except ImportError:
    print("Cryptography not found!")