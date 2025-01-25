import os
import numpy as np
import plotly.graph_objects as go

# Folder path to the .obj files
folder_path = '/Users/vspendyala/Downloads/BP51200_FMA3_2_1_inference_partof_FMA7161_Cardiovascular_system'

def load_obj(filename):
    vertices = []
    faces = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Lines starting with 'v' contain vertex data
                parts = line.split()
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('f '):  # Lines starting with 'f' contain face data
                parts = line.split()[1:]
                # Parse vertex indices and subtract 1 (OBJ indices start at 1, Python uses 0-based indexing)
                face = [int(idx.split('/')[0]) - 1 for idx in parts]
                faces.append(face)
    return np.array(vertices), faces

def plot_obj_files(folder_path):
    fig = go.Figure()

    # Iterate through all .obj files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.obj'):
            file_path = os.path.join(folder_path, filename)
            vertices, faces = load_obj(file_path)

            # Extract triangular faces for Plotly (ignores non-triangular faces)
            i, j, k = [], [], []
            for face in faces:
                if len(face) == 3:  # Ensure it's a triangular face
                    i.append(face[0])
                    j.append(face[1])
                    k.append(face[2])
                elif len(face) > 3:  # Handle polygons with >3 vertices (optional)
                    for n in range(1, len(face) - 1):
                        i.append(face[0])
                        j.append(face[n])
                        k.append(face[n + 1])

            # Add a mesh plot for the object
            fig.add_trace(go.Mesh3d(
                x=vertices[:, 0],
                y=vertices[:, 1],
                z=vertices[:, 2],
                i=i,  # Vertex 1 indices of triangles
                j=j,  # Vertex 2 indices of triangles
                k=k,  # Vertex 3 indices of triangles
                color='red',  # Color of the object
                opacity=0.5,  # Transparency
                name=filename  # Set the legend entry
            ))

    # Set labels, title, and layout styles
    fig.update_layout(
        scene=dict(
            xaxis_title='X Axis',
            yaxis_title='Y Axis',
            zaxis_title='Z Axis',
            xaxis=dict(
                backgroundcolor="rgb(255, 255, 255)",
                gridcolor="rgb(200, 200, 200)",
                showgrid=True,
                zeroline=True,
            ),
            yaxis=dict(
                backgroundcolor="rgb(255, 255, 255)",
                gridcolor="rgb(200, 200, 200)",
                showgrid=True,
                zeroline=True,
            ),
            zaxis=dict(
                backgroundcolor="rgb(255, 255, 255)",
                gridcolor="rgb(200, 200, 200)",
                showgrid=True,
                zeroline=True,
            ),
            aspectmode='data',  # Maintain aspect ratio based on the data
        ),
        title='3D Visualization of OBJ Files',
        paper_bgcolor='rgb(240, 240, 240)',
        plot_bgcolor='rgb(255, 255, 255)',
        font=dict(
            size=18,
            color='rgb(50, 50, 50)',
            family='Times New Roman'
        ),
        showlegend=True,
        margin=dict(l=0, r=0, b=0, t=40),
        height=900,
        width=1600,
        legend=dict(
            x=1.02,
            y=0.5,
            traceorder='normal',
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='Black',
            borderwidth=2,
            font=dict(
                size=10,
                color='rgb(0, 0, 0)',
            ),
            orientation='v',
        ),
    )

    # Show the figure
    fig.show()

# Call the function to plot the .obj files
plot_obj_files(folder_path)
