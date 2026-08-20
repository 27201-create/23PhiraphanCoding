import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ข้อมูลผู้ใช้งานในระบบ (Username: Password)
USERS = {
    "teacher": {"pass": "1234", "role": "ครู", "name": "ครูสมชาย ใจดี"},
    "student": {"pass": "072628", "role": "นักเรียน", "name": "พีรพันธุ์ ช้างเขียว"},
    "parent": {"pass": "1234", "role": "ผู้ปกครอง", "name": "ผู้ปกครองพีรพันธุ์"}
}

# ข้อมูลนักเรียน
student = {
    "name": "พีรพันธุ์ ช้างเขียว",
    "class": "ม.4/4",
    "number": 23,
    "base_score": 100,
    "logs": []
}

def get_behavior_advice(score):
    if score < 50:
        return {"level": "🔴 วิกฤต (ต่ำกว่า 50 คะแนน)", "action": "ต้องพบครูฝ่ายปกครองพร้อมผู้ปกครองด่วน ห้ามกระทำผิดซ้ำ และต้องทำกิจกรรมบำเพ็ญประโยชน์", "color": "#E74C3C"}
    elif score < 60:
        return {"level": "🟠 เตือนระดับสูง (ต่ำกว่า 60 คะแนน)", "action": "ต้องรายงานตัวกับครูที่ปรึกษาทุกสัปดาห์ ทบทวนระเบียบโรงเรียน และหลีกเลี่ยงความเสี่ยงถูกตัดคะแนน", "color": "#E67E22"}
    elif score < 70:
        return {"level": "🟡 เตือนระดับต้น (ต่ำกว่า 70 คะแนน)", "action": "ควรระวังเรื่องความประพฤติ การแต่งกาย และการเข้าเรียน เร่งทำกิจกรรมบวกคะแนนเพิ่ม", "color": "#F1C40F"}
    else:
        return {"level": "🟢 ปกติ (70 คะแนนขึ้นไป)", "action": "รักษามาตรฐานความประพฤติตามระเบียบโรงเรียนต่อไป", "color": "#2ECC71"}

# --- หน้าต่างสมัครสมาชิก ---
class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("สมัครสมาชิก - D-Point System")
        self.geometry("380x380")
        self.config(bg="#F5F6FA")
        self.resizable(False, False)

        tk.Label(self, text="📝 สมัครสมาชิกใหม่", font=("Helvetica", 14, "bold"), bg="#F5F6FA", fg="#2C3E50").pack(pady=15)

        frame = tk.Frame(self, bg="#F5F6FA")
        frame.pack(pady=5)

        tk.Label(frame, text="ชื่อ-นามสกุล:", font=("Helvetica", 10), bg="#F5F6FA").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_fullname = ttk.Entry(frame, font=("Helvetica", 10))
        self.entry_fullname.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="ชื่อผู้ใช้งาน (Username):", font=("Helvetica", 10), bg="#F5F6FA").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_user = ttk.Entry(frame, font=("Helvetica", 10))
        self.entry_user.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="รหัสผ่าน:", font=("Helvetica", 10), bg="#F5F6FA").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_pass = ttk.Entry(frame, show="*", font=("Helvetica", 10))
        self.entry_pass.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="สถานะ / สถานะบทบาท:", font=("Helvetica", 10), bg="#F5F6FA").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.role_combo = ttk.Combobox(frame, values=["นักเรียน", "ครู", "ผู้ปกครอง"], state="readonly", font=("Helvetica", 10), width=17)
        self.role_combo.grid(row=3, column=1, pady=5)
        self.role_combo.current(0)

        tk.Button(self, text="ยืนยันลงทะเบียน", bg="#2ECC71", fg="white", font=("Helvetica", 10, "bold"),
                  relief=tk.FLAT, command=self.register_user, cursor="hand2", padx=20, pady=5).pack(pady=20)

    def register_user(self):
        fullname = self.entry_fullname.get().strip()
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        role = self.role_combo.get()

        if not fullname or not username or not password:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกข้อมูลให้ครบทุกช่อง!", parent=self)
            return

        if username in USERS:
            messagebox.showerror("ข้อผิดพลาด", "ชื่อผู้ใช้งานนี้มีอยู่ในระบบแล้ว!", parent=self)
            return

        USERS[username] = {
            "pass": password,
            "role": role,
            "name": fullname
        }

        messagebox.showinfo("สำเร็จ", "ลงทะเบียนเรียบร้อยแล้ว! สามารถใช้ Username นี้เข้าสู่ระบบได้ทันที", parent=self)
        self.destroy()

