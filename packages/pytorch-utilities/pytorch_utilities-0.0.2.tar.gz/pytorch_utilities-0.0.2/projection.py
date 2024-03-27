# This is the code for HW2 of Machine Vision (2023-2024 Spring) course at University of Tehran,
# It is implemented by `Arash Hajian nezhad`, with student number `810102115`.

import numpy as np
import matplotlib.pyplot as plt


# Functions for rotation and projection
def rotate_vertices(vertices, axis, angle_degrees):
    angle_radians = np.radians(angle_degrees)
    cos_angle, sin_angle = np.cos(angle_radians), np.sin(angle_radians)
    
    if axis == 'x':
        rotation_matrix = np.array([[1, 0, 0], [0, cos_angle, -sin_angle], [0, sin_angle, cos_angle]])
    elif axis == 'y':
        rotation_matrix = np.array([[cos_angle, 0, sin_angle], [0, 1, 0], [-sin_angle, 0, cos_angle]])
    elif axis == 'z':
        rotation_matrix = np.array([[cos_angle, -sin_angle, 0], [sin_angle, cos_angle, 0], [0, 0, 1]])
    else:
        raise ValueError('Invalid rotation axis.')

    return np.dot(vertices, rotation_matrix.T)

def perspective_projection(vertices, focal_length=5):
    projected_vertices = vertices / (focal_length - vertices[:, 2].reshape(-1, 1))
    return projected_vertices[:, :2]

def parallel_projection(vertices):
    return vertices[:, :2]


# Modify the plot_cuboid function to accept an Axes object
def plot_cuboid(ax, vertices, edges, title):
    if vertices.shape[1] == 3:  # 3D plot for the original cuboid
        ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2])
        for idx, (start, end) in enumerate(edges):
            if idx < 12:
                color = 'b'
            elif idx < 14:
                color = 'r'
            else:
                color = "g"
            ax.plot3D(*zip(*vertices[[start, end],]), color=color)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
    else:  # 2D plot for the projected cuboid
        ax.scatter(vertices[:, 0], vertices[:, 1])
        for idx, (start, end) in enumerate(edges):
            if idx < 12:
                color = "b"
            elif idx < 14:
                color = "r"
            else:
                color = "g"
            ax.plot(*zip(*vertices[[start, end],]), color=color)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
    ax.set_title(title)
    ax.grid(True)
    ax.axis('equal')


def plot_projection(rotation_axis, rotation_angle, projection_type):
    # Original cuboid vertices
    vertices = np.array([[0, 0, 0], [2, 0, 0], [2, 3, 0], [0, 3, 0],
                        [0, 0, 4], [2, 0, 4], [2, 3, 4], [0, 3, 4]])

    # Edges connecting vertices (for plotting)
    edges = [(0, 1), (1, 2), (2, 3), (3, 0),  # Bottom face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Top face
            (0, 4), (1, 5), (2, 6), (3, 7),  # Side edges
            (0, 2), (1, 3), (4, 6), (5, 7)]  # Diagonals for better visualization

    # Create a new figure
    fig = plt.figure(figsize=(12, 4), dpi=200)

    # Create 3D subplot for the original cuboid
    ax1 = fig.add_subplot(121, projection='3d')
    annotation_text = 'Original Cuboid'
    plot_cuboid(ax1, vertices, edges, annotation_text)

    # Apply the rotation and plot the result
    rotated_vertices = rotate_vertices(vertices, rotation_axis, rotation_angle)
    if projection_type == 'parallel':
        projected_vertices = parallel_projection(rotated_vertices)
    elif projection_type == 'perspective':
        projected_vertices = perspective_projection(rotated_vertices)
    
    # Create 2D subplot for the projection after rotation
    ax2 = fig.add_subplot(122)
    annotation_text = f"{projection_type.capitalize()} Projection\nAxis: {rotation_axis.upper()}, Angle: {rotation_angle}°"
    plot_cuboid(ax2, projected_vertices, edges, annotation_text)

    # Show the plots
    plt.tight_layout()
    plt.show()


# Input from the user
rotation_axis = input("Enter rotation axis (x, y, z): ").strip().lower()
rotation_angle = float(input("Enter rotation angle (in degrees): "))
projection_type = input("Enter projection type (parallel or perspective): ").strip().lower()

plot_projection(rotation_axis, rotation_angle, projection_type)