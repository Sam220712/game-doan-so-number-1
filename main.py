import random
import streamlit as st

st.set_page_config(page_title="Game Đoán Số", page_icon="🎮", layout="centered")
st.title("🎮 Trò Chơi Đoán Số Thông Minh")

# Khởi tạo bộ nhớ game
if "started" not in st.session_state:
    st.session_state.update({"started": False, "secret": 0, "turns": 0, "max": 50, "over": False, "hint": ""})

# Giao diện chọn mức độ
if not st.session_state.started:
    st.subheader("⚙️ Chọn Mức Độ Khó")
    level = st.radio("Mức độ:", ("Dễ (1-50, 10 lượt)", "Vừa (1-100, 7 lượt)", "Khó (1-200, 5 lượt)"))
    if st.button("Bắt đầu chơi"):
        limit, turns = (50, 10) if "Dễ" in level else (100, 7) if "Vừa" in level else (200, 5)
        st.session_state.update({"started": True, "secret": random.randint(1, limit), "turns": turns, "max": limit, "over": False, "hint": ""})
        st.rerun()
else:
    st.info(f"❤️ Số lượt đoán còn lại: **{st.session_state.turns}**")
    if st.session_state.hint: st.warning(st.session_state.hint)

    # Ô nhập số thông minh, tự động khóa cứng giới hạn đầu vào
    guess = st.number_input(f"Nhập số (1 - {st.session_state.max}):", 1, st.session_state.max, step=1, key="num")
    valid = 1 <= guess <= st.session_state.max
    if not valid: st.error("⚠️ Số nhập vào không hợp lệ!")

    if st.button("Đoán số", disabled=(st.session_state.over or not valid)):
        st.session_state.turns -= 1
        if guess == st.session_state.secret:
            st.success(f"🎉 Đúng rồi! Số bí mật là **{st.session_state.secret}**."); st.balloons()
            st.session_state.over = True
        elif st.session_state.turns == 0:
            st.error(f"💥 Bạn thua rồi! Số bí mật là **{st.session_state.secret}**.")
            st.session_state.over = True
        else:
            st.session_state.hint = f"📉 Số {guess} QUÁ THẤP!" if guess < st.session_state.secret else f"📈 Số {guess} QUÁ CAO!"
            st.rerun()

    if st.session_state.over and st.button("Chơi lại"):
        st.session_state.started = False; st.rerun()
