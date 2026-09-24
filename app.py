import streamlit as st
import datetime
import base64
import os
import subprocess
import tempfile

##### ==========================================================
##### 1. Page Configuration
##### ==========================================================
st.set_page_config(
    page_title="نظام إدارة وإصدار شهادات الإشراف الأكاديمي - مدارس الثغر النموذجية الأهلية",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

##### ==========================================================
##### 2. Sample Digital Signature SVG (Base64)
##### ==========================================================
SAMPLE_DIGITAL_SIG_SVG = "data:image/svg+xml;base64," + base64.b64encode('''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 70" width="220" height="70">
  <path d="M 15 45 C 35 12, 65 58, 95 25 C 115 5, 135 60, 165 30 C 185 10, 195 45, 210 25" fill="none" stroke="#006C35" stroke-width="3" stroke-linecap="round"/>
  <path d="M 30 52 C 70 58, 120 50, 180 54" fill="none" stroke="#D4AF37" stroke-width="2" stroke-dasharray="4,2"/>
  <text x="110" y="66" font-family="'Amiri', 'Cairo', sans-serif" font-size="11" font-weight="bold" fill="#006C35" text-anchor="middle">توقيع رقمي معتمد ✦</text>
</svg>
'''.strip().encode('utf-8')).decode('utf-8')

##### ==========================================================
##### 3. Load School Logo (embedded as base64)
##### ==========================================================
@st.cache_data(show_spinner=False)
def load_logo_b64():
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "thaghr_logo.png"),
        "thaghr_logo.png",
    ]
    for p in candidates:
        try:
            if os.path.exists(p):
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode()
        except Exception:
            pass
    return ""

LOGO_B64 = load_logo_b64()
LOGO_SRC = f"data:image/png;base64,{LOGO_B64}" if LOGO_B64 else ""

##### ==========================================================
##### 4. Advanced CSS for Streamlit UI (Full RTL & Modern Styling)
##### ==========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    
    /* Full Application Right-To-Left (RTL) Enforcement */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Cairo', 'Noto Sans Arabic', 'Segoe UI', Tahoma, sans-serif !important;
    }

    /* Sidebar RTL styling */
    [data-testid="stSidebar"] {
        direction: rtl !important;
        text-align: right !important;
    }

    /* All Input Widgets RTL */
    .stTextInput input, .stTextArea textarea, .stSelectbox select, div[role="combobox"], 
    .stMultiSelect div, div[role="radiogroup"], .stNumberInput input, .stDateInput input {
        direction: rtl !important;
        text-align: right !important;
    }

    /* Labels & Radio / Checkbox Texts RTL */
    label, .stRadio label, .stCheckbox label, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        direction: rtl !important;
        text-align: right !important;
    }

    /* Custom Credit Badge */
    .designer-credit-badge {
        background: linear-gradient(135deg, #006C35 0%, #0B2A4A 100%);
        color: #D4AF37;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        font-size: 14px;
        border: 1px solid #D4AF37;
        margin-top: 15px;
        direction: rtl;
    }

    /* Custom PDF Export Button Highlight */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #006C35 0%, #004D25 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 8px !important;
        padding: 10px 16px !important;
    }

    /* Adjust Columns RTL spacing */
    [data-testid="column"] {
        direction: rtl !important;
        text-align: right !important;
    }
</style>
""", unsafe_allow_html=True)

##### ==========================================================
##### 5. Main Site Header
##### ==========================================================
_header_logo = f'<div class="mh-logo"><img src="{LOGO_SRC}" alt="logo" style="height: 65px; margin-bottom: 6px;"></div>' if LOGO_SRC else ""
st.markdown(f"""
<div style="text-align: center; padding: 12px; background: linear-gradient(135deg, #006C35 0%, #0B2A4A 100%); color: white; border-radius: 10px; margin-bottom: 20px; direction: rtl;">
    {_header_logo}
    <h1 style="margin:0; font-size: 26px;">📜 نظام إدارة وإصدار شهادات الإشراف الأكاديمي</h1>
    <h3 style="margin:5px 0 0 0; font-size: 16px; color: #D4AF37;">مدارس الثغر النموذجية الأهلية</h3>
