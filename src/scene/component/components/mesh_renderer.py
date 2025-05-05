import numpy as np
from pyrr import Matrix44
from pywavefront import Wavefront


class MeshRenderer:
    def __init__(self, ctx, obj_path: str):
        self.ctx = ctx
        self.scene = Wavefront(obj_path, collect_faces=True)
        self.vertices, self.vertex_indices = self._prepare_vertex_data()
        self.vbo = self.ctx.buffer(self.vertices.tobytes())
        self.program = self._create_shader_program()
        self.vao = self.ctx.vertex_array(self.program, [(self.vbo, '3f 3f', 'in_vert', 'in_normal')])
        self.model_matrix = Matrix44.identity()

    def _prepare_vertex_data(self):
        vertex_list = self.scene.vertices
        normals_accum = np.zeros((len(vertex_list), 3), dtype='f4')
        vertex_indices = []

        for _, mesh in self.scene.meshes.items():
            for face in mesh.faces:
                v1 = np.array(vertex_list[face[0]], dtype='f4')
                v2 = np.array(vertex_list[face[1]], dtype='f4')
                v3 = np.array(vertex_list[face[2]], dtype='f4')

                edge1 = v2 - v1
                edge2 = v3 - v1
                normal = np.cross(edge1, edge2) # changed
                norm_len = np.linalg.norm(normal)
                if norm_len == 0:
                    continue
                normal /= norm_len
                normals_accum[face] += normal
                vertex_indices.extend(face)

        normals = []
        for n in normals_accum:
            norm_len = np.linalg.norm(n)
            normals.append(n / norm_len if norm_len != 0 else np.array([0.0, 0.0, 1.0], dtype='f4'))

        vertices = []
        for vi in vertex_indices:
            vertices.extend(vertex_list[vi])
            vertices.extend(normals[vi])

        return np.array(vertices, dtype='f4'), vertex_indices

    def _create_shader_program(self):
        return self.ctx.program(
            vertex_shader='''
                #version 330
                uniform mat4 mvp;
                uniform mat4 model;
                in vec3 in_vert;
                in vec3 in_normal;
                out vec3 frag_normal;
                void main() {
                    frag_normal = mat3(transpose(inverse(model))) * in_normal;
                    gl_Position = mvp * vec4(in_vert, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330
                in vec3 frag_normal;
                uniform vec3 light_dir;
                out vec4 f_color;
                void main() {
                    vec3 normal = normalize(frag_normal);
                    float brightness = max(dot(normal, normalize(light_dir)), 0.0);
                    f_color = vec4(vec3(0.4, 0.6, 0.9) * brightness, 1.0);
                }
            '''
        )

    def set_model_matrix(self, matrix: Matrix44):
        self.model_matrix = matrix

    def render(self, view_matrix: Matrix44, projection_matrix: Matrix44, light_dir=(1.0, 1.0, 1.0)):
        mvp = projection_matrix * view_matrix * self.model_matrix
        self.program['mvp'].write(mvp.astype('f4').tobytes())
        self.program['model'].write(self.model_matrix.astype('f4').tobytes())
        self.program['light_dir'].value = light_dir
        self.vao.render()
