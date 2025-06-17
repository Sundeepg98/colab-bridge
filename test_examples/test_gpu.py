import torch
print("🚀 GPU Test")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    x = torch.randn(1000, 1000).cuda()
    print(f"Tensor on GPU: {x.device}")