</div>
""", unsafe_allow_html=True)

if not LOGO_SRC:
    st.warning("⚠️ لم يتم العثور على ملف الشعار (thaghr_logo.png). ضعه بجانب ملف app.py لإظهار الشعار في الشهادة.")

##### ==========================================================
##### 6. Initialize Session State with Teachers
##### ==========================================================
INTERMEDIATE_TEACHERS_FROM_SOURCE = [
    "أ/ محمد سامي السعيد",
    "أ/ علي محمد معوض",
    "أ/ أحمد عبد الحميد سعيد",
    "أ/ محمد عبد المنعم أبو كيلة",
    "أ/ هيثم رضا عطية",
    "أ/ عماد الدين نصر كرم",
    "أ/ السيد الغريب بدوي",
    "أ/ محمد إبراهيم عبد الرحمن",
    "أ/ أسامة أحمد سالم",
    "أ/ عماد بكر عارف",
    "أ/ إبراهيم علي العتيبي",
    "أ/ عيسى خالد العويس",
    "أ/ زيد بن علي التميمي",
    "أ/ أحمد سلامة"
]

if "dept_teachers_dict" not in st.session_state:
    st.session_state["dept_teachers_dict"] = {
        "القسم المتوسط بنين": list(INTERMEDIATE_TEACHERS_FROM_SOURCE),
        "القسم المتوسط بنات": ["معلم جديد"],
        "القسم الابتدائي بنين": ["معلم جديد"],
        "القسم الابتدائي بنات": ["معلم جديد"],
        "القسم الثانوي بنين": ["معلم جديد"],
        "القسم الثانوي بنات": ["معلم جديد"]
    }

if "courses_list" not in st.session_state:
    st.session_state["courses_list"] = [
        "استراتيجيات التعليم الحديثة وتقنيات الذكاء الاصطناعي",
        "الإدارة الصفية الفعالة وبناء البيئة الإيجابية",
        "مهارات التقويم التكويني والتغذية الراجعة",
        "توظيف التقنية في التدريس الرقمي",
        "مشاريع التعلم المبني على الكفايات"
    ]

if "signatures_list" not in st.session_state:
    st.session_state["signatures_list"] = [
        {"role": "المدير الأكاديمي لمدارس الثغر", "name": "د. ياسين البدراوي"},
        {"role": "مدير المدرسة", "name": "أ. إبراهيم بن موسى التميمي"},
        {"role": "مشرف المرحلة الابتدائية", "name": "أ. محمد مصطفى"},
        {"role": "وكيل الشؤون التعليمية", "name": "أ. محمد مبروك السيد"},
        {"role": "وكيل شؤون الطلاب", "name": "أ. صالح بن عبدالله الدعجاني"}
    ]

col_ctrl, col_preview = st.columns([0.75, 2.25])

with col_ctrl:
    st.markdown("### ⚙️ لوحة التحكم والإعدادات")

    cert_type = st.radio(
        "🏷️ نوع الشهادة:",
        ["🎓 شهادة حضور دورة تدريبية", "🎖️ شهادة شكر وتقدير للمعلم"],
        index=0
    )

    st.markdown("---")

    selected_dept = st.selectbox(
        "🏢 القسم / المرحلة الدراسية:",
        [
            "القسم المتوسط بنين",
            "القسم المتوسط بنات",
            "القسم الابتدائي بنين",
            "القسم الابتدائي بنات",
            "القسم الثانوي بنين",
            "القسم الثانوي بنات"
        ],
        index=0
    )

    st.markdown("---")

    st.markdown("#### 👤 المعلمون المكرمون")

    teachers_names_list = st.session_state["dept_teachers_dict"].get(selected_dept, [])

    if not teachers_names_list:
        st.info(f"ℹ️ لا يوجد معلمون مضافون في ({selected_dept}) حالياً. يمكنك إضافة أسماء المعلمين فوراً من النموذج أدناه.")
        selected_teachers = []
    else:
        select_all_teachers = st.checkbox("✅ تحديد جميع معلمي القسم المحدد", value=True)
        if select_all_teachers:
            default_teachers = teachers_names_list
        else:
            default_teachers = [teachers_names_list[0]] if teachers_names_list else []

        selected_teachers = st.multiselect(
            f"اختر معلمي ({selected_dept}):",
            options=teachers_names_list,
            default=default_teachers
        )

    with st.expander("➕ إضافة معلم جديد لهذا القسم"):
        new_teacher_input = st.text_input("اسم المعلم الجديد:", placeholder="أ/ اكتب الاسم رباعياً...", key="input_new_teacher")
        if st.button("💾 حفظ وإضافة القائمة", key="btn_add_teacher"):
            if new_teacher_input.strip():
                if new_teacher_input.strip() not in st.session_state["dept_teachers_dict"][selected_dept]:
                    st.session_state["dept_teachers_dict"][selected_dept].append(new_teacher_input.strip())
                    st.success(f"✅ تم إضافة المعلم إلى {selected_dept}: {new_teacher_input.strip()}")
                    st.rerun()

    st.markdown("---")

    if "حضور دورة" in cert_type:
        st.markdown("#### 📚 الدورة التدريبية")
        selected_course = st.selectbox(
            "اختر الدورة التدريبية:",
            st.session_state["courses_list"]
        )
        with st.expander("➕ إضافة دورة جديدة"):
            new_course_input = st.text_input("عنوان الدورة الجديد:", placeholder="اكتب عنوان الدورة...", key="input_new_course")
            if st.button("💾 حفظ والدورة", key="btn_add_course"):
                if new_course_input.strip():
                    if new_course_input.strip() not in st.session_state["courses_list"]:
                        st.session_state["courses_list"].append(new_course_input.strip())
                        st.success(f"✅ تم إضافة الدورة: {new_course_input.strip()}")
                        st.rerun()
                    else:
                        st.warning("⚠️ عنوان الدورة موجود بالفعل.")
        course_hours = st.number_input("عدد الساعات التدريبية:", min_value=1, max_value=100, value=15)
        course_date = st.date_input("تاريخ انعقاد الدورة:", value=datetime.date.today())
        formatted_date = course_date.strftime("%Y/%m/%d") + " م"
        cert_main_title = "شهادة حضور دورة تدريبية"
        default_body_prefix = "يُسَّر إدارة الإشراف الأكاديمي بمدارس الثغر النموذجية الأهلية منح المعلم"
        default_body_text = f"شهادة حضور وذلك لاجتيازه بنجاح الدورة التدريبية بعنوان:\n« {selected_course} »\nوالتي عقدت بتاريخ {formatted_date} بواقع ({course_hours}) ساعات تدريبية معتمدة من إدارة الإشراف الأكاديمي. متمنين له دوام التوفيق والنجاح."
    else:
        st.markdown("#### 📖 التخصص / المادة")
        subject_name = st.text_input("المادة / التخصص:", value="تكنولوجيا المعلومات والتعليم الرقمي")
        formatted_date = datetime.date.today().strftime("%Y/%m/%d") + " م"
        cert_main_title = "شهادة شكر وتقدير"
        default_body_prefix = "تتقدم إدارة الإشراف الأكاديمي بمدارس الثغر النموذجية الأهلية ببالغ الشكر والتقدير للمعلم"
        default_body_text = f"تقديرًا لجهوده المتميزة وعطائه المخلص في رفع مستوى الأداء التعليمي بمادة ({subject_name})، ومشاركته الفاعلة مع إدارة الإشراف الأكاديمي والأنشطة المدرسية خلال العام الدراسي."

    st.markdown("#### 📝 تخصيص النص والديباجة")
    cert_custom_prefix = st.text_input("صياغة المقطع الافتتاحي (الديباجة):", value=default_body_prefix)
    cert_custom_text = st.text_area("صياغة متن الشهادة:", value=default_body_text, height=100)

    st.markdown("---")

    st.markdown("#### ✍️ التوقيعات والتوقيع الإلكتروني")
    sig_options_map = {f"{s['role']}: {s['name']}": s for s in st.session_state["signatures_list"]}
    default_sig_keys = list(sig_options_map.keys())
    selected_sig_keys = st.multiselect(
        "اختر التوقيعات الظاهرة بالشهادة:",
        options=list(sig_options_map.keys()),
        default=default_sig_keys
    )
    chosen_signatures = [sig_options_map[k] for k in selected_sig_keys]

    enable_digital_sig = st.checkbox("✒️ تفعيل إدراج التوقيع الإلكتروني الرقمي بالشهادة (أسفل الاسم)", value=True)
    digital_sig_src = SAMPLE_DIGITAL_SIG_SVG

    if enable_digital_sig:
        uploaded_sig_file = st.file_uploader("📤 رفع صورة التوقيع الرقمي (اختياري PNG/JPG):", type=["png", "jpg", "jpeg", "svg"])
        if uploaded_sig_file is not None:
            sig_bytes = uploaded_sig_file.read()
            sig_b64 = base64.b64encode(sig_bytes).decode()
            mime = uploaded_sig_file.type
            digital_sig_src = f"data:{mime};base64,{sig_b64}"

    with st.expander("➕ إضافة توقيع مسؤول جديد"):
        new_sig_role = st.text_input("المسمى الوظيفي:", placeholder="مثال: رئيس قسم الإشراف الأكاديمي", key="input_sig_role")
        new_sig_name = st.text_input("اسم صاحب التوقيع:", placeholder="مثال: د. محمد العتيبي", key="input_sig_name")
        if st.button("💾 حفظ التوقيع", key="btn_add_sig"):
            if new_sig_role.strip() and new_sig_name.strip():
                st.session_state["signatures_list"].append({"role": new_sig_role.strip(), "name": new_sig_name.strip()})
                st.success("✅ تم إضافة التوقيع بنجاح!")
                st.rerun()

    st.markdown("---")

    st.markdown("""
    <div class="designer-credit-badge">
        ✨ تصميم وتطوير: أ. محمد سامي السعيد
    </div>
    """, unsafe_allow_html=True)

##### ==========================================================
##### 7. Certificate Print/Export CSS (Saudi National Identity Theme)
##### ==========================================================
CERT_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Amiri:ital,wght@0,700;1,400&display=swap');
@page { size: A4 landscape; margin: 0; }
body { margin: 0; padding: 15px; background-color: #eef2f7; font-family: 'Cairo', sans-serif; direction: rtl; text-align: center; color: #0f172a; }
.page-break { page-break-after: always; break-after: page; margin-bottom: 30px; }
.certificate-container { width: 980px; height: 650px; margin: 0 auto; background: #ffffff; padding: 20px; box-sizing: border-box; position: relative; border: 14px solid #006C35; outline: 4px solid #D4AF37; outline-offset: -9px; border-radius: 14px; box-shadow: 0 14px 38px rgba(0,0,0,0.14); overflow: hidden; background-image: radial-gradient(circle at 50% 0%, #ffffff 0%, #fbfdfe 60%, #f3f7f5 100%); direction: rtl; }
.watermark-logo { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 440px; height: auto; opacity: 0.055; pointer-events: none; z-index: 1; }
.corner { position: absolute; width: 44px; height: 44px; z-index: 3; border-color: #D4AF37; }
.corner-tr { top: 16px; right: 16px; border-top: 3px solid #D4AF37; border-right: 3px solid #D4AF37; border-radius: 0 8px 0 0; }
.corner-tl { top: 16px; left: 16px; border-top: 3px solid #D4AF37; border-left: 3px solid #D4AF37; border-radius: 8px 0 0 0; }
.corner-br { bottom: 16px; right: 16px; border-bottom: 3px solid #D4AF37; border-right: 3px solid #D4AF37; border-radius: 0 0 8px 0; }
.corner-bl { bottom: 16px; left: 16px; border-bottom: 3px solid #D4AF37; border-left: 3px solid #D4AF37; border-radius: 0 0 0 8px; }
.inner-border { border: 2px solid #D4AF37; height: 100%; padding: 12px 26px; box-sizing: border-box; border-radius: 8px; position: relative; z-index: 2; background: rgba(255,255,255,0.88); }
.saudi-nat-header-bar { height: 5px; background: linear-gradient(90deg, #006C35 0%, #004d25 35%, #D4AF37 50%, #004d25 65%, #006C35 100%); border-radius: 3px; margin-bottom: 8px; }
.cert-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #006C35; padding-bottom: 8px; margin-bottom: 8px; direction: rtl; }
.header-side { font-size: 11.5px; font-weight: 700; color: #1e293b; line-height: 1.5; text-align: right; flex: 1.1; }
.header-side.left-side { text-align: left; direction: ltr; }
.saudi-title { color: #006C35; font-weight: 900; font-size: 12.5px; }
.office-highlight { display: inline-block; background: linear-gradient(135deg, #006C35 0%, #004d25 100%); color: #ffffff; padding: 2px 10px; border-radius: 6px; font-weight: 800; border: 1px solid #D4AF37; font-size: 11px; margin-top: 2px; }
.logo-box-center { flex: 1.2; text-align: center; display: flex; flex-direction: column; align-items: center; }
.thaghr-logo-img { height: 70px; width: auto; margin-bottom: 4px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.12)); }
.dept-sub-badge { display: inline-block; font-size: 11px; color: #ffffff; background: linear-gradient(135deg, #006C35 0%, #0B2A4A 100%); padding: 2px 14px; border-radius: 12px; font-weight: 700; border: 1px solid #D4AF37; }
.cert-title-badge { display: inline-block; background: linear-gradient(135deg, #006C35 0%, #0B2A4A 100%); color: #ffffff; font-size: 21px; font-weight: 900; padding: 5px 40px; border-radius: 28px; border: 2px solid #D4AF37; box-shadow: 0 4px 14px rgba(0,108,53,0.25); margin: 2px 0 10px; letter-spacing: 0.5px; }
.cert-body-box { margin-bottom: 8px; padding: 0 16px; }
.cert-prefix-text { font-size: 14.5px; font-weight: 700; color: #334155; }
.teacher-name { font-size: 27px; font-weight: 900; color: #006C35; margin: 4px 0; font-family: 'Amiri', serif; letter-spacing: 0.5px; text-shadow: 1px 1px 0 rgba(212,175,55,0.3); }
.teacher-name::before, .teacher-name::after { content: " ✦ "; color: #D4AF37; font-size: 16px; vertical-align: middle; }
.cert-body-text { font-size: 15px; line-height: 1.8; color: #1e293b; font-weight: 600; }
.signatures-section { display: flex; direction: rtl; flex-direction: row; justify-content: space-between; align-items: flex-start; margin-top: 12px; padding-top: 4px; text-align: center; }
.signatures-section.single-sig-mode { display: flex; justify-content: center; align-items: flex-start; position: relative; padding: 0 120px; }
.signatures-section.single-sig-mode .sig-box { margin: 0 auto; }
.signatures-section.single-sig-mode .school-seal { position: absolute; left: 20px; top: -5px; }
.sig-box { min-width: 140px; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; direction: rtl; }
.sig-role { font-size: 12px; font-weight: 800; color: #006C35; margin-bottom: 2px; }
.sig-name { font-size: 13.5px; font-weight: 800; color: #0f172a; margin-top: 0px; margin-bottom: 4px; }
.sig-img-container { height: 40px; display: flex; align-items: center; justify-content: center; margin-top: 2px; }
.digital-signature-img { max-height: 38px; width: auto; filter: drop-shadow(0 1px 2px rgba(0,0,0,0.15)); }
.school-seal { display: flex; flex-direction: column; align-items: center; margin: 0 8px; }
.seal-ring { position: relative; width: 114px; height: 114px; border-radius: 50%; border: 3px double #006C35; box-shadow: 0 0 0 4px rgba(212,175,55,0.35), inset 0 0 0 2px rgba(212,175,55,0.4); display: flex; align-items: center; justify-content: center; background: #ffffff; transform: rotate(-3deg); }
.seal-logo-img { width: 50px; height: auto; opacity: 0.92; }
.seal-caption { margin-top: 3px; font-size: 9px; font-weight: 800; color: #006C35; }
.cert-footer-date { position: absolute; bottom: 8px; right: 28px; font-size: 10.5px; color: #64748b; font-weight: 700; }
.cert-footer-serial { position: absolute; bottom: 8px; left: 28px; font-size: 10.5px; color: #64748b; font-weight: 700; direction: ltr; }
@media print { body { background: none; padding: 0; } .page-break { margin-bottom: 0; } .certificate-container { box-shadow: none; width: 100%; max-width: 1000px; border-radius: 0; } }
"""

