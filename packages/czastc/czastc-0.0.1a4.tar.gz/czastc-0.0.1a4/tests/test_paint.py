import turtle
import czastc.paint
turtle = turtle.Turtle()
color_list = czastc.paint.generate_color_gradient(100, [[255, 255, 0], [255, 0, 0], [255, 0, 255]])
for i, color in enumerate(color_list):
    if i % 2 == 0:
        turtle.right(90)
        turtle.color(color)
        turtle.forward(100)
        turtle.left(90)
        turtle.forward(1)
    else:
        turtle.left(90)
        turtle.color(color)
        turtle.forward(100)
        turtle.right(90)
        turtle.forward(1)
turtle.screen.mainloop()
