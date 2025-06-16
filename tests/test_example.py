# Test Python file for Cloud Shell Editor
import math

print("🧮 Mathematical Computations:")
print(f"π = {math.pi:.4f}")
print(f"e = {math.e:.4f}")

# Data processing
data = [1, 4, 9, 16, 25]
sqrt_data = [math.sqrt(x) for x in data]

print(f"\n📊 Data Processing:")
print(f"Original: {data}")
print(f"Square roots: {sqrt_data}")

# Algorithm demo
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(f"\n🔢 Fibonacci sequence:")
fib_seq = [fibonacci(i) for i in range(7)]
print(f"F(0-6): {fib_seq}")

print("\n✅ Cloud Shell Editor → Colab execution successful\!")
