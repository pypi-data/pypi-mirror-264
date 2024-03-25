import streamlit as st
from code_editor import code_editor
from css import custom_btns, info_bar
import subprocess
from until import check_code, write_code

def side_bar():
    with st.sidebar:
        st.markdown("## :heartbeat: :heartbeat: Hướng dẫn  :heartbeat: :heartbeat:")
        st.markdown("1. Đặt tên file (không bắt buộc)")
        st.markdown("2. Viết mã Python vào ô bên dưới")
        st.markdown("3. Nhấn nút **Run** để thực thi mã")
        st.markdown("4. Kết quả sẽ hiển thị ở ô bên dưới")
        st.markdown("5. Bạn có thể tải file Python bằng cách nhấn vào nút **Save file**")
        
        file_name = st.text_input("Tên file:", "st-test.py")
        st.write("Chill chút nhỉ? ^^")
        st.audio("https://cdn.pixabay.com/audio/2023/01/10/audio_5f83ba4572.mp3", format="audio/mp3")
        st.audio("https://cdn.pixabay.com/audio/2023/04/30/audio_6b3a512606.mp3", format="audio/mp3")
        st.audio("https://ia800209.us.archive.org/12/items/ECHOSAXEND/ECHOSAXEND.mp3", format="audio/mp3")
        
        return file_name
    
def heading():
    col_1, col_2, col_3 = st.columns([0.2, 0.5, 0.4])
    with col_2:
        st.title("AIO Code Editor")
    with col_3:
        st.image("shark.png", width=150)

def codes_box():
    sample_code = """#Bạn viết code ở đây nhé!\nprint("AI VIET NAM XIN CHÀO!")\n"""
    response_dict = code_editor(sample_code, buttons=custom_btns, height=[10, 30], info=info_bar)
    codes = response_dict["text"]
    type = response_dict["type"]
    return codes, type

def run_code(file_name, codes, type):
    if check_code(codes):     
        if type == "submit":
            # Lưu mã vào file Python
            write_code(codes)
            # Hiển thị button đownload file
            st.download_button(
                label="Save file",
                data=open(file_name, 'rb').read(),
                file_name= file_name,
                mime="text/plain")
            
            # Thực thi file Python và lấy đầu ra và lỗi (nếu có)
            result = subprocess.run(['python', file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Hiển thị kết quả trong st.text_area
            st.text_area("Output", result.stdout)
            if result.stderr:
                st.text_area("Error", result.stderr)
    else:
        st.error("Mã của bạn có thể nguy hiểm, vui lòng kiểm tra lại!")