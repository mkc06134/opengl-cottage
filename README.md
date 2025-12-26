# OpenGL Textured Cottage Scene

A 3D OpenGL scene rendered using Python, featuring a textured cottage interior composed of multiple mesh objects, bitmap textures, and custom GLSL shaders. The scene supports real-time camera movement and demonstrates mesh loading, texture mapping, and shader-based rendering.

## Features
- Textured 3D environment composed of multiple PLY mesh objects
- Bitmap (BMP) texture mapping for walls, floor, furniture, and objects
- Custom vertex and fragment shaders
- Real-time camera movement using keyboard input
- Depth testing and perspective projection
- Modular asset organization (meshes, textures, shaders)

## Controls
- **Up Arrow**: Move camera forward
- **Down Arrow**: Move camera backward
- **Left Arrow**: Rotate camera left
- **Right Arrow**: Rotate camera right

## Project Structure
opengl-cottage-scene/
├── src/
│ └── a4.py
├── shaders/
│ ├── shader.vert
│ └── shader.frag
├── assets/
│ ├── meshes/
│ │ └── *.ply
│ └── textures/
│ └── *.bmp
├── screenshots/
│ ├── screenshot1.png
│ ├── screenshot2.png
│ └── screenshot3.png
├── requirements.txt
└── README.md


## Setup

### Requirements
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### Run
From the project root directory:
```bash
python src/a4.py
```

## Screenshots
Rendered views of the cottage interior can be found in the screenshots/ folder.

## Notes
All mesh and texture files must remain in their respective directories for the program to run correctly.
The project focuses on graphics programming concepts including transformation matrices, texture mapping, and shader pipelines.