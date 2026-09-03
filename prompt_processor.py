"""
معالج الأوامر النصية للتصميم 3D
يعمل محلياً بدون API Key باستخدام regex وتحليل النصوص
"""
import re
import json

class PromptProcessor:
    """معالج ذكي للأوامر النصية"""

    def __init__(self):
        self.commands = {
            'scale': ['كبر', 'صغر', 'حجم', 'scale', 'resize', 'size', 'dimension'],
            'rotate': ['دور', 'لف', 'rotate', 'turn', 'spin'],
            'translate': ['حرك', 'نقل', 'move', 'translate', 'shift'],
            'extrude': ['بعد', 'اكسترود', 'extrude', 'height', 'depth', 'thickness'],
            'color': ['لون', 'صبغ', 'color', 'paint', 'tint'],
            'mirror': ['عكس', 'mirror', 'flip'],
            'duplicate': ['كرر', 'نسخ', 'duplicate', 'copy', 'clone'],
            'delete': ['حذف', 'امسح', 'delete', 'remove'],
            'smooth': ['نعم', 'smooth', 'refine', 'polish'],
            'chamfer': ['شطف', 'chamfer', 'bevel'],
            'fillet': ['دائر', 'fillet', 'round'],
            'hole': ['ثقب', 'hole', 'drill', 'pierce'],
            'pattern': ['تكرار', 'pattern', 'array', 'grid']
        }

        self.units = {
            'mm': 1.0,
            'cm': 10.0,
            'm': 1000.0,
            'inch': 25.4,
            'ft': 304.8
        }

    def parse_command(self, text):
        """تحليل الأمر النصي واستخراج العمليات"""
        text = text.lower()
        operations = []

        # استخراج الأرقام مع الوحدات
        numbers = self._extract_numbers(text)

        # تحديد نوع العملية
        for cmd_type, keywords in self.commands.items():
            for keyword in keywords:
                if keyword in text:
                    op = {
                        'type': cmd_type,
                        'value': numbers[0] if numbers else 1.0,
                        'axis': self._detect_axis(text),
                        'unit': self._detect_unit(text),
                        'original': text
                    }
                    operations.append(op)
                    break

        return operations

    def _extract_numbers(self, text):
        """استخراج الأرقام من النص"""
        # يدعم الأرقام العربية والإنجليزية
        arabic_nums = {'٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
                       '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'}
        for ar, en in arabic_nums.items():
            text = text.replace(ar, en)

        numbers = re.findall(r'\d+\.?\d*', text)
        return [float(n) for n in numbers]

    def _detect_axis(self, text):
        """اكتشاف المحور"""
        axes = {'x': ['x', 'س'], 'y': ['y', 'ص'], 'z': ['z', 'ع']}
        for axis, keywords in axes.items():
            for kw in keywords:
                if kw in text:
                    return axis
        return 'all'

    def _detect_unit(self, text):
        """اكتشاف الوحدة"""
        for unit in self.units.keys():
            if unit in text:
                return unit
        return 'mm'

    def apply_to_mesh(self, mesh, operations):
        """تطبيق العمليات على الـ mesh"""
        import numpy as np
        import trimesh

        for op in operations:
            cmd_type = op['type']
            value = op['value']
            axis = op['axis']
            unit = op['unit']
            factor = self.units.get(unit, 1.0)

            if cmd_type == 'scale':
                scale_factors = [1.0, 1.0, 1.0]
                idx = {'x': 0, 'y': 1, 'z': 2}.get(axis, None)
                if idx is not None:
                    scale_factors[idx] = value
                else:
                    scale_factors = [value] * 3
                mesh.apply_scale(scale_factors)

            elif cmd_type == 'rotate':
                angle = np.radians(value)
                idx = {'x': 0, 'y': 1, 'z': 2}.get(axis, 2)
                mesh.apply_transform(trimesh.transformations.rotation_matrix(
                    angle, [1 if i == idx else 0 for i in range(3)]
                ))

            elif cmd_type == 'translate':
                translation = [0.0, 0.0, 0.0]
                idx = {'x': 0, 'y': 1, 'z': 2}.get(axis, None)
                if idx is not None:
                    translation[idx] = value * factor
                mesh.apply_translation(translation)

            elif cmd_type == 'extrude':
                # تعديل الارتفاع
                bounds = mesh.bounds
                current_height = bounds[1][2] - bounds[0][2]
                if current_height > 0:
                    scale_z = (value * factor) / current_height
                    mesh.apply_scale([1.0, 1.0, scale_z])

        return mesh

    def generate_from_description(self, text):
        """توليد mesh أساسي من وصف نصي"""
        import trimesh
        import numpy as np

        text = text.lower()

        # كلمات مفتاحية للأشكال الأساسية
        if any(w in text for w in ['مكعب', 'cube', 'صندوق', 'box']):
            size = self._extract_numbers(text)[0] if self._extract_numbers(text) else 10
            return trimesh.creation.box(extents=[size, size, size])

        elif any(w in text for w in ['كرة', 'sphere', 'دائرة', 'ball']):
            radius = self._extract_numbers(text)[0] if self._extract_numbers(text) else 5
            return trimesh.creation.icosphere(radius=radius)

        elif any(w in text for w in ['أسطوانة', 'cylinder', 'عمود']):
            nums = self._extract_numbers(text)
            radius = nums[0] if len(nums) > 0 else 5
            height = nums[1] if len(nums) > 1 else 20
            return trimesh.creation.cylinder(radius=radius, height=height)

        elif any(w in text for w in ['مخروط', 'cone']):
            nums = self._extract_numbers(text)
            radius = nums[0] if len(nums) > 0 else 5
            height = nums[1] if len(nums) > 1 else 20
            return trimesh.creation.cone(radius=radius, height=height)

        elif any(w in text for w in ['طارة', 'torus', 'حلقة', 'ring']):
            nums = self._extract_numbers(text)
            major = nums[0] if len(nums) > 0 else 10
            minor = nums[1] if len(nums) > 1 else 2
            return trimesh.creation.torus(major_radius=major, minor_radius=minor)

        elif any(w in text for w in ['هرم', 'pyramid']):
            return trimesh.creation.cylinder(radius=5, height=10, sections=4)

        else:
            # افتراضياً: مكعب
            return trimesh.creation.box(extents=[10, 10, 10])
