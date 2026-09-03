"""
مولد النماذج ثلاثية الأبعاد من الصور
يحول الصورة 2D إلى mesh 3D باستخدام extrusion
"""
import numpy as np
import trimesh
from PIL import Image
import cv2

class ImageTo3D:
    """تحويل الصور إلى نماذج 3D"""

    def __init__(self):
        self.default_height = 5.0
        self.smooth_iterations = 1

    def image_to_mesh(self, image_path, extrude_height=10.0, resolution=100, 
                      invert=False, smooth=True, colorize=True):
        """
        تحويل صورة إلى mesh 3D

        Parameters:
        -----------
        image_path : str
            مسار الصورة
        extrude_height : float
            ارتفاع ال extrusion
        resolution : int
            دقة النموذج (عدد النقاط)
        invert : bool
            عكس الألوان (للنقوش الغائرة)
        smooth : bool
            تنعيم الحواف
        colorize : bool
            تلوين النموذج حسب الصورة
        """
        # قراءة الصورة
        img = Image.open(image_path).convert('L')  # تحويل للرمادي

        # تغيير الحجم للدقة المطلوبة
        img = img.resize((resolution, resolution), Image.Resampling.LANCZOS)

        # تحويل إلى مصفوفة numpy
        img_array = np.array(img)

        if invert:
            img_array = 255 - img_array

        # تطبيع القيم (0 إلى 1)
        height_map = img_array / 255.0

        # تطبيق extrude height
        height_map = height_map * extrude_height

        # إنشاء mesh من height map
        mesh = self._heightmap_to_mesh(height_map, resolution)

        # تنعيم إذا طُلب
        if smooth:
            mesh = mesh.smoothed()

        # تلوين
        if colorize:
            img_color = Image.open(image_path).convert('RGB')
            img_color = img_color.resize((resolution, resolution))
            colors = np.array(img_color).reshape(-1, 3) / 255.0
            mesh.visual.vertex_colors = colors[:len(mesh.vertices)]

        return mesh

    def _heightmap_to_mesh(self, height_map, resolution):
        """تحويل height map إلى trimesh"""
        # إنشاء شبكة نقاط
        x = np.linspace(-50, 50, resolution)
        y = np.linspace(-50, 50, resolution)
        xx, yy = np.meshgrid(x, y)

        # النقاط
        vertices = np.column_stack([
            xx.ravel(),
            yy.ravel(),
            height_map.ravel()
        ])

        # إنشاء وجوه المثلثات
        faces = []
        for i in range(resolution - 1):
            for j in range(resolution - 1):
                # رباعي مقسم لمثلثين
                v0 = i * resolution + j
                v1 = i * resolution + (j + 1)
                v2 = (i + 1) * resolution + j
                v3 = (i + 1) * resolution + (j + 1)

                faces.append([v0, v1, v2])
                faces.append([v1, v3, v2])

        faces = np.array(faces)

        # إنشاء mesh
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

        # إصلاح الشكل
        mesh.process()

        return mesh

    def create_parametric_shape(self, shape_type, params):
        """إنشاء شكل parametric"""
        if shape_type == 'box':
            w, h, d = params.get('width', 10), params.get('height', 10), params.get('depth', 10)
            return trimesh.creation.box(extents=[w, h, d])

        elif shape_type == 'sphere':
            r = params.get('radius', 5)
            return trimesh.creation.icosphere(radius=r, subdivisions=3)

        elif shape_type == 'cylinder':
            r, h = params.get('radius', 5), params.get('height', 20)
            return trimesh.creation.cylinder(radius=r, height=h)

        elif shape_type == 'cone':
            r, h = params.get('radius', 5), params.get('height', 20)
            return trimesh.creation.cone(radius=r, height=h)

        elif shape_type == 'torus':
            R, r = params.get('major', 10), params.get('minor', 2)
            return trimesh.creation.torus(major_radius=R, minor_radius=r)

        elif shape_type == 'capsule':
            r, h = params.get('radius', 3), params.get('height', 10)
            return trimesh.creation.capsule(radius=r, height=h)

        return trimesh.creation.box(extents=[10, 10, 10])

    def apply_modifiers(self, mesh, modifiers):
        """تطبيق المعدلات على الـ mesh"""
        for mod in modifiers:
            mod_type = mod.get('type')

            if mod_type == 'subdivide':
                iterations = mod.get('iterations', 1)
                mesh = mesh.subdivide().subdivide() if iterations > 1 else mesh.subdivide()

            elif mod_type == 'smooth':
                mesh = mesh.smoothed()

            elif mod_type == 'decimate':
                factor = mod.get('factor', 0.5)
                target = int(len(mesh.faces) * factor)
                mesh = mesh.simplify_quadric_decimation(target)

        return mesh
