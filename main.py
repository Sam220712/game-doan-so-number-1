import random
import streamlit as st
import json
import os

st.set_page_config(page_title="Game Đoán Số", page_icon="🎮", layout="centered")
st.title("🎮 Trò Chơi Đoán Số & Bảng Xếp Hạng")

# Khởi tạo bộ nhớ game
if "started" not in st.session_state:
    st.session_state.update({"started": False, "secret": 0, "turns": 0, "max": 50, "factor": 10, "over": False, "hint": ""})

# Hàm đọc/ghi Bảng xếp hạng (BXH) bằng JSON để không bị mất khi F5
def doc_bxh():
    if not os.path.exists("bxh.json"): return []
    with open("bxh.json", "r", encoding="utf-8") as f: return json.load(f)

def luu_diem(ten, diem, muc_do):
    bxh = doc_bxh()
    bxh.append({"Tên": ten, "Điểm": diem, "Mức độ": muc_do})
    # Sắp xếp điểm từ cao xuống thấp và chỉ lấy top 5
    bxh = sorted(bxh, key=lambda x: x["Điểm"], reverse=True)[:5]
    with open("bxh.json", "w", encoding="utf-8") as f:
        json.dump(bxh, f, ensure_ascii=False, indent=4)

# GIAO DIỆN CHÍNH
tab1, tab2 = st.tabs(["🎮 Chơi Game", "🏆 Bảng Xếp Hạng Top 5"])

with tab1:
    if not st.session_state.started:
        st.subheader("⚙️ Chọn Mức Độ Khó")
        level = st.radio("Mức độ:", ("Dễ (1-50, 10 lượt)", "Vừa (1-100, 7 lượt)", "Khó (1-200, 5 lượt)"))
        if st.button("Bắt đầu chơi"):
            limit, turns, factor = (50, 10, 10) if "Dễ" in level else (100, 7, 20) if "Vừa" in level else (200, 5, 50)
            st.session_state.update({"started": True, "secret": random.randint(1, limit), "turns": turns, "max": limit, "factor": factor, "over": False, "hint": "", "level_name": level.split()[0]})
            st.rerun()
    else:
        st.info(f"❤️ Số lượt đoán còn lại: **{st.session_state.turns}**")
        if st.session_state.hint: st.warning(st.session_state.hint)

        # Khóa cứng đầu vào chặn số trên trời
        guess = st.number_input(f"Nhập số (1 - {st.session_state.max}):", 1, st.session_state.max, step=1, key="num")
        valid = 1 <= guess <= st.session_state.max
        if not valid: st.error("⚠️ Số nhập vào không hợp lệ!")

        if st.button("Đoán số", disabled=(st.session_state.over or not valid)):
            st.session_state.turns -= 1
            
            if guess == st.session_state.secret:
                diem = (st.session_state.turns + 1) * st.session_state.factor
                st.success(f"🎉 Đúng rồi! Số bí mật là **{st.session_state.secret}**.")
                st.balloons()
                st.write(f"🏆 Bạn giành được: **{diem} điểm**!")
                
                # Ô nhập tên lưu kỷ lục
                ten_nguoi_choi = st.text_input("Nhập tên của bạn để ghi danh BXH:", "Người chơi ẩn danh")
                if st.button("Lưu điểm số"):
                    luu_diem(ten_nguoi_choi, diem, st.session_state.level_name)
                    st.success("Đã ghi danh thành công! Hãy qua tab BXH để xem.")
                st.session_state.over = True
            elif st.session_state.turns == 0:
                st.error(f"💥 Bạn thua rồi! Số bí mật là **{st.session_state.secret}**.")
                st.session_state.over = True
            else:
                st.session_state.hint = f"📉 Số {guess} QUÁ THẤP!" if guess < st.session_state.secret else f"📈 Số {guess} QUÁ CAO!"
                st.rerun()

        if st.session_state.over and st.button("Chơi lại"):
            st.session_state.started = False
            st.rerun()

with tab2:
    st.subheader("🏅 Những Người Chơi Xuất Sắc Nhất")
    du_lieu_bxh = doc_bxh()
    if du_lieu_bxh:
        for idx, p in enumerate(du_lieu_bxh, 1):
            st.write(f"**Top {idx}**: {p['Tên']} - `{p['Điểm']} điểm` (Mức: {p['Mức độ']})")
    else:
        st.write("Hiện chưa có ai ghi danh. Hãy là người đầu tiên!")
