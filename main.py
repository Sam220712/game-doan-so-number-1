import random
import streamlit as st

# Cấu hình giao diện web
st.set_page_config(page_title="Game Đoán Số", page_icon="🎮", layout="centered")
st.title("🎮 Trò Chơi Đoán Số Thông Minh")

# Khởi tạo dữ liệu game
if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.so_bi_mat = 0
    st.session_state.luot_doan = 0
    st.session_state.he_so = 0
    st.session_state.gioi_han_so = 0
    st.session_state.game_over = False


def bat_dau_game(muc_do):
    if muc_do == "Dễ (1-50, 10 lượt)":
        st.session_state.gioi_han_so, st.session_state.luot_doan, (
            st.session_state.he_so
        ) = 50, 10, 10
    elif muc_do == "Vừa (1-100, 7 lượt)":
        st.session_state.gioi_han_so, st.session_state.luot_doan, (
            st.session_state.he_so
        ) = 100, 7, 20
    else:
        st.session_state.gioi_han_so, st.session_state.luot_doan, (
            st.session_state.he_so
        ) = 200, 5, 50

    st.session_state.so_bi_mat = random.randint(
        1, st.session_state.gioi_han_so
    )
    st.session_state.game_started = True
    st.session_state.game_over = False


# Giao diện chính
if not st.session_state.game_started:
    st.subheader("⚙️ Chọn Mức Độ Khó")
    muc_do_chon = st.radio(
        "Mức độ:",
        (
            "Dễ (1-50, 10 lượt)",
            "Vừa (1-100, 7 lượt)",
            "Khó (1-200, 5 lượt)",
        ),
    )
    if st.button("Bắt đầu chơi"):
        bat_dau_game(muc_do_chon)
        st.rerun()
else:
    st.write(
        f"Đang đoán số từ **1 đến {st.session_state.gioi_han_so}**. Hệ số điểm: **x{st.session_state.he_so}**"
    )

    # Hiển thị số lượt đoán hiện tại trước khi bấm nút
    st.info(f"❤️ Số lượt đoán còn lại: **{st.session_state.luot_doan}**")

    so_nhap = st.number_input(
        "Nhập số bạn nghĩ vào đây:",
        min_value=1,
        max_value=st.session_state.gioi_han_so,
        step=1,
    )

    if st.button("Đoán số", disabled=st.session_state.game_over):
        # Trừ lượt đoán ngay khi người chơi bấm nút
        st.session_state.luot_doan -= 1

        if so_nhap == st.session_state.so_bi_mat:
            # Điểm được tính dựa trên số lượt thực tế sau khi đã trừ
            diem = st.session_state.luot_doan * st.session_state.he_so
            st.success(
                f"🎉 Chúc mừng! Bạn đã đoán đúng số bí mật là **{st.session_state.so_bi_mat}**."
            )
            st.balloons()
            st.write(f"🏆 Tổng điểm nhận được: **{diem} điểm**!")
            st.session_state.game_over = True
        elif st.session_state.luot_doan == 0:
            st.error(
                f"💥 Bạn đã hết lượt! Số bí mật là **{st.session_state.so_bi_mat}**. Bạn thua rồi."
            )
            st.session_state.game_over = True
        elif so_nhap < st.session_state.so_bi_mat:
            st.warning("📉 Số bạn đoán QUÁ THẤP!")
            # Ép trang web tải lại ngay lập tức để cập nhật số lượt đoán mới trên màn hình
            st.rerun()
        else:
            st.warning("📈 Số bạn đoán QUÁ CAO!")
            # Ép trang web tải lại ngay lập tức để cập nhật số lượt đoán mới trên màn hình
            st.rerun()

    if st.session_state.game_over:
        if st.button("Chơi lại lượt mới"):
            st.session_state.game_started = False
            st.rerun()
