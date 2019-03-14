import random
secret =random.randint(1,10)


temp = input("guess the number I'm thinking :")
guess = int(temp)

while guess!=secret:
  if guess == secret:
         print("that's right")
        
  else:
    temp = input("try again:")
    guess=int(temp)
    if guess == secret:
      print("nice!!")
    else:
         if guess >secret:
             print(" a little bit smaller")
         if guess <secret:
             print("a little bit bigger")
    

    
print("game over")
input("任意键退出")
#程序不怎么牛啤  :-D