import numpy as np
import matplotlib.pyplot as plt

# 假設三個麥克風的間距和頻率範圍
microphone_positions = np.array([[-1, 0], [0, 0], [1, 0]])  # 麥克風位置 (例如, 單位距離)
frequencies = np.linspace(100, 1000, 10)  # 假設的頻率範圍
angles = np.linspace(-np.pi, np.pi, 360)  # 角度範圍 (-180度到180度)

# 初始化方向圖數據
beam_pattern = np.zeros_like(angles)

# 計算每個方向的增益
for i, angle in enumerate(angles):
    # 計算每個頻率下的增益 (假設簡化為某種形式)
    gain = 0
    for freq in frequencies:
        # 計算每個方向上的增益 (簡化示例)
        gain += np.abs(np.sum(np.exp(-1j * freq * np.dot(microphone_positions, [np.cos(angle), np.sin(angle)]))))
    beam_pattern[i] = np.abs(gain)

# 正規化方向圖數據
beam_pattern = beam_pattern / np.max(beam_pattern)

# 計算半峰全寬 (FWHM)
max_value = np.max(beam_pattern)
half_max_value = max_value / 2
indices = np.where(beam_pattern >= half_max_value)[0]
theta_fwhm = angles[indices]
fwhm = np.abs(theta_fwhm[-1] - theta_fwhm[0])

# 輸出結果
print(f"半峰全寬 (FWHM): {np.degrees(fwhm):.2f} 度")

# 視覺化結果
plt.plot(np.degrees(angles), beam_pattern, label='Beam Pattern')
plt.axhline(y=half_max_value, color='r', linestyle='--', label='Half Maximum')
plt.axvline(x=np.degrees(theta_fwhm[0]), color='g', linestyle='--', label='FWHM Start')
plt.axvline(x=np.degrees(theta_fwhm[-1]), color='g', linestyle='--', label='FWHM End')
plt.xlabel('Angle (degrees)')
plt.ylabel('Normalized Gain')
plt.title('Beam Pattern and FWHM for 3-Microphone Array')
plt.legend()
plt.grid(True)
plt.show()
