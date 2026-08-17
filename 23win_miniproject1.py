from datetime import datetime

# ข้อมูลนักเรียนตั้งต้น
student = {
    "name": "พีรพันธุ์ ช้างเขียว",
    "class": "ม.4/4",
    "number": 23,
    "base_score": 100,
    "logs": []
}

def get_behavior_advice(score):
    """ฟังก์ชันประเมินข้อควรปฏิบัติตามระดับคะแนน"""
    if score < 50:
        return {
            "level": "🔴 วิกฤต (ต่ำกว่า 50 คะแนน)",
            "action": "ข้อควรปฏิบัติ: ต้องพบครูฝ่ายปกครองพร้อมผู้ปกครองด่วน ห้ามกระทำผิดซ้ำ และต้องทำกิจกรรมบำเพ็ญประโยชน์เพื่อฟื้นฟูคะแนน"
        }
    elif score < 60:
        return {
            "level": "🟠 เตือนระดับสูง (ต่ำกว่า 60 คะแนน)",
            "action": "ข้อควรปฏิบัติ: ต้องรายงานตัวกับครูที่ปรึกษาทุกสัปดาห์ ทบทวนระเบียบโรงเรียน และหลีกเลี่ยงความเสี่ยงถูกตัดคะแนนเพิ่ม"
        }
    elif score < 70:
        return {
            "level": "🟡 เตือนระดับต้น (ต่ำกว่า 70 คะแนน)",
            "action": "ข้อควรปฏิบัติ: ควรระวังเรื่องความประพฤติ การแต่งกาย และการเข้าเรียน เร่งทำกิจกรรมบวกคะแนนเพิ่ม"
        }
    else:
        return {
            "level": "🟢 ปกติ (70 คะแนนขึ้นไป)",
            "action": "ข้อควรปฏิบัติ: รักษามาตรฐานความประพฤติตามระเบียบโรงเรียนต่อไป"
        }

def display_report():
    """ฟังก์ชันคำนวณและแสดงผลหน้าจอ"""
    total_change = sum(item["points"] for item in student["logs"])
    current_score = max(0, student["base_score"] + total_change)
    advice = get_behavior_advice(current_score)
    
    print("\n" + "="*60)
    print(f"📋 สรุปคะแนนความประพฤติ: {student['name']} ({student['class']} เลขที่ {student['number']})")
    print("="*60)
    print(f"คะแนนคงเหลือปัจจุบัน: {current_score} / 100")
    print(f"สถานะปัจจุบัน: {advice['level']}")
    print(f"👉 {advice['action']}")
    print("-"*60)
    print("ประวัติรายการทั้งหมด:")
    
    if not student["logs"]:
        print("  (ยังไม่มีรายการ)")
    else:
        for idx, log in enumerate(student["logs"], 1):
            sign = "+" if log["points"] > 0 else ""
            print(f"  {idx}. [{log['date']}] {log['reason']}: {sign}{log['points']} คะแนน")
    print("="*60 + "\n")

# ==========================================
# ส่วนการทำงานหลัก (Interactive Menu)
# ==========================================
while True:
    display_report()
    print("เลือกทำรายการ:")
    print("1) เพิ่มคะแนน (+)")
    print("2) ตัดคะแนน (-)")
    print("3) ออกจากโปรแกรม")
    
    choice = input("กรอกหมายเลขเมนู (1-3): ").strip()
    
    if choice in ["1", "2"]:
        try:
            pts = float(input("กรอกจำนวนคะแนน (เช่น 5, 10, 15): "))
            reason = input("กรอกเหตุผล/รายการ: ").strip()
            
            if not reason:
                reason = "ไม่ระบุเหตุผล"
                
            # ถ้าเลือกตัดคะแนน ให้แปลงค่าเป็นติดลบ
            final_pts = abs(pts) if choice == "1" else -abs(pts)
            
            student["logs"].append({
                "points": final_pts,
                "reason": reason,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            print("\n✅ บันทึกรายการสำเร็จ!")
            
        except ValueError:
            print("\n❌ กรุณากรอกตัวเลขคะแนนให้ถูกต้อง!")
            
    elif choice == "3":
        print("\nขอบคุณที่ใช้งานระบบ D-Point!")
        break
    else:
        print("\n❌ เมนูไม่ถูกต้อง กรุณาเลือกใหม่อีกครั้ง")
