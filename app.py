import streamlit as st
import datetime
import base64
import os
import subprocess
import tempfile
import json
import requests

###### ==========================================================
###### 1. Page Configuration
###### ==========================================================
st.set_page_config(
    page_title="نظام إدارة وإصدار شهادات الإشراف الأكاديمي - مدارس الثغر النموذجية الأهلية",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

###### ==========================================================
###### 2. Sample Digital Signature SVG (Base64)
###### ==========================================================
_svg_str = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 70" width="220" height="70"><path d="M 15 45 C 35 12, 65 58, 95 25 C 115 5, 135 60, 165 30 C 185 10, 195 45, 210 25" fill="none" stroke="#006C35" stroke-width="3" stroke-linecap="round"/><path d="M 30 52 C 70 58, 120 50, 180 54" fill="none" stroke="#D4AF37" stroke-width="2" stroke-dasharray="4,2"/><text x="110" y="66" font-family="\'Amiri\', \'Cairo\', sans-serif" font-size="11" font-weight="bold" fill="#006C35" text-anchor="middle">توقيع رقمي معتمد ✦</text></svg>'
SAMPLE_DIGITAL_SIG_SVG = "data:image/svg+xml;base64," + base64.b64encode(_svg_str.strip().encode('utf-8')).decode('utf-8')

###### ==========================================================
###### 3. Load School Logo (embedded as base64)
###### ==========================================================
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

###### ==========================================================
###### 4. Advanced CSS for Streamlit UI (Full RTL & Modern Styling)
###### ==========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    .stApp {
        background-color: #f8fafc;
    }
    .main-header-title {
        background: linear-gradient(135deg, #006C35 0%, #0B2A4A 100%);
        color: white;
        padding: 22px 30px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0, 108, 53, 0.18);
        border: 2px solid #D4AF37;
    }
    .main-header-title h1 {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 26px !important;
        margin: 0 0 6px 0 !important;
    }
    .main-header-title p {
        color: #e2e8f0 !important;
        font-size: 15px !important;
        margin: 0 !important;
        font-weight: 600;
    }
    .designer-credit-badge {
        background: linear-gradient(135deg, #006C35 0%, #0B2A4A 100%);
        color: #ffffff;
        padding: 10px 16px;
        border-radius: 12px;
        text-align: center;
        font-weight: 800;
        font-size: 13.5px;
        border: 1px solid #D4AF37;
        margin-top: 15px;
        box-shadow: 0 4px 12px rgba(0,108,53,0.15);
    }
</style>
""", unsafe_allow_html=True)

###### ==========================================================
###### 5. Main Site Header
###### ==========================================================
_header_logo = f'<div class="mh-logo"><img src="{LOGO_SRC}" alt="logo" style="height: 65px; margin-bottom: 6px;"></div>' if LOGO_SRC else ""
st.markdown(f"""
<div class="main-header-title">
    {_header_logo}
    <h1>📜 نظام إدارة وإصدار شهادات الإشراف الأكاديمي</h1>
    <p>مدارس الثغر النموذجية الأهلية - منظومة الإصدار والتصدير الرقمي الموحد</p>
</div>
""", unsafe_allow_html=True)

if not LOGO_SRC:
    st.warning("⚠️ لم يتم العثور على ملف الشعار (thaghr_logo.png). ضعه بجانب ملف app.py لإظهار الشعار في الشهادة.")

###### ==========================================================
###### Supabase Persistence & Local File Database Helper Functions
###### ==========================================================
TEACHERS_FILE = "teachers.json"
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
]

def get_supabase_credentials():
    """الحصول الفعّال على بيانات الاتصال بـ Supabase بجميع صيغ الأسماء الممكنة في st.secrets و env"""
    url = ""
    key = ""
    try:
        if hasattr(st, "secrets") and st.secrets is not None:
            url_keys = ["SUPABASE_URL", "supabase_url", "SUPABASE_PROJECT_URL", "URL", "url"]
            key_keys = ["SUPABASE_KEY", "supabase_key", "SUPABASE_ANON_KEY", "SUPABASE_SERVICE_KEY", "KEY", "key"]

            for k in url_keys:
                try:
                    val = st.secrets.get(k, None) if hasattr(st.secrets, "get") else (st.secrets[k] if k in st.secrets else None)
                    if val:
                        url = str(val)
                        break
                except Exception:
                    pass

            for k in key_keys:
                try:
                    val = st.secrets.get(k, None) if hasattr(st.secrets, "get") else (st.secrets[k] if k in st.secrets else None)
                    if val:
                        key = str(val)
                        break
                except Exception:
                    pass

            if not url or not key:
                for table_key in ["supabase", "SUPABASE", "db", "database"]:
                    try:
                        if table_key in st.secrets:
                            tbl = st.secrets[table_key]
                            if not url:
                                for uk in ["url", "URL", "supabase_url", "SUPABASE_URL"]:
                                    if uk in tbl:
                                        url = str(tbl[uk])
                                        break
                            if not key:
                                for kk in ["key", "KEY", "anon_key", "service_key", "supabase_key", "SUPABASE_KEY"]:
                                    if kk in tbl:
                                        key = str(tbl[kk])
                                        break
                    except Exception:
                        pass
    except Exception:
        pass

    if not url:
        for k in ["SUPABASE_URL", "supabase_url"]:
            if os.getenv(k):
                url = os.getenv(k)
                break
    if not key:
        for k in ["SUPABASE_KEY", "supabase_key", "SUPABASE_ANON_KEY"]:
            if os.getenv(k):
                key = os.getenv(k)
                break

    return str(url or "").strip().rstrip('/'), str(key or "").strip()

def check_supabase_connection():
    """اختبار الاتصال الفعلي بقاعدة بيانات Supabase والتحقق من وجود الجدول ورغبة الوصول"""
    url, key = get_supabase_credentials()
    if not url or not key:
        return False, "لم يتم العثور على مفاتيح SUPABASE_URL أو SUPABASE_KEY في Secrets"
    try:
        headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        resp = requests.get(f"{url}/rest/v1/department_teachers?select=department", headers=headers, timeout=5)
        if resp.status_code == 200:
            return True, "الاتصال ناجح مع Supabase والجدول جاهز"
        elif resp.status_code in [401, 403]:
            return False, "المفتاح (API Key) غير صحيح أو لا يملك صلاحيات الوصول"
        elif resp.status_code == 404:
            return False, "جدول department_teachers غير موجود في قاعدة البيانات"
        else:
            return False, f"رمز الاستجابة من Supabase: {resp.status_code}"
    except Exception as e:
        return False, f"خطأ في شبكة الاتصال: {str(e)}"

def load_teachers_from_supabase():
    """تحميل قائمة المعلمين من قاعدة بيانات Supabase عبر REST API"""
    url, key = get_supabase_credentials()
    if not url or not key:
        return None
    try:
        headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        resp = requests.get(f"{url}/rest/v1/department_teachers?select=department,teachers", headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list) and len(data) > 0:
                res_dict = {}
                for row in data:
                    dept = row.get("department")
                    t_list = row.get("teachers", [])
                    if dept and isinstance(t_list, list):
                        res_dict[dept] = t_list
                return res_dict
            elif isinstance(data, list) and len(data) == 0:
                default_data = load_teachers_local()
                save_teachers_to_supabase(default_data)
                return default_data
    except Exception:
        pass
    return None

def save_teachers_to_supabase(dept_teachers_dict):
    """حفظ جميع الأقسام والمعلمين في قاعدة بيانات Supabase"""
    url, key = get_supabase_credentials()
    if not url or not key:
        return False
    try:
        headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates"
        }
        payload = [
            {"department": dept, "teachers": teachers} for dept, teachers in dept_teachers_dict.items()
        ]
        resp = requests.post(f"{url}/rest/v1/department_teachers", headers=headers, json=payload, timeout=5)
        if resp.status_code in [200, 201, 204]:
            return True
    except Exception:
        pass
    return False

def load_teachers_local():
    """تحميل القائمة من ملف JSON المحلي عند عدم توفر Supabase"""
    if os.path.exists(TEACHERS_FILE):
        try:
            with open(TEACHERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "القسم المتوسط بنين": list(INTERMEDIATE_TEACHERS_FROM_SOURCE),
        "القسم المتوسط بنات": ["معلم جديد"],
        "القسم الابتدائي بنين": ["معلم جديد"],
        "القسم الابتدائي بنات": ["معلم جديد"],
        "القسم الثانوي بنين": ["معلم جديد"],
        "القسم الثانوي بنات": ["معلم جديد"]
    }

def save_teachers_local(data):
    """حفظ القائمة محلياً في ملف JSON"""
    try:
        with open(TEACHERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

###### ==========================================================
###### 6. Initialize Session State with Teachers
###### ==========================================================
if "dept_teachers_dict" not in st.session_state:
    sp_data = load_teachers_from_supabase()
    if sp_data:
        default_dict = load_teachers_local()
        for dept, t_list in default_dict.items():
            if dept not in sp_data:
                sp_data[dept] = t_list
        st.session_state["dept_teachers_dict"] = sp_data
    else:
        st.session_state["dept_teachers_dict"] = load_teachers_local()

if "courses_list" not in st.session_state:
    st.session_state["courses_list"] = [
        "السياسات الإشرافية ",
        "خارطة تنفيذ الدرس ",
        "استراتيجيات التعلم النشط وزيادة مشاركة الطلاب ",
        "الذكاء الاصطناعي في التعلم Notebook LM",
        "أساليب التقويم البديل ",
        "تصميم أنشطة تعليمية بالذكاء الاصطناعي ",
        "سلم المهارات "
    ]

if "signatures_list" not in st.session_state:
    st.session_state["signatures_list"] = [
        {"role": "المدير الأكاديمي لمدارس الثغر", "name": "د. ياسين البدراوي"},
        {"role": "مشرف المرحلة الابتدائية", "name": "أ. محمد مصطفى أبو سنة"},
    ]

col_ctrl, col_preview = st.columns([0.75, 2.25])
with col_ctrl:
    st.markdown("### ⚙️ لوحة التحكم والإعدادات")
    
    # مؤشر حالة الربط بقاعدة البيانات (Supabase)
    is_connected, status_detail = check_supabase_connection()
    if is_connected:
        st.markdown("""
        <div style="background-color: #d1fae5; color: #065f46; padding: 12px 16px; border-radius: 12px; border: 1.5px solid #34d399; font-weight: 800; text-align: center; margin-bottom: 18px; font-size: 14.5px; box-shadow: 0 2px 8px rgba(52, 211, 153, 0.15);">
            🟢 حالة الاتصال: متصل بـ Supabase (الحفظ الدائم مفعل)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color: #fee2e2; color: #991b1b; padding: 12px 16px; border-radius: 12px; border: 1.5px solid #f87171; font-weight: 800; text-align: center; margin-bottom: 8px; font-size: 14.5px; box-shadow: 0 2px 8px rgba(248, 113, 113, 0.15);">
            🔴 حالة الاتصال: غير متصل بـ Supabase (حفظ محلي مؤقت)
        </div>
        <div style="font-size: 11.5px; color: #991b1b; text-align: center; margin-bottom: 18px; font-weight: 700; background: #fff5f5; padding: 6px 10px; border-radius: 8px;">
            ℹ️ {status_detail}
        </div>
        """, unsafe_allow_html=True)

    cert_type = st.radio(
        "🏷️ نوع الشهادة:",
        ["🎓 شهادة حضور تدريب", "🎖️ شهادة شكر وتقدير للمعلم"],
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
                t_clean = new_teacher_input.strip()
                if t_clean not in st.session_state["dept_teachers_dict"][selected_dept]:
                    st.session_state["dept_teachers_dict"][selected_dept].append(t_clean)
                    
                    # 1. الحفظ المحلي في ملف JSON
                    save_teachers_local(st.session_state["dept_teachers_dict"])
                    
                    # 2. الحفظ السحابي في Supabase
                    sp_saved = save_teachers_to_supabase(st.session_state["dept_teachers_dict"])
                    
                    if sp_saved:
                        st.success(f"✅ تم إضافة المعلم وحفظه دائماً في Supabase ومحلياً: {t_clean}")
                    else:
                        st.success(f"✅ تم إضافة المعلم وحفظه محلياً: {t_clean}")
                    st.rerun()

    st.markdown("---")

    if "حضور تدريب" in cert_type:
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
        cert_main_title = "شهادة حضور تدريب"
        default_body_prefix = "تشهد مدارس الثغر النموذجية الأهلية أن الأستاذ/"
        default_body_text = f"قد حضر برنامجا تدريبيا بعنوان/ \n<span class=\"course-name\">« {selected_course} »</span>\nوالتي عقدت بتاريخ {formatted_date} بواقع ({course_hours}) ساعات تدريبية وعليه مُنح هذه الشهادة متمنين له دوام التوفيق ."
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

###### ==========================================================
###### 7. Certificate Print/Export CSS (Saudi National Identity Theme)
###### ==========================================================
CERT_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Amiri:ital,wght@0,700;1,400&display=swap');

@page { 
    size: A4 landscape; 
    margin: 0; 
}

*, *:before, *:after {
    box-sizing: border-box;
}

html, body { 
    width: 100% !important; 
    height: 100% !important; 
    margin: 0 !important; 
    padding: 0 !important; 
    background-color: #ffffff; 
    font-family: 'Cairo', 'Amiri', 'Traditional Arabic', 'Tahoma', sans-serif; 
    direction: rtl; 
    text-align: center; 
    color: #0f172a; 
    -webkit-print-color-adjust: exact !important; 
    print-color-adjust: exact !important; 
    /* overflow: hidden; */ 
}

.page-break { 
    page-break-after: always; 
    break-after: page; 
    margin: 0 !important; 
    padding: 0 !important; 
}

.certificate-container { 
    width: 100% !important; 
    height: 100% !important; 
    margin: 0 !important; 
    background: #ffffff; 
    padding: 12px; 
    position: relative; 
    border: 12px solid #006C35; 
    outline: 4px solid #D4AF37; 
    outline-offset: -8px; 
    background-image: radial-gradient(circle at 50% 0%, #ffffff 0%, #fbfdfe 60%, #f3f7f5 100%); 
    direction: rtl; 
    box-shadow: none; 
}

.watermark-logo { 
    position: absolute; 
    top: 50%; 
    left: 50%; 
    transform: translate(-50%, -50%); 
    width: 320px; 
    opacity: 0.05; 
    pointer-events: none; 
    z-index: 1; 
}

.corner { 
    position: absolute; 
    width: 24px; 
    height: 24px; 
    z-index: 5; 
}
.corner-tr { top: 12px; right: 12px; border-top: 3px solid #D4AF37; border-right: 3px solid #D4AF37; border-radius: 0 6px 0 0; }
.corner-tl { top: 12px; left: 12px; border-top: 3px solid #D4AF37; border-left: 3px solid #D4AF37; border-radius: 6px 0 0 0; }
.corner-br { bottom: 12px; right: 12px; border-bottom: 3px solid #D4AF37; border-right: 3px solid #D4AF37; border-radius: 0 0 6px 0; }
.corner-bl { bottom: 12px; left: 12px; border-bottom: 3px solid #D4AF37; border-left: 3px solid #D4AF37; border-radius: 0 0 0 6px; }

.inner-border { 
    border: 2px solid #D4AF37; 
    height: 100%; 
    width: 100%; 
    padding: 12px 20px 24px 20px; 
    border-radius: 6px; 
    position: relative; 
    z-index: 2; 
    background: rgba(255,255,255,0.88); 
}

.saudi-nat-header-bar { 
    height: 4px; 
    background: linear-gradient(90deg, #006C35 0%, #004d25 35%, #D4AF37 50%, #004d25 65%, #006C35 100%); 
    border-radius: 2px; 
    margin-bottom: 6px; 
}

.cert-header-table { 
    width: 100%; 
    border-bottom: 2px solid #006C35; 
    padding-bottom: 6px; 
    margin-bottom: 8px; 
}

.header-side-rtl { 
    font-size: 13px; 
    font-weight: 700; 
    color: #1e293b; 
    line-height: 1.4; 
    text-align: right; 
    width: 32%; 
    vertical-align: middle; 
}

.header-side-ltr { 
    font-size: 13px; 
    font-weight: 700; 
    color: #1e293b; 
    line-height: 1.4; 
    text-align: left; 
    width: 32%; 
    direction: ltr; 
    vertical-align: middle; 
}

.logo-box-center { 
    text-align: center; 
    width: 36%; 
    vertical-align: middle; 
}

.saudi-title { 
    color: #006C35; 
    font-weight: 900; 
    font-size: 14.5px; 
}

.office-highlight { 
    display: inline-block; 
    background: linear-gradient(135deg, #006C35 0%, #004d25 100%); 
    color: #ffffff; 
    padding: 2px 8px; 
    border-radius: 5px; 
    font-weight: 800; 
    border: 1px solid #D4AF37; 
    font-size: 12px; 
    margin-top: 2px; 
}

.thaghr-logo-img { 
    height: 65px; 
    width: auto; 
    margin-bottom: 2px; 
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.12)); 
}

.dept-sub-badge { 
    display: inline-block; 
    font-size: 13px; 
    color: #ffffff; 
    background: linear-gradient(135deg, #006C35 0%, #0B2A4A 100%); 
    padding: 3px 16px; 
    border-radius: 12px; 
    font-weight: 700; 
    border: 1px solid #D4AF37; 
}

.cert-title-badge { 
    display: inline-block; 
    background: linear-gradient(135deg, #006C35 0%, #0B2A4A 100%); 
    color: #ffffff; 
    font-size: 24px; 
    font-weight: 900; 
    padding: 5px 44px; 
    border-radius: 26px; 
    border: 2px solid #D4AF37; 
    box-shadow: 0 4px 12px rgba(0,108,53,0.22); 
    margin: 4px auto 8px; 
    letter-spacing: 0.5px; 
}

.cert-body-box { 
    margin-bottom: 6px; 
    padding: 0 16px; 
}

.cert-prefix-text { 
    font-size: 20px; 
    font-weight: 700; 
    color: #334155; 
}

.teacher-name { 
    font-size: 29px; 
    font-weight: 900; 
    color: #006C35; 
    margin: 4px 0; 
    font-family: 'Amiri', 'Traditional Arabic', serif; 
    letter-spacing: 0.5px; 
}

.teacher-name::before, .teacher-name::after { 
    content: " ✦ "; 
    color: #D4AF37; 
    font-size: 18px; 
    vertical-align: middle; 
}

.course-name { 
    font-size: 25px; 
    font-weight: 900; 
    color: #006C35; 
    margin: 4px 0; 
    font-family: 'Amiri', 'Traditional Arabic', serif; 
    letter-spacing: 0.5px; 
    display: block; 
}

.course-name::before, .course-name::after { 
    content: " ✦ "; 
    color: #D4AF37; 
    font-size: 16px; 
    vertical-align: middle; 
}

.cert-body-text { 
    font-size: 24.5px; 
    line-height: 1.7; 
    color: #1e293b; 
    font-weight: 600; 
}

.signatures-table { 
    width: 100%; 
    margin-top: 28px; 
    direction: rtl; 
}

.sig-td { 
    text-align: center; 
    vertical-align: top; 
}

.sig-role { 
    font-size: 14px; 
    font-weight: 800; 
    color: #006C35; 
    margin-bottom: 2px; 
}

.sig-name { 
    font-size: 16px; 
    font-weight: 800; 
    color: #0f172a; 
}

.sig-img-container { 
    height: 38px; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    margin-top: 2px; 
}

.digital-signature-img { 
    max-height: 36px; 
    width: auto; 
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.15)); 
}

.school-seal { 
    display: flex; 
    flex-direction: column; 
    align-items: center; 
    margin: 0 auto; 
}

.seal-ring { 
    position: relative; 
    width: 95px; 
    height: 95px; 
    border-radius: 50%; 
    border: 3px double #006C35; 
    box-shadow: 0 0 0 3px rgba(212,175,55,0.35), inset 0 0 0 2px rgba(212,175,55,0.4); 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    background: #ffffff; 
    margin: 0 auto; 
}

.seal-logo-img { 
    width: 42px; 
    height: auto; 
    opacity: 0.92; 
}

.seal-caption { 
    margin-top: 2px; 
    font-size: 9.5px; 
    font-weight: 800; 
    color: #006C35; 
}

.cert-footer-date { 
    position: absolute; 
    bottom: 8px; 
    right: 24px; 
    font-size: 11.5px; 
    color: #64748b; 
    font-weight: 700; 
}

.cert-footer-serial { 
    position: absolute; 
    bottom: 8px; 
    left: 24px; 
    font-size: 11.5px; 
    color: #64748b; 
    font-weight: 700; 
    direction: ltr; 
}


.cert-page-wrapper {
    width: 297mm;
    height: 210mm;
    box-sizing: border-box;
    page-break-after: always !important;
    break-after: page !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    margin: 0 auto 30px auto;
    overflow: hidden;
    position: relative;
    background: #ffffff;
}

@media print {
    .no-print {
        display: none !important;
    }
    html, body {
        width: 297mm !important;
        height: 210mm !important;
        margin: 0 !important;
        padding: 0 !important;
        background: none !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }

    .cert-page-wrapper {
        margin: 0 !important;
        padding: 0 !important;
        width: 297mm !important;
        height: 210mm !important;
        page-break-after: always !important;
        break-after: page !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        overflow: hidden !important;
    }

    .certificate-container {
        width: 297mm !important;
        height: 210mm !important;
        max-width: none !important;
        margin: 0 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        box-sizing: border-box !important;
        page-break-inside: avoid;
    }
}
"""

###### ==========================================================
###### 8. Single Certificate HTML Generator
###### ==========================================================
def build_certificate_single_html(teacher_name):
    sigs_tds = ""
    for sig in chosen_signatures:
        sig_img_html = f'<div class="sig-img-container"><img src="{digital_sig_src}" class="digital-signature-img" alt="signature"></div>' if enable_digital_sig else '<div class="sig-img-container"></div>'
        sigs_tds += f'''
        <td class="sig-td">
            <div class="sig-role">{sig['role']}</div>
            <div class="sig-name">{sig['name']}</div>
            {sig_img_html}
        </td>'''

    watermark_html = f'<img class="watermark-logo" src="{LOGO_SRC}" alt="">' if LOGO_SRC else ""
    header_logo_html = f'<img class="thaghr-logo-img" src="{LOGO_SRC}" alt="logo">' if LOGO_SRC else ""
    seal_logo_html = f'<img class="seal-logo-img" src="{LOGO_SRC}" alt="">' if LOGO_SRC else ""

    seal_td_html = f'''
    <td class="sig-td" style="vertical-align: top;">
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
    </td>'''

    body_text_html = cert_custom_text.replace(chr(10), "<br>")
    body_html = f'''
    <div class="cert-prefix-text">{cert_custom_prefix}</div>
    <div class="teacher-name">{teacher_name}</div>
    <div class="cert-body-text">{body_text_html}</div>'''

    if len(chosen_signatures) == 1:
        sig = chosen_signatures[0]
        sig_img_html = f'<div class="sig-img-container"><img src="{digital_sig_src}" class="digital-signature-img" alt="signature"></div>' if enable_digital_sig else '<div class="sig-img-container"></div>'
        signatures_table_html = f'''
        <table class="signatures-table" style="width: 100%; table-layout: fixed;">
            <tr>
                <td style="width: 32%;"></td>
                <td class="sig-td" style="width: 36%; text-align: center; vertical-align: top;">
                    <div class="sig-role">{sig['role']}</div>
                    <div class="sig-name">{sig['name']}</div>
                    {sig_img_html}
                </td>
                {seal_td_html}
            </tr>
        </table>'''
    else:
        signatures_table_html = f'''
        <table class="signatures-table">
            <tr>
                {sigs_tds}
                {seal_td_html}
            </tr>
        </table>'''

    return f'''
    <div class="certificate-container">
        {watermark_html}
        <div class="corner corner-tr"></div>
        <div class="corner corner-tl"></div>
        <div class="corner corner-br"></div>
        <div class="corner corner-bl"></div>

        <div class="inner-border">
            <div class="saudi-nat-header-bar"></div>
            
            <table class="cert-header-table">
                <tr>
                    <td class="header-side-rtl">
                        <span class="saudi-title">المملكة العربية السعودية</span><br>
                        وزارة التعليم<br>
                        إدارة التعليم بمنطقة الرياض<br>
                        <span class="office-highlight">مكتب التعليم الخاص</span>
                    </td>
                    <td class="logo-box-center">
                        {header_logo_html}<br>
                        <div class="dept-sub-badge">إدارة الإشراف الأكاديمي - {selected_dept}</div>
                    </td>
                    <td class="header-side-ltr">
                        Kingdom of Saudi Arabia<br>
                        Ministry of Education<br>
                        Riyadh Education Directorate<br>
                        <strong>Private Education Office</strong>
                    </td>
                </tr>
            </table>

            <div class="cert-title-badge">{cert_main_title}</div>

            <div class="cert-body-box">
                {body_html}
            </div>

            {signatures_table_html}

            <div class="cert-footer-date">تاريخ الإصدار: {formatted_date}</div>
            <div class="cert-footer-serial">الرقم التسلسلي: THG-{formatted_date.replace("-", "")}-001</div>
        </div>
    </div>
    '''



###### ==========================================================
###### 9. Full Batch Certificates Document HTML Generator
###### ==========================================================
def build_full_certificates_document_html(teachers_list):
    single_certs_html = ""
    for idx, t_name in enumerate(teachers_list):
        single_certs_html += f'<div class="cert-page-wrapper">{build_certificate_single_html(t_name)}</div>'
    
    teachers_count = len(teachers_list)
    print_toolbar = f'''
    <div class="no-print" style="position: sticky; top: 0; z-index: 9999; background: #006C35; color: white; padding: 12px 20px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15); font-family: 'Cairo', sans-serif; margin-bottom: 20px;">
        <span style="font-size: 16px; font-weight: bold; margin-left: 15px;">📜 العرض المجمع للشهادات - عدد المعلمين ({teachers_count})</span>
        <button onclick="window.print()" style="background: #D4AF37; color: #006C35; font-size: 16px; font-weight: 800; padding: 8px 24px; border: none; border-radius: 8px; cursor: pointer; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
            🖨️ طباعة كافة الشهادات A4 (Ctrl + P) / حفظ كـ PDF
        </button>
    </div>
    '''

    css = CERT_CSS
    full_html = (
        '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">'
        f'<title>{cert_main_title} - مدارس الثغر النموذجية الأهلية</title>'
        f'<style>{css}</style></head><body>{print_toolbar}{single_certs_html}</body></html>'
    )
    return full_html

###### ==========================================================
###### 10. PDF File Generator Helper Function (Safe Temp Directory)
###### ==========================================================
def find_wkhtmltopdf_binary():
    import shutil
    p = shutil.which("wkhtmltopdf")
    if p:
        return p
    common_paths = [
        "/usr/bin/wkhtmltopdf",
        "/usr/local/bin/wkhtmltopdf",
        r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
        r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\wkhtmltopdf\bin\wkhtmltopdf.exe"),
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    return None

def generate_pdf_bytes(html_content):
    wkhtmltopdf_bin = find_wkhtmltopdf_binary()
    if not wkhtmltopdf_bin:
        return None, "لم يتم العثور على أداة wkhtmltopdf مثبتة على النظام."

    try:
        temp_dir = tempfile.gettempdir()
        temp_html = os.path.join(temp_dir, f"temp_certs_{os.getpid()}.html")
        temp_pdf = os.path.join(temp_dir, f"temp_certs_{os.getpid()}.pdf")

        with open(temp_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        cmd = [
            wkhtmltopdf_bin,
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
            return pdf_data, None
        else:
            err_msg = res.stderr.decode('utf-8', errors='ignore') if res.stderr else "فشل توليد ملف PDF."
            return None, f"خطأ من أداة wkhtmltopdf: {err_msg}"
    except Exception as e:
        return None, f"خطأ أثناء التوصيل مع wkhtmltopdf: {e}" 

###### ==========================================================
###### 11. Live Preview & PDF/HTML Export UI
###### ==========================================================
with col_preview:
    st.markdown("### 🖼️ المعاينة الحية والتصدير والطباعة")
    if not selected_teachers:
        st.warning("⚠️ يرجى اختيار معلم واحد على الأقل من القائمة لتوليد الشهادات.")
    else:
        st.markdown(f"**عدد المعلمين المحدد لإصدار شهاداتهم حالياً: ({len(selected_teachers)} معلم)**")

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
            pdf_bytes, pdf_err = generate_pdf_bytes(full_batch_html)
            if pdf_bytes:
                st.download_button(
                    label=f"📥 📄 تحميل شهادات جميع المعلمين ({len(selected_teachers)}) كـ ملف PDF مباشر",
                    data=pdf_bytes,
                    file_name=f"Thaghr_Certificates_({len(selected_teachers)}_teachers).pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ **تنبيه حول تصدير الـ PDF المباشر السيرفري:**")
                st.info(
                    "يتطلب التنزيل المباشر لملف الـ PDF من السيرفر وجود أداة **wkhtmltopdf** مثبتة على نظام التشغيل.\n\n"
                    "💡 **خطوات التثبيت السريعة:**\n"
                    "- **Linux / Ubuntu:** `sudo apt install wkhtmltopdf`\n"
                    "- **Windows / Mac:** تحميل أداة `wkhtmltopdf` وإضافتها لمسار النظام (PATH).\n\n"
                    "✨ **البديل الفوري دون الحاجة لبرامج:** يمكنك استخدام زر **فتح العرض المجمع للطباعة (HTML)** على اليسار، ثم الضغط على **طباعة (Ctrl + P)** وحفظ كـ PDF لجميع الشهادات بصفحات A4 مستقلة عبر المتصفح."
                )

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
