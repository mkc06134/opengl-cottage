# Import libraries
import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from PIL import Image
from plyfile import PlyData
import glm
import time

# load bitmap image
# reads data from the bmp files at the points into the data pointer
def load_bitmap_image(image_path):
    image = Image.open(image_path).convert('RGBA').transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(image, dtype=np.uint8)
    return img_data, image.width, image.height

# load PLY file
# reads the mesh data from ply files
def read_ply_file(file_path):
    ply = PlyData.read(file_path)
    vertices = np.array([
        (
            v[0], v[1], v[2], 
            v[6], v[7]   
        ) for v in ply['vertex']
    ], dtype=np.float32)

    faces = np.concatenate(ply['face'].data['vertex_indices']).astype(np.uint32)
    return vertices, faces

# texture mesh class
class TexturedMesh:
    # constructor
    def __init__(self, ply_path, bmp_path):
        self.vertices, self.faces = read_ply_file(ply_path)
        self.texture_data, self.tex_width, self.tex_height = load_bitmap_image(bmp_path)
        self.setup()

    # sets up the mesh and texture files and object data
    def setup(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(12))

        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.faces.nbytes, self.faces, GL_STATIC_DRAW)

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.tex_width, self.tex_height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, self.texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        glBindVertexArray(0)

    # renders the object by enabling blending
    def draw(self, MVP, shader):
        glUseProgram(shader)
        MVP_loc = glGetUniformLocation(shader, "MVP")
        glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glUniform1i(glGetUniformLocation(shader, "tex"), 0)

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(self.faces), GL_UNSIGNED_INT, None)


# main function to intialize the window and create the objects
def main():
    glfw.init()
    window = glfw.create_window(1200, 800, "A4 - Cottage Camera", None, None)
    glfw.make_context_current(window)

    shader = compileProgram(
        compileShader(open('shaders/shader.vert').read(), GL_VERTEX_SHADER),
        compileShader(open('shaders/shader.frag').read(), GL_FRAGMENT_SHADER)
    )

    mesh_files = [
        ("assets/meshes/Walls.ply", "assets/textures/walls.bmp"),
        ("assets/meshes/WoodObjects.ply", "assets/textures/woodobjects.bmp"),
        ("assets/meshes/Table.ply", "assets/textures/table.bmp"),
        ("assets/meshes/WindowBG.ply", "assets/textures/windowbg.bmp"),
        ("assets/meshes/Patio.ply", "assets/textures/patio.bmp"),
        ("assets/meshes/Floor.ply", "assets/textures/floor.bmp"),
        ("assets/meshes/Bottles.ply", "assets/textures/bottles.bmp"),
        ("assets/meshes/DoorBG.ply", "assets/textures/doorbg.bmp"),
        ("assets/meshes/MetalObjects.ply", "assets/textures/metalobjects.bmp"),
        ("assets/meshes/Curtains.ply", "assets/textures/curtains.bmp")
    ]

    meshes = [TexturedMesh(*file_pair) for file_pair in mesh_files]

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    cameraPos = glm.vec3(0.5, 0.4, 0.5)
    cameraDir = glm.vec3(0, 0, -1)
    upVector = glm.vec3(0, 1, 0)
    key_rotation = 0.0

    while not glfw.window_should_close(window):
        glfw.poll_events()
        if glfw.get_key(window, glfw.KEY_UP):
            cameraPos += cameraDir * 0.05
        if glfw.get_key(window, glfw.KEY_DOWN):
            cameraPos -= cameraDir * 0.05
        if glfw.get_key(window, glfw.KEY_LEFT):
            key_rotation -= 3
        if glfw.get_key(window, glfw.KEY_RIGHT):
            key_rotation += 3

        cameraDir = glm.vec3(glm.cos(glm.radians(key_rotation)), 0, glm.sin(glm.radians(key_rotation)))
        projection = glm.perspective(glm.radians(45.0), 1200 / 800, 0.1, 100.0)
        view = glm.lookAt(cameraPos, cameraPos + cameraDir, upVector)
        MVP = projection * view

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for mesh in meshes:
            mesh.draw(MVP, shader)

        glfw.swap_buffers(window)
        time.sleep(1/30)

    glfw.terminate()

main()
