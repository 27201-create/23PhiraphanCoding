print ("คำนวณBMI")

kg = float(input("ใส่น้ำหนัก:"))
m = float(input("ใส่ส่วนสูง(เมตร):"))
BMI = kg / (m * m)

print ("ค่า BMI:", BMI)
if BMI <= 18.5:
    print("น้ำหนักน้อย")
elif BMI <= 22.9:
    print("ปกติ")
elif BMI <= 24.9:
    print("น้ำหนักเกิน")
else:
    print("อ้วน")
