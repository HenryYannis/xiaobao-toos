import turtle
import time
turtle.bgcolor("black")
turtle.pencolor("white")
turtle.penup()
turtle.goto(0, -100)
turtle.pendown()
for i in range(10, -1, -1):
    turtle.write(i, align="center", font=("HeiTi", 200, "bold"))
    time.sleep(1)
    turtle.clear()
turtle.done()
