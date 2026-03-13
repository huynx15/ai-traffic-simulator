import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Cấu hình giao diện trang web
st.set_page_config(page_title="AI Traffic Simulator", layout="wide", page_icon="🚦")

st.title("🚦 Hệ thống AI phân tích giao thông")
st.markdown("**Đội thi:** Next Level")
st.write("Bản mô phỏng (Prototype) phân tích lưu lượng phương tiện qua camera và đề xuất chu kỳ đèn tín hiệu thông minh.")

st.divider()

# 2. Cấu hình API Key từ Streamlit Secrets (Dành cho quá trình deploy)
try:
    # Hệ thống sẽ tự động lấy API Key đã được khai báo ẩn trên Streamlit Cloud
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("Chưa tìm thấy API Key. Vui lòng kiểm tra lại mục 'Advanced settings > Secrets' trên Streamlit Cloud.")
    st.stop()

# 3. Khu vực tải hình ảnh giao thông
st.subheader("1. Thu thập dữ liệu")
st.write("Tải lên hình ảnh camera tại nút giao để hệ thống tiến hành phân tích mật độ phương tiện.")
uploaded_file = st.file_uploader("Chọn file ảnh (jpg, jpeg, png)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Hiển thị ảnh
    image = Image.open(uploaded_file)
    st.image(image, caption="Dữ liệu đầu vào từ Camera", use_container_width=True)
    
    # 4. Nút bấm kích hoạt AI
    if st.button("Phân tích dữ liệu & Mô phỏng chu kỳ đèn", type="primary"):
        with st.spinner("AI đang đếm phương tiện và tính toán mật độ..."):
            try:
                # Gọi mô hình Gemini 2.5 Flash mới nhất của Google
                model = genai.GenerativeModel('models/gemini-2.5-flash')
                
                # Cấu trúc Prompt (câu lệnh) để hướng dẫn AI thực hiện nhiệm vụ
                prompt = """
                Bạn là một hệ thống AI phân tích dữ liệu giao thông đô thị.
                Hãy quan sát bức ảnh camera giao thông này và thực hiện các bước sau:
                1. Ước lượng số lượng xe máy và ô tô đang dừng chờ.
                2. Đánh giá mật độ giao thông tại hướng này (Thấp, Trung bình, Cao, Rất Cao).
                3. Đề xuất chu kỳ đèn xanh tối ưu. Sử dụng quy tắc sau: Mật độ Thấp = 20s, Trung bình = 35s, Cao = 50s, Rất Cao = 65s.
                
                Trình bày kết quả thật chuyên nghiệp, rõ ràng theo dạng gạch đầu dòng để hiển thị lên Dashboard quản lý.
                """
                
                # Gửi ảnh và prompt cho AI xử lý
                response = model.generate_content([prompt, image])
                
                # 5. Hiển thị kết quả
                st.divider()
                st.subheader("📊 Kết quả phân tích & Đề xuất điều tiết")
                st.info(response.text)
                
                st.success("Mô phỏng thành công! Kết quả này cho thấy tính khả thi của việc dùng AI thay thế chu kỳ đèn cố định.")
                
            except Exception as e:
                st.error(f"Có lỗi xảy ra trong quá trình kết nối AI: {e}")
else:

    st.info("👈 Vui lòng tải lên một bức ảnh giao thông để bắt đầu trải nghiệm.")
