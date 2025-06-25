import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="تحليل بيانات Excel", layout="wide")
st.title("📊 منصة تحليل ملفات Excel")

uploaded_file = st.file_uploader("🔼 ارفع ملف Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ تم تحميل الملف بنجاح")

        st.header("البيانات")
        st.dataframe(df)
        st.divider()

        
        x_col = st.selectbox("X اختر عمود محور ",df.columns)
        y_col = st.selectbox("Y اختر عمود محور ",df.columns)

        chart_type = st.selectbox(
            "📊 اختر نوع الرسم البياني",
            ["Line", "Bar", "Scatter", "Histogram"]
        )

        if st.button("🎨 عرض الرسم البياني"):
            if chart_type == "Line":
                fig = px.line(df, x=x_col, y=y_col)
            elif chart_type == "Bar":
                fig = px.bar(df, x=x_col, y=y_col)
            elif chart_type == "Scatter":
                fig = px.scatter(df, x=x_col, y=y_col)
            elif chart_type == "Histogram":
                fig = px.histogram(df, x=x_col)  

            fig.update_layout(title=f"{chart_type} Chart of {y_col} vs {x_col}")
            st.plotly_chart(fig)

            st.subheader("🔍تحليل القيم ")
            # محاولة تحويل القيم في العمود المختار إلى أرقام
            df[y_col] = pd.to_numeric(df[y_col], errors='coerce')

# استخراج القيم غير صفرية وغير فارغة (بعد التحويل)
            valid_y = df[y_col][(df[y_col] != 0) & (df[y_col].notna())]

            if not valid_y.empty:
            # استخراج الصف ذو القيمة العليا
             max_row = df.loc[df[y_col].idxmax()]

    # استخراج الصف ذو أقل قيمة صالحة
             min_value = valid_y.min()
             min_row = df[df[y_col] == min_value].iloc[0]

            st.write("🔺 أعلى قيمة:")
            st.dataframe(pd.DataFrame([max_row]))

            st.write("🔻 أقل قيمة (تجاهل القيم الفارغة والصفرية):")
            st.dataframe(pd.DataFrame([min_row]))
        else:
            st.warning("⚠️ لا توجد قيم رقمية صالحة (غير صفرية وغير فارغة) في العمود المحدد.")

    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
else:
    st.info("📂 الرجاء رفع ملف Excel لبدء التحليل.")
