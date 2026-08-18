import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ข้อมูลนักเรียนตั้งต้น (โครงสร้างเดิมของคุณ)
student = {
    "name": "พีรพันธุ์ ช้างเขียว",
    "class": "ม.4/4",
    "number": 23,
    "base_score": 100,
    "logs": []
}

def get_behavior_advice(score):
    """ฟังก์ชันประเมินข้อควรปฏิบัติตามระดับคะแนน (ฟังก์ชันเดิม)"""
    if score < 50:
        return {
            "level": "🔴 วิกฤต (ต่ำกว่า 50 คะแนน)",
            "action": "ต้องพบครูฝ่ายปกครองพร้อมผู้ปกครองด่วน ห้ามกระทำผิดซ้ำ และต้องทำกิจกรรมบำเพ็ญประโยชน์",
            "color": "#E74C3C"
        }
    elif score < 60:
        return {
            "level": "🟠 เตือนระดับสูง (ต่ำกว่า 60 คะแนน)",
            "action": "ต้องรายงานตัวกับครูที่ปรึกษาทุกสัปดาห์ ทบทวนระเบียบโรงเรียน และหลีกเลี่ยงความเสี่ยงถูกตัดคะแนน",
            "color": "#E67E22"
        }
    elif score < 70:
        return {
            "level": "🟡 เตือนระดับต้น (ต่ำกว่า 70 คะแนน)",
            "action": "ควรระวังเรื่องความประพฤติ การแต่งกาย และการเข้าเรียน เร่งทำกิจกรรมบวกคะแนนเพิ่ม",
            "color": "#F1C40F"
        }
    else:
        return {
            "level": "🟢 ปกติ (70 คะแนนขึ้นไป)",
            "action": "รักษามาตรฐานความประพฤติตามระเบียบโรงเรียนต่อไป",
            "color": "#2ECC71"
        }

class DPointGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ระบบจัดการคะแนนความประพฤติ (D-Point System)")
        self.root.geometry("780x560")
        self.root.config(bg="#F5F6FA")

        # Header ข้อมูลนักเรียน
        header_frame = tk.Frame(self.root, bg="#2C3E50", pady=12)
        header_frame.pack(fill=tk.X)
        
        student_info = f"📋 {student['name']} | ชั้น {student['class']} เลขที่ {student['number']}"
        tk.Label(header_frame, text=student_info, font=("Helvetica", 14, "bold"), fg="white", bg="#2C3E50").pack()

        # Frame รวมการทำงาน
        main_frame = tk.Frame(self.root, bg="#F5F6FA", padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ฝั่งซ้าย: ฟอร์มกรอกข้อมูล
        left_frame = tk.LabelFrame(main_frame, text=" บันทึกรายการ ", font=("Helvetica", 11, "bold"), bg="white", padx=15, pady=15)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(left_frame, text="จำนวนคะแนน:", bg="white", font=("Helvetica", 10)).pack(anchor=tk.W, pady=(5, 2))
        self.entry_pts = ttk.Entry(left_frame, font=("Helvetica", 10))
        self.entry_pts.pack(fill=tk.X, pady=(0, 10))

        tk.Label(left_frame, text="เหตุผล / รายการ:", bg="white", font=("Helvetica", 10)).pack(anchor=tk.W, pady=(5, 2))
        self.entry_reason = ttk.Entry(left_frame, font=("Helvetica", 10))
        self.entry_reason.pack(fill=tk.X, pady=(0, 15))

        btn_add = tk.Button(left_frame, text="➕ เพิ่มคะแนน (+)", bg="#2ECC71", fg="white", font=("Helvetica", 10, "bold"),
                            relief=tk.FLAT, command=lambda: self.add_log(is_positive=True), cursor="hand2")
        btn_add.pack(fill=tk.X, pady=5, ipady=5)

        btn_deduct = tk.Button(left_frame, text="➖ ตัดคะแนน (-)", bg="#E74C3C", fg="white", font=("Helvetica", 10, "bold"),
                               relief=tk.FLAT, command=lambda: self.add_log(is_positive=False), cursor="hand2")
        btn_deduct.pack(fill=tk.X, pady=5, ipady=5)

        # ฝั่งขวา: แสดงคะแนนและประวัติ
        right_frame = tk.Frame(main_frame, bg="#F5F6FA")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # การ์ดคะแนน
        self.card_score = tk.Frame(right_frame, bg="white", highlightthickness=1, highlightbackground="#DCDDE1", pady=10)
        self.card_score.pack(fill=tk.X, pady=(0, 10))

        self.lbl_score = tk.Label(self.card_score, text="100", font=("Helvetica", 24, "bold"), bg="white")
        self.lbl_score.pack()

        self.lbl_level = tk.Label(self.card_score, text="", font=("Helvetica", 10, "bold"), bg="white")
        self.lbl_level.pack()

        self.lbl_action = tk.Label(self.card_score, text="", font=("Helvetica", 9), bg="white", wraplength=350, justify=tk.CENTER)
        self.lbl_action.pack(pady=5)

        # ตารางประวัติ (Treeview)
        history_frame = tk.LabelFrame(right_frame, text=" ประวัติรายการทั้งหมด ", font=("Helvetica", 11, "bold"), bg="white", padx=10, pady=10)
        history_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("date", "reason", "points")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=6)
        self.tree.heading("date", text="วัน-เวลา")
        self.tree.heading("reason", text="เหตุผล")
        self.tree.heading("points", text="คะแนน")

        self.tree.column("date", width=110, anchor=tk.CENTER)
        self.tree.column("reason", width=170, anchor=tk.W)
        self.tree.column("points", width=60, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.update_ui()

    def update_ui(self):
        """คำนวณและอัปเดตข้อมูลบน GUI"""
        total_change = sum(item["points"] for item in student["logs"])
        current_score = max(0, student["base_score"] + total_change)
        advice = get_behavior_advice(current_score)

        # อัปเดตการ์ดคะแนน
        self.lbl_score.config(text=f"{current_score} / 100", fg=advice["color"])
        self.lbl_level.config(text=advice["level"], fg=advice["color"])
        self.lbl_action.config(text=f"👉 {advice['action']}")

        # อัปเดตรายการในตาราง
        for item in self.tree.get_children():
            self.tree.delete(item)

        for log in reversed(student["logs"]):
            sign = "+" if log["points"] > 0 else ""
            self.tree.insert("", tk.END, values=(log["date"], log["reason"], f"{sign}{log['points']}"))

    def add_log(self, is_positive=True):
        """บันทึกรายการเพิ่ม/ตัดคะแนน"""
        pts_text = self.entry_pts.get().strip()
        reason = self.entry_reason.get().strip() or "ไม่ระบุเหตุผล"

        try:
            pts = float(pts_text)
            final_pts = abs(pts) if is_positive else -abs(pts)

            student["logs"].append({
                "points": final_pts,
                "reason": reason,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")
            })

            self.entry_pts.delete(0, tk.END)
            self.entry_reason.delete(0, tk.END)
            self.update_ui()
            messagebox.showinfo("สำเร็จ", "บันทึกรายการสำเร็จ!")
        except ValueError:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกตัวเลขคะแนนให้ถูกต้อง!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DPointGUI(root)
    root.mainloop()