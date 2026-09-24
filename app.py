import streamlit as st
import datetime

# 1. إعداد الصفحة العامة
st.set_page_config(
    page_title="نظام إصدار شهادات المعلمين - مدارس الثغر النموذجية الأهلية",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تنسيقات CSS احترافية لحل مشكلة تداخل النصوص في الأيقونات والقوائم
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800;900&display=swap');

html, body, [class*="css"], div, p, span, button, input, select, textarea {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}

.stApp {
    background-color: #f8fafc;
}

/* إصلاح تداخل النصوص والأيقونات في القوائم والأزرار */
.stRadio > label, .stSelectbox > label, .stMultiSelect > label, .stTextInput > label, .stTextArea > label {
    font-size: 15px !important;
    font-weight: 700 !important;
    color: #005A2B !important;
    margin-bottom: 8px !important;
}

/* ضبط المسافات في أزرار الراديو لمنع التداخل */
div[data-testid="stMarkdownContainer"] p {
    margin-bottom: 4px !important;
    line-height: 1.6 !important;
}

div[role="radiogroup"] {
    gap: 12px !important;
    padding: 6px 0 !important;
}

div[role="radiogroup"] label {
    background: #ffffff !important;
    padding: 10px 16px !important;
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
    transition: all 0.2s ease !important;
    margin-left: 8px !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.03) !important;
}

div[role="radiogroup"] label:hover {
    border-color: #005A2B !important;
    background: #f0fdf4 !important;
}

/* تحسين عناصر الاختيار المتعدد MultiSelect */
.stMultiSelect [data-baseweb="tag"] {
    background-color: #005A2B !important;
    color: #ffffff !important;
    border-radius: 6px !important;
    padding: 4px 8px !important;
    font-weight: 700 !important;
}

/* الهيدر الرئيسي للموقع */
.main-header {
    background: linear-gradient(135deg, #005A2B 0%, #00381B 100%);
    color: white;
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0, 90, 43, 0.18);
    margin-bottom: 24px;
    border-bottom: 4px solid #D4AF37;
    text-align: center !important;
}

.main-header h1 {
    color: #ffffff !important;
    font-size: 26px !important;
    font-weight: 800 !important;
    margin: 6px 0 !important;
    text-align: center !important;
}

.main-header p {
    color: #f1f5f9 !important;
    font-size: 14px !important;
    margin: 0 !important;
    text-align: center !important;
}

