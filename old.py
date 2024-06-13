import matplotlib.pyplot as plt
import numpy as np

# Sensor parameters
max_distance = 140  # maximum reach in cm
fov = 60  # total field of view in degrees (±30 degrees from the center)

# Calculate the angles for the field of view
angles = np.linspace(-fov / 2, fov / 2, 100)
angles_rad = np.deg2rad(angles)

# Calculate the Y coordinates for the sensor range at each angle
x = max_distance * np.sin(angles_rad)
y = max_distance * np.cos(angles_rad)

# Plotting the sensor range
plt.figure()
plt.plot([-fov / 2, fov / 2], [0, 0], 'k--')  # X axis
plt.plot([0, 0], [0, max_distance], 'k--')  # Y axis

# Plot the cone boundaries
plt.plot(angles, y, 'b')  # Boundary of the sensor range

# Fill the detection area
plt.fill_between(angles, 0, y, color='lightblue', alpha=0.5)

plt.xlabel('Angle (degrees)')
plt.ylabel('Distance (cm)')
plt.title('Sensor Range Visualization')
plt.grid(True)
plt.ylim(0, max_distance)
plt.xlim(-fov / 2, fov / 2)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.show()
