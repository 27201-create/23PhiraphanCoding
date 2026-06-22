print("โปรแกรมคำนวณคะแนน")

math = int(input("ระบุคะแนนวิชาคณิตศาสตร์"))
science = int(input("ระบุคะแนนวิชาวิทยาศาสตร์"))
thai = int(input("ระบุคะแนนวิชาภาษาไทย"))

total_point = math + science +thai
average = total_point / 3

print("คะแนนรวม", total_point)
print("คะแนนเฉลี่ย", average)
if total_point / 3 >= 80:
    print("ดีเยี่ยม")
elif total_point / 3 >= 60:
    print("ผ่าน")
else :
    print("ควรปรับปรุง")
print("made by phiraphan changkiew Win No.23")