# --- หน้าต่าง Login ---
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("ลงชื่อเข้าใช้ - D-Point System")
        self.root.geometry("380x350")
        self.root.config(bg="#F5F6FA")
        self.root.resizable(False, False)

        tk.Label(root, text="🔒 เข้าสู่ระบบ D-Point", font=("Helvetica", 16, "bold"), bg="#F5F6FA", fg="#2C3E50").pack(pady=15)

        frame = tk.Frame(root, bg="#F5F6FA")
        frame.pack(pady=5)

        tk.Label(frame, text="ชื่อผู้ใช้งาน:", font=("Helvetica", 10), bg="#F5F6FA").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_user = ttk.Entry(frame, font=("Helvetica", 10))
        self.entry_user.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="รหัสผ่าน:", font=("Helvetica", 10), bg="#F5F6FA").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_pass = ttk.Entry(frame, show="*", font=("Helvetica", 10))
        self.entry_pass.grid(row=1, column=1, pady=5)

        btn_frame = tk.Frame(root, bg="#F5F6FA")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="เข้าสู่ระบบ", bg="#3498DB", fg="white", font=("Helvetica", 10, "bold"),
                  relief=tk.FLAT, command=self.check_login, cursor="hand2", padx=15, pady=5).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="สร้างบัญชีใหม่", bg="#E67E22", fg="white", font=("Helvetica", 10, "bold"),
                  relief=tk.FLAT, command=self.open_register, cursor="hand2", padx=15, pady=5).pack(side=tk.LEFT, padx=5)

    def check_login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if username in USERS and USERS[username]["pass"] == password:
            user_info = USERS[username]
            self.root.destroy()
            main_root = tk.Tk()
            DPointGUI(main_root, user_info)
            main_root.mainloop()
        else:
            messagebox.showerror("ผิดพลาด", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง!")

    def open_register(self):
        RegisterWindow(self.root)

# --- หน้าต่างหลัก (D-Point GUI) ---
class DPointGUI:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("ระบบจัดการคะแนนความประพฤติ (D-Point System)")
        self.root.geometry("820x580")
        self.root.config(bg="#F5F6FA")

        header_frame = tk.Frame(self.root, bg="#2C3E50", pady=10, padx=15)
        header_frame.pack(fill=tk.X)
        
        student_info = f"📋 ข้อมูล: {student['name']} | ชั้น {student['class']} เลขที่ {student['number']}"
        user_info_str = f"👤 ผู้ใช้งาน: {current_user['name']} ({current_user['role']})"
        
        tk.Label(header_frame, text=student_info, font=("Helvetica", 11, "bold"), fg="white", bg="#2C3E50").pack(side=tk.LEFT)
        
        # ส่วนแสดงชื่อผู้ใช้และปุ่มสลับบัญชีทางด้านขวา
        right_header = tk.Frame(header_frame, bg="#2C3E50")
        right_header.pack(side=tk.RIGHT)
        
        tk.Label(right_header, text=user_info_str, font=("Helvetica", 10), fg="#BDC3C7", bg="#2C3E50").pack(side=tk.LEFT, padx=(0, 10))
        
        btn_logout = tk.Button(right_header, text="🔄 สลับบัญชี", bg="#E74C3C", fg="white", font=("Helvetica", 9, "bold"),
                               relief=tk.FLAT, command=self.logout, cursor="hand2", padx=8, pady=2)
        btn_logout.pack(side=tk.RIGHT)

        main_frame = tk.Frame(self.root, bg="#F5F6FA", padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        if self.current_user["role"] == "ครู":
            left_frame = tk.LabelFrame(main_frame, text=" บันทึกรายการ (เฉพาะครู) ", font=("Helvetica", 11, "bold"), bg="white", padx=15, pady=15)
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

        right_frame = tk.Frame(main_frame, bg="#F5F6FA")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.card_score = tk.Frame(right_frame, bg="white", highlightthickness=1, highlightbackground="#DCDDE1", pady=10)
        self.card_score.pack(fill=tk.X, pady=(0, 10))

        self.lbl_score = tk.Label(self.card_score, text="100", font=("Helvetica", 24, "bold"), bg="white")
        self.lbl_score.pack()

        self.lbl_level = tk.Label(self.card_score, text="", font=("Helvetica", 10, "bold"), bg="white")
        self.lbl_level.pack()

        self.lbl_action = tk.Label(self.card_score, text="", font=("Helvetica", 9), bg="white", wraplength=350, justify=tk.CENTER)
        self.lbl_action.pack(pady=5)

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
        total_change = sum(item["points"] for item in student["logs"])
        current_score = max(0, student["base_score"] + total_change)
        advice = get_behavior_advice(current_score)

        self.lbl_score.config(text=f"{current_score} / 100", fg=advice["color"])
        self.lbl_level.config(text=advice["level"], fg=advice["color"])
        self.lbl_action.config(text=f"👉 {advice['action']}")

        for item in self.tree.get_children():
            self.tree.delete(item)

        for log in reversed(student["logs"]):
            sign = "+" if log["points"] > 0 else ""
            self.tree.insert("", tk.END, values=(log["date"], log["reason"], f"{sign}{log['points']}"))

    def add_log(self, is_positive=True):
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

    def logout(self):
        """ออกจากระบบแล้วเปิดหน้า Login ขึ้นมาใหม่"""
        if messagebox.askyesno("ยืนยัน", "คุณต้องการสลับบัญชีหรือออกจากระบบใช่หรือไม่?"):
            self.root.destroy()
            login_root = tk.Tk()
            LoginWindow(login_root)
            login_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()