##### ==========================================================
##### 8. Single Certificate HTML Generator
##### ==========================================================
def build_certificate_single_html(teacher_name):
    sigs_html = ""
    for sig in chosen_signatures:
        sig_img_html = f'<div class="sig-img-container"><img src="{digital_sig_src}" class="digital-signature-img" alt="signature"></div>' if enable_digital_sig else '<div class="sig-img-container"></div>'
        sigs_html += f'''
        <div class="sig-box">
            <div class="sig-role">{sig['role']}</div>
            <div class="sig-name">{sig['name']}</div>
            {sig_img_html}
        </div>'''

    sig_section_class = "signatures-section single-sig-mode" if len(chosen_signatures) == 1 else "signatures-section"

    body_text_html = cert_custom_text.replace("\n", "<br>")
    body_html = f'''
    <div class="cert-prefix-text">{cert_custom_prefix}</div>
    <div class="teacher-name">{teacher_name}</div>
    <div class="cert-body-text">{body_text_html}</div>'''

    watermark_html = f'<img class="watermark-logo" src="{LOGO_SRC}" alt="">' if LOGO_SRC else ""
    header_logo_html = f'<img class="thaghr-logo-img" src="{LOGO_SRC}" alt="logo">' if LOGO_SRC else ""
    seal_logo_html = f'<img class="seal-logo-img" src="{LOGO_SRC}" alt="">' if LOGO_SRC else ""

    return f'''
    <div class="certificate-container">
        {watermark_html}
        <div class="corner corner-tr"></div>
        <div class="corner corner-tl"></div>
        <div class="corner corner-br"></div>
        <div class="corner corner-bl"></div>

        <div class="inner-border">
            <div class="saudi-nat-header-bar"></div>
            <div class="cert-header">
                <div class="header-side">
                    <span class="saudi-title">المملكة العربية السعودية</span><br>
                    وزارة التعليم<br>
                    إدارة التعليم بمنطقة الرياض<br>
                    <span class="office-highlight">مكتب التعليم الخاص</span>
                </div>
                <div class="logo-box-center">
                    {header_logo_html}
                    <div class="dept-sub-badge">إدارة الإشراف الأكاديمي - {selected_dept}</div>
                </div>
                <div class="header-side left-side">
                    Kingdom of Saudi Arabia<br>
                    Ministry of Education<br>
                    Riyadh Education Directorate<br>
                    <strong>Private Education Office</strong>
                </div>
            </div>

            <div class="cert-title-badge">{cert_main_title}</div>

            <div class="cert-body-box">
                {body_html}
            </div>

            <div class="{sig_section_class}">
                {sigs_html}
                <div class="school-seal">
                    <div class="seal-ring">
                        {seal_logo_html}
                        <svg viewBox="0 0 120 120" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;">
                            <defs>
                                <path id="textArcTop" d="M 15,60 A 45,45 0 0,1 105,60" fill="none"/>
                                <path id="textArcBottom" d="M 105,60 A 43,43 0 0,1 15,60" fill="none"/>
                            </defs>
                            <text font-size="9" font-weight="800" fill="#006C35" letter-spacing="0.5">
                                <textPath href="#textArcTop" startOffset="50%" text-anchor="middle">
                                    ✦ مدارس الثغر ✦
                                </textPath>
                            </text>
                            <text font-size="8.5" font-weight="700" fill="#0B2A4A" letter-spacing="0.5">
                                <textPath href="#textArcBottom" startOffset="50%" text-anchor="middle">
                                    الإشراف الأكاديمي
                                </textPath>
                            </text>
                        </svg>
                    </div>
                    <div class="seal-caption">ختم معتمد</div>
                </div>
            </div>

            <div class="cert-footer-date">تاريخ الإصدار: {formatted_date}</div>
            <div class="cert-footer-serial">رقم الوثيقة: TH-{abs(hash(teacher_name)) % 900000 + 100000}</div>
        </div>
    </div>
    '''

