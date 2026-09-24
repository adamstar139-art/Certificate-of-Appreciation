import streamlit as st
import datetime
import base64
import os

### ==========================================================
### 1. Page Configuration
### ==========================================================
st.set_page_config(
    page_title="نظام إصدار شهادات المعلمين - مدارس الثغر النموذجية الأهلية",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

### ==========================================================
### 2. Load School Logo (embedded as base64 for self-contained export)
### ==========================================================
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

### ==========================================================
### 3. Advanced CSS for Streamlit UI (Saudi National Identity Accents)
### ==========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }
    
    /* Compact Control Panel Container */
    div[data-testid="column"]:first-child {
        background: #f8fafc;
        padding: 12px 16px;
        border-radius: 12px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    
    div[data-testid="column"]:first-child .stMarkdown {
        margin-bottom: -6px;
    }
    
    div[data-testid="column"]:first-child .stSelectbox, 
    div[data-testid="column"]:first-child .stTextInput,
    div[data-testid="column"]:first-child .stMultiSelect,
    div[data-testid="column"]:first-child .stNumberInput,
    div[data-testid="column"]:first-child .stDateInput {
        margin-bottom: 8px;
    }
    
    /* Saudi National Identity Header Ribbon */
    .saudi-top-bar {
        height: 6px;
        background: linear-gradient(90deg, #006C35 0%, #004d25 35%, #D4AF37 50%, #004d25 65%, #006C35 100%);
        border-radius: 4px;
        margin-bottom: 12px;
    }
    
    /* Footer Credit Badge */
    .designer-credit-badge {
        text-align: center;
        background: linear-gradient(135deg, #006C35 0%, #0B2A4A 100%);
        color: #ffffff;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 12.5px;
        font-weight: 700;
        border: 1px solid #D4AF37;
        box-shadow: 0 2px 6px rgba(0,108,53,0.2);
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

### ==========================================================
### 4. Main Site Header with Saudi National Identity Colors
### ==========================================================
_header_logo = f'<div class="mh-logo"><img src="{LOGO_SRC}" alt="logo" style="height: 70px; margin-bottom: 8px;"></div>' if LOGO_SRC else ""
st.markdown(f"""
<div class="saudi-top-bar"></div>
<div style="text-align: center; padding: 5px 0 15px 0; border-bottom: 2px solid #006C35; margin-bottom: 20px;">
    {_header_logo}
    <h1 style="color: #006C35; font-family: 'Cairo', sans-serif; margin-bottom: 4px; font-size: 25px; font-weight: 800;">📜 نظام إصدار شهادات التقدير والحضور الرقمية</h1>
    <h3 style="color: #0B2A4A; margin-top: 0; font-size: 17px; font-weight: 700;">مدارس الثغر النموذجية الأهلية</h3>
    <div style="display: inline-block; background: linear-gradient(135deg, #006C35 0%, #0B2A4A 100%); color: #ffffff; padding: 4px 18px; border-radius: 20px; font-size: 12.5px; font-weight: 700; border: 1px solid #D4AF37;">
        ✨ تصميم وتطوير: أ. محمد سامي السعيد
    </div>
</div>
""", unsafe_allow_html=True)

if not LOGO_SRC:
    st.warning("⚠️ لم يتم العثور على ملف الشعار (thaghr_logo.png). ضعه بجانب ملف app.py لإظهار الشعار في الشهادة.")

### ==========================================================
### 5. Initialize Session State
### ==========================================================
if "teachers_list" not in st.session_state:
    st.session_state["teachers_list"] = [
        "أ/ محمد سامي السعيد",
        "أ/ صالح بن عبدالله الدعجاني",
        "أ/ محمد مبروك السيد",
        "أ/ أحمد محمود علي",
        "أ/ خالد عبدالسلام عمر",
        "أ/ عبدالمجيد منصور القحطاني",
        "أ/ ياسر بن فهد الدوسري"
    ]

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
        {"role": "وكيل الشؤون التعليمية", "name": "أ. محمد مبروك السيد"},
        {"role": "وكيل شؤون الطلاب", "name": "أ. صالح بن عبدالله الدعجاني"}
    ]

# Optimized Column Layout: Compact control panel (0.75), Wide preview canvas (2.25)
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
            "القسم الابتدائي بنين",
            "القسم الابتدائي بنات",
            "القسم المتوسط بنين",
            "القسم المتوسط بنات",
            "القسم الثانوي بنين",
            "القسم الثانوي بنات"
        ],
        index=2
    )

    st.markdown("---")

    st.markdown("#### 👤 المعلمون المكرمون")

    select_all_teachers = st.checkbox("✅ تحديد جميع معلمي القائمة")
    if select_all_teachers:
        default_teachers = st.session_state["teachers_list"]
    else:
        default_teachers = [st.session_state["teachers_list"][0]]

    selected_teachers = st.multiselect(
        "اختر المعلمين لإصدار شهاداتهم معاً:",
        options=st.session_state["teachers_list"],
        default=default_teachers
    )

    with st.expander("➕ إضافة معلم جديد"):
        new_teacher_input = st.text_input("اسم المعلم الجديد:", placeholder="أ/ اكتب الاسم رباعياً...", key="input_new_teacher")
        if st.button("💾 حفظ وإضافة", key="btn_add_teacher"):
            if new_teacher_input.strip():
                if new_teacher_input.strip() not in st.session_state["teachers_list"]:
                    st.session_state["teachers_list"].append(new_teacher_input.strip())
                    st.success(f"✅ تم إضافة المعلم: {new_teacher_input.strip()}")
                    st.rerun()
                else:
                    st.warning("⚠️ هذا الاسم موجود بالفعل.")

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
        default_body_text = f"شهادة حضور وذلك لاجتيازه بنجاح الدورة التدريبية بعنوان:\n« {selected_course} »\nوالتي عقدت بتاريخ {formatted_date} بواقع ({course_hours}) ساعات تدريبية معتمدة. متمنين له دوام التوفيق والنجاح."
    else:
        st.markdown("#### 📖 التخصص / المادة")
        subject_name = st.text_input("المادة / التخصص:", value="تكنولوجيا المعلومات والتعليم الرقمي")
        formatted_date = datetime.date.today().strftime("%Y/%m/%d") + " م"
        cert_main_title = "شهادة شكر وتقدير"
        default_body_prefix = "تتقدم إدارة الإشراف الأكاديمي بمدارس الثغر النموذجية الأهلية ببالغ الشكر والتقدير للمعلم"
        default_body_text = f"تقديرًا لجهوده المتميزة وعطائه المخلص في رفع مستوى الأداء التعليمي بمادة ({subject_name})، ومشاركته الفاعلة في إنجاح الأنشطة المدرسية خلال العام الدراسي."

    st.markdown("#### 📝 تخصيص النص")
    cert_custom_prefix = st.text_input("صياغة المقطع الافتتاحي:", value=default_body_prefix)
    cert_custom_text = st.text_area("صياغة متن الشهادة:", value=default_body_text, height=100)

    st.markdown("---")

    st.markdown("#### ✍️ التوقيعات المعتمدة")
    sig_options_map = {f"{s['role']}: {s['name']}": s for s in st.session_state["signatures_list"]}
    default_sig_keys = [
        f"{st.session_state['signatures_list'][0]['role']}: {st.session_state['signatures_list'][0]['name']}",
        f"{st.session_state['signatures_list'][1]['role']}: {st.session_state['signatures_list'][1]['name']}"
    ]
    selected_sig_keys = st.multiselect(
        "اختر التوقيعات الظاهرة بالشهادة:",
        options=list(sig_options_map.keys()),
        default=default_sig_keys
    )
    chosen_signatures = [sig_options_map[k] for k in selected_sig_keys]

    with st.expander("➕ إضافة توقيع جديد"):
        new_sig_role = st.text_input("المسمى الوظيفي:", placeholder="مثال: رئيس القسم / وكيل النشاط", key="input_sig_role")
        new_sig_name = st.text_input("اسم صاحب التوقيع:", placeholder="مثال: أ. أحمد العتيبي", key="input_sig_name")
        if st.button("💾 حفظ التوقيع", key="btn_add_sig"):
            if new_sig_role.strip() and new_sig_name.strip():
                st.session_state["signatures_list"].append({"role": new_sig_role.strip(), "name": new_sig_name.strip()})
                st.success("✅ تم إضافة التوقيع بنجاح!")
                st.rerun()

    st.markdown("""
    <div class="designer-credit-badge">
        ✨ تصميم وتطوير: أ. محمد سامي السعيد
    </div>
    """, unsafe_allow_html=True)

### ==========================================================
### 6. Certificate Print/Export CSS (Saudi National Identity Theme)
### ==========================================================
CERT_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Amiri:ital,wght@0,700;1,400&display=swap');

@page {
    size: A4 landscape;
    margin: 0;
}

body {
    margin: 0;
    padding: 15px;
    background-color: #eef2f7;
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    text-align: center;
    color: #0f172a;
}

.page-break {
    page-break-after: always;
    break-after: page;
    margin-bottom: 30px;
}

.certificate-container {
    width: 980px;
    height: 650px;
    margin: 0 auto;
    background: #ffffff;
    padding: 20px;
    box-sizing: border-box;
    position: relative;
    border: 14px solid #006C35;
    outline: 4px solid #D4AF37;
    outline-offset: -9px;
    border-radius: 14px;
    box-shadow: 0 14px 38px rgba(0,0,0,0.14);
    overflow: hidden;
    background-image: radial-gradient(circle at 50% 0%, #ffffff 0%, #fbfdfe 60%, #f3f7f5 100%);
}

/* Faint Watermark Centered */
.watermark-logo {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 440px;
    height: auto;
    opacity: 0.055;
    pointer-events: none;
    z-index: 1;
}

/* Decorative Gold Corners */
.corner {
    position: absolute;
    width: 44px;
    height: 44px;
    z-index: 3;
    border-color: #D4AF37;
}
.corner-tr {
    top: 16px;
    right: 16px;
    border-top: 3px solid #D4AF37;
    border-right: 3px solid #D4AF37;
    border-radius: 0 8px 0 0;
}
.corner-tl {
    top: 16px;
    left: 16px;
    border-top: 3px solid #D4AF37;
    border-left: 3px solid #D4AF37;
    border-radius: 8px 0 0 0;
}
.corner-br {
    bottom: 16px;
    right: 16px;
    border-bottom: 3px solid #D4AF37;
    border-right: 3px solid #D4AF37;
    border-radius: 0 0 8px 0;
}
.corner-bl {
    bottom: 16px;
    left: 16px;
    border-bottom: 3px solid #D4AF37;
    border-left: 3px solid #D4AF37;
    border-radius: 0 0 0 8px;
}

.inner-border {
    border: 2px solid #D4AF37;
    height: 100%;
    padding: 12px 26px;
    box-sizing: border-box;
    border-radius: 8px;
    position: relative;
    z-index: 2;
    background: rgba(255,255,255,0.88);
}

/* Header with Saudi National Identity Colors */
.saudi-nat-header-bar {
    height: 5px;
    background: linear-gradient(90deg, #006C35 0%, #004d25 35%, #D4AF37 50%, #004d25 65%, #006C35 100%);
    border-radius: 3px;
    margin-bottom: 8px;
}

.cert-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #006C35;
    padding-bottom: 8px;
    margin-bottom: 8px;
}

.header-side {
    font-size: 11.5px;
    font-weight: 700;
    color: #1e293b;
    line-height: 1.5;
    text-align: right;
    flex: 1;
}

.header-side.left-side {
    text-align: left;
    direction: ltr;
}

.saudi-title {
    color: #006C35;
    font-weight: 900;
    font-size: 12.5px;
}

.office-highlight {
    display: inline-block;
    background: linear-gradient(135deg, #006C35 0%, #004d25 100%);
    color: #ffffff;
    padding: 2px 10px;
    border-radius: 6px;
    font-weight: 800;
    border: 1px solid #D4AF37;
    font-size: 11px;
    margin-top: 2px;
}

.logo-box-center {
    flex: 1.3;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.thaghr-logo-img {
    height: 70px;
    width: auto;
    margin-bottom: 4px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.12));
}

.dept-sub-badge {
    display: inline-block;
    font-size: 11px;
    color: #ffffff;
    background: linear-gradient(135deg, #006C35 0%, #0B2A4A 100%);
    padding: 2px 14px;
    border-radius: 12px;
    font-weight: 700;
    border: 1px solid #D4AF37;
}

.cert-title-badge {
    display: inline-block;
    background: linear-gradient(135deg, #006C35 0%, #0B2A4A 100%);
    color: #ffffff;
    font-size: 21px;
    font-weight: 900;
    padding: 5px 40px;
    border-radius: 28px;
    border: 2px solid #D4AF37;
    box-shadow: 0 4px 14px rgba(0,108,53,0.25);
    margin: 2px 0 10px;
    letter-spacing: 0.5px;
}

.cert-body-box {
    margin-bottom: 8px;
    padding: 0 16px;
}

.cert-prefix-text {
    font-size: 14.5px;
    font-weight: 700;
    color: #334155;
}

.teacher-name {
    font-size: 27px;
    font-weight: 900;
    color: #006C35;
    margin: 4px 0;
    font-family: 'Amiri', serif;
    letter-spacing: 0.5px;
    text-shadow: 1px 1px 0 rgba(212,175,55,0.3);
}

.teacher-name::before, .teacher-name::after {
    content: " ✦ ";
    color: #D4AF37;
    font-size: 16px;
    vertical-align: middle;
}

.cert-body-text {
    font-size: 15px;
    line-height: 1.8;
    color: #1e293b;
    font-weight: 600;
}

/* Signatures Section: Dots placed UNDER the name for signature */
.signatures-section {
    display: flex;
    justify-content: space-around;
    align-items: flex-start;
    margin-top: 12px;
    padding-top: 4px;
}

.sig-box {
    min-width: 170px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.sig-role {
    font-size: 12.5px;
    font-weight: 800;
    color: #006C35;
    margin-bottom: 4px;
}

.sig-name {
    font-size: 14px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 2px;
}

.sig-dots-line {
    color: #0B2A4A;
    font-weight: 800;
    font-size: 13px;
    letter-spacing: 2.5px;
    opacity: 0.75;
    margin-top: 4px;
}

/* Professional round seal with upright SVG circular text */
.school-seal {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0 8px;
}

.seal-ring {
    position: relative;
    width: 114px;
    height: 114px;
    border-radius: 50%;
    border: 3px double #006C35;
    box-shadow: 0 0 0 4px rgba(212,175,55,0.35), inset 0 0 0 2px rgba(212,175,55,0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    background: #ffffff;
    transform: rotate(-3deg);
}

.seal-logo-img {
    width: 50px;
    height: auto;
    opacity: 0.92;
}

.seal-caption {
    margin-top: 3px;
    font-size: 9px;
    font-weight: 800;
    color: #006C35;
}

.cert-footer-date {
    position: absolute;
    bottom: 8px;
    right: 28px;
    font-size: 10.5px;
    color: #64748b;
    font-weight: 700;
}

.cert-footer-serial {
    position: absolute;
    bottom: 8px;
    left: 28px;
    font-size: 10.5px;
    color: #64748b;
    font-weight: 700;
    direction: ltr;
}

@media print {
    body {
        background: none;
        padding: 0;
    }
    .page-break {
        margin-bottom: 0;
    }
    .certificate-container {
        box-shadow: none;
        width: 100%;
        max-width: 1000px;
        border-radius: 0;
    }
}
"""

### ==========================================================
### 7. Single Certificate HTML Generator
### ==========================================================
def build_certificate_single_html(teacher_name):
    sigs_html = ""
    for sig in chosen_signatures:
        sigs_html += f'''
        <div class="sig-box">
            <div class="sig-role">{sig['role']}</div>
            <div class="sig-name">{sig['name']}</div>
            <div class="sig-dots-line">. . . . . . . . . . . . . . . . . . . . .</div>
        </div>'''
    
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
                    <div class="dept-sub-badge">{selected_dept}</div>
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

            <div class="signatures-section">
                {sigs_html}
                <div class="school-seal">
                    <div class="seal-ring">
                        {seal_logo_html}
                        <svg viewBox="0 0 120 120" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;">
                            <defs>
                                <!-- Top Arc: Right to Left over top (105,60 -> 15,60) -->
                                <path id="textArcTop" d="M 105,60 A 45,45 0 0,0 15,60" fill="none"/>
                                <!-- Bottom Arc: Right to Left under bottom (105,60 -> 15,60) -->
                                <path id="textArcBottom" d="M 105,60 A 45,45 0 0,1 15,60" fill="none"/>
                            </defs>
                            <text font-size="8.5" font-weight="800" fill="#006C35" letter-spacing="0.5">
                                <textPath href="#textArcTop" startOffset="50%" text-anchor="middle">
                                    ✦ مدارس الثغر النموذجية ✦
                                </textPath>
                            </text>
                            <text font-size="8" font-weight="700" fill="#0B2A4A" letter-spacing="0.5">
                                <textPath href="#textArcBottom" startOffset="50%" text-anchor="middle">
                                    الإشراف الأكاديمي المعتمد
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

### ==========================================================
### 8. Full Batch Certificates Document HTML Generator
### ==========================================================
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

### ==========================================================
### 9. Live Preview & Batch Export UI
### ==========================================================
with col_preview:
    st.markdown("### 🖼️ المعاينة الحية والتصدير الجماعي للشهادات")
    if not selected_teachers:
        st.warning("⚠️ يرجى اختيار معلم واحد على الأقل من القائمة لتوليد الشهادات.")
    else:
        st.markdown(f"**عدد المعلمين المحدد لاصدار شهاداتهم حالياً: ({len(selected_teachers)} معلم)**")

        preview_tabs = st.tabs([f"📜 شهادة: {t}" for t in selected_teachers[:6]])
        for idx, tab_teacher in enumerate(selected_teachers[:6]):
            with preview_tabs[idx]:
                single_cert_html = build_full_certificates_document_html([tab_teacher])
                st.components.v1.html(single_cert_html, height=720, scrolling=True)

        if len(selected_teachers) > 6:
            st.caption(f"ℹ️ يتم عرض المعاينة لأول 6 معلمين فقط، وسيتم تضمين باقي المعلمين ({len(selected_teachers)}) في الملف المطبوع المجمع.")

        st.markdown("---")
        full_batch_html = build_full_certificates_document_html(selected_teachers)
        st.download_button(
            label=f"🖨️ تصدير وطباعة شهادات جميع المعلمين المحددين ({len(selected_teachers)} معلم) (HTML / PDF)",
            data=full_batch_html,
            file_name=f"Thaghr_Certificates_Batch_({len(selected_teachers)}_teachers).html",
            mime="text/html",
            use_container_width=True
        )
        st.info("💡 **تلميح الطباعة والتصدير:** عند فتح الملف المنزّل، اضغط (Ctrl + P) واختر اتجاه الطباعة **أفقي (Landscape)** لتطبع شهادة كل معلم في صفحة مستقلة A4 بدقة احترافية عالية. وتأكد من تفعيل خيار (الرسومات الخلفية / Background graphics) لإظهار الألوان والشعار.")
