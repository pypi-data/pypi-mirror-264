import numpy as np
import torch

def load_icosahedron(path):
    with open(path, "r") as file:
        lines = file.readlines()

    # Parse the vertices
    points_start = lines.index("POINTS 42 float\n") + 1
    points_end = points_start + 42
    vertices = []
    for line in lines[points_start:points_end]:
        coords = [float(coord) for coord in line.strip().split()]
        vertices.append(coords)

    # Parse the faces
    polygons_start = lines.index("POLYGONS 80 320\n") + 1
    polygons_end = polygons_start + 80
    faces = []
    for line in lines[polygons_start:polygons_end]:
        face_indices = [int(index) for index in line.strip().split()[1:]]
        faces.append(face_indices)

    # Extract edges from faces
    edges = set()
    for face_indices in faces:
        for i in range(len(face_indices)):
            edge = tuple(sorted([face_indices[i], face_indices[(i+1)%len(face_indices)]]))
            edges.add(edge)

    edges = list(edges)

    # Convert to torch tensors
    vertices = torch.tensor(vertices, dtype=torch.float32)
    edges = torch.tensor(edges, dtype=torch.int64)
    faces = torch.tensor(faces, dtype=torch.int64)

    return vertices, faces, edges
