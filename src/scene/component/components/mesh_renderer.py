import sys
import os
BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '../../../')))    # Fix the import path
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "..", ".."))
DEFAULT_MODEL_PATH = os.path.join(PROJECT_ROOT, "assets", "models", "banana duck.obj")

import threading
import numpy as np
from pywavefront import Wavefront
from scene.component.component import Component
from core.component_registry import register_component


@register_component
class MeshRenderer(Component):
    def __init__(self, ctx, obj_path=DEFAULT_MODEL_PATH, name="MeshRenderer"):
        super().__init__(name=name)
        self.enabled = True

        self.ctx = ctx
        self.scene = Wavefront(obj_path, collect_faces=True)
        self.vertices, self.vertex_indices = self._prepare_vertex_data()
        self.vbo = self.ctx.buffer(self.vertices.tobytes())
        self.program = self._create_shader_program()
        self.vao = self.ctx.vertex_array(self.program, [(self.vbo, '3f 3f', 'in_vert', 'in_normal')])
        self.transform = np.identity(4)
        self.lock = threading.Lock()


    def subscribe(self, event_emitter):
        with self.lock:
            # On spawn, enable the mesh renderer
            event_emitter.on("onSpawn", self.enable)
            # On destroy, disable the mesh renderer
            event_emitter.on("onDestroy", self.disable)


    def enable(self):
        with self.lock:
            if self.enabled:
                raise RuntimeError("Mesh Renderer is already enabled.")
            self.enabled = True

    def disable(self):
        with self.lock:
            if not self.enabled:
                raise RuntimeError("Collider is already disabled.")
            self.enabled = False

    def set_transform(self, transform):
        # Ensure transform is a 4x4 matrix
        if transform.shape != (4, 4):
            raise ValueError("Transform must be a 4x4 matrix.")

        with self.lock:
            if self.get_parent():
                self.transform = np.dot(self.get_parent().transform, transform)
            else:
                self.transform = transform

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

    def render(self, view_matrix, projection_matrix, light_dir=(1.0, 1.0, 1.0)):
        with self.lock:
            if not self.enabled:
                return
            mvp = np.dot( np.dot(projection_matrix, view_matrix), self.transform )
            self.program['mvp'].write(mvp.T.astype('f4').tobytes())
            self.program['model'].write(self.transform.astype('f4').tobytes())
            self.program['light_dir'].value = light_dir
            self.vao.render()

    def to_dict(self):
        with self.lock:
            base = super().to_dict()
            # Update base
            return base

    @classmethod
    def from_dict(self, data, scene_manager):
        pass