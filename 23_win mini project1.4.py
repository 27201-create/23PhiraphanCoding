import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ข้อมูลผู้ใช้งานในระบบ (Username: Password)
USERS = {
    "teacher": {"pass": "1234", "role": "ครู", "name": "ครูสมชาย ใจดี"},
    "student": {"pass": "072628", "role": "นักเรียน", "name": "พีรพันธุ์ ช้างเขียว"},
    "parent": {"pass": "1234", "role": "ผู้ปกครอง", "name": "ผู้ปกครองพีรพันธุ์", "child_username": "student"}
}

# ฐานข้อมูลนักเรียน (จัดเก็บตาม Username)
STUDENTS_DATA = {
    "student": {
        "name": "พีรพันธุ์ ช้างเขียว",
        "class": "ม.4/4",
        "number": "23",
        "base_score": 100,
        "logs": []
    }
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
        self.geometry("420x480")
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

        tk.Label(frame, text="สถานะ / บทบาท:", font=("Helvetica", 10), bg="#F5F6FA").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.role_combo = ttk.Combobox(frame, values=["นักเรียน", "ครู", "ผู้ปกครอง"], state="readonly", font=("Helvetica", 10), width=17)
        self.role_combo.grid(row=3, column=1, pady=5)
        self.role_combo.current(0)
        self.role_combo.bind("<<ComboboxSelected>>", self.toggle_dynamic_fields)

        # --- ฟิลด์สำหรับนักเรียน ---
        self.lbl_class = tk.Label(frame, text="ระดับชั้นปี:", font=("Helvetica", 10), bg="#F5F6FA")
        self.lbl_class.grid(row=4, column=0, sticky=tk.W, pady=5)
        self.class_combo = ttk.Combobox(frame, values=["ม.1/1", "ม.1/2", "ม.2/1", "ม.2/2", "ม.3/1", "ม.3/2", "ม.4/1", "ม.4/4", "ม.5/1", "ม.6/1"], font=("Helvetica", 10), width=17)
        self.class_combo.grid(row=4, column=1, pady=5)
        self.class_combo.set("ม.4/4")

        self.lbl_number = tk.Label(frame, text="เลขที่:", font=("Helvetica", 10), bg="#F5F6FA")
        self.lbl_number.grid(row=5, column=0, sticky=tk.W, pady=5)
        self.entry_number = ttk.Entry(frame, font=("Helvetica", 10))
        self.entry_number.grid(row=5, column=1, pady=5)

        # --- ฟิลด์สำหรับผู้ปกครอง ---
        self.lbl_child = tk.Label(frame, text="เป็นผู้ปกครองของ:", font=("Helvetica", 10), bg="#F5F6FA")
        self.lbl_child.grid(row=6, column=0, sticky=tk.W, pady=5)
        self.child_combo = ttk.Combobox(frame, state="readonly", font=("Helvetica", 10), width=17)
        self.child_combo.grid(row=6, column=1, pady=5)

        tk.Button(self, text="ยืนยันลงทะเบียน", bg="#2ECC71", fg="white", font=("Helvetica", 10, "bold"),
                  relief=tk.FLAT, command=self.register_user, cursor="hand2", padx=20, pady=5).pack(pady=20)

        # เริ่มต้นอัปเดตฟิลด์ตามบทบาท
        self.update_child_combo()
        self.toggle_dynamic_fields()

    def update_child_combo(self):
        """อัปเดตรายชื่อนักเรียนในตัวเลือกผู้ปกครอง"""
        self.student_keys = list(STUDENTS_DATA.keys())
        student_names = [f"{STUDENTS_DATA[k]['name']} ({STUDENTS_DATA[k]['class']})" for k in self.student_keys]
        self.child_combo['values'] = student_names
        if student_names:
            self.child_combo.current(0)

    def toggle_dynamic_fields(self, event=None):
        """ซ่อน/แสดง ฟิลด์ข้อมูลตามบทบาทที่เลือก"""
        role = self.role_combo.get()
        if role == "นักเรียน":
            self.lbl_class.grid()
            self.class_combo.grid()
            self.lbl_number.grid()
            self.entry_number.grid()
            self.lbl_child.grid_remove()
            self.child_combo.grid_remove()
        elif role == "ผู้ปกครอง":
            self.lbl_class.grid_remove()
            self.class_combo.grid_remove()
            self.lbl_number.grid_remove()
            self.entry_number.grid_remove()
            self.lbl_child.grid()
            self.child_combo.grid()
            self.update_child_combo()
        else: # ครู
            self.lbl_class.grid_remove()
            self.class_combo.grid_remove()
            self.lbl_number.grid_remove()
            self.entry_number.grid_remove()
            self.lbl_child.grid_remove()
            self.child_combo.grid_remove()

    def register_user(self):
        fullname = self.entry_fullname.get().strip()
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        role = self.role_combo.get()

        if not fullname or not username or not password:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกข้อมูลพื้นฐานให้ครบถ้วน!", parent=self)
            return

        if username in USERS:
            messagebox.showerror("ข้อผิดพลาด", "ชื่อผู้ใช้งานนี้มีอยู่ในระบบแล้ว!", parent=self)
            return

        # ตรวจสอบข้อมูลเฉพาะบทบาท
        child_username = None
        if role == "นักเรียน":
            num = self.entry_number.get().strip()
            student_class = self.class_combo.get().strip()
            if not num or not student_class:
                messagebox.showerror("ข้อผิดพลาด", "กรุณาระบุชั้นปีและเลขที่!", parent=self)
                return
        elif role == "ผู้ปกครอง":
            if not self.student_keys:
                messagebox.showerror("ข้อผิดพลาด", "ยังไม่มีข้อมูลนักเรียนในระบบ กรุณาให้นักเรียนลงทะเบียนก่อน!", parent=self)
                return
            idx = self.child_combo.current()
            child_username = self.student_keys[idx]

        # บันทึกข้อมูลบัญชี
        user_data = {
            "pass": password,
            "role": role,
            "name": fullname
        }
        if child_username:
            user_data["child_username"] = child_username

        USERS[username] = user_data

        # หากเป็นนักเรียน ให้สร้างข้อมูลในฐานข้อมูลนักเรียน
        if role == "นักเรียน":
            STUDENTS_DATA[username] = {
                "name": fullname,
                "class": self.class_combo.get().strip(),
                "number": self.entry_number.get().strip(),
                "base_score": 100,
                "logs": []
            }

        messagebox.showinfo("สำเร็จ", "ลงทะเบียนเรียบร้อยแล้ว!", parent=self)
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
            user_info["username"] = username
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
        
        # กำหนดนักเรียนที่จะแสดงผลตามบทบาท
        username = self.current_user.get("username", "")
        role = self.current_user.get("role", "")

        if role == "นักเรียน":
            self.selected_student_username = username
        elif role == "ผู้ปกครอง":
            # ดึง Username ของลูกที่ผูกไว้
            self.selected_student_username = self.current_user.get("child_username")
        else:  # ครู
            self.selected_student_username = list(STUDENTS_DATA.keys())[0] if STUDENTS_DATA else None

        self.root.title("ระบบจัดการคะแนนความประพฤติ (D-Point System)")
        self.root.geometry("860x600")
        self.root.config(bg="#F5F6FA")

        # Header Frame
        header_frame = tk.Frame(self.root, bg="#2C3E50", pady=10, padx=15)
        header_frame.pack(fill=tk.X)
        
        self.lbl_student_info = tk.Label(header_frame, text="", font=("Helvetica", 11, "bold"), fg="white", bg="#2C3E50")
        self.lbl_student_info.pack(side=tk.LEFT)
        
        right_header = tk.Frame(header_frame, bg="#2C3E50")
        right_header.pack(side=tk.RIGHT)
        
        user_info_str = f"👤 ผู้ใช้งาน: {current_user['name']} ({current_user['role']})"
        tk.Label(right_header, text=user_info_str, font=("Helvetica", 10), fg="#BDC3C7", bg="#2C3E50").pack(side=tk.LEFT, padx=(0, 10))
        
        btn_logout = tk.Button(right_header, text="🔄 สลับบัญชี", bg="#E74C3C", fg="white", font=("Helvetica", 9, "bold"),
                               relief=tk.FLAT, command=self.logout, cursor="hand2", padx=8, pady=2)
        btn_logout.pack(side=tk.RIGHT)

        main_frame = tk.Frame(self.root, bg="#F5F6FA", padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Panel ซ้าย (เฉพาะครู)
        if self.current_user["role"] == "ครู":
            left_frame = tk.LabelFrame(main_frame, text=" บันทึกรายการ (เฉพาะครู) ", font=("Helvetica", 11, "bold"), bg="white", padx=15, pady=15)
            left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

            tk.Label(left_frame, text="เลือกลด/เพิ่มคะแนนให้นักเรียน:", bg="white", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(0, 2))
            
            self.student_combo = ttk.Combobox(left_frame, state="readonly", font=("Helvetica", 10))
            self.student_combo.pack(fill=tk.X, pady=(0, 15))
            self.student_combo.bind("<<ComboboxSelected>>", self.on_select_student)

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

            self.update_student_combo()

        # Panel ขวา (แสดงคะแนนและประวัติ)
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

    def update_student_combo(self):
        """อัปเดตรายชื่อนักเรียนใน Dropdown สำหรับครู"""
        self.student_list = list(STUDENTS_DATA.keys())
        combo_values = [f"{STUDENTS_DATA[u]['name']} ({STUDENTS_DATA[u]['class']} เลขที่ {STUDENTS_DATA[u]['number']})" for u in self.student_list]
        self.student_combo['values'] = combo_values
        if self.selected_student_username in self.student_list:
            idx = self.student_list.index(self.selected_student_username)
            self.student_combo.current(idx)

    def on_select_student(self, event):
        """เมื่อครูเลือกนักเรียนคนใหม่จาก Dropdown"""
        idx = self.student_combo.current()
        if idx != -1:
            self.selected_student_username = self.student_list[idx]
            self.update_ui()

    def update_ui(self):
        """อัปเดตหน้าจอตามข้อมูลนักเรียนที่ถูกเลือก"""
        if not self.selected_student_username or self.selected_student_username not in STUDENTS_DATA:
            self.lbl_student_info.config(text="⚠️ ไม่พบข้อมูลนักเรียน")
            return

        student_info = STUDENTS_DATA[self.selected_student_username]
        
        # อัปเดต Header
        info_str = f"📋 ข้อมูล: {student_info['name']} | ชั้น {student_info['class']} เลขที่ {student_info['number']}"
        self.lbl_student_info.config(text=info_str)

        # คำนวณคะแนน
        total_change = sum(item["points"] for item in student_info["logs"])
        current_score = max(0, student_info["base_score"] + total_change)
        advice = get_behavior_advice(current_score)

        self.lbl_score.config(text=f"{current_score} / 100", fg=advice["color"])
        self.lbl_level.config(text=advice["level"], fg=advice["color"])
        self.lbl_action.config(text=f"👉 {advice['action']}")

        # อัปเดตตารางประวัติ
        for item in self.tree.get_children():
            self.tree.delete(item)

        for log in reversed(student_info["logs"]):
            sign = "+" if log["points"] > 0 else ""
            self.tree.insert("", tk.END, values=(log["date"], log["reason"], f"{sign}{log['points']}"))

    def add_log(self, is_positive=True):
        if not self.selected_student_username:
            messagebox.showerror("ข้อผิดพลาด", "ไม่พบบัญชีนักเรียนที่ต้องการบันทึกคะแนน!")
            return

        pts_text = self.entry_pts.get().strip()
        reason = self.entry_reason.get().strip() or "ไม่ระบุเหตุผล"

        try:
            pts = float(pts_text)
            final_pts = abs(pts) if is_positive else -abs(pts)

            STUDENTS_DATA[self.selected_student_username]["logs"].append({
                "points": final_pts,
                "reason": reason,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")
            })

            self.entry_pts.delete(0, tk.END)
            self.entry_reason.delete(0, tk.END)
            self.update_ui()
            messagebox.showinfo("สำเร็จ", f"บันทึกรายการสำหรับ {STUDENTS_DATA[self.selected_student_username]['name']} สำเร็จ!")
        except ValueError:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกตัวเลขคะแนนให้ถูกต้อง!")

    def logout(self):
        if messagebox.askyesno("ยืนยัน", "คุณต้องการสลับบัญชีหรือออกจากระบบใช่หรือไม่?"):
            self.root.destroy()
            login_root = tk.Tk()
            LoginWindow(login_root)
            login_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
