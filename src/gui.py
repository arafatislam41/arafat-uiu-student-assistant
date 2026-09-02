import sys
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox

sys.path.insert(0, str(Path(__file__).resolve().parent))

from profile import get_profile, update_profile
from cgpa import CourseResult, calculate_gpa, calculate_target_cgpa, can_reach_target_cgpa
from probation import check_probation_status, check_waiver_eligibility
from tuition import calculate_tuition, calculate_installments
from courses import get_course_info, normalize_code, check_prerequisites
from graduation import check_degree_progress, calculate_final_exam_target

# UIU Official Brand Colors
UIU_ORANGE = "#F26522"
UIU_ORANGE_HOVER = "#D9531E"
UIU_DARK_BG = "#121820"
UIU_SIDEBAR_BG = "#1A222D"
UIU_CARD_BG = "#222C3A"
UIU_TEXT_MUTED = "#9BA1A6"

ctk.set_appearance_mode("Dark")


class UIUAssistantGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UIU Student Assistant V2 — Official Edition")
        self.geometry("1000x700")
        self.minsize(880, 600)
        self.configure(fg_color=UIU_DARK_BG)

        self.profile = get_profile()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_tabs()

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=230, corner_radius=0, fg_color=UIU_SIDEBAR_BG)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)

        # UIU Logo Header Badge
        badge = ctk.CTkLabel(
            self.sidebar,
            text="UIU",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white",
            fg_color=UIU_ORANGE,
            corner_radius=8,
            width=85,
            height=45,
        )
        badge.grid(row=0, column=0, padx=20, pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="STUDENT ASSISTANT\nV2 Official Theme",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="white"
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Profile Card
        prof_card = ctk.CTkFrame(self.sidebar, fg_color=UIU_CARD_BG, corner_radius=8)
        prof_card.grid(row=2, column=0, padx=15, pady=10, sticky="ew")

        self.user_lbl = ctk.CTkLabel(prof_card, text=f"👤 {self.profile.get('name', 'Student')}", font=ctk.CTkFont(size=13, weight="bold"), text_color="white")
        self.user_lbl.pack(padx=10, pady=(8, 2))

        self.cgpa_lbl = ctk.CTkLabel(prof_card, text=f"CGPA: {self.profile.get('current_cgpa', 0.0):.2f}", font=ctk.CTkFont(size=12, weight="bold"), text_color=UIU_ORANGE)
        self.cgpa_lbl.pack(padx=10, pady=2)

        self.cr_lbl = ctk.CTkLabel(prof_card, text=f"Credits: {self.profile.get('completed_credits', 0.0):.1f}", font=ctk.CTkFont(size=11), text_color=UIU_TEXT_MUTED)
        self.cr_lbl.pack(padx=10, pady=(2, 8))

        ctk.CTkLabel(self.sidebar, text="Appearance:", font=ctk.CTkFont(size=11), text_color=UIU_TEXT_MUTED).grid(row=8, column=0, padx=20, pady=(10, 0))
        self.theme_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Dark", "Light"],
            command=ctk.set_appearance_mode,
            fg_color=UIU_CARD_BG,
            button_color=UIU_ORANGE,
            button_hover_color=UIU_ORANGE_HOVER
        )
        self.theme_menu.grid(row=9, column=0, padx=20, pady=(5, 20))

    def _build_main_tabs(self):
        self.tabview = ctk.CTkTabview(
            self,
            corner_radius=10,
            fg_color=UIU_SIDEBAR_BG,
            segmented_button_selected_color=UIU_ORANGE,
            segmented_button_selected_hover_color=UIU_ORANGE_HOVER,
            segmented_button_unselected_color=UIU_CARD_BG
        )
        self.tabview.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        self.tab_gpa = self.tabview.add("GPA Calc")
        self.tab_planner = self.tabview.add("Target Planner")
        self.tab_exam = self.tabview.add("Final Target")
        self.tab_tuition = self.tabview.add("Tuition & Installments")
        self.tab_degree = self.tabview.add("Degree Audit")
        self.tab_courses = self.tabview.add("Prerequisites")
        self.tab_profile = self.tabview.add("Profile")

        self._setup_gpa_tab()
        self._setup_planner_tab()
        self._setup_exam_tab()
        self._setup_tuition_tab()
        self._setup_degree_tab()
        self._setup_courses_tab()
        self._setup_profile_tab()

    # --- TAB 1: GPA CALCULATOR ---
    def _setup_gpa_tab(self):
        frame = self.tab_gpa
        ctk.CTkLabel(frame, text="Trimester GPA Calculator", font=ctk.CTkFont(size=18, weight="bold"), text_color=UIU_ORANGE).pack(pady=10)

        self.gpa_inputs = []
        scroll_frame = ctk.CTkScrollableFrame(frame, height=290, fg_color=UIU_CARD_BG)
        scroll_frame.pack(fill="x", padx=10, pady=10)

        for i in range(1, 6):
            row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=f"Course {i}:", width=70, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
            code_entry = ctk.CTkEntry(row, placeholder_text="Code (e.g. CSE1111)", width=140)
            code_entry.pack(side="left", padx=5)
            grade_opt = ctk.CTkOptionMenu(
                row,
                values=["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"],
                width=85,
                fg_color=UIU_ORANGE,
                button_color=UIU_ORANGE_HOVER
            )
            grade_opt.pack(side="left", padx=5)
            credit_entry = ctk.CTkEntry(row, placeholder_text="Credits", width=90)
            credit_entry.insert(0, "3.0")
            credit_entry.pack(side="left", padx=5)
            self.gpa_inputs.append((code_entry, grade_opt, credit_entry))

        calc_btn = ctk.CTkButton(frame, text="Calculate GPA", fg_color=UIU_ORANGE, hover_color=UIU_ORANGE_HOVER, command=self._compute_gpa)
        calc_btn.pack(pady=12)

        self.gpa_result_lbl = ctk.CTkLabel(frame, text="GPA: --", font=ctk.CTkFont(size=20, weight="bold"))
        self.gpa_result_lbl.pack(pady=5)

    def _compute_gpa(self):
        courses = []
        try:
            for code_e, grade_o, cr_e in self.gpa_inputs:
                code = code_e.get().strip()
                if not code:
                    continue
                courses.append(CourseResult(course_code=code, grade=grade_o.get(), credits=float(cr_e.get())))
            if not courses:
                messagebox.showwarning("Notice", "Please enter at least one course code.")
                return
            gpa = calculate_gpa(courses)
            self.gpa_result_lbl.configure(text=f"Calculated GPA: {gpa:.2f}", text_color=UIU_ORANGE)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid values: {e}")

    # --- TAB 2: TARGET PLANNER ---
    def _setup_planner_tab(self):
        frame = self.tab_planner
        ctk.CTkLabel(frame, text="Target CGPA Planner", font=ctk.CTkFont(size=18, weight="bold"), text_color=UIU_ORANGE).pack(pady=10)

        ctk.CTkLabel(frame, text="Target CGPA:").pack(pady=(10, 2))
        self.target_entry = ctk.CTkEntry(frame, placeholder_text="e.g. 3.25", width=220)
        self.target_entry.pack()

        ctk.CTkLabel(frame, text="Future Credits Planned:").pack(pady=(10, 2))
        self.future_cr_entry = ctk.CTkEntry(frame, placeholder_text="e.g. 15.0", width=220)
        self.future_cr_entry.insert(0, "15.0")
        self.future_cr_entry.pack()

        btn = ctk.CTkButton(frame, text="Evaluate Target", fg_color=UIU_ORANGE, hover_color=UIU_ORANGE_HOVER, command=self._compute_target)
        btn.pack(pady=15)

        self.planner_result = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=14))
        self.planner_result.pack(pady=10)

    def _compute_target(self):
        try:
            target = float(self.target_entry.get())
            future_cr = float(self.future_cr_entry.get())
            curr_cgpa = self.profile.get("current_cgpa", 0.0)
            curr_cr = self.profile.get("completed_credits", 0.0)

            req = calculate_target_cgpa(curr_cgpa, curr_cr, target, future_cr)
            reach = can_reach_target_cgpa(curr_cgpa, curr_cr, target, future_cr)

            if reach:
                self.planner_result.configure(text=f"Required Future GPA: {req:.2f}\n\nStatus: ✅ TARGET IS MATHEMATICALLY REACHABLE", text_color="#2ECC71")
            else:
                self.planner_result.configure(text=f"Required Future GPA: {req:.2f}\n\nStatus: ❌ TARGET UNREACHABLE (> 4.00 required)", text_color="#E74C3C")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- TAB 3: FINAL EXAM TARGET ---
    def _setup_exam_tab(self):
        frame = self.tab_exam
        ctk.CTkLabel(frame, text="Final Exam Target Calculator", font=ctk.CTkFont(size=18, weight="bold"), text_color=UIU_ORANGE).pack(pady=10)
        ctk.CTkLabel(frame, text="UIU Continuous: Attendance (5) + Quiz (25) + Midterm (30) = 60 Marks\nFinal Exam = 40 Marks", text_color=UIU_TEXT_MUTED).pack(pady=3)

        ctk.CTkLabel(frame, text="Attendance Marks (out of 5):").pack(pady=(6, 2))
        self.att_entry = ctk.CTkEntry(frame, width=220)
        self.att_entry.insert(0, "5.0")
        self.att_entry.pack()

        ctk.CTkLabel(frame, text="Quiz / Assignment Marks (out of 25):").pack(pady=(6, 2))
        self.quiz_entry = ctk.CTkEntry(frame, width=220)
        self.quiz_entry.insert(0, "20.0")
        self.quiz_entry.pack()

        ctk.CTkLabel(frame, text="Midterm Marks (out of 30):").pack(pady=(6, 2))
        self.mid_entry = ctk.CTkEntry(frame, width=220)
        self.mid_entry.insert(0, "22.0")
        self.mid_entry.pack()

        ctk.CTkLabel(frame, text="Target Grade:").pack(pady=(6, 2))
        self.exam_target_grade = ctk.CTkOptionMenu(
            frame,
            values=["A", "A-", "B+", "B", "B-", "C+", "C", "D"],
            width=120,
            fg_color=UIU_ORANGE,
            button_color=UIU_ORANGE_HOVER
        )
        self.exam_target_grade.pack()

        ctk.CTkButton(frame, text="Calculate Needed Final Marks", fg_color=UIU_ORANGE, hover_color=UIU_ORANGE_HOVER, command=self._compute_exam_target).pack(pady=14)
        self.exam_target_res = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=14))
        self.exam_target_res.pack(pady=5)

    def _compute_exam_target(self):
        try:
            att = float(self.att_entry.get())
            quiz = float(self.quiz_entry.get())
            mid = float(self.mid_entry.get())
            grade = self.exam_target_grade.get()

            res = calculate_final_exam_target(att, quiz, mid, grade)
            if res["is_achievable"]:
                msg = f"Continuous Total: {res['current_total']:.1f} / 60.0\nTarget: {grade} (Min {res['min_total_required']} marks)\n\n✅ Needed in Final: {res['needed_in_final']:.1f} / 40.0"
                self.exam_target_res.configure(text=msg, text_color="#2ECC71")
            else:
                msg = f"Continuous Total: {res['current_total']:.1f} / 60.0\nTarget: {grade}\n\n❌ {res['reason']}"
                self.exam_target_res.configure(text=msg, text_color="#E74C3C")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- TAB 4: TUITION & INSTALLMENTS ---
    def _setup_tuition_tab(self):
        frame = self.tab_tuition
        ctk.CTkLabel(frame, text="Tuition & 3-Installment Schedule", font=ctk.CTkFont(size=18, weight="bold"), text_color=UIU_ORANGE).pack(pady=10)

        ctk.CTkLabel(frame, text="Registered Credits this Trimester:").pack(pady=(6, 2))
        self.tuition_cr_entry = ctk.CTkEntry(frame, placeholder_text="e.g. 9.0", width=220)
        self.tuition_cr_entry.insert(0, "9.0")
        self.tuition_cr_entry.pack()

        btn = ctk.CTkButton(frame, text="Calculate Tuition & Schedule", fg_color=UIU_ORANGE, hover_color=UIU_ORANGE_HOVER, command=self._compute_tuition)
        btn.pack(pady=12)

        card = ctk.CTkFrame(frame, fg_color=UIU_CARD_BG, corner_radius=8)
        card.pack(fill="x", padx=20, pady=10)
        self.tuition_result = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=13), justify="left")
        self.tuition_result.pack(padx=15, pady=12)

    def _compute_tuition(self):
        try:
            cr = float(self.tuition_cr_entry.get())
            cgpa = self.profile.get("current_cgpa", 0.0)

            prob = check_probation_status(cgpa)
            waiver = check_waiver_eligibility(cgpa)
            t_data = calculate_tuition(cr, waiver["percentage"])
            inst = calculate_installments(t_data["total_payable"])

            out = (
                f"Academic Standing : {prob['status']}\n"
                f"Merit Waiver      : {waiver['percentage']}%\n"
                f"Total Payable     : {t_data['total_payable']:,.2f} BDT\n"
                f"----------------------------------------------------------\n"
                f"1st Installment ({inst[0]['percentage']}%) : {inst[0]['amount']:,.2f} BDT ({inst[0]['deadline']})\n"
                f"2nd Installment ({inst[1]['percentage']}%) : {inst[1]['amount']:,.2f} BDT ({inst[1]['deadline']})\n"
                f"3rd Installment ({inst[2]['percentage']}%) : {inst[2]['amount']:,.2f} BDT ({inst[2]['deadline']})"
            )
            self.tuition_result.configure(text=out)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- TAB 5: DEGREE AUDIT ---
    def _setup_degree_tab(self):
        frame = self.tab_degree
        ctk.CTkLabel(frame, text="CSE Degree Audit (140 Credits)", font=ctk.CTkFont(size=18, weight="bold"), text_color=UIU_ORANGE).pack(pady=10)

        ctk.CTkLabel(frame, text="Completed Credits:").pack(pady=(10, 2))
        self.audit_cr_entry = ctk.CTkEntry(frame, width=220)
        self.audit_cr_entry.insert(0, str(self.profile.get("completed_credits", 0.0)))
        self.audit_cr_entry.pack()

        ctk.CTkButton(frame, text="Evaluate Progress", fg_color=UIU_ORANGE, hover_color=UIU_ORANGE_HOVER, command=self._compute_degree).pack(pady=12)
        self.progress_bar = ctk.CTkProgressBar(frame, width=380, progress_color=UIU_ORANGE)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.degree_lbl = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=13))
        self.degree_lbl.pack(pady=5)

    def _compute_degree(self):
        try:
            cr = float(self.audit_cr_entry.get())
            audit = check_degree_progress(cr, "CSE")
            ratio = audit["progress_percentage"] / 100.0
            self.progress_bar.set(ratio)

            msg = (
                f"Degree Progress : {audit['progress_percentage']:.1f}%\n"
                f"Credits Done    : {audit['completed']:.1f} / {audit['total_required']:.1f}\n"
                f"Credits Left    : {audit['remaining']:.1f}\n"
                f"Est. Trimesters : ~{round(audit['remaining']/12, 1)} (at 12 cr/trimester)"
            )
            self.degree_lbl.configure(text=msg)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- TAB 6: PREREQUISITES ---
    def _setup_courses_tab(self):
        frame = self.tab_courses
        ctk.CTkLabel(frame, text="Prerequisite Eligibility Tester", font=ctk.CTkFont(size=18, weight="bold"), text_color=UIU_ORANGE).pack(pady=10)

        ctk.CTkLabel(frame, text="Target Course Code:").pack(pady=(6, 2))
        self.target_course_entry = ctk.CTkEntry(frame, placeholder_text="e.g. CSE2215", width=240)
        self.target_course_entry.pack()

        ctk.CTkLabel(frame, text="Completed Courses (comma-separated):").pack(pady=(6, 2))
        self.completed_courses_entry = ctk.CTkEntry(frame, placeholder_text="e.g. CSE1111, CSE2213", width=340)
        self.completed_courses_entry.pack()

        btn = ctk.CTkButton(frame, text="Check Eligibility", fg_color=UIU_ORANGE, hover_color=UIU_ORANGE_HOVER, command=self._check_prereqs)
        btn.pack(pady=12)

        self.course_result_lbl = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=14))
        self.course_result_lbl.pack(pady=5)

    def _check_prereqs(self):
        code = self.target_course_entry.get().strip()
        if not code:
            return
        completed = [c.strip() for c in self.completed_courses_entry.get().split(",") if c.strip()]
        res = check_prerequisites(code, completed)

        if res["can_take"]:
            self.course_result_lbl.configure(text=f"✅ ELIGIBLE to enroll in {normalize_code(code)}!", text_color="#2ECC71")
        else:
            self.course_result_lbl.configure(text=f"❌ INELIGIBLE!\nMissing Prerequisites: {', '.join(res['missing'])}", text_color="#E74C3C")

    # --- TAB 7: PROFILE EDIT ---
    def _setup_profile_tab(self):
        frame = self.tab_profile
        ctk.CTkLabel(frame, text="Edit Student Profile", font=ctk.CTkFont(size=18, weight="bold"), text_color=UIU_ORANGE).pack(pady=10)

        ctk.CTkLabel(frame, text="Full Name:").pack(pady=(3, 2))
        self.name_entry = ctk.CTkEntry(frame, width=260)
        self.name_entry.insert(0, self.profile.get("name", ""))
        self.name_entry.pack()

        ctk.CTkLabel(frame, text="Student ID:").pack(pady=(3, 2))
        self.id_entry = ctk.CTkEntry(frame, width=260)
        self.id_entry.insert(0, self.profile.get("student_id", ""))
        self.id_entry.pack()

        ctk.CTkLabel(frame, text="Current CGPA:").pack(pady=(3, 2))
        self.prof_cgpa_entry = ctk.CTkEntry(frame, width=260)
        self.prof_cgpa_entry.insert(0, str(self.profile.get("current_cgpa", 0.0)))
        self.prof_cgpa_entry.pack()

        ctk.CTkLabel(frame, text="Completed Credits:").pack(pady=(3, 2))
        self.prof_cr_entry = ctk.CTkEntry(frame, width=260)
        self.prof_cr_entry.insert(0, str(self.profile.get("completed_credits", 0.0)))
        self.prof_cr_entry.pack()

        btn = ctk.CTkButton(frame, text="Save Profile", fg_color=UIU_ORANGE, hover_color=UIU_ORANGE_HOVER, command=self._save_profile_data)
        btn.pack(pady=18)

    def _save_profile_data(self):
        try:
            name = self.name_entry.get().strip()
            sid = self.id_entry.get().strip()
            cgpa = float(self.prof_cgpa_entry.get())
            credits = float(self.prof_cr_entry.get())

            update_profile(name=name, student_id=sid, cgpa=cgpa, credits=credits)
            self.profile = get_profile()

            self.user_lbl.configure(text=f"👤 {self.profile.get('name')}")
            self.cgpa_lbl.configure(text=f"CGPA: {self.profile.get('current_cgpa'):.2f}")
            self.cr_lbl.configure(text=f"Credits: {self.profile.get('completed_credits'):.1f}")

            messagebox.showinfo("Success", "Profile updated and saved to data/profile.json!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")


def launch_gui():
    app = UIUAssistantGUI()
    app.mainloop()


if __name__ == "__main__":
    launch_gui()
