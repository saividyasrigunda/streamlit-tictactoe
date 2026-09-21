import math
import streamlit as st

st.set_page_config(page_title="Competitive Tic-Tac-Toe AI", page_icon="🎮")

st.title("🎮 Competitive Tic-Tac-Toe")
st.subheader("Unbeatable Minimax AI Opponent")

# Initialize Session States
if "board" not in st.session_state:
    st.session_state.board = [" " for _ in range(9)]
if "player_score" not in st.session_state:
    st.session_state.player_score = 0
if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0
if "draw_score" not in st.session_state:
    st.session_state.draw_score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "winner_msg" not in st.session_state:
    st.session_state.winner_msg = ""

human = "X"
ai = "O"

WINNING_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

def check_winner(b, player):
    for combo in WINNING_COMBINATIONS:
        if b[combo[0]] == b[combo[1]] == b[combo[2]] == player:
            return True
    return False

def is_draw(b):
    return " " not in b

def minimax(b, depth, is_maximizing):
    if check_winner(b, ai):
        return 10 - depth
    if check_winner(b, human):
        return depth - 10
    if is_draw(b):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = ai
                score = minimax(b, depth + 1, False)
                b[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = human
                score = minimax(b, depth + 1, True)
                b[i] = " "
                best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -math.inf
    move = -1
    for i in range(9):
        if st.session_state.board[i] == " ":
            st.session_state.board[i] = ai
            score = minimax(st.session_state.board, 0, False)
            st.session_state.board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

def handle_click(index):
    if st.session_state.board[index] == " " and not st.session_state.game_over:
        # Human Move
        st.session_state.board[index] = human
        
        if check_winner(st.session_state.board, human):
            st.session_state.player_score += 1
            st.session_state.winner_msg = "🎉 You Won!"
            st.session_state.game_over = True
            return
        elif is_draw(st.session_state.board):
            st.session_state.draw_score += 1
            st.session_state.winner_msg = "🤝 It's a Draw!"
            st.session_state.game_over = True
            return

        # AI Move
        ai_index = best_move()
        if ai_index != -1:
            st.session_state.board[ai_index] = ai

        if check_winner(st.session_state.board, ai):
            st.session_state.ai_score += 1
            st.session_state.winner_msg = "🤖 AI Wins!"
            st.session_state.game_over = True
        elif is_draw(st.session_state.board):
            st.session_state.draw_score += 1
            st.session_state.winner_msg = "🤝 It's a Draw!"
            st.session_state.game_over = True

def reset_board():
    st.session_state.board = [" " for _ in range(9)]
    st.session_state.game_over = False
    st.session_state.winner_msg = ""

def reset_all():
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.draw_score = 0
    reset_board()

# Scoreboard
col1, col2, col3 = st.columns(3)
col1.metric("You (X)", st.session_state.player_score)
col2.metric("AI (O)", st.session_state.ai_score)
col3.metric("Draws", st.session_state.draw_score)

st.write("---")

if st.session_state.winner_msg:
    st.success(st.session_state.winner_msg)

# Game Board Grid
for i in range(0, 9, 3):
    cols = st.columns(3)
    for j in range(3):
        idx = i + j
        label = st.session_state.board[idx]
        cols[j].button(
            label if label != " " else " ",
            key=f"btn_{idx}",
            on_click=handle_click,
            args=(idx,),
            use_container_width=True,
            disabled=st.session_state.game_over or st.session_state.board[idx] != " "
        )

st.write("---")

col_btn1, col_btn2 = st.columns(2)
col_btn1.button("🎮 Play Again", on_click=reset_board, use_container_width=True)
col_btn2.button("🔄 Reset Score", on_click=reset_all, use_container_width=True)
