import matplotlib.pyplot as plt
import numpy as np

print("📊 Creating plot...")
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.title("Sine Wave from Colab GPU")
plt.savefig("sine_wave_colab.png")
print("✅ Plot saved as sine_wave_colab.png")
