import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def main():
    # 1. Load Data
    try:
        df = pd.read_csv('cones.csv')
    except FileNotFoundError:
        print("Error: cones.csv not found. Please ensure it is in the same directory.")
        return

    # 2. Estimate Track Center
    center_x = df['x'].mean()
    center_y = df['y'].mean()

    # 3. Separate Cones
    blue_cones = df[df['color'] == 'blue'][['x', 'y']].values
    yellow_cones = df[df['color'] == 'yellow'][['x', 'y']].values

    # 4. Sort Angularly
    def get_sorted_cones(cones, cx, cy):
        angles = np.arctan2(cones[:, 1] - cy, cones[:, 0] - cx)
        sorted_idx = np.argsort(angles)
        return cones[sorted_idx], angles[sorted_idx]

    blue_sorted, blue_angles = get_sorted_cones(blue_cones, center_x, center_y)
    yellow_sorted, yellow_angles = get_sorted_cones(yellow_cones, center_x, center_y)

    # 5. Interpolate to corresponding pairs
    num_points = 200
    common_angles = np.linspace(-np.pi, np.pi, num_points)

    def interpolate_boundary(angles, coords, target_angles):
        # Pad to handle periodic boundary conditions for smooth interpolation
        padded_angles = np.concatenate(([angles[-1] - 2*np.pi], angles, [angles[0] + 2*np.pi]))
        padded_x = np.concatenate(([coords[-1, 0]], coords[:, 0], [coords[0, 0]]))
        padded_y = np.concatenate(([coords[-1, 1]], coords[:, 1], [coords[0, 1]]))
        
        interp_x = np.interp(target_angles, padded_angles, padded_x)
        interp_y = np.interp(target_angles, padded_angles, padded_y)
        return np.column_stack([interp_x, interp_y])

    blue_resampled = interpolate_boundary(blue_angles, blue_sorted, common_angles)
    yellow_resampled = interpolate_boundary(yellow_angles, yellow_sorted, common_angles)

    # 6. Compute Centerline
    centerline = (blue_resampled + yellow_resampled) / 2

    # Close the loop
    centerline = np.vstack([centerline, centerline[0]])

    # 7. Visualization and Animation
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.set_facecolor('#f0f0f0')

    # Plot cones
    ax.scatter(blue_cones[:, 0], blue_cones[:, 1], c='blue', s=50, label='Blue Cones', edgecolor='white')
    ax.scatter(yellow_cones[:, 0], yellow_cones[:, 1], c='gold', s=50, label='Yellow Cones', edgecolor='black')

    # Plot Centerline (static part)
    ax.plot(centerline[:, 0], centerline[:, 1], 'r--', alpha=0.5, label='Centerline')

    point, = ax.plot([], [], 'ro', markersize=12, markeredgecolor='black', label='Vehicle')

    ax.legend()
    ax.set_title("Race Track Reconstruction & Trajectory")
    
    def init():
        point.set_data([], [])
        return point,

    def update(frame):
        idx = frame % len(centerline)
        point.set_data([centerline[idx, 0]], [centerline[idx, 1]])
        return point,

    ani = FuncAnimation(fig, update, frames=len(centerline), init_func=init, blit=True, interval=20)
    
    output_file = 'track_reconstruction.mp4'
    print(f"Saving animation to {output_file}...")
    
    try:
        # Requires ffmpeg installed on system and in PATH
        ani.save(output_file, writer='ffmpeg', fps=30)
        print("Success! Animation saved.")
    except Exception as e:
        print(f"Error saving animation: {e}")
        print("Ensure ffmpeg is installed. Alternatively, run the script to see the plot (if interactive mode is on).")
        # Fallback to showing the plot if save fails
        plt.show()

if __name__ == "__main__":
    main()