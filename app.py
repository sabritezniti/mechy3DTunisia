"""
╔═══════════════════════════════════════════════════════════════╗
║  AI 3D Designer - المصمم الذكي ثلاثي الأبعاد              ║
║  تحويل الصور إلى تصميمات 3D مع تحرير تفاعلي               ║
╚═══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import numpy as np
import trimesh
from PIL import Image
import json
import base64
import io
import os
import sys

# إضافة المكونات
sys.path.insert(0, os.path.dirname(__file__))
from components.translator import translate_text, get_supported_languages
from components.prompt_processor import PromptProcessor
from components.mesh_generator import ImageTo3D
from components.exporters import ModelExporter

# ═══════════════════════════════════════════════════════════════
# إعدادات الصفحة
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AI 3D Designer",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# CSS مخصص - ألوان زاهية ومتناسقة
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* الألوان الرئيسية */
    :root {
        --primary: #6366f1;
        --primary-light: #818cf8;
        --secondary: #f472b6;
        --accent: #22d3ee;
        --success: #34d399;
        --warning: #fbbf24;
        --danger: #f87171;
        --dark: #1e1b4b;
        --light: #f8fafc;
        --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }

    /* خلفية التطبيق */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    /* العناوين */
    h1 {
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        text-align: center;
        padding: 20px 0;
        font-size: 3rem !important;
    }

    h2 {
        color: var(--accent) !important;
        border-bottom: 2px solid var(--primary-light);
        padding-bottom: 10px;
    }

    h3 {
        color: var(--secondary) !important;
    }

    /* البطاقات */
    .stCard {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    /* الأزرار */
    .stButton > button {
        background: var(--gradient-1) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6) !important;
    }

    /* زر التصدير */
    .export-btn {
        background: var(--gradient-2) !important;
    }

    /* حقول الإدخال */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    /* الشريط الجانبي */
    .css-1d391kg {
        background: rgba(15, 12, 41, 0.95) !important;
    }

    /* المقاييس */
    .stSlider > div > div > div {
        background: var(--gradient-3) !important;
    }

    /* الجداول */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px;
    }

    /* تلميحات */
    .stAlert {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* شريط التقدم */
    .stProgress > div > div > div {
        background: var(--gradient-3) !important;
    }

    /* تنسيق خاص للـ 3D viewer */
    .viewer-container {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        border: 2px solid rgba(99, 102, 241, 0.3);
    }

    /* معلومات القطعة */
    .piece-info {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(244, 114, 182, 0.2));
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* تأثيرات حركية */
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.3); }
        50% { box-shadow: 0 0 40px rgba(99, 102, 241, 0.6); }
    }

    .glow-effect {
        animation: glow 3s ease-in-out infinite;
    }

    /* شريط اللغة */
    .lang-bar {
        display: flex;
        gap: 10px;
        padding: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# حالة الجلسة
# ═══════════════════════════════════════════════════════════════
if 'mesh' not in st.session_state:
    st.session_state.mesh = None
if 'mesh_history' not in st.session_state:
    st.session_state.mesh_history = []
if 'language' not in st.session_state:
    st.session_state.language = 'ar'
if 'selected_piece' not in st.session_state:
    st.session_state.selected_piece = None
if 'scene_objects' not in st.session_state:
    st.session_state.scene_objects = []

# ═══════════════════════════════════════════════════════════════
# الدوال المساعدة
# ═══════════════════════════════════════════════════════════════

def t(text):
    """ترجمة النص"""
    return translate_text(text, target_lang=st.session_state.language)

def get_threejs_html(mesh_data, color="#6366f1"):
    """
    إنشاء HTML viewer باستخدام Three.js
    """
    vertices = mesh_data['vertices'].tolist() if hasattr(mesh_data['vertices'], 'tolist') else mesh_data['vertices']
    faces = mesh_data['faces'].tolist() if hasattr(mesh_data['faces'], 'tolist') else mesh_data['faces']

    vertices_json = json.dumps(vertices)
    faces_json = json.dumps(faces)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin: 0; overflow: hidden; background: #0a0a1a; }}
            #canvas-container {{ width: 100%; height: 600px; }}
            .controls {{
                position: absolute;
                top: 10px;
                left: 10px;
                background: rgba(0,0,0,0.7);
                padding: 15px;
                border-radius: 10px;
                color: white;
                font-family: Arial;
                z-index: 100;
            }}
            .controls button {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                border: none;
                color: white;
                padding: 8px 16px;
                margin: 5px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
            }}
            .controls button:hover {{
                transform: scale(1.05);
            }}
            .info {{
                position: absolute;
                bottom: 10px;
                right: 10px;
                background: rgba(0,0,0,0.7);
                padding: 10px;
                border-radius: 8px;
                color: #22d3ee;
                font-family: monospace;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="controls">
            <div>🎮 التحكم</div>
            <button onclick="resetView()">🔄 إعادة ضبط</button>
            <button onclick="toggleWireframe()">🔲 Wireframe</button>
            <button onclick="toggleAutoRotate()">🔄 تدوير تلقائي</button>
            <div style="margin-top:10px; font-size:12px;">
                🖱️ يسار: تدوير | 🖱️ يمين: تحريك | ⚙️ عجلة: تقريب
            </div>
        </div>
        <div class="info" id="info">
            Vertices: {len(vertices)} | Faces: {len(faces)}
        </div>
        <div id="canvas-container"></div>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

        <script>
            let scene, camera, renderer, controls, mesh, wireframe;
            let autoRotate = false;

            function init() {{
                const container = document.getElementById('canvas-container');

                // المشهد
                scene = new THREE.Scene();
                scene.background = new THREE.Color(0x0a0a1a);
                scene.fog = new THREE.Fog(0x0a0a1a, 100, 500);

                // الكاميرا
                camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
                camera.position.set(80, 60, 80);

                // العارض
                renderer = new THREE.WebGLRenderer({{ antialias: true }});
                renderer.setSize(container.clientWidth, container.clientHeight);
                renderer.setPixelRatio(window.devicePixelRatio);
                renderer.shadowMap.enabled = true;
                renderer.shadowMap.type = THREE.PCFSoftShadowMap;
                container.appendChild(renderer.domElement);

                // التحكم
                controls = new THREE.OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;
                controls.dampingFactor = 0.05;
                controls.minDistance = 20;
                controls.maxDistance = 200;

                // الإضاءة
                const ambientLight = new THREE.AmbientLight(0x404040, 2);
                scene.add(ambientLight);

                const dirLight = new THREE.DirectionalLight(0xffffff, 1.5);
                dirLight.position.set(50, 100, 50);
                dirLight.castShadow = true;
                scene.add(dirLight);

                const pointLight1 = new THREE.PointLight(0x6366f1, 1, 100);
                pointLight1.position.set(-50, 50, -50);
                scene.add(pointLight1);

                const pointLight2 = new THREE.PointLight(0xf472b6, 1, 100);
                pointLight2.position.set(50, -50, 50);
                scene.add(pointLight2);

                // إنشاء الـ mesh
                createMesh();

                // الشبكة الأرضية
                const gridHelper = new THREE.GridHelper(200, 20, 0x6366f1, 0x1a1a3e);
                scene.add(gridHelper);

                // المحاور
                const axesHelper = new THREE.AxesHelper(50);
                scene.add(axesHelper);

                // حلقة الرسم
                animate();

                // تغيير الحجم
                window.addEventListener('resize', onWindowResize);
            }}

            function createMesh() {{
                const vertices = {vertices_json};
                const faces = {faces_json};

                const geometry = new THREE.BufferGeometry();

                // إعادة ترتيع الوجوه للـ Three.js
                const threeFaces = [];
                for (let i = 0; i < faces.length; i++) {{
                    const face = faces[i];
                    threeFaces.push(
                        vertices[face[0]][0], vertices[face[0]][1], vertices[face[0]][2],
                        vertices[face[1]][0], vertices[face[1]][1], vertices[face[1]][2],
                        vertices[face[2]][0], vertices[face[2]][1], vertices[face[2]][2]
                    );
                }}

                const positions = new Float32Array(threeFaces);
                geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
                geometry.computeVertexNormals();

                // المادة
                const material = new THREE.MeshPhongMaterial({{
                    color: 0x6366f1,
                    specular: 0x222222,
                    shininess: 100,
                    side: THREE.DoubleSide,
                    transparent: true,
                    opacity: 0.9
                }});

                mesh = new THREE.Mesh(geometry, material);
                mesh.castShadow = true;
                mesh.receiveShadow = true;

                // Wireframe
                const wireGeo = new THREE.WireframeGeometry(geometry);
                const wireMat = new THREE.LineBasicMaterial({{ color: 0x22d3ee, transparent: true, opacity: 0.3 }});
                wireframe = new THREE.LineSegments(wireGeo, wireMat);
                wireframe.visible = false;

                const group = new THREE.Group();
                group.add(mesh);
                group.add(wireframe);

                // توسيط
                geometry.computeBoundingBox();
                const center = new THREE.Vector3();
                geometry.boundingBox.getCenter(center);
                group.position.sub(center);

                scene.add(group);
            }}

            function animate() {{
                requestAnimationFrame(animate);

                if (autoRotate) {{
                    scene.rotation.y += 0.005;
                }}

                controls.update();
                renderer.render(scene, camera);
            }}

            function onWindowResize() {{
                const container = document.getElementById('canvas-container');
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }}

            function resetView() {{
                camera.position.set(80, 60, 80);
                controls.reset();
                scene.rotation.y = 0;
            }}

            function toggleWireframe() {{
                wireframe.visible = !wireframe.visible;
            }}

            function toggleAutoRotate() {{
                autoRotate = !autoRotate;
            }}

            init();
        </script>
    </body>
    </html>
    """
    return html

