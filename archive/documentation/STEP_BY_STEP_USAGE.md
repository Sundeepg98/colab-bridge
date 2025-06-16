# 🎯 Step-by-Step: How to "Run in Colab" from .py Files

## 📋 **SIMPLE 3-STEP PROCESS:**

### **Step 1: Create/Open your .py file**
```bash
# In Cloud Shell Editor or terminal
nano my_script.py
# OR open any existing .py file
```

### **Step 2: Write your Python code**
```python
# Example: my_script.py
import math

print("Hello from my Python script!")
result = math.sqrt(144)
print(f"Square root of 144 = {result}")

# Your data analysis, ML models, algorithms, etc.
data = [1, 2, 3, 4, 5]
processed = [x ** 2 for x in data]
print(f"Squared data: {processed}")
```

### **Step 3: Run it in Colab**
```bash
python3 cloud_shell_runner.py run my_script.py
```

**That's it! Your code runs instantly with results displayed!**

---

## 📺 **What You See When Running:**

```
🚀 Running my_script.py in Colab...
✅ VS Code API Bridge ready!
⚡ Executing code...
📺 Colab Output:
==================================================
✅ Executed via local

Hello from my Python script!
Square root of 144 = 12.0
Squared data: [1, 4, 9, 16, 25]

==================================================
✅ Execution completed!
```

---

## 🎮 **Cloud Shell Editor Workflow:**

### **Method 1: Editor + Terminal**
1. **Top Panel**: Open .py file in Cloud Shell Editor
2. **Bottom Panel**: Terminal with command
3. **Workflow**: 
   - Edit code in editor
   - Save file (Ctrl+S)
   - Run: `python3 cloud_shell_runner.py run filename.py`
   - See results in terminal

### **Method 2: All Terminal**
```bash
# Create file
nano my_analysis.py

# Write code, save and exit

# Run in Colab
python3 cloud_shell_runner.py run my_analysis.py
```

### **Method 3: Code Selection**
1. **Select code** in editor (highlight text)
2. **Copy** (Ctrl+C)
3. **Terminal**: `python3 cloud_shell_runner.py selection`
4. **Paste** and press Ctrl+D

---

## 🔥 **Real Examples:**

### **Data Analysis Script:**
```python
# File: data_analysis.py
import statistics

sales_data = [1200, 1500, 1100, 1800, 1350, 1650, 1400]

print("📊 Sales Analysis:")
print(f"Total Sales: ${sum(sales_data):,}")
print(f"Average: ${statistics.mean(sales_data):,.2f}")
print(f"Best Day: ${max(sales_data):,}")
print(f"Worst Day: ${min(sales_data):,}")
```

**Run it:**
```bash
python3 cloud_shell_runner.py run data_analysis.py
```

### **Math Computation Script:**
```python
# File: math_calc.py
import math

angles = [0, 30, 45, 60, 90]
print("Trigonometric Table:")
for angle in angles:
    rad = math.radians(angle)
    print(f"{angle:2d}°: sin={math.sin(rad):.3f}, cos={math.cos(rad):.3f}")
```

**Run it:**
```bash
python3 cloud_shell_runner.py run math_calc.py
```

### **Algorithm Script:**
```python
# File: sorting.py
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

data = [64, 34, 25, 12, 22, 11, 90]
print(f"Original: {data}")
sorted_data = bubble_sort(data.copy())
print(f"Sorted: {sorted_data}")
```

**Run it:**
```bash
python3 cloud_shell_runner.py run sorting.py
```

---

## ⚡ **Quick Commands Reference:**

| Command | What it does |
|---------|--------------|
| `python3 cloud_shell_runner.py run myfile.py` | Execute entire .py file |
| `python3 cloud_shell_runner.py selection` | Execute copied code |
| `python3 cloud_shell_runner.py interactive` | Live coding mode |

---

## 💡 **Pro Tips:**

### **1. File Organization**
```bash
# Organize your scripts
mkdir my_projects
cd my_projects
nano analysis.py
python3 ../cloud_shell_runner.py run analysis.py
```

### **2. Quick Testing**
```bash
# Test small code snippets
echo 'print("Quick test:", 2+2)' | python3 cloud_shell_runner.py selection
```

### **3. Error Debugging**
```bash
# If script has errors, you'll see clear error messages
python3 cloud_shell_runner.py run buggy_script.py
# Shows exactly what's wrong and where
```

---

## 🎯 **This Replaces:**

❌ **Manual Colab workflow:**
- Open browser → Colab
- Upload .py file
- Copy/paste code
- Run cells manually
- Download results

✅ **Your new workflow:**
- Edit .py file
- Run one command
- See instant results
- Continue coding

**You now have instant "Run in Colab" for any .py file!**