import random
secret_number = random.randint(1, 101)
count = 0
count += 1

print("ยินดีต้อนรับสู่เกมทายเลข")
while True:
    guess = int(input("ทายตัวเลข:"))
    if guess > secret_number:
        print("มากไป")
    elif guess < secret_number:
        print("น้อยไป")
    else:
        print("ถูกต้อง\nคุณทายถูกในครั้งที่", count)
        break