Problem Statement:

You are given a CSV file (cones.csv) containing unordered 2D positions of blue and yellow cones that represent the left and right boundaries of a closed race track. Using only NumPy, pandas, and Matplotlib, reconstruct the track centerline by estimating the overall track center, sorting the cones angularly around this center, computing midpoints between corresponding blue–yellow cone pairs, and forming a continuous closed-loop trajectory with a consistent direction of travel. Visualize the cones and the generated centerline, animate a particle moving along the trajectory, and export the animation as an MP4 file to validate the result.

Methodology:

Data Loading: The cone positions and colors were loaded from cones.csv.

Center Estimation: The centroid of all cones was calculated to serve as the reference point for angular sorting.

Angular Sorting: Both blue (left) and yellow (right) cones were sorted by their angle relative to the center .

Resampling & Pairing: To handle potential disparities in cone counts and ensuring smooth alignment, both boundaries were resampled to a common set of 200 angular steps using linear interpolation.

Centerline Calculation: The trajectory was computed as the midpoint between the resampled blue and yellow boundaries.

Visualization: The result is visualized with the cones and a particle animating along the path.

Steps:

    1. Load Data

    2. Estimate Track Center
    
    3. Separate Cones
    
    4. Sort Angularly
    
    5. Interpolate to corresponding pairs
    
    6. Compute Centerline
    
    7. Visualization and Animation

