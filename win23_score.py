subj1 = int(input("Enter your score: "))
subj2 = int(input("Enter your score: "))
subj3 = int(input("Enter your score: "))
total_score = subj1 + subj2 + subj3
average = total_score/3
print("total score: ", total_score)
print("คะแนนเฉลี่ย: ", average)
if total_score / 3 >= 80:
    print("ดีเยี่ยม")
elif total_score / 3 >= 60:
    print("ผ่าน")
else:
    print("ควรปรับปรุง")