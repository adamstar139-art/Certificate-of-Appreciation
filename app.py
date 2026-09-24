import streamlit as st
import datetime

# 1. إعداد الصفحة العامة
st.set_page_config(
    page_title="نظام إصدار شهادات المعلمين - مدارس الثغر النموذجية الأهلية",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تنسيقات CSS للواجهة الرئيسية (Cairo Font + الأخضر والذهبي)
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

.main-header {
    background: linear-gradient(135deg, #005A2B 0%, #004D25 100%);
    color: white;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0, 90, 43, 0.15);
    margin-bottom: 24px;
    border-bottom: 4px solid #D4AF37;
    text-align: center !important;
}

.main-header h1 {
    color: #ffffff !important;
    font-size: 26px !important;
    font-weight: 800 !important;
    margin: 0 0 8px 0 !important;
    text-align: center !important;
}

.main-header p {
    color: #e2e8f0 !important;
    font-size: 14px !important;
    margin: 0 !important;
    text-align: center !important;
}

.stButton > button {
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    padding: 8px 20px !important;
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

# 3. الترويسة الرئيسية للموقع
st.markdown("""
<div class="main-header">
    <div style="font-size: 13px; color: #D4AF37; font-weight: 700; margin-bottom: 4px;">المملكة العربية السعودية • وزارة التعليم</div>
    <h1>📜 نظام إصدار وطباعة الشهادات المعتمدة</h1>
    <p>مدارس الثغر النموذجية الأهلية • الهوية المعتمدة بـ (لوجو الثغر)</p>
</div>
""", unsafe_allow_html=True)

# 4. تهيئة بيانات الجلسة (st.session_state)
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
        {"role": "مدير المدرسة", "name": "أ. إبراهيم بن موسى التميمي"},
        {"role": "المدير الأكاديمي", "name": "د. ياسين البدراوي"},
        {"role": "وكيل شؤون الطلاب", "name": "أ. صالح بن عبدالله الدعجاني"},
        {"role": "وكيل الشؤون التعليمية", "name": "أ. محمد مبروك السيد"}
    ]

# تقسيم واجهة المستخدم إلى عمودين: التحكم والمعاينة
col_ctrl, col_preview = st.columns([1, 2])

with col_ctrl:
    st.markdown("### ⚙️ لوحة التحكم وإعدادات الشهادة")
    
    # 1. نوع الشهادة
    cert_type = st.radio(
        "🏷️ اختر نوع الشهادة:",
        ["🎓 شهادة حضور دورة تدريبية", "🎖️ شهادة شكر وتقدير للمعلم"],
        index=0
    )
    
    st.markdown("---")
    
    # 2. القائمة المنسدلة لاختيار القسم
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
    
    # 3. اختيار المعلم + أيقونة إضافة معلم جديد
    st.markdown("#### 👤 اختيار / إضافة المعلم")
    selected_teacher = st.selectbox(
        "اختر اسم المعلم من القائمة المنسدلة:",
        st.session_state["teachers_list"]
    )
    
    with st.expander("➕ أيقونة إضافة معلم جديد"):
        new_teacher_input = st.text_input("اسم المعلم الجديد:", placeholder="أ/ اكتب الاسم رباعياً...")
        if st.button("💾 إضافة المعلم للقائمة", key="btn_add_teacher"):
            if new_teacher_input.strip():
                if new_teacher_input.strip() not in st.session_state["teachers_list"]:
                    st.session_state["teachers_list"].append(new_teacher_input.strip())
                    st.success(f"✅ تم إضافة المعلم: {new_teacher_input.strip()}")
                    st.rerun()
                else:
                    st.warning("⚠️ هذا الاسم موجود بالفعل في القائمة.")

    st.markdown("---")
    
    # 4. اختيار / إضافة اسم الدورة التدريبية
    if "حضور دورة" in cert_type:
        st.markdown("#### 📚 اختيار / إضافة الدورة التدريبية")
        selected_course = st.selectbox(
            "اختر اسم الدورة من القائمة المنسدلة:",
            st.session_state["courses_list"]
        )
        
        with st.expander("➕ أيقونة إضافة دورة تدريبية جديدة"):
            new_course_input = st.text_input("اسم الدورة الجديدة:", placeholder="اكتب عنوان الدورة...")
            if st.button("💾 إضافة الدورة للقائمة", key="btn_add_course"):
                if new_course_input.strip():
                    if new_course_input.strip() not in st.session_state["courses_list"]:
                        st.session_state["courses_list"].append(new_course_input.strip())
                        st.success(f"✅ تم إضافة الدورة: {new_course_input.strip()}")
                        st.rerun()
                    else:
                        st.warning("⚠️ اسم الدورة موجود بالفعل.")
                        
        course_hours = st.number_input("عدد الساعات التدريبية:", min_value=1, max_value=100, value=15)
        course_date = st.date_input("تاريخ انعقاد الدورة:", value=datetime.date.today())
        formatted_date = course_date.strftime("%Y/%m/%d") + " م"
        cert_main_title = "شهادة حضور دورة تدريبية"
        
        default_body_text = f"قد حضر وأتم بنجاح الدورة التدريبية بعنوان: « {selected_course} » والتي عقدت بتاريخ {formatted_date} بواقع ({course_hours}) ساعات تدريبية معتمدة، سائلين الله له دوام التوفيق والنجاح."
    else:
        st.markdown("#### 📖 التخصص / المادة")
        subject_name = st.text_input("المادة / التخصص:", value="تكنولوجيا المعلومات والتعليم الرقمي")
        formatted_date = datetime.date.today().strftime("%Y/%m/%d") + " م"
        cert_main_title = "شهادة شكر وتقدير"
        
        default_body_text = f"تقديرًا لجهوده المتميزة وعطائه المخلص في رفع مستوى الأداء التعليمي بمادة ({subject_name})، ومشاركته الفاعلة في إنجاح الأنشطة المدرسية خلال العام الدراسي."

    # 5. أيقونة/خانة لإضافة النص الذي يظهر في الشهادة
    st.markdown("#### 📝 تخصيص النص الظاهر في الشهادة")
    cert_custom_text = st.text_area(
        "أيقونة تعديل وتخصيص نص الشهادة:",
        value=default_body_text,
        height=120
    )

    st.markdown("---")

    # 6. إضافة وتحديد التوقيعات والأسماء التي تظهر بأسفل الشهادة
    st.markdown("#### ✍️ التوقيعات المعتمدة بأسفل الشهادة")
    
    sig_options_map = {f"{s['role']}: {s['name']}": s for s in st.session_state["signatures_list"]}
    
    default_selected_keys = [
        f"{st.session_state['signatures_list'][0]['role']}: {st.session_state['signatures_list'][0]['name']}",
        f"{st.session_state['signatures_list'][1]['role']}: {st.session_state['signatures_list'][1]['name']}"
    ]
    
    selected_sig_keys = st.multiselect(
        "📌 أيقونة اختيار الأسماء والتوقيعات التي تظهر في نهاية الشهادة:",
        options=list(sig_options_map.keys()),
        default=default_selected_keys
    )
    
    chosen_signatures = [sig_options_map[k] for k in selected_sig_keys]
    
    with st.expander("➕ أيقونة إضافة توقيع جديد (المسمى الوظيفي والاسم)"):
        new_sig_role = st.text_input("المسمى الوظيفي:", placeholder="مثال: رئيس القسم / وكيل النشاط")
        new_sig_name = st.text_input("اسم صاحب التوقيع:", placeholder="مثال: أ. أحمد العتيبي")
        if st.button("💾 حفظ التوقيع الجديد", key="btn_add_sig"):
            if new_sig_role.strip() and new_sig_name.strip():
                new_sig_obj = {"role": new_sig_role.strip(), "name": new_sig_name.strip()}
                st.session_state["signatures_list"].append(new_sig_obj)
                st.success("✅ تم إضافة التوقيع الجديد بنجاح!")
                st.rerun()

# 5. بناء كود HTML الفاخر للشهادة (تتضمن شعار لوجو الثغر بوسط الديباجة وبخلفية العلامة المائية)
def generate_certificate_html():
    # بناء كتل التوقيعات الديناميكية
    sigs_html = ""
    for sig in chosen_signatures:
        sigs_html += f"""
        <div class="sig-box">
            <div class="sig-role">{sig['role']}</div>
            <div style="height: 28px;"></div>
            <div class="sig-name">{sig['name']}</div>
        </div>
        """
        
    if "حضور دورة" in cert_type:
        body_html = f"""
        تشهد إدارة <strong>مدارس الثغر النموذجية الأهلية</strong> - <span style="color:#005A2B;">({selected_dept})</span> بأن المعلم القدير:
        <div class="teacher-name">{selected_teacher}</div>
        {cert_custom_text}
        """
    else:
        body_html = f"""
        تتقدم إدارة <strong>مدارس الثغر النموذجية الأهلية</strong> - <span style="color:#005A2B;">({selected_dept})</span> بأسمى عبارات الشكر والامتنان للمعلم القدير:
        <div class="teacher-name">{selected_teacher}</div>
        {cert_custom_text}
        """

    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>{cert_main_title}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Amiri:ital,wght@0,700;1,400&display=swap');
        
        @page {{
            size: A4 landscape;
            margin: 0;
        }}
        
        body {{
            margin: 0;
            padding: 20px;
            background-color: #f1f5f9;
            font-family: 'Cairo', sans-serif;
            direction: rtl;
            text-align: center;
            color: #0f172a;
        }}
        
        .certificate-container {{
            width: 1000px;
            height: 680px;
            margin: 0 auto;
            background: #ffffff;
            padding: 25px;
            box-sizing: border-box;
            position: relative;
            border: 12px solid #005A2B;
            outline: 4px solid #D4AF37;
            outline-offset: -8px;
            border-radius: 12px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.12);
            overflow: hidden;
        }}
        
        /* شعار لوجو الثغر-02 في خلفية الشهادة (علامة مائية خفيفة شفافة) */
        .watermark-logo {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 440px;
            height: 440px;
            opacity: 0.05;
            pointer-events: none;
            z-index: 1;
        }}
        
        .inner-border {{
            border: 2px solid #D4AF37;
            height: 100%;
            padding: 20px 35px;
            box-sizing: border-box;
            border-radius: 6px;
            position: relative;
            z-index: 2;
            background: rgba(255, 255, 255, 0.94);
        }}
        
        /* الترويسة الوطنية مع شعار لوجو الثغر بوسط الديباجة */
        .cert-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #005A2B;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        
        .header-side {{
            font-size: 12px;
            font-weight: 700;
            color: #334155;
            line-height: 1.6;
            text-align: right;
            flex: 1;
        }}

        .header-side.left-side {{
            text-align: left;
        }}

        /* شعار لوجو الثغر بوسط الديباجة بالأعلى */
        .logo-box-center {{
            flex: 1;
            text-align: center;
        }}

        .thaghr-logo-badge {{
            width: 82px;
            height: 82px;
            background: linear-gradient(135deg, #005A2B 0%, #00381B 100%);
            border: 3px solid #D4AF37;
            border-radius: 50%;
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(0,90,43,0.25);
            margin: 0 auto;
        }}

        .thaghr-logo-icon {{
            font-size: 28px;
            line-height: 1;
            margin-bottom: 2px;
        }}

        .thaghr-logo-text {{
            font-size: 9px;
            font-weight: 900;
            color: #D4AF37;
            letter-spacing: 0.5px;
        }}

        .school-dept-title {{
            font-size: 14px;
            font-weight: 800;
            color: #005A2B;
            margin-top: 4px;
        }}
        
        /* عنوان الشهادة الرئيسي */
        .cert-title-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #005A2B 0%, #004D25 100%);
            color: #ffffff;
            font-size: 22px;
            font-weight: 900;
            padding: 6px 40px;
            border-radius: 30px;
            border: 2px solid #D4AF37;
            box-shadow: 0 4px 14px rgba(0, 90, 43, 0.25);
            margin-top: 8px;
            margin-bottom: 16px;
        }}
        
        /* نص الشهادة */
        .cert-body {{
            font-size: 16px;
            line-height: 1.8;
            color: #1e293b;
            margin-bottom: 20px;
            font-weight: 600;
            padding: 0 20px;
        }}
        
        .teacher-name {{
            font-size: 28px;
            font-weight: 900;
            color: #005A2B;
            margin: 8px 0;
            font-family: 'Amiri', serif;
            letter-spacing: 0.5px;
            text-shadow: 1px 1px 0px rgba(212, 175, 55, 0.3);
        }}
        
        /* التوقيعات المعتمدة الديناميكية بأسفل الشهادة */
        .signatures-section {{
            display: flex;
            justify-content: space-around;
            align-items: flex-end;
            margin-top: 25px;
            padding-top: 10px;
        }}
        
        .sig-box {{
            min-width: 180px;
            text-align: center;
        }}
        
        .sig-role {{
            font-size: 13px;
            font-weight: 800;
            color: #005A2B;
            margin-bottom: 4px;
        }}
        
        .sig-name {{
            font-size: 14px;
            font-weight: 800;
            color: #0f172a;
            border-top: 1px dashed #cbd5e1;
            padding-top: 5px;
        }}

        /* ختم المدرسة بمنتصف التوقيعات */
        .school-seal {{
            width: 85px;
            height: 85px;
            border: 3px double #005A2B;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #005A2B;
            font-size: 8px;
            font-weight: 800;
            padding: 3px;
            background: #ffffff;
            box-shadow: 0 0 0 3px rgba(0, 90, 43, 0.05);
            transform: rotate(-5deg);
            margin: 0 10px;
        }}
        
        .cert-footer-date {{
            position: absolute;
            bottom: 10px;
            right: 35px;
            font-size: 11px;
            color: #64748b;
            font-weight: 700;
        }}

        @media print {{
            body {{
                background: none;
                padding: 0;
            }}
            .certificate-container {{
                box-shadow: none;
                width: 100%;
                height: 100vh;
            }}
        }}
    </style>