/* تحسين الأزرار */
.stButton > button {
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    background: linear-gradient(135deg, #005A2B 0%, #007A3D 100%) !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(0, 90, 43, 0.2) !important;
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #007A3D 0%, #004D25 100%) !important;
    transform: translateY(-2px);
}

.stExpander {
    background: #ffffff;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# 3. الهيدر العادي بالهوية الوطنية
st.markdown("""
<div class="main-header">
    <div style="font-size: 13px; color: #D4AF37; font-weight: 800; margin-bottom: 4px;">المملكة العربية السعودية • وزارة التعليم • إدارة التعليم بمنطقة الرياض • مكتب التعليم الخاص</div>
    <h1>📜 نظام إصدار وطباعة شهادات المعلمين المعتمدة</h1>
    <p>إدارة الإشراف الأكاديمي بمدارس الثغر النموذجية الأهلية</p>
</div>
""", unsafe_allow_html=True)

# 4. إدارة حالة الجلسة (st.session_state)
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
        {"role": "المدير الأكاديمي", "name": "د. ياسين البدراوي"},
        {"role": "مدير المدرسة", "name": "أ. إبراهيم بن موسى التميمي"},
        {"role": "وكيل الشؤون التعليمية", "name": "أ. محمد مبروك السيد"},
        {"role": "وكيل شؤون الطلاب", "name": "أ. صالح بن عبدالله الدعجاني"}
    ]

# تقسيم الصفحة إلى لوحة تحكم ومعاينة
col_ctrl, col_preview = st.columns([1.1, 1.9])

with col_ctrl:
    st.markdown("### ⚙️ لوحة التحكم وإعدادات الشهادة")
    
    # 1. نوع الشهادة بأيقونات واضحة دون تداخل
    cert_type = st.radio(
        "🏷️ اختر نوع الشهادة المراد إصدارها:",
        ["🎓 شهادة حضور دورة تدريبية", "🎖️ شهادة شكر وتقدير للمعلم"],
        index=0
    )
    
    st.markdown("---")
    
    # 2. القائمة المنسدلة لاختيار القسم / المرحلة
    selected_dept = st.selectbox(
        "🏢 اختر القسم / المرحلة الدراسية:",
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
    
    # 3. اختيار المعلمين (دعم اختيار معلم واحد أو أكثر لتصديرهم دفعة واحدة)
    st.markdown("#### 👥 اختيار المعلمين المكرمين")
    
    select_all_teachers = st.checkbox("✅ تحديد جميع المعلمين القائمة")
    
    if select_all_teachers:
        default_teachers = st.session_state["teachers_list"]
    else:
        default_teachers = [st.session_state["teachers_list"][0]]
        
    selected_teachers = st.multiselect(
        "اختر اسم معلم أو أكثر لإصدار شهاداتهم معاً:",
        options=st.session_state["teachers_list"],
        default=default_teachers
    )
    
    with st.expander("➕ أيقونة إضافة معلم جديد للقائمة"):
        new_teacher_input = st.text_input("اسم المعلم الجديد:", placeholder="أ/ اكتب الاسم رباعياً...")
        if st.button("💾 إضافة المعلم", key="btn_add_teacher"):
            if new_teacher_input.strip():
                if new_teacher_input.strip() not in st.session_state["teachers_list"]:
                    st.session_state["teachers_list"].append(new_teacher_input.strip())
                    st.success(f"✅ تم إضافة المعلم: {new_teacher_input.strip()}")
                    st.rerun()
                else:
                    st.warning("⚠️ هذا الاسم موجود بالفعل.")

    st.markdown("---")
    
    # 4. إعدادات الدورة أو التخصص
    if "حضور دورة" in cert_type:
        st.markdown("#### 📚 اختيار / إضافة الدورة التدريبية")
        selected_course = st.selectbox(
            "اختر اسم الدورة من القائمة المنسدلة:",
            st.session_state["courses_list"]
        )
        
        with st.expander("➕ أيقونة إضافة دورة تدريبية جديدة"):
            new_course_input = st.text_input("عنوان الدورة الجديد:", placeholder="اكتب عنوان الدورة...")
            if st.button("💾 إضافة الدورة", key="btn_add_course"):
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
        
        # النص المطلوب تحديداً عند حضور الدورة
        default_body_prefix = "يسر إدارة الإشراف الأكاديمي بمدارس الثغر النموذجية الأهلية منح المعلم"
        default_body_text = f"شهادة حضور وذلك لاجتيازه بنجاح الدورة التدريبية بعنوان:\n« {selected_course} »\nوالتي عقدت بتاريخ {formatted_date} بواقع ({course_hours}) ساعات تدريبية معتمدة. متمنين له دوام التوفيق والنجاح."
    else:
        st.markdown("#### 📖 التخصص / المادة")
        subject_name = st.text_input("المادة / التخصص:", value="تكنولوجيا المعلومات والتعليم الرقمي")
        formatted_date = datetime.date.today().strftime("%Y/%m/%d") + " م"
        cert_main_title = "شهادة شكر وتقدير"
        
        default_body_prefix = "تتقدم إدارة الإشراف الأكاديمي بمدارس الثغر النموذجية الأهلية ببالغ الشكر والتقدير للمعلم"
        default_body_text = f"تقديرًا لجهوده المتميزة وعطائه المخلص في رفع مستوى الأداء التعليمي بمادة ({subject_name})، ومشاركته الفاعلة في إنجاح الأنشطة المدرسية خلال العام الدراسي."

    # 5. أيقونة تعديل النص الظاهر في الشهادة
    st.markdown("#### 📝 أيقونة تخصيص النص الظاهر بالشهادة")
    cert_custom_prefix = st.text_input("صياغة المقطع الافتتاحي:", value=default_body_prefix)
    cert_custom_text = st.text_area("صياغة متن الشهادة:", value=default_body_text, height=110)

    st.markdown("---")

    # 6. اختيار وتخصيص التوقيعات بأسفل الشهادة
    st.markdown("#### ✍️ أيقونة تحديد التوقيعات المعتمدة بأسفل الشهادة")
    
    sig_options_map = {f"{s['role']}: {s['name']}": s for s in st.session_state["signatures_list"]}
    
    default_sig_keys = [
        f"{st.session_state['signatures_list'][0]['role']}: {st.session_state['signatures_list'][0]['name']}",
        f"{st.session_state['signatures_list'][1]['role']}: {st.session_state['signatures_list'][1]['name']}"
    ]
    
    selected_sig_keys = st.multiselect(
        "📌 اختر الأسماء والتوقيعات التي تظهر في نهاية الشهادة:",
        options=list(sig_options_map.keys()),
        default=default_sig_keys
    )
    
    chosen_signatures = [sig_options_map[k] for k in selected_sig_keys]
    
    with st.expander("➕ أيقونة إضافة توقيع جديد (المسمى والاسم)"):
        new_sig_role = st.text_input("المسمى الوظيفي:", placeholder="مثال: رئيس القسم / وكيل النشاط")
        new_sig_name = st.text_input("اسم صاحب التوقيع:", placeholder="مثال: أ. أحمد العتيبي")
        if st.button("💾 حفظ التوقيع", key="btn_add_sig"):
            if new_sig_role.strip() and new_sig_name.strip():
                new_sig_obj = {"role": new_sig_role.strip(), "name": new_sig_name.strip()}
                st.session_state["signatures_list"].append(new_sig_obj)
                st.success("✅ تم إضافة التوقيع بنجاح!")
                st.rerun()

# 5. دالة توليد HTML لشهادة معلم واحد (مع شعار لوجو الثغر بوسط الديباجة وبخلفية العلامة المائية)
def build_certificate_single_html(teacher_name):
    sigs_html = ""
    for sig in chosen_signatures:
        sigs_html += f"""
        <div class="sig-box">
            <div class="sig-role">{sig['role']}</div>
            <div style="height: 28px;"></div>
            <div class="sig-name">{sig['name']}</div>
        </div>
        """

    # تنسيق نص الشهادة
    body_html = f"""
    <div class="cert-prefix-text">{cert_custom_prefix}</div>
    <div class="teacher-name">{teacher_name}</div>
    <div class="cert-body-text">{cert_custom_text.replace('\n', '<br>')}</div>
    """

    return f"""
<div class="certificate-container">
    <!-- شعار لوجو الثغر-02 في خلفية الشهادة (علامة مائية خفيفة شفافة) -->
    <svg class="watermark-logo" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="100" r="88" fill="none" stroke="#005A2B" stroke-width="4" stroke-dasharray="6,4" opacity="0.4"/>
        <circle cx="100" cy="100" r="76" fill="#005A2B" opacity="0.06"/>
        <!-- كتاب مفتوح -->
        <path d="M 40 120 Q 100 145 160 120 L 160 100 Q 100 125 40 100 Z" fill="#D4AF37" opacity="0.3"/>
        <path d="M 45 105 L 100 55 L 155 105 Q 100 88 45 105 Z" fill="#005A2B" opacity="0.2"/>
        <circle cx="100" cy="45" r="10" fill="#D4AF37" opacity="0.4"/>
    </svg>

    <div class="inner-border">
        <!-- الترويسة الوطنية المحدثة التي تحتوي على مكتب التعليم الخاص وشعار لوجو الثغر بوسط الديباجة -->
        <div class="cert-header">
            <div class="header-side">
                المملكة العربية السعودية<br>
                وزارة التعليم<br>
                إدارة التعليم بمنطقة الرياض<br>
                <span class="office-highlight">مكتب التعليم الخاص</span>
            </div>
            
            <!-- شعار لوجو الثغر-02 بوسط الديباجة بالأعلى -->
            <div class="logo-box-center">
                <div class="thaghr-logo-badge">
                    <svg width="42" height="42" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="50" cy="50" r="46" fill="#005A2B" stroke="#D4AF37" stroke-width="3"/>
                        <!-- رسم رمز الكتاب والقمة المتألقة لشعار الثغر -->
                        <path d="M 20 65 Q 50 80 80 65 L 80 52 Q 50 67 20 52 Z" fill="#D4AF37"/>
                        <path d="M 25 55 L 50 25 L 75 55 Q 50 42 25 55 Z" fill="#ffffff"/>
                        <circle cx="50" cy="20" r="6" fill="#D4AF37"/>
                    </svg>
                </div>
                <div class="school-dept-title">مدارس الثغر النموذجية الأهلية</div>
                <div class="dept-sub-badge">{selected_dept}</div>
            </div>
            
            <div class="header-side left-side">
                Kingdom of Saudi Arabia<br>
                Ministry of Education<br>
                Riyadh Education Directorate<br>
                <strong>Private Education Office</strong>
            </div>
        </div>

        <!-- عنوان الشهادة الرئيسي -->
        <div class="cert-title-badge">{cert_main_title}</div>

        <!-- نص الشهادة الفاخر -->
        <div class="cert-body-box">
            {body_html}
        </div>

        <!-- التوقيعات المعتمدة الديناميكية والختم الرسمي -->
        <div class="signatures-section">
            {sigs_html}

            <div class="school-seal">
                <div>مدارس الثغر</div>
                <div style="font-size: 13px; margin: 2px 0; color: #D4AF37;">🏫</div>
                <div>مكتب التعليم الخاص</div>
            </div>
        </div>

        <div class="cert-footer-date">
            تاريخ الإصدار: {formatted_date}
        </div>
    </div>
</div>
"""

# 6. دالة تجميع شهادات جميع المعلمين في مستند واحد مجهز للطباعة والتصدير A4
def build_full_certificates_document_html(teachers_list):
    single_certs_html = ""
    for idx, t_name in enumerate(teachers_list):
        page_break_class = "page-break" if idx < len(teachers_list) - 1 else ""
        single_certs_html += f"""
        <div class="{page_break_class}">
            {build_certificate_single_html(t_name)}
        </div>
        """

    full_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>{cert_main_title} - مدارس الثغر النموذجية الأهلية</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Amiri:ital,wght@0,700;1,400&display=swap');
        
        @page {{
            size: A4 landscape;
            margin: 0;
        }}
        
        body {{
            margin: 0;
            padding: 15px;
            background-color: #f1f5f9;
            font-family: 'Cairo', sans-serif;
            direction: rtl;
            text-align: center;
            color: #0f172a;
        }}
        
        .page-break {{
            page-break-after: always;
            break-after: page;
            margin-bottom: 30px;
        }}
        
        .certificate-container {{
            width: 1000px;
            height: 670px;
            margin: 0 auto;
            background: #ffffff;
            padding: 22px;
            box-sizing: border-box;
            position: relative;
            border: 12px solid #005A2B;
            outline: 4px solid #D4AF37;
            outline-offset: -8px;
            border-radius: 12px;
            box-shadow: 0 12px 32px rgba(0,0,0,0.1);
            overflow: hidden;
            background-color: #ffffff;
        }}
        
        /* العلامة المائية الشفافة بشعار الثغر في الخلفية */
        .watermark-logo {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 480px;
            height: 480px;
            pointer-events: none;
            z-index: 1;
        }}
        
        .inner-border {{
            border: 2px solid #D4AF37;
            height: 100%;
            padding: 18px 30px;
            box-sizing: border-box;
            border-radius: 6px;
            position: relative;
            z-index: 2;
            background: rgba(255, 255, 255, 0.95);
        }}
        
        /* الترويسة الوطنية شاملة مكتب التعليم الخاص */
        .cert-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #005A2B;
            padding-bottom: 8px;
            margin-bottom: 12px;
        }}
        
        .header-side {{
            font-size: 11.5px;
            font-weight: 700;
            color: #334155;
            line-height: 1.5;
            text-align: right;
            flex: 1;
        }}

        .header-side.left-side {{
            text-align: left;
        }}

        .office-highlight {{
            color: #005A2B;
            font-weight: 800;
        }}

        /* شعار لوجو الثغر بوسط الديباجة */
        .logo-box-center {{
            flex: 1.2;
            text-align: center;
        }}

        .thaghr-logo-badge {{
            display: inline-block;
            margin-bottom: 2px;
        }}

        .school-dept-title {{
            font-size: 15px;
            font-weight: 900;
            color: #005A2B;
            margin-top: 2px;
        }}

        .dept-sub-badge {{
            display: inline-block;
            font-size: 11px;
            color: #ffffff;
            background: #005A2B;
            padding: 2px 10px;
            border-radius: 12px;
            font-weight: 700;
            margin-top: 3px;
        }}
        
        /* عنوان الشهادة */
        .cert-title-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #005A2B 0%, #00381B 100%);
            color: #ffffff;
            font-size: 21px;
            font-weight: 900;
            padding: 5px 38px;
            border-radius: 25px;
            border: 2px solid #D4AF37;
            box-shadow: 0 4px 12px rgba(0, 90, 43, 0.2);
            margin-top: 6px;
            margin-bottom: 14px;
        }}
        
        /* نص الشهادة */
        .cert-body-box {{
            margin-bottom: 15px;
            padding: 0 15px;
        }}

        .cert-prefix-text {{
            font-size: 15px;
            font-weight: 700;
            color: #334155;
        }}
        
        .teacher-name {{
            font-size: 27px;
            font-weight: 900;
            color: #005A2B;
            margin: 6px 0;
            font-family: 'Amiri', serif;
            letter-spacing: 0.5px;
            text-shadow: 1px 1px 0px rgba(212, 175, 55, 0.25);
        }}

        .cert-body-text {{
            font-size: 15.5px;
            line-height: 1.8;
            color: #1e293b;
            font-weight: 600;
        }}
        
        /* التوقيعات والاعتماد بأسفل الشهادة */
        .signatures-section {{
            display: flex;
            justify-content: space-around;
            align-items: flex-end;
            margin-top: 20px;
            padding-top: 8px;
        }}
        
        .sig-box {{
            min-width: 170px;
            text-align: center;
        }}
        
        .sig-role {{
            font-size: 12.5px;
            font-weight: 800;
            color: #005A2B;
            margin-bottom: 4px;
        }}
        
        .sig-name {{
            font-size: 13.5px;
            font-weight: 800;
            color: #0f172a;
            border-top: 1px dashed #cbd5e1;
            padding-top: 4px;
        }}

        /* الختم الرسمي بمنتصف التوقيعات */
        .school-seal {{
            width: 80px;
            height: 80px;
            border: 3px double #005A2B;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #005A2B;
            font-size: 8px;
            font-weight: 800;
            padding: 2px;
            background: #ffffff;
            box-shadow: 0 0 0 3px rgba(0, 90, 43, 0.05);
            transform: rotate(-5deg);
            margin: 0 10px;
        }}
        
        .cert-footer-date {{
            position: absolute;
            bottom: 8px;
            right: 30px;
            font-size: 10.5px;
            color: #64748b;
            font-weight: 700;
        }}

        @media print {{
            body {{
                background: none;
                padding: 0;
            }}
            .page-break {{
                margin-bottom: 0;
            }}
            .certificate-container {{
                box-shadow: none;
                width: 100%;
                height: 100vh;
                border-radius: 0;
            }}
        }}
    </style>
