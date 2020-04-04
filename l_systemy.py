import turtle


# prevedie mi axiom podla pravidiel na novy axiom
def transform_axiom(axioms, rules, no_of_iterations):
    for _ in range(no_of_iterations):
        new = ''

        # prejde kazdy znak
        for char in axioms:
            if char in rules:
                new += rules[char]  # prida do noveho axiomu pravu stranu pravidla ak existuje pravidlo, napr F -> FFF
            else:
                new += char  # ak neexistuje pravidlo prida znak, napr "["
        axioms = new
    return axioms


def draw(axiom, angle):
    screen = turtle.Screen()
    turt = turtle.Turtle()

    turt.speed(50)

    turtle_positions = []  # For tracking turtle positions
    for c in axiom:
        if c == 'F':
            turt.forward(25)  # 20 bodov dopredu

        if c == '+':
            turt.left(angle)

        if c == '-':
            turt.right(angle)

        if c == '[':
            turtle_positions.append((turt.heading(), turt.pos()))  # vlozim do stacku poziciu

        if c == ']':
            heading, position = turtle_positions.pop()  # popnem zo stacku
            turt.penup()  # vypnem kreslenie
            turt.goto(position)  # presuniem sa na poziciu zo stacku
            turt.setheading(heading)  # nastavim heading
            turt.pendown()  # zapnem kreslenie

    screen.onkey(screen.bye, 'q')
    screen.listen()
    turtle.mainloop()


rules1 = {"F": "F+F-F-FF+F+F-F"}
axiom1 = 'F+F+F+F'
angle1 = 90

rules2 = {"F": "F+F--F+F"}
axiom2 = 'F++F++F'
angle2 = 60

rules3 = {"F": "F[+F]F[-F]F"}
axiom3 = 'F'
angle3 = 180 / 7.0

rules4 = {"F": "FF+[+F-F-F]-[-F+F+F]"}
axiom4 = 'F'
angle4 = 180 / 8.0

# draw(transform_axiom(axiom1, rules1, 2), angle1)
# draw(transform_axiom(axiom2, rules2, 2), angle2)
# draw(transform_axiom(axiom3, rules3, 2), angle3)
draw(transform_axiom(axiom4, rules4, 2), angle4)
