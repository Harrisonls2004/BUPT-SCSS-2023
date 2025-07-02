import turtle

def drawLine(draw):   #绘制单段数码管
    turtle.pendown() if draw else turtle.penup()
    turtle.fd(40)
    turtle.right(90)
def drawDigit(digit): #根据数字绘制七段数码管
    drawLine(True) if digit in [2,3,4,5,6,8,9] else drawLine(False)
    drawLine(True) if digit in [0,1,3,4,5,6,7,8,9] else drawLine(False)
    drawLine(True) if digit in [0,2,3,5,6,8,9] else drawLine(False)
    drawLine(True) if digit in [0,2,6,8] else drawLine(False)
    turtle.left(90)
    drawLine(True) if digit in [0,4,5,6,8,9] else drawLine(False)
    drawLine(True) if digit in [0,2,3,5,6,7,8,9] else drawLine(False)
    drawLine(True) if digit in [0,1,2,3,4,7,8,9] else drawLine(False)
    turtle.left(180)
    turtle.penup() #为绘制后续数字确定位置
    turtle.fd(20)  #为绘制后续数字确定位置
    
def drawDate(date): #根据日期绘制七段数码管
    for i in date:
        if i == '-':
            turtle.write('年')
            turtle.fd(20)
        elif i == '=':
            turtle.write('月')
            turtle.fd(20)
        elif i == '+':
            turtle.write('日')
            turtle.fd(20)
        else:
            drawDigit(eval(i)) 

def main():
    turtle.setup(800,350,200,200)
    turtle.penup()
    turtle.fd(-300)
    turtle.pendown()
    turtle.pensize(5)
    turtle.pencolor("red")
    drawDate('20250422')
    turtle.hideturtle()
    turtle.done()
    
main()