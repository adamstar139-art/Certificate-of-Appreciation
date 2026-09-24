import streamlit as st
import datetime
import base64
import os

# ==========================================================
# 1. Page Configuration
# ==========================================================
st.set_page_config(
    page_title="نظام إصدار شهادات المعلمين - مدارس الثغر النموذجية الأهلية",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# 2. Load School Logo (embedded as base64 so exported HTML is self-contained)
# ==========================================================
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

# ==========================================================
# 3. Advanced Clean CSS for the Streamlit control panel (RTL)
# ==========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
    background-color: #f8fafc !important;
}

.main-header {
    background: linear-gradient(135deg, #0B2A4A 0%, #071B31 100%);
    color: #ffffff;
    padding: 20px 28px;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(11, 42, 74, 0.22);
    margin-bottom: 24px;
    border-bottom: 4px solid #D4AF37;
    text-align: center !important;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 18px;
}
.main-header .mh-logo img { height: 74px; width: auto; filter: drop-shadow(0 2px 6px rgba(0,0,0,0.3)); }
.main-header h1 { color: #ffffff !important; font-size: 24px !important; font-weight: 800 !important; margin: 6px 0 !important; }
.main-header p { color: #dbe6f2 !important; font-size: 14px !important; margin: 0 !important; }
.main-header .mh-top { font-size: 12.5px; color: #D4AF37; font-weight: 800; margin-bottom: 4px; }

label[data-testid="stWidgetLabel"] { display: block !important; width: 100% !important; margin-bottom: 6px !important; padding: 0 !important; }
label[data-testid="stWidgetLabel"] p { font-family: 'Cairo', sans-serif !important; font-size: 14.5px !important; font-weight: 700 !important; color: #0B2A4A !important; line-height: 1.5 !important; margin: 0 !important; }

div[data-testid="stTextInput"], div[data-testid="stSelectbox"], div[data-testid="stMultiSelect"],
div[data-testid="stTextArea"], div[data-testid="stNumberInput"], div[data-testid="stDateInput"] {
    margin-bottom: 14px !important; clear: both !important;
}

div[data-testid="stExpander"] { background-color: #ffffff !important; border: 1px solid #cbd5e1 !important; border-radius: 12px !important; margin-bottom: 16px !important; box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important; overflow: hidden !important; }
div[data-testid="stExpander"] details summary { padding: 12px 16px !important; background-color: #f8fafc !important; border-bottom: 1px solid #e2e8f0 !important; color: #0B2A4A !important; font-weight: 700 !important; font-size: 15px !important; cursor: pointer !important; }
div[data-testid="stExpander"] details summary:hover { background-color: #eff6ff !important; color: #0B2A4A !important; }
div[data-testid="stExpander"] details summary p { font-size: 15px !important; font-weight: 700 !important; color: #0B2A4A !important; margin: 0 !important; line-height: 1.5 !important; display: inline-block !important; }

.stMultiSelect [data-baseweb="tag"] { background-color: #0B2A4A !important; color: #ffffff !important; border-radius: 6px !important; padding: 4px 10px !important; font-weight: 700 !important; font-size: 13px !important; }

div[role="radiogroup"] { display: flex !important; flex-direction: column !important; gap: 10px !important; margin-top: 6px !important; }
div[role="radiogroup"] label { background: #ffffff !important; padding: 10px 14px !important; border-radius: 10px !important; border: 1px solid #cbd5e1 !important; margin: 0 !important; display: flex !important; align-items: center !important; gap: 8px !important; box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important; cursor: pointer !important; }
div[role="radiogroup"] label:hover { border-color: #0B2A4A !important; background-color: #eff6ff !important; }

.stButton > button { font-family: 'Cairo', sans-serif !important; font-weight: 700 !important; border-radius: 10px !important; padding: 10px 22px !important; background: linear-gradient(135deg, #0B2A4A 0%, #16457a 100%) !important; color: #ffffff !important; border: none !important; box-shadow: 0 4px 12px rgba(11, 42, 74, 0.2) !important; width: 100% !important; transition: all 0.2s ease !important; }
.stButton > button:hover { background: linear-gradient(135deg, #16457a 0%, #0B2A4A 100%) !important; transform: translateY(-2px) !important; box-shadow: 0 6px 16px rgba(11, 42, 74, 0.3) !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# 4. Main Site Header (with real school logo)
# ==========================================================
_header_logo = f'<div class="mh-logo"><img src="{LOGO_SRC}" alt="logo"></div>' if LOGO_SRC else ""
st.markdown(f"""
<div class="main-header">
    {_header_logo}
    <div>
        <div class="mh-top">المملكة العربية السعودية • وزارة التعليم • إدارة التعليم بمنطقة الرياض • مكتب التعليم الخاص</div>
        <h1>📜 نظام إصدار وطباعة شهادات المعلمين المعتمدة</h1>
        <p>إدارة الإشراف الأكاديمي بمدارس الثغر النموذجية الأهلية</p>
    </div>
</div>
""", unsafe_allow_html=True)

if not LOGO_SRC:
    st.warning("⚠️ لم يتم العثور على ملف الشعار (thaghr_logo.png). ضعه بجانب ملف app.py لإظهار الشعار في الشهادة.")

# ==========================================================
# 5. Initialize Session State
# ==========================================================
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

col_ctrl, col_preview = st.columns([1.1, 1.9])

with col_ctrl:
    st.markdown("### ⚙️ لوحة التحكم وإعدادات الشهادة")

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

    st.markdown("#### 👤 اختيار المعلمين المكرمين")

    select_all_teachers = st.checkbox("✅ تحديد جميع معلمي القائمة")
    if select_all_teachers:
        default_teachers = st.session_state["teachers_list"]
    else:
        default_teachers = [st.session_state["teachers_list"][0]]

    selected_teachers = st.multiselect(
        "اختر المعلمين المحددين لإصدار شهاداتهم معاً:",
        options=st.session_state["teachers_list"],
        default=default_teachers
    )

    with st.expander("➕ إضافة معلم جديد للقائمة"):
        new_teacher_input = st.text_input("اسم المعلم الجديد:", placeholder="أ/ اكتب الاسم رباعياً...", key="input_new_teacher")
        if st.button("💾 حفظ وإضافة المعلم", key="btn_add_teacher"):
            if new_teacher_input.strip():
                if new_teacher_input.strip() not in st.session_state["teachers_list"]:
                    st.session_state["teachers_list"].append(new_teacher_input.strip())
                    st.success(f"✅ تم إضافة المعلم: {new_teacher_input.strip()}")
                    st.rerun()
                else:
                    st.warning("⚠️ هذا الاسم موجود بالفعل.")

    st.markdown("---")

    if "حضور دورة" in cert_type:
        st.markdown("#### 📚 اختيار / إضافة الدورة التدريبية")
        selected_course = st.selectbox(
            "اختر الدورة من القائمة المنسدلة:",
            st.session_state["courses_list"]
        )
        with st.expander("➕ إضافة دورة تدريبية جديدة"):
            new_course_input = st.text_input("عنوان الدورة الجديد:", placeholder="اكتب عنوان الدورة...", key="input_new_course")
            if st.button("💾 حفظ وإضافة الدورة", key="btn_add_course"):
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

    st.markdown("#### 📝 تخصيص نص الشهادة")
    cert_custom_prefix = st.text_input("صياغة المقطع الافتتاحي:", value=default_body_prefix)
    cert_custom_text = st.text_area("صياغة متن الشهادة:", value=default_body_text, height=110)

    st.markdown("---")

    st.markdown("#### ✍️ التوقيعات المعتمدة أسفل الشهادة")
    sig_options_map = {f"{s['role']}: {s['name']}": s for s in st.session_state["signatures_list"]}
    default_sig_keys = [
        f"{st.session_state['signatures_list'][0]['role']}: {st.session_state['signatures_list'][0]['name']}",
        f"{st.session_state['signatures_list'][1]['role']}: {st.session_state['signatures_list'][1]['name']}"
    ]
    selected_sig_keys = st.multiselect(
        "اختر الأسماء والمسميات الوظيفية التي تظهر أسفل الشهادة:",
        options=list(sig_options_map.keys()),
        default=default_sig_keys
    )
    chosen_signatures = [sig_options_map[k] for k in selected_sig_keys]

    with st.expander("➕ إضافة مسمى وظيفي وتوقيع جديد"):
        new_sig_role = st.text_input("المسمى الوظيفي:", placeholder="مثال: رئيس القسم / وكيل النشاط", key="input_sig_role")
        new_sig_name = st.text_input("اسم صاحب التوقيع:", placeholder="مثال: أ. أحمد العتيبي", key="input_sig_name")
        if st.button("💾 حفظ التوقيع الجديد", key="btn_add_sig"):
            if new_sig_role.strip() and new_sig_name.strip():
                st.session_state["signatures_list"].append({"role": new_sig_role.strip(), "name": new_sig_name.strip()})
                st.success("✅ تم إضافة التوقيع بنجاح!")
                st.rerun()

# ==========================================================
# 6. Single Certificate HTML Generator (with logo header, watermark & pro seal)
# ==========================================================
def build_certificate_single_html(teacher_name):
    sigs_html = ""
    for sig in chosen_signatures:
        sigs_html += f'''
        <div class="sig-box">
            <div class="sig-role">{sig['role']}</div>
            <div class="sig-space"></div>
            <div class="sig-name">{sig['name']}</div>
        </div>'''

    body_text_html = cert_custom_text.replace("\n", "<br>")
    body_html = f'''
    <div class="cert-prefix-text">{cert_custom_prefix}</div>
    <div class="teacher-name">{teacher_name}</div>
    <div class="cert-body-text">{body_text_html}</div>'''

    # Real logo in header center + faint background watermark
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
        <div class="cert-header">
            <div class="header-side">
                المملكة العربية السعودية<br>
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
                    <span class="seal-star seal-star-top">✦</span>
                    <span class="seal-star seal-star-bottom">✦</span>
                    {seal_logo_html}
                    <div class="seal-arc-top">✦ مدارس الثغر النموذجية ✦</div>
                    <div class="seal-arc-bottom">الإشراف الأكاديمي المعتمد</div>
                </div>
                <div class="seal-caption">ختم معتمد</div>
            </div>
        </div>

        <div class="cert-footer-date">تاريخ الإصدار: {formatted_date}</div>
        <div class="cert-footer-serial">رقم الوثيقة: TH-{abs(hash(teacher_name)) % 900000 + 100000}</div>
    </div>
</div>'''

# ==========================================================
# 7. Full Batch Certificates Document HTML Generator
# ==========================================================
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

# ==========================================================
# 8. Certificate print/export CSS (navy + gold professional theme)
# ==========================================================
CERT_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Amiri:ital,wght@0,700;1,400&display=swap');
@page { size: A4 landscape; margin: 0; }
body { margin: 0; padding: 15px; background-color: #eef2f7; font-family: 'Cairo', sans-serif; direction: rtl; text-align: center; color: #0f172a; }
.page-break { page-break-after: always; break-after: page; margin-bottom: 30px; }

.certificate-container {
    width: 1000px; height: 675px; margin: 0 auto; background: #ffffff;
    padding: 20px; box-sizing: border-box; position: relative;
    border: 14px solid #0B2A4A; outline: 4px solid #D4AF37; outline-offset: -9px;
    border-radius: 14px; box-shadow: 0 14px 38px rgba(0,0,0,0.14); overflow: hidden;
    background-image: radial-gradient(circle at 50% 0%, #ffffff 0%, #fbfcfe 60%, #f4f7fb 100%);
}

/* faint school logo watermark centered */
.watermark-logo { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    width: 460px; height: auto; opacity: 0.06; pointer-events: none; z-index: 1; filter: grayscale(10%); }

/* decorative gold corners */
.corner { position: absolute; width: 46px; height: 46px; z-index: 3; border-color: #D4AF37; }
.corner-tr { top: 16px; right: 16px; border-top: 3px solid #D4AF37; border-right: 3px solid #D4AF37; border-radius: 0 8px 0 0; }
.corner-tl { top: 16px; left: 16px; border-top: 3px solid #D4AF37; border-left: 3px solid #D4AF37; border-radius: 8px 0 0 0; }
.corner-br { bottom: 16px; right: 16px; border-bottom: 3px solid #D4AF37; border-right: 3px solid #D4AF37; border-radius: 0 0 8px 0; }
.corner-bl { bottom: 16px; left: 16px; border-bottom: 3px solid #D4AF37; border-left: 3px solid #D4AF37; border-radius: 0 0 0 8px; }

.inner-border { border: 2px solid #D4AF37; height: 100%; padding: 16px 30px; box-sizing: border-box;
    border-radius: 8px; position: relative; z-index: 2; background: rgba(255,255,255,0.86); }

.cert-header { display: flex; justify-content: space-between; align-items: center;
    border-bottom: 2px solid #0B2A4A; padding-bottom: 8px; margin-bottom: 10px; }
.header-side { font-size: 11.5px; font-weight: 700; color: #334155; line-height: 1.5; text-align: right; flex: 1; }
.header-side.left-side { text-align: left; direction: ltr; }
.office-highlight { color: #0B2A4A; font-weight: 800; }

.logo-box-center { flex: 1.3; text-align: center; display: flex; flex-direction: column; align-items: center; }
.thaghr-logo-img { height: 76px; width: auto; margin-bottom: 4px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.15)); }
.dept-sub-badge { display: inline-block; font-size: 11px; color: #ffffff;
    background: linear-gradient(135deg,#0B2A4A,#16457a); padding: 2px 12px; border-radius: 12px;
    font-weight: 700; border: 1px solid #D4AF37; }

.cert-title-badge { display: inline-block; background: linear-gradient(135deg, #0B2A4A 0%, #071B31 100%);
    color: #ffffff; font-size: 22px; font-weight: 900; padding: 6px 42px; border-radius: 28px;
    border: 2px solid #D4AF37; box-shadow: 0 4px 14px rgba(11,42,74,0.25); margin: 4px 0 12px; letter-spacing: 0.5px; }

.cert-body-box { margin-bottom: 12px; padding: 0 18px; }
.cert-prefix-text { font-size: 15px; font-weight: 700; color: #334155; }
.teacher-name { font-size: 28px; font-weight: 900; color: #0B2A4A; margin: 6px 0;
    font-family: 'Amiri', serif; letter-spacing: 0.5px; text-shadow: 1px 1px 0 rgba(212,175,55,0.25); }
.teacher-name::before, .teacher-name::after { content: " ✦ "; color: #D4AF37; font-size: 16px; vertical-align: middle; }
.cert-body-text { font-size: 15.5px; line-height: 1.85; color: #1e293b; font-weight: 600; }

.signatures-section { display: flex; justify-content: space-around; align-items: flex-end; margin-top: 16px; padding-top: 8px; }
.sig-box { min-width: 165px; text-align: center; }
.sig-role { font-size: 12.5px; font-weight: 800; color: #0B2A4A; margin-bottom: 4px; }
.sig-space { height: 26px; }
.sig-name { font-size: 13.5px; font-weight: 800; color: #0f172a; border-top: 1.5px dashed #94a3b8; padding-top: 5px; }

/* professional round seal with real logo */
.school-seal { display: flex; flex-direction: column; align-items: center; margin: 0 8px; }
.seal-ring { position: relative; width: 118px; height: 118px; border-radius: 50%;
    border: 3px double #0B2A4A; box-shadow: 0 0 0 4px rgba(212,175,55,0.35), inset 0 0 0 2px rgba(212,175,55,0.4);
    display: flex; align-items: center; justify-content: center; background: #ffffff; transform: rotate(-4deg); }
.seal-logo-img { width: 52px; height: auto; opacity: 0.92; }
.seal-arc-top { position: absolute; top: 9px; left: 0; right: 0; text-align: center;
    font-size: 7.5px; font-weight: 800; color: #0B2A4A; }
.seal-arc-bottom { position: absolute; bottom: 9px; left: 0; right: 0; text-align: center;
    font-size: 7px; font-weight: 700; color: #D4AF37; }
.seal-star { position: absolute; color: #D4AF37; font-size: 9px; }
.seal-star-top { top: 22px; }
.seal-star-bottom { bottom: 22px; }
.seal-caption { margin-top: 4px; font-size: 9px; font-weight: 800; color: #0B2A4A; }

.cert-footer-date { position: absolute; bottom: 8px; right: 30px; font-size: 10.5px; color: #64748b; font-weight: 700; }
.cert-footer-serial { position: absolute; bottom: 8px; left: 30px; font-size: 10.5px; color: #64748b; font-weight: 700; direction: ltr; }

@media print {
    body { background: none; padding: 0; }
    .page-break { margin-bottom: 0; }
    .certificate-container { box-shadow: none; width: 100%; height: 100vh; border-radius: 0; }
}
"""

# ==========================================================
# 9. Live Preview & Batch Export UI
# ==========================================================
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
