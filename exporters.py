"""
مكتبة تصدير الملفات: STL, PDF, STEP
"""
import trimesh
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import io
import os

class ModelExporter:
    """تصدير النماذج 3D إلى صيغ مختلفة"""

    def export_stl(self, mesh, filepath):
        """تصدير STL"""
        mesh.export(filepath)
        return filepath

    def export_obj(self, mesh, filepath):
        """تصدير OBJ مع MTL"""
        mesh.export(filepath)
        return filepath

    def export_ply(self, mesh, filepath):
        """تصدير PLY"""
        mesh.export(filepath)
        return filepath

    def export_step(self, mesh, filepath):
        """
        تصدير STEP
        ملاحظة: يتطلب cadquery أو build123d
        """
        try:
            import cadquery as cq
            from cadquery import exporters

            # تحويل trimesh إلى cadquery Workplane
            vertices = mesh.vertices
            faces = mesh.faces

            # إنشاء Workplane من النقاط
            wp = cq.Workplane("XY")

            # طريقة بديلة: حفظ STL أولاً ثم تحويل
            temp_stl = filepath.replace('.step', '_temp.stl')
            mesh.export(temp_stl)

            # قراءة STL وتحويله
            shape = cq.importers.importShape(temp_stl)
            shape.val().exportStep(filepath)

            # حذف الملف المؤقت
            if os.path.exists(temp_stl):
                os.remove(temp_stl)

            return filepath
        except Exception as e:
            # في حالة الفشل، نصدر STL كبديل
            stl_path = filepath.replace('.step', '.stl')
            mesh.export(stl_path)
            return stl_path

    def export_pdf(self, mesh, filepath, views=None):
        """
        تصدير PDF مع رؤى متعددة
        views: list of tuples (axis, angle, name)
        """
        if views is None:
            views = [
                ('front', 0, 'الواجهة الأمامية'),
                ('top', 0, 'المنظور العلوي'),
                ('iso', 0, 'المنظور ثلاثي الأبعاد'),
                ('side', 0, 'المنظور الجانبي')
            ]

        # إنشاء صور للمنظورات
        images = []
        for view_name, angle, label in views:
            img = self._render_view(mesh, view_name, label)
            images.append((img, label))

        # إنشاء PDF
        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4

        # عنوان
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 50, "AI 3D Designer - Technical Drawing")

        # معلومات النموذج
        c.setFont("Helvetica", 12)
        info_y = height - 80
        c.drawString(50, info_y, f"Vertices: {len(mesh.vertices)}")
        c.drawString(50, info_y - 20, f"Faces: {len(mesh.faces)}")
        bounds = mesh.bounds
        c.drawString(50, info_y - 40, f"Dimensions: {bounds[1] - bounds[0]}")

        # وضع الصور
        img_width = (width - 100) / 2
        img_height = img_width * 0.75
        x_positions = [50, width/2 + 25]
        y_positions = [height - 350, height - 350 - img_height - 50]

        for idx, (img, label) in enumerate(images[:4]):
            x = x_positions[idx % 2]
            y = y_positions[idx // 2]

            # حفظ الصورة مؤقتاً
            temp_img = f"/tmp/view_{idx}.png"
            img.save(temp_img)

            c.drawImage(temp_img, x, y, width=img_width, height=img_height)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(x, y - 15, label)

        c.save()

        # تنظيف
        for idx in range(4):
            temp = f"/tmp/view_{idx}.png"
            if os.path.exists(temp):
                os.remove(temp)

        return filepath

    def _render_view(self, mesh, view_name, label):
        """رسم منظور واحد"""
        # نسخة من الـ mesh
        view_mesh = mesh.copy()

        # تدوير حسب المنظور
        if view_name == 'top':
            view_mesh.apply_transform(trimesh.transformations.rotation_matrix(
                np.radians(-90), [1, 0, 0]))
        elif view_name == 'side':
            view_mesh.apply_transform(trimesh.transformations.rotation_matrix(
                np.radians(90), [0, 1, 0]))
        elif view_name == 'iso':
            view_mesh.apply_transform(trimesh.transformations.rotation_matrix(
                np.radians(45), [0, 1, 0]))
            view_mesh.apply_transform(trimesh.transformations.rotation_matrix(
                np.radians(30), [1, 0, 0]))

        # رسم بسيط باستخدام PIL
        img_size = 400
        img = Image.new('RGB', (img_size, img_size), 'white')
        draw = ImageDraw.Draw(img)

        # عرض wireframe بسيط
        vertices = view_mesh.vertices
        faces = view_mesh.faces

        # تسطيح (projection)
        # نستخدم إسقاط orthographic بسيط
        verts_2d = vertices[:, :2]  # نأخذ x,y فقط

        # تطبيع
        if len(verts_2d) > 0:
            min_vals = verts_2d.min(axis=0)
            max_vals = verts_2d.max(axis=0)
            ranges = max_vals - min_vals
            ranges[ranges == 0] = 1

            verts_2d = (verts_2d - min_vals) / ranges
            verts_2d = verts_2d * (img_size - 60) + 30

            # رسم الوجوه
            for face in faces[:500]:  # نحدد العدد للأداء
                pts = [tuple(verts_2d[v]) for v in face]
                # لون عشوائي خفيف
                color = (200, 200, 220)
                draw.polygon(pts, fill=color, outline=(100, 100, 120))

        # عنوان
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        except:
            font = ImageFont.load_default()

        draw.text((10, 10), label, fill=(50, 50, 80), font=font)

        return img

    def get_mesh_info(self, mesh):
        """معلومات عن الـ mesh"""
        bounds = mesh.bounds
        dimensions = bounds[1] - bounds[0]

        return {
            'vertices': len(mesh.vertices),
            'faces': len(mesh.faces),
            'edges': len(mesh.edges_unique) if hasattr(mesh, 'edges_unique') else 0,
            'volume': float(mesh.volume) if mesh.is_watertight else 0.0,
            'surface_area': float(mesh.area),
            'bounds': bounds.tolist(),
            'dimensions': dimensions.tolist(),
            'center_of_mass': mesh.center_mass.tolist() if hasattr(mesh, 'center_mass') else [0,0,0],
            'is_watertight': mesh.is_watertight,
            'is_winding_consistent': mesh.is_winding_consistent
        }