</head>
<body>

{single_certs_html}

</body>
</html>"""
    return full_html

# 7. عرض المعاينة الحية والتصدير الجماعي للشهادات
with col_preview:
    st.markdown("### 🖼️ المعاينة الحية والتصدير الجماعي للشهادات")
    
    if not selected_teachers:
        st.warning("⚠️ يرجى اختيار معلم واحد على الأقل من القائمة المنسدلة الجانبية لتوليد الشهادات.")
    else:
        # تبويبات لملاحظة كل معلم على حدة في المعاينة
        st.markdown(f"**عدد المعلمين المحدد لاصدار شهاداتهم حالياً: ({len(selected_teachers)} معلم)**")
        
        preview_tabs = st.tabs([f"📜 شهادة: {t}" for t in selected_teachers[:6]])
        
        for idx, tab_teacher in enumerate(selected_teachers[:6]):
            with preview_tabs[idx]:
                single_cert_html = build_full_certificates_document_html([tab_teacher])
                st.components.v1.html(single_cert_html, height=710, scrolling=True)
                
        if len(selected_teachers) > 6:
            st.caption(f"ℹ️ يتم عرض المعاينة لأول 6 معلمين فقط، وسيتم تضمين باقي المعلمين ({len(selected_teachers)}) في الملف المطبوع المجمع.")

        st.markdown("---")
        
        # إنشاء ملف التصدير الموحد لجميع المعلمين المحددين
        full_batch_html = build_full_certificates_document_html(selected_teachers)
        
        st.download_button(
            label=f"🖨️ تصدير وطباعة شهادات جميع المعلمين المحددين ({len(selected_teachers)} معلم) (HTML / PDF)",
            data=full_batch_html,
            file_name=f"Thaghr_Certificates_Batch_({len(selected_teachers)}_teachers).html",
            mime="text/html",
            use_container_width=True
        )
        
        st.info("💡 **تلميح الطباعة والتصدير:** عند فتح الملف المنزّل، اضغط (Ctrl + P) واختر اتجاه الطباعة **أفقي (Landscape)** ليتم طباعة شهادة كل معلم في صفحة مستقلة A4 بدقة احترافية عالية.")