def get_simple_3d_viewer(mesh):
    """عرض 3D بسيط باستخدام trimesh + HTML"""
    # حفظ مؤقت
    tmp_path = "/tmp/mesh_viewer.html"
    mesh.export(tmp_path)

    # قراءة كـ HTML
    scene = mesh.scene()
    html = scene.save_image(resolution=[800, 600])
    return html

def display_mesh_stats(mesh):
    """عرض إحصائيات الـ mesh"""
    exporter = ModelExporter()
    info = exporter.get_mesh_info(mesh)

    cols = st.columns(4)
    stats = [
        ("🎯 النقاط", info['vertices'], "#6366f1"),
        ("🔷 الوجوه", info['faces'], "#22d3ee"),
        ("📐 الحجم", f"{info['volume']:.2f} mm³", "#34d399"),
        ("📏 المساحة", f"{info['surface_area']:.2f} mm²", "#f472b6")
    ]

    for col, (label, value, color) in zip(cols, stats):
        col.markdown(f"""
        <div style="background: linear-gradient(135deg, {color}22, {color}44); 
                    padding: 15px; border-radius: 15px; text-align: center;
                    border: 1px solid {color}66;">
            <div style="font-size: 24px; font-weight: bold; color: {color};">{value}</div>
            <div style="font-size: 14px; color: #ccc;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# الشريط الجانبي
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 2.5rem; margin: 0;">🎨</h1>
        <h2 style="font-size: 1.2rem; color: #22d3ee; margin-top: 10px;">AI 3D Designer</h2>
        <p style="color: #888; font-size: 0.9rem;">المصمم الذكي ثلاثي الأبعاد</p>
    </div>
    """, unsafe_allow_html=True)

    # اختيار اللغة
    st.markdown("### 🌐 " + t("Language"))
    langs = get_supported_languages()
    lang_names = list(langs.values())
    lang_codes = list(langs.keys())

    selected_lang_name = st.selectbox(
        t("اختر اللغة"),
        lang_names,
        index=lang_codes.index(st.session_state.language)
    )
    st.session_state.language = lang_codes[lang_names.index(selected_lang_name)]

    st.markdown("---")

    # القائمة
    st.markdown("### 📋 " + t("Menu"))
    menu_option = st.radio("", [
        t("🏠 الرئيسية"),
        t("📷 تحويل صورة"),
        t("✏️ تصميم من النص"),
        t("⚙️ المكتبة"),
        t("📤 التصدير"),
        t("ℹ️ المساعدة")
    ], label_visibility="collapsed")

    st.markdown("---")

    # معلومات
    st.markdown("""
    <div style="background: rgba(99, 102, 241, 0.1); padding: 15px; border-radius: 12px;">
        <h4 style="color: #22d3ee; margin: 0;">💡 نصيحة</h4>
        <p style="color: #aaa; font-size: 0.85rem; margin: 5px 0 0 0;">
            استخدم أوامر مثل: "كبر 2x" أو "دور 45 درجة على محور Y"
        </p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# الصفحة الرئيسية
# ═══════════════════════════════════════════════════════════════

if t("🏠 الرئيسية") in menu_option:
    st.title("🎨 AI 3D Designer")
    st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <h3 style="color: #f472b6;">{t('حوّل أفكارك إلى واقع ثلاثي الأبعاد')}</h3>
        <p style="color: #aaa; font-size: 1.1rem;">
            {t('صمم، عدّل، وصدر نماذجك باستخدام الذكاء الاصطناعي')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # بطاقات الميزات
    cols = st.columns(3)
    features = [
        ("📷", t("تحويل الصور"), t("حوّل أي صورة 2D إلى نموذج 3D قابل للتحرير")),
        ("🤖", t("أوامر ذكية"), t("صف ما تريد باللغة الطبيعية وسنبنيه لك")),
        ("🎮", t("تحكم تفاعلي"), t("دوّر، حرّك، وعدّل بكل حرية في المتصفح"))
    ]

    for col, (icon, title, desc) in zip(cols, features):
        col.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 20px; 
                    text-align: center; border: 1px solid rgba(255,255,255,0.1); height: 200px;">
            <div style="font-size: 3rem;">{icon}</div>
            <h4 style="color: #22d3ee; margin: 15px 0 10px 0;">{title}</h4>
            <p style="color: #888; font-size: 0.9rem;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    # عرض نموذج افتراضي
    st.markdown("---")
    st.markdown(f"### 🎯 {t('معاينة سريعة')}")

    if st.session_state.mesh is None:
        # إنشاء نموذج افتراضي
        default_mesh = trimesh.creation.icosphere(radius=20, subdivisions=3)
        st.session_state.mesh = default_mesh

    display_mesh_stats(st.session_state.mesh)

    # عرض 3D
    mesh_data = {
        'vertices': st.session_state.mesh.vertices,
        'faces': st.session_state.mesh.faces
    }
    html_viewer = get_threejs_html(mesh_data)
    st.components.v1.html(html_viewer, height=620, scrolling=False)

# ═══════════════════════════════════════════════════════════════
# تحويل الصور
# ═══════════════════════════════════════════════════════════════
elif t("📷 تحويل صورة") in menu_option:
    st.title("📷 " + t("تحويل الصور إلى 3D"))

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"### {t('إعدادات التحويل')}")

        uploaded_file = st.file_uploader(
            t("اختر صورة"),
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff']
        )

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption=t("الصورة الأصلية"), use_column_width=True)

        # الإعدادات
        extrude_height = st.slider(t("ارتفاع الـ Extrusion"), 1.0, 50.0, 10.0, 0.5)
        resolution = st.slider(t("الدقة"), 50, 300, 150, 10)
        invert = st.checkbox(t("عكس الألوان (نقش غائر)"), False)
        smooth_mesh = st.checkbox(t("تنعيم الحواف"), True)

        if st.button(t("🚀 تحويل إلى 3D"), key="convert_btn"):
            if uploaded_file:
                with st.spinner(t("جاري المعالجة...")):
                    # حفظ الصورة مؤقتاً
                    temp_path = "/tmp/uploaded_image.png"
                    image.save(temp_path)

                    # التحويل
                    generator = ImageTo3D()
                    mesh = generator.image_to_mesh(
                        temp_path,
                        extrude_height=extrude_height,
                        resolution=resolution,
                        invert=invert,
                        smooth=smooth_mesh
                    )

                    st.session_state.mesh = mesh
                    st.session_state.mesh_history.append(mesh.copy())
                    st.success(t("✅ تم التحويل بنجاح!"))
            else:
                st.warning(t("⚠️ يرجى رفع صورة أولاً"))

    with col2:
        st.markdown(f"### {t('النموذج ثلاثي الأبعاد')}")

        if st.session_state.mesh is not None:
            display_mesh_stats(st.session_state.mesh)

            mesh_data = {
                'vertices': st.session_state.mesh.vertices,
                'faces': st.session_state.mesh.faces
            }
            html_viewer = get_threejs_html(mesh_data)
            st.components.v1.html(html_viewer, height=500, scrolling=False)
        else:
            st.info(t("🎨 سيتم عرض النموذج هنا بعد التحويل"))

# ═══════════════════════════════════════════════════════════════
# تصميم من النص
# ═══════════════════════════════════════════════════════════════
elif t("✏️ تصميم من النص") in menu_option:
    st.title("✏️ " + t("التصميم بالأوامر النصية"))

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"### {t('أكتب ما تريد تصميمه')}")

        prompt = st.text_area(
            t("وصف التصميم"),
            placeholder=t("مثال: مكعب بطول 20 وعرض 30 وارتفاع 15"),
            height=100
        )

        st.markdown(f"### {t('أو اختر شكل جاهز')}")
        shape_type = st.selectbox(
            t("الشكل"),
            ['box', 'sphere', 'cylinder', 'cone', 'torus', 'capsule']
        )

        st.markdown(f"### {t('البارامترات')}")

        params = {}
        if shape_type == 'box':
            c1, c2, c3 = st.columns(3)
            params['width'] = c1.number_input(t("الطول"), 1.0, 100.0, 20.0)
            params['height'] = c2.number_input(t("الارتفاع"), 1.0, 100.0, 20.0)
            params['depth'] = c3.number_input(t("العمق"), 1.0, 100.0, 20.0)

        elif shape_type == 'sphere':
            params['radius'] = st.slider(t("نصف القطر"), 1.0, 50.0, 10.0)

        elif shape_type == 'cylinder':
            c1, c2 = st.columns(2)
            params['radius'] = c1.number_input(t("نصف القطر"), 1.0, 50.0, 5.0)
            params['height'] = c2.number_input(t("الارتفاع"), 1.0, 100.0, 20.0)

        elif shape_type == 'cone':
            c1, c2 = st.columns(2)
            params['radius'] = c1.number_input(t("نصف القطر"), 1.0, 50.0, 5.0)
            params['height'] = c2.number_input(t("الارتفاع"), 1.0, 100.0, 20.0)

        elif shape_type == 'torus':
            c1, c2 = st.columns(2)
            params['major'] = c1.number_input(t("نصف القطر الكبير"), 1.0, 50.0, 10.0)
            params['minor'] = c2.number_input(t("نصف القطر الصغير"), 0.5, 20.0, 2.0)

        elif shape_type == 'capsule':
            c1, c2 = st.columns(2)
            params['radius'] = c1.number_input(t("نصف القطر"), 1.0, 20.0, 3.0)
            params['height'] = c2.number_input(t("الارتفاع"), 1.0, 100.0, 10.0)

        # تعديلات إضافية
        st.markdown(f"### {t('تعديلات إضافية')}")

        mod_cols = st.columns(3)
        with mod_cols[0]:
            scale_x = st.slider("Scale X", 0.1, 5.0, 1.0, 0.1)
        with mod_cols[1]:
            scale_y = st.slider("Scale Y", 0.1, 5.0, 1.0, 0.1)
        with mod_cols[2]:
            scale_z = st.slider("Scale Z", 0.1, 5.0, 1.0, 0.1)

        rot_cols = st.columns(3)
        with rot_cols[0]:
            rot_x = st.slider("Rotate X", 0, 360, 0, 5)
        with rot_cols[1]:
            rot_y = st.slider("Rotate Y", 0, 360, 0, 5)
        with rot_cols[2]:
            rot_z = st.slider("Rotate Z", 0, 360, 0, 5)

        if st.button(t("🎨 إنشاء النموذج"), key="create_btn"):
            with st.spinner(t("جاري الإنشاء...")):
                generator = ImageTo3D()

                # إنشاء من الوصف أو الشكل المختار
                if prompt.strip():
                    processor = PromptProcessor()
                    mesh = processor.generate_from_description(prompt)
                else:
                    mesh = generator.create_parametric_shape(shape_type, params)

                # تطبيق التعديلات
                mesh.apply_scale([scale_x, scale_y, scale_z])
                mesh.apply_transform(trimesh.transformations.rotation_matrix(
                    np.radians(rot_x), [1, 0, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(
                    np.radians(rot_y), [0, 1, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(
                    np.radians(rot_z), [0, 0, 1]))

                st.session_state.mesh = mesh
                st.session_state.mesh_history.append(mesh.copy())
                st.success(t("✅ تم الإنشاء بنجاح!"))

    with col2:
        st.markdown(f"### {t('المعاينة')}")

        if st.session_state.mesh is not None:
            display_mesh_stats(st.session_state.mesh)

            mesh_data = {
                'vertices': st.session_state.mesh.vertices,
                'faces': st.session_state.mesh.faces
            }
            html_viewer = get_threejs_html(mesh_data)
            st.components.v1.html(html_viewer, height=500, scrolling=False)
        else:
            st.info(t("🎨 سيتم عرض النموذج هنا"))

# ═══════════════════════════════════════════════════════════════
# المكتبة
# ═══════════════════════════════════════════════════════════════
elif t("⚙️ المكتبة") in menu_option:
    st.title("⚙️ " + t("مكتبة التعديلات"))

    if st.session_state.mesh is not None:
        st.markdown(f"### {t('تعديل النموذج الحالي')}")

        # عرض الإحصائيات
        display_mesh_stats(st.session_state.mesh)

        # تعديلات متقدمة
        st.markdown(f"### {t('تعديلات متقدمة')}")

        tabs = st.tabs([
            t("🔧 تحجيم"),
            t("🔄 تدوير"),
            t("📍 إزاحة"),
            t("✨ تنعيم"),
            t("🔍 تفاصيل")
        ])

        with tabs[0]:
            st.markdown(f"#### {t('تغيير الحجم')}")
            c1, c2, c3 = st.columns(3)
            with c1:
                sx = st.number_input("Scale X", 0.1, 10.0, 1.0, 0.1, key="sx")
            with c2:
                sy = st.number_input("Scale Y", 0.1, 10.0, 1.0, 0.1, key="sy")
            with c3:
                sz = st.number_input("Scale Z", 0.1, 10.0, 1.0, 0.1, key="sz")

            if st.button(t("تطبيق التحجيم")):
                st.session_state.mesh.apply_scale([sx, sy, sz])
                st.success(t("تم التحجيم!"))

        with tabs[1]:
            st.markdown(f"#### {t('التدوير')}")
            c1, c2, c3 = st.columns(3)
            with c1:
                rx = st.slider("X°", 0, 360, 0, key="rx")
            with c2:
                ry = st.slider("Y°", 0, 360, 0, key="ry")
            with c3:
                rz = st.slider("Z°", 0, 360, 0, key="rz")

            if st.button(t("تطبيق التدوير")):
                st.session_state.mesh.apply_transform(trimesh.transformations.rotation_matrix(
                    np.radians(rx), [1, 0, 0]))
                st.session_state.mesh.apply_transform(trimesh.transformations.rotation_matrix(
                    np.radians(ry), [0, 1, 0]))
                st.session_state.mesh.apply_transform(trimesh.transformations.rotation_matrix(
                    np.radians(rz), [0, 0, 1]))
                st.success(t("تم التدوير!"))

        with tabs[2]:
            st.markdown(f"#### {t('الإزاحة')}")
            c1, c2, c3 = st.columns(3)
            with c1:
                tx = st.number_input("X", -100.0, 100.0, 0.0, 1.0, key="tx")
            with c2:
                ty = st.number_input("Y", -100.0, 100.0, 0.0, 1.0, key="ty")
            with c3:
                tz = st.number_input("Z", -100.0, 100.0, 0.0, 1.0, key="tz")

            if st.button(t("تطبيق الإزاحة")):
                st.session_state.mesh.apply_translation([tx, ty, tz])
                st.success(t("تمت الإزاحة!"))

        with tabs[3]:
            st.markdown(f"#### {t("تنعيم الحواف")}")
            iterations = st.slider(t("عدد مرات التنعيم"), 1, 5, 1)

            if st.button(t("تطبيق التنعيم")):
                for _ in range(iterations):
                    st.session_state.mesh = st.session_state.mesh.smoothed()
                st.success(t("تم التنعيم!"))

        with tabs[4]:
            st.markdown(f"#### {t("تفاصيل النموذج")}")
            exporter = ModelExporter()
            info = exporter.get_mesh_info(st.session_state.mesh)

            st.json(info)

        # عرض 3D
        st.markdown(f"### {t("المعاينة المباشرة")}")
        mesh_data = {
            'vertices': st.session_state.mesh.vertices,
            'faces': st.session_state.mesh.faces
        }
        html_viewer = get_threejs_html(mesh_data)
        st.components.v1.html(html_viewer, height=500, scrolling=False)
    else:
        st.warning(t("لا يوجد نموذج. يرجى إنشاء نموذج أولاً."))

# ═══════════════════════════════════════════════════════════════
# التصدير
# ═══════════════════════════════════════════════════════════════
elif t("📤 التصدير") in menu_option:
    st.title("📤 " + t("تصدير النماذج"))

    if st.session_state.mesh is not None:
        st.markdown(f"### {t("اختر صيغة التصدير")}")

        col1, col2, col3 = st.columns(3)

        exporter = ModelExporter()

        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #6366f122, #22d3ee22); 
                        padding: 20px; border-radius: 15px; text-align: center;">
                <div style="font-size: 3rem;">🔷</div>
                <h4 style="color: #22d3ee;">STL</h4>
                <p style="color: #888; font-size: 0.8rem;">Standard Tessellation Language</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(t("تصدير STL"), key="stl"):
                path = "/tmp/model.stl"
                exporter.export_stl(st.session_state.mesh, path)
                with open(path, 'rb') as f:
                    st.download_button(
                        label=t("⬇️ تحميل STL"),
                        data=f.read(),
                        file_name="model.stl",
                        mime="application/octet-stream"
                    )

        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f472b622, #fbbf2422); 
                        padding: 20px; border-radius: 15px; text-align: center;">
                <div style="font-size: 3rem;">📄</div>
                <h4 style="color: #fbbf24;">PDF</h4>
                <p style="color: #888; font-size: 0.8rem;">Technical Drawing</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(t("تصدير PDF"), key="pdf"):
                path = "/tmp/model.pdf"
                exporter.export_pdf(st.session_state.mesh, path)
                with open(path, 'rb') as f:
                    st.download_button(
                        label=t("⬇️ تحميل PDF"),
                        data=f.read(),
                        file_name="model.pdf",
                        mime="application/pdf"
                    )

        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #34d39922, #22d3ee22); 
                        padding: 20px; border-radius: 15px; text-align: center;">
                <div style="font-size: 3rem;">🔧</div>
                <h4 style="color: #34d399;">STEP</h4>
                <p style="color: #888; font-size: 0.8rem;">CAD Standard</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(t("تصدير STEP"), key="step"):
                path = "/tmp/model.step"
                result = exporter.export_step(st.session_state.mesh, path)
                with open(result, 'rb') as f:
                    file_name = "model.step" if result.endswith('.step') else "model.stl"
                    mime = "application/step" if result.endswith('.step') else "application/octet-stream"
                    st.download_button(
                        label=t("⬇️ تحميل") + " " + file_name.split('.')[-1].upper(),
                        data=f.read(),
                        file_name=file_name,
                        mime=mime
                    )

        # صيغ إضافية
        st.markdown("---")
        st.markdown(f"### {t("صيغ إضافية")}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button(t("تصدير OBJ"), key="obj"):
                path = "/tmp/model.obj"
                exporter.export_obj(st.session_state.mesh, path)
                with open(path, 'rb') as f:
                    st.download_button(
                        label=t("⬇️ تحميل OBJ"),
                        data=f.read(),
                        file_name="model.obj",
                        mime="text/plain"
                    )

        with c2:
            if st.button(t("تصدير PLY"), key="ply"):
                path = "/tmp/model.ply"
                exporter.export_ply(st.session_state.mesh, path)
                with open(path, 'rb') as f:
                    st.download_button(
                        label=t("⬇️ تحميل PLY"),
                        data=f.read(),
                        file_name="model.ply",
                        mime="application/octet-stream"
                    )
    else:
        st.warning(t("لا يوجد نموذج للتصدير. يرجى إنشاء نموذج أولاً."))

# ═══════════════════════════════════════════════════════════════
# المساعدة
# ═══════════════════════════════════════════════════════════════
elif t("ℹ️ المساعدة") in menu_option:
    st.title("ℹ️ " + t("مركز المساعدة"))

    st.markdown(f"""
    ### {t("أوامر Prompt المدعومة")}

    يمكنك استخدام الأوامر التالية باللغة العربية أو الإنجليزية:

    | {t("الأمر")} | {t("الوصف")} | {t("مثال")} |
    |---|---|---|
    | **{t("كبر/صغر")}** | {t("تغيير الحجم")} | "كبر 2 أضعاف" |
    | **{t("دور/لف")}** | {t("تدوير النموذج")} | "دور 45 درجة على محور Y" |
    | **{t("حرك/نقل")}** | {t("إزاحة النموذج")} | "حرك 10 ملم على محور X" |
    | **{t("بعد/ارتفاع")}** | {t("تغيير الارتفاع")} | "اجعل الارتفاع 20 ملم" |
    | **{t("لون")}** | {t("تغيير اللون")} | "لون أحمر" |
    | **{t("نعم")}** | {t("تنعيم الحواف")} | "نعم النموذج" |
    | **{t("شطف")}** | {t("إضافة شطف")} | "شطف الحواف بـ 2 ملم" |

    ### {t("أشكال Parametric")}

    - **{t("مكعب")}**: "مكعب 20x30x15"
    - **{t("كرة")}**: "كرة نصف قطر 10"
    - **{t("أسطوانة")}**: "أسطوانة نصف قطر 5 وارتفاع 20"
    - **{t("مخروط")}**: "مخروط نصف قطر 5 وارتفاع 15"
    - **{t("طارة")}**: "طارة نصف قطر كبير 10 وصغير 2"

    ### {t("اختصارات لوحة المفاتيح")}

    - **{t("فأرة يسار")}**: {t("تدوير")}
    - **{t("فأرة يمين")}**: {t("تحريك")}
    - **{t("عجلة الفأرة")}**: {t("تقريب/تبعيد")}
    - **{t("زر R")}**: {t("إعادة ضبط المنظور")}

    ### {t("نصائح")}

    1. {t("استخدم صور عالية التباين للحصول على نتائج أفضل")}
    2. {t("ابدأ بدقة منخفضة (50-100) للاختبار ثم ارفع الدقة")}
    3. {t("احفظ تاريخ النماذج باستخدام زر 'حفظ في التاريخ'")}
    4. {t("استخدم التنعيم للتخلص من الحواف الحادة")}
    """)

# ═══════════════════════════════════════════════════════════════
# شريط التذييل
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p>🎨 AI 3D Designer | Powered by DEVELOPPINI</p>
    <p style="font-size: 0.8rem;">Streamlit + Three.js + Trimesh + Python</p>
</div>
""", unsafe_allow_html=True)
