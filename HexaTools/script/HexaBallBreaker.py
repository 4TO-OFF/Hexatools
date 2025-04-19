import tkinter as tk
import random

# 📏 Paramètres du jeu
WIDTH = 600
HEIGHT = 400
BALL_SPEED = 4
PADDLE_SPEED = 20
BRICK_ROWS = 5
BRICK_COLS = 8

# 🎮 Fenêtre
root = tk.Tk()
root.title("🧱 Ball Breaker")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# 🟥 Briques
bricks = []
brick_width = WIDTH // BRICK_COLS
brick_height = 20
for i in range(BRICK_ROWS):
    for j in range(BRICK_COLS):
        x1 = j * brick_width
        y1 = i * brick_height
        x2 = x1 + brick_width - 2
        y2 = y1 + brick_height - 2
        brick = canvas.create_rectangle(x1, y1, x2, y2, fill="red")
        bricks.append(brick)

# 🟡 Balle
ball = canvas.create_oval(WIDTH//2-10, HEIGHT//2-10, WIDTH//2+10, HEIGHT//2+10, fill="yellow")
ball_dx = BALL_SPEED
ball_dy = -BALL_SPEED

# 🟩 Plateforme
paddle = canvas.create_rectangle(WIDTH//2-50, HEIGHT-20, WIDTH//2+50, HEIGHT-10, fill="white")

# 🧠 Mouvement plateforme
def move_paddle(event):
    x1, _, x2, _ = canvas.coords(paddle)
    if event.keysym == "Left" and x1 > 0:
        canvas.move(paddle, -PADDLE_SPEED, 0)
    elif event.keysym == "Right" and x2 < WIDTH:
        canvas.move(paddle, PADDLE_SPEED, 0)

root.bind("<Left>", move_paddle)
root.bind("<Right>", move_paddle)

# 🔁 Boucle de jeu
def game_loop():
    global ball_dx, ball_dy

    canvas.move(ball, ball_dx, ball_dy)
    ball_coords = canvas.coords(ball)
    paddle_coords = canvas.coords(paddle)

    # 🧱 Collision murs
    if ball_coords[0] <= 0 or ball_coords[2] >= WIDTH:
        ball_dx *= -1
    if ball_coords[1] <= 0:
        ball_dy *= -1

    # 🕳️ Balle tombée
    if ball_coords[3] >= HEIGHT:
        canvas.create_text(WIDTH//2, HEIGHT//2, text="Game Over", fill="white", font=("Arial", 24))
        return

    # 🟩 Collision paddle
    if (ball_coords[2] >= paddle_coords[0] and
        ball_coords[0] <= paddle_coords[2] and
        ball_coords[3] >= paddle_coords[1] and
        ball_coords[1] <= paddle_coords[3]):
        ball_dy *= -1

    # 💥 Collision briques
    for brick in bricks[:]:
        if canvas.bbox(ball) and canvas.bbox(brick):
            if canvas.bbox(ball)[2] > canvas.bbox(brick)[0] and \
               canvas.bbox(ball)[0] < canvas.bbox(brick)[2] and \
               canvas.bbox(ball)[3] > canvas.bbox(brick)[1] and \
               canvas.bbox(ball)[1] < canvas.bbox(brick)[3]:
                canvas.delete(brick)
                bricks.remove(brick)
                ball_dy *= -1
                break

    root.after(20, game_loop)

game_loop()
root.mainloop()
