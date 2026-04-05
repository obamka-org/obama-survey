import streamlit as st
import time

# Настройка страницы
st.set_page_config(
    page_title="Опрос Обамы",
    page_icon="🎯",
    layout="centered"
)

# Заголовок
st.markdown("<h1 style='text-align: center; font-weight: bold;'>АНОНИМНЫЙ ОПРОС ОТ ОБАМЫ</h1>", unsafe_allow_html=True)

# Предупреждение
st.markdown(
    "<p style='text-align: center; color: red; font-weight: bold; font-size: 18px;'>⚠️ ВНИМАНИЕ! УБЕДИТЕСЬ СТРАНИЦА НЕ ПЕРЕВЕДЕНА НА РУССКИЙ. ВОЗНИКАЮТ ОШИБКИ! ⚠️</p>",
    unsafe_allow_html=True)
st.divider()

# Инициализация состояния
if 'опрос_завершен' not in st.session_state:
    st.session_state.опрос_завершен = False
if 'ответы' not in st.session_state:
    st.session_state.ответы = {}
if 'отправлено' not in st.session_state:
    st.session_state.отправлено = False
if 'таймер_запущен' not in st.session_state:
    st.session_state.таймер_запущен = False
if 'таймер_значение' not in st.session_state:
    st.session_state.таймер_значение = 10

# Вопросы
questions = {
    1: "Вы подпишитесь на YouTube: @obamka-org?",
    2: "Вы подпишитесь на TikTok: mjk_org?",
    3: "Барак Обама - лучший правитель всех времён?",
    4: "Вы поддерживаете Обаму?",
    5: "Вы умрёте за Обаму?"
}


# Функция для сброса опроса
def reset_survey():
    st.session_state.опрос_завершен = False
    st.session_state.отправлено = False
    st.session_state.ответы = {}
    st.session_state.таймер_запущен = False
    st.session_state.таймер_значение = 10


# Если опрос ещё не завершён и не отправлен
if not st.session_state.опрос_завершен and not st.session_state.отправлено:

    # Задаём все вопросы
    for num, question in questions.items():
        st.subheader(f"Вопрос {num}")

        if num in [1, 2]:
            ответ = st.radio(
                question,
                ["Да", "ДА"],
                key=f"q{num}",
                horizontal=True,
                index=None
            )
        else:
            ответ = st.radio(
                question,
                ["Да", "Нет"],
                key=f"q{num}",
                horizontal=True,
                index=None
            )

        if ответ:
            if num in [1, 2]:
                st.session_state.ответы[num] = "да"
            else:
                st.session_state.ответы[num] = "да" if ответ == "Да" else "нет"

        st.write("")
        st.divider()

    # Кнопка отправки
    if st.button("ОТПРАВИТЬ ОТВЕТЫ", type="primary", use_container_width=True):

        # Проверяем, все ли вопросы отвечены
        if len(st.session_state.ответы) < 5:
            st.error("Пожалуйста, ответьте на ВСЕ вопросы!")
        else:
            st.session_state.отправлено = True
            # Проверяем, есть ли хоть один ответ "нет" среди вопросов 3-5
            ответы_3_5 = [st.session_state.ответы.get(num) for num in [3, 4, 5]]

            if "нет" in ответы_3_5:
                st.session_state.опрос_завершен = True
                st.session_state.результат = "fail"
                st.session_state.таймер_запущен = True
                st.session_state.нарушения = [num for num in [3, 4, 5] if st.session_state.ответы.get(num) == "нет"]
            else:
                st.session_state.опрос_завершен = True
                st.session_state.результат = "success"

            st.rerun()

# Показываем результат
if st.session_state.опрос_завершен:
    if st.session_state.результат == "success":
        st.markdown("<h1 style='text-align: center; color: green; font-size: 48px;'>✅ ВЫ УСПЕШНО ПРОШЛИ ОПРОС!</h1>",
                    unsafe_allow_html=True)

        if st.button("ПРОЙТИ ОПРОС ЗАНОВО", use_container_width=True):
            reset_survey()
            st.rerun()

    else:
        st.markdown("<h1 style='text-align: center; color: red; font-size: 36px;'>⚠️ ВНИМАНИЕ! ⚠️</h1>",
                    unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: darkred;'>Ваши ответы были неверны.</h2>",
                    unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: red;'>По вашим координатам был отправлен ДРОН HAROP.</h3>",
                    unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align: center; font-size: 20px; font-weight: bold;'>🚀 Просим не покидать своё место нахождения! 🚀</p>",
            unsafe_allow_html=True)

        st.divider()

        st.subheader("ДЕТАЛИ НАРУШЕНИЯ:")

        if 3 in st.session_state.нарушения:
            st.error("❌ Вопрос 3: Вы не считаете Обаму лучшим правителем!")

        if 4 in st.session_state.нарушения:
            st.error("❌ Вопрос 4: Вы не поддерживаете Обаму!")

        if 5 in st.session_state.нарушения:
            st.error("❌ Вопрос 5: Вы не готовы умереть за Обаму!")

        st.divider()

        # Таймер 10 секунд (без перезапуска страницы)
        if st.session_state.таймер_запущен:
            countdown_placeholder = st.empty()

            # Ручной цикл таймера с time.sleep
            for i in range(st.session_state.таймер_значение, 0, -1):
                countdown_placeholder.markdown(
                    f"<h1 style='text-align: center; color: orange;'>💥 ДРОН HAROP ПРИБУДЕТ ЧЕРЕЗ: {i} СЕКУНД 💥</h1>",
                    unsafe_allow_html=True)
                time.sleep(1)
                st.session_state.таймер_значение = i - 1

            countdown_placeholder.markdown(
                "<h1 style='text-align: center; color: green;'>🕊️ Обама вас пощадил 🕊️</h1>", unsafe_allow_html=True)
            st.session_state.таймер_запущен = False

        st.divider()

        if st.button("ПРОЙТИ ОПРОС ЗАНОВО", use_container_width=True):
            reset_survey()
            st.rerun()