</head>
<body>

<div class="certificate-container">
    <!-- شعار لوجو الثغر-02 في الخلفية لكل شهادة كعلامة مائية خفيفة شفافة -->
    <svg class="watermark-logo" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="100" r="90" fill="#005A2B" stroke="#D4AF37" stroke-width="6"/>
        <path d="M 40 130 Q 100 160 160 130 L 160 110 Q 100 140 40 110 Z" fill="#D4AF37"/>
        <path d="M 50 115 L 100 60 L 150 115 Q 100 95 50 115 Z" fill="#ffffff"/>
        <circle cx="100" cy="50" r="12" fill="#D4AF37"/>
        <text x="100" y="180" font-family="Cairo" font-weight="bold" font-size="14" fill="#005A2B" text-anchor="middle">لوجو الثغر</text>
    </svg>

    <div class="inner-border">
        <!-- الترويسة العليا مع شعار لوجو الثغر في الأعلى بوسط الديباجة -->
        <div class="cert-header">
            <div class="header-side">
                المملكة العربية السعودية<br>
                وزارة التعليم<br>
                إدارة التعليم بمنطقة الرياض
            </div>
            
            <!-- شعار لوجو الثغر بوسط الديباجة بالأعلى -->
            <div class="logo-box-center">
                <div class="thaghr-logo-badge">
                    <div class="thaghr-logo-icon">📖</div>
                    <div class="thaghr-logo-text">لوجو الثغر</div>
                </div>
                <div class="school-dept-title">مدارس الثغر النموذجية الأهلية</div>
                <div style="font-size: 11px; color: #64748b; font-weight: 700;">{selected_dept}</div>
            </div>
            
            <div class="header-side left-side">
                Kingdom of Saudi Arabia<br>
                Ministry of Education<br>
                Al-Thaghr Model Schools
            </div>
        </div>

        <!-- عنوان الشهادة -->
        <div class="cert-title-badge">{cert_main_title}</div>

        <!-- نص الشهادة المخصص -->
        <div class="cert-body">
            {body_html}
        </div>

        <!-- التوقيعات المختارة والاعتماد الرسمي بأسفل الشهادة -->
        <div class="signatures-section">
            {sigs_html}

            <div class="school-seal">
                <div>مدارس الثغر</div>
                <div style="font-size: 14px; margin: 1px 0;">🏫</div>
                <div>الختم المعتمد</div>
            </div>
        </div>

        <div class="cert-footer-date">
            تاريخ الإصدار: {formatted_date}
        </div>
    </div>
</div>

</body>
</html>"""
    return html

# 6. عرض المعاينة والتصدير المباشر
with col_preview:
    st.markdown("### 🖼️ المعاينة الحية للشهادة (A4 Landscape)")
    
    cert_html = generate_certificate_html()
    
    st.components.v1.html(cert_html, height=730, scrolling=True)
    
    st.markdown("---")
    
    # زر تصدير وطباعة الشهادة
    st.download_button(
        label=f"🖨️ طباعة / تصدير {cert_main_title} (HTML / PDF)",
        data=cert_html,
        file_name=f"Certificate_{selected_teacher.replace(' ', '_')}.html",
        mime="text/html",
        use_container_width=True
    )
    
    st.info("💡 **إرشادات الطباعة الممتازة:** عند فتح الملف المنزّل، اختر خيار الاتجاه **أفقي (Landscape)** عند الطباعة للحصول على الشهادة بجودة عالية وإطار A4 كامل.")