##### ==========================================================
##### 9. Full Batch Certificates Document HTML Generator
##### ==========================================================
def build_full_certificates_document_html(teachers_list):
    single_certs_html = ""
    for idx, t_name in enumerate(teachers_list):
        page_break_class = "page-break" if idx < len(teachers_list) - 1 else ""
        single_certs_html += f'<div class="{page_break_class}">{build_certificate_single_html(t_name)}</div>'
    
    css = CERT_CSS
    full_html = (
        '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">'
        f'<title>{cert_main_title} - مدارس الثغر النموذجية الأهلية</title>'
        f'<style>{css}</style></head><body>{single_certs_html}</body></html>'
    )
    return full_html

##### ==========================================================
##### 10. PDF File Generator Helper Function (Safe Temp Directory)
##### ==========================================================
def generate_pdf_bytes(html_content):
    try:
        temp_dir = tempfile.gettempdir()
        temp_html = os.path.join(temp_dir, f"temp_certs_{os.getpid()}.html")
        temp_pdf = os.path.join(temp_dir, f"temp_certs_{os.getpid()}.pdf")

        with open(temp_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        cmd = [
            "wkhtmltopdf",
            "--quiet",
            "--enable-local-file-access",
            "-O", "Landscape",
            "-s", "A4",
            "-T", "0", "-B", "0", "-L", "0", "-R", "0",
            temp_html,
            temp_pdf
        ]
        res = subprocess.run(cmd, capture_output=True)
        if os.path.exists(temp_pdf) and os.path.getsize(temp_pdf) > 0:
            with open(temp_pdf, "rb") as f:
                pdf_data = f.read()
            try:
                os.remove(temp_html)
                os.remove(temp_pdf)
            except Exception:
                pass
            return pdf_data
    except Exception:
        pass
    return None

##### ==========================================================
##### 11. Live Preview & PDF/HTML Export UI
##### ==========================================================
with col_preview:
    st.markdown("### 🖼️ المعاينة الحية والتصدير والطباعة")
    if not selected_teachers:
        st.warning("⚠️ يرجى اختيار معلم واحد على الأقل من القائمة لتوليد الشهادات.")
    else:
        st.markdown(f" **عدد المعلمين المحدد لإصدار شهاداتهم حالياً: ({len(selected_teachers)} معلم)** ")

        preview_tabs = st.tabs([f"📜 شهادة: {t}" for t in selected_teachers[:6]])
        for idx, tab_teacher in enumerate(selected_teachers[:6]):
            with preview_tabs[idx]:
                single_cert_html = build_full_certificates_document_html([tab_teacher])
                st.components.v1.html(single_cert_html, height=710, scrolling=True)

        if len(selected_teachers) > 6:
            st.caption(f"ℹ️ يتم عرض المعاينة لأول 6 معلمين فقط، وسيتم تضمين باقي المعلمين ({len(selected_teachers)}) في الملف المطبوع المجمع.")

        st.markdown("---")

        full_batch_html = build_full_certificates_document_html(selected_teachers)

        col_pdf, col_html = st.columns(2)

        with col_pdf:
            st.markdown("#### 📄 تصدير الشهادات كـ PDF")
            pdf_bytes = generate_pdf_bytes(full_batch_html)
            if pdf_bytes:
                st.download_button(
                    label=f"📥 📄 تحميل شهادات جميع المعلمين ({len(selected_teachers)}) كـ ملف PDF مباشر",
                    data=pdf_bytes,
                    file_name=f"Thaghr_Certificates_({len(selected_teachers)}_teachers).pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.info("ℹ️ خيار التنزيل المباشر كـ PDF يعمل عند تثبيت أداة wkhtmltopdf، ويمكنك استخدام خيار الطباعة المباشرة أدناه للتنزيل كـ PDF فوراً.")

        with col_html:
            st.markdown("#### 🖨️ تصدير وطباعة التنسيق الكامل (HTML/PDF)")
            st.download_button(
                label=f"📥 🖨️ فتح العرض المجمع للطباعة كـ PDF عبر المتصفح ({len(selected_teachers)} معلم)",
                data=full_batch_html,
                file_name=f"Thaghr_Certificates_Batch_({len(selected_teachers)}_teachers).html",
                mime="text/html",
                use_container_width=True
            )

        st.info("💡 **تلميح للتحميل والتصدير:** يمكنك النقر على زر **`📥 📄 تحميل كـ ملف PDF مباشر`**، أو استخدام زر العرض المجمع للطباعة مباشرة من المتصفح عبر (Ctrl + P) واختيار **أفقي (Landscape)** ورسومات الخلفية.")
