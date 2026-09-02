import sys
import webbrowser
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox

sys.path.insert(0, str(Path(__file__).resolve().parent))

from profile import get_profile, update_profile, reset_to_guest
from cgpa import CourseResult, calculate_gpa, calculate_target_cgpa, can_reach_target_cgpa
from probation import check_probation_status, check_waiver_eligibility
from tuition import calculate_tuition, calculate_installments
from courses import normalize_code, check_prerequisites
from graduation import check_degree_progress, calculate_final_exam_target, get_available_departments
from transport import get_all_routes, find_routes_by_stop
from database import init_db, add_trimester_record, get_all_trimesters, get_cumulative_metrics, delete_trimester_record
from analytics import PerformanceChart
from schedule import check_schedule_conflicts
from exporter import export_schedule_csv, export_academic_summary_html
from examcon import open_examcon_portal, save_exam_entry, get_all_exam_entries, delete_exam_entry

UIU_ORANGE = "#F26522"
UIU_ORANGE_HOVER = "#D9531E"
UIU_DARK_BG = "#10141B"
UIU_SIDEBAR_BG = "#171F2A"
UIU_CARD_BG = "#1F2A38"
UIU_TEXT_MUTED = "#8A94A0"

ctk.set_appearance_mode("Dark")


class OnboardingDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_complete_callback, current_prof=None):
        super().__init__(parent)
        self.title("Student Profile Setup")
        self.geometry("460x490")
        self.resizable(False, False)
        self.configure(fg_color=UIU_DARK_BG)
        self.on_complete_callback = on_complete_callback
        self.current_prof = current_prof or {}

        self.transient(parent)
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Student Profile Setup",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=UIU_ORANGE
        ).pack(pady=(22, 4))

        ctk.CTkLabel(
            self,
            text="Enter your university details to personalize the dashboard.",
            wraplength=380,
            text_color=UIU_TEXT_MUTED,
            font=ctk.CTkFont(size=12)
        ).pack(pady=(0, 18))

        form = ctk.CTkFrame(self, fg_color=UIU_CARD_BG, corner_radius=10)
        form.pack(fill="x", padx=30, pady=5)

        ctk.CTkLabel(form, text="Full Name:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(12, 2))
        self.name_entry = ctk.CTkEntry(form, placeholder_text="e.g. your name", width=360)
        curr_name = self.current_prof.get("name", "")
        if curr_name and curr_name != "Guest Student":
            self.name_entry.insert(0, curr_name)
        self.name_entry.pack(padx=15, pady=(0, 10))

        ctk.CTkLabel(form, text="Student ID:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(2, 2))
        self.id_entry = ctk.CTkEntry(form, placeholder_text="e.g. 011231000", width=360)
        curr_id = self.current_prof.get("student_id", "")
        if curr_id and curr_id != "Not Set":
            self.id_entry.insert(0, curr_id)
        self.id_entry.pack(padx=15, pady=(0, 10))

        ctk.CTkLabel(form, text="Department:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(2, 2))
        self.dept_opt = ctk.CTkOptionMenu(
            form,
            values=get_available_departments(),
            width=360,
            fg_color=UIU_SIDEBAR_BG,
            button_color=UIU_ORANGE,
            button_hover_color=UIU_ORANGE_HOVER
        )
        curr_dept = self.current_prof.get("department", "CSE")
        self.dept_opt.set(curr_dept)
        self.dept_opt.pack(padx=15, pady=(0, 15))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=30, pady=22)

        ctk.CTkButton(
            btn_row,
            text="Skip / Cancel",
            fg_color=UIU_CARD_BG,
            hover_color=UIU_SIDEBAR_BG,
            width=130,
            command=self._skip
        ).pack(side="left")

        ctk.CTkButton(
            btn_row,
            text="Save Profile",
            fg_color=UIU_ORANGE,
            hover_color=UIU_ORANGE_HOVER,
            width=190,
            command=self._save
        ).pack(side="right")

    def _save(self):
        name = self.name_entry.get().strip() or "UIU Student"
        sid = self.id_entry.get().strip() or "Not Set"
        dept = self.dept_opt.get()

        update_profile(name=name, student_id=sid, department=dept, is_first_run=False)
        self.destroy()
        self.on_complete_callback()

    def _skip(self):
        update_profile(is_first_run=False)
        self.destroy()
        self.on_complete_callback()


class UIUAssistantGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        init_db()

        self.title("UIU Universal Student Assistant V2")
        self.geometry("1100x750")
        self.minsize(960, 660)
        self.configure(fg_color=UIU_DARK_BG)

        self.profile = get_profile()
        self.current_dept = self.profile.get("department", "CSE")
        self._sync_metrics()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_tabs()

        if self.profile.get("is_first_run", True):
            self.after(200, lambda: self._open_profile_dialog())

    def _open_profile_dialog(self):
        self.profile = get_profile()
        OnboardingDialog(self, self._on_profile_saved, self.profile)

    def _on_profile_saved(self):
        self.profile = get_profile()
        self.current_dept = self.profile.get("department", "CSE")

        self.user_lbl.configure(text=f"👤 {self.profile.get('name')}")
        self.dept_lbl.configure(text=f"Dept: {self.current_dept}")
        self.dept_selector.set(self.current_dept)

        if hasattr(self, "prof_tab_name"):
            self.prof_tab_name.delete(0, "end")
            self.prof_tab_name.insert(0, self.profile.get("name", ""))
            self.prof_tab_id.delete(0, "end")
            self.prof_tab_id.insert(0, self.profile.get("student_id", ""))
            self.prof_tab_dept.set(self.current_dept)

        self._compute_degree()
        self._compute_tuition()
        messagebox.showinfo("Profile Updated", "Your student information has been successfully saved!")

    def _sync_metrics(self):
        metrics = get_cumulative_metrics()
        if metrics["total_credits"] > 0:
            self.current_cgpa = metrics["cgpa"]
            self.total_credits = metrics["total_credits"]
        else:
            self.current_cgpa = self.profile.get("current_cgpa", 0.0)
            self.total_credits = self.profile.get("completed_credits", 0.0)

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=UIU_SIDEBAR_BG)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)

        badge = ctk.CTkLabel(
            self.sidebar,
            text="UIU",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white",
            fg_color=UIU_ORANGE,
            corner_radius=8,
            width=80,
            height=42,
        )
        badge.grid(row=0, column=0, padx=20, pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="ALL-STUDENT OS\nUniversal Edition",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white"
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 15))

        self.stat_card = ctk.CTkFrame(self.sidebar, fg_color=UIU_CARD_BG, corner_radius=8)
        self.stat_card.grid(row=2, column=0, padx=15, pady=5, sticky="ew")

        self.user_lbl = ctk.CTkLabel(self.stat_card, text=f"👤 {self.profile.get('name')}", font=ctk.CTkFont(size=13, weight="bold"), text_color="white")
        self.user_lbl.pack(padx=10, pady=(8, 2))

        self.dept_lbl = ctk.CTkLabel(self.stat_card, text=f"Dept: {self.current_dept}", font=ctk.CTkFont(size=11, weight="bold"), text_color=UIU_ORANGE)
        self.dept_lbl.pack(padx=10, pady=1)

        self.cgpa_lbl = ctk.CTkLabel(self.stat_card, text=f"CGPA: {self.current_cgpa:.2f}", font=ctk.CTkFont(size=13, weight="bold"), text_color=UIU_ORANGE)
        self.cgpa_lbl.pack(padx=10, pady=2)

        self.cr_lbl = ctk.CTkLabel(self.stat_card, text=f"Earned: {self.total_credits:.1f} Cr", font=ctk.CTkFont(size=11), text_color=UIU_TEXT_MUTED)
        self.cr_lbl.pack(padx=10, pady=(2, 6))

        self.edit_prof_btn = ctk.CTkButton(
            self.stat_card,
            text="✎ Edit Info",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=UIU_SIDEBAR_BG,
            hover_color=UIU_ORANGE,
            height=26,
            command=self._open_profile_dialog
        )
        self.edit_prof_btn.pack(padx=10, pady=(2, 8), fill="x")

        standing = check_probation_status(self.current_cgpa)
        status_color = "#2ECC71" if not standing["is_on_probation"] else "#E74C3C"
        self.standing_badge = ctk.CTkLabel(
            self.sidebar,
            text=f"● {standing['status']}",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=status_color
        )
        self.standing_badge.grid(row=3, column=0, padx=20, pady=(5, 10))

        ctk.CTkLabel(self.sidebar, text="Active Department:", font=ctk.CTkFont(size=11), text_color=UIU_TEXT_MUTED).grid(row=4, column=0, padx=20, pady=(10, 2))
        self.dept_selector = ctk.CTkOptionMenu(
            self.sidebar,
            values=get_available_departments(),
            command=self._on_dept_changed,
            fg_color=UIU_CARD_BG,
            button_color=UIU_ORANGE,
            button_hover_color=UIU_ORANGE_HOVER
        )
        self.dept_selector.set(self.current_dept)
        self.dept_selector.grid(row=5, column=0, padx=20, pady=(2, 10))

    def _on_dept_changed(self, selected_dept):
        self.current_dept = selected_dept
        update_profile(department=selected_dept)
        self.dept_lbl.configure(text=f"Dept: {self.current_dept}")
        self._compute_degree()
        self._compute_tuition()

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

        self.tab_analytics = self.tabview.add("Analytics")
        self.tab_examcon = self.tabview.add("Exam Routine")
        self.tab_clash = self.tabview.add("Routine Clash")
        self.tab_degree = self.tabview.add("Degree Audit")
        self.tab_tuition = self.tabview.add("Tuition")
        self.tab_gpa = self.tabview.add("GPA Calc")
        self.tab_target = self.tabview.add("Planner")
        self.tab_exam = self.tabview.add("Exam Target")
        self.tab_bus = self.tabview.add("Transport")
        self.tab_courses = self.tabview.add("Prerequisites")
        self.tab_profile = self.tabview.add("Profile Settings")

        self._setup_analytics_tab()
        self._setup_examcon_tab()
        self._setup_clash_tab()
        self._setup_degree_tab()
        self._setup_tuition_tab()
        self._setup_gpa_tab()
        self._setup_target_tab()
        self._setup_exam_tab()
        self._setup_bus_tab()
        self._setup_courses_tab()
        self._setup_profile_tab()

    # --- TAB: EXAM ROUTINE & EXAMCON PORTAL ACCESS ---
    def _setup_examcon_tab(self):
        frame = self.tab_examcon
        ctk.CTkLabel(frame, text="UIU Exam Routine & Controller Portal Access", font=ctk.CTkFont(size=18, weight="bold"), text_color=UIU_ORANGE).pack(pady=(8, 2))

        # Portal Launch Banner
        banner = ctk.CTkFrame(frame, fg_color=UIU_CARD_BG, corner_radius=8)
        banner.pack(fill="x", padx=15, pady=6)

        ctk.CTkLabel(banner, text="Official Exam Automation Portal: examcon.uiu.ac.bd", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=15, pady=12)
        ctk.CTkButton(banner, text="🌐 Launch Examcon Online", fg_color=UIU_ORANGE, hover_color=UIU_ORANGE_HOVER, command=open_examcon_portal).pack(side="right", padx=15, pady=10)

        # Local Save / Cache Form
        form = ctk.CTkFrame(frame, fg_color="transparent")
        form.pack(fill="x", padx=15, pady=4)

        self.ex_code = ctk.CTkEntry(form, placeholder_text="Course (e.g. CSE2213)", width=140)
        self.ex_code.pack(side="left", padx=3)

        self.ex_type = ctk.CTkOptionMenu(form, values=["Midterm Exam", "Final Exam"], width=120, fg_color=UIU_ORANGE, button_color=UIU_ORANGE_HOVER)
        self.ex_type.pack(side="left", padx=3)

        self.ex_date = ctk.CTkEntry(form, placeholder_text="Date (YYYY-MM-DD)", width=120)
        self.ex_date.pack(side="left", padx=3)

        self.ex_time = ctk.CTkEntry(form, placeholder_text="Time (e.g. 09:00 AM)", width=130)
        self.ex_time.pack(side="left", padx=3)

        self.ex_room = ctk.CTkEntry(form, placeholder_text="Room (e.g. 412)", width=90)
        self.ex_room.pack(side="left", padx=3)

        ctk.CTkButton(form, text="+ Add to My Routine", fg_color=UIU_CARD_BG, hover_color=UIU_SIDEBAR_BG, command=self._add_exam_schedule).pack(side="left", padx=5)

        # Routine Schedule Display
        self.exam_scroll = ctk.CTkScrollableFrame(frame, height=270, fg_color=UIU_CARD_BG)
        self.exam_scroll.pack(fill="both", expand=True, padx=15, pady=8)

        self._refresh_exam_schedule_view()

    def _add_exam_schedule(self):
        code = self.ex_code.get().strip()
        etype = self.ex_type.get()
        edate = self.ex_date.get().strip()
        etime = self.ex_time.get().strip()
        room = self.ex_room.get().strip() or "TBA"

        if not code or not edate or not etime:
            messagebox.showwarning("Incomplete", "Please supply at least Course Code, Date, and Time.")
            return

        save_exam_entry(code, etype, edate, etime, room)
        self._refresh_exam_schedule_view()
        self.ex_code.delete(0, "end")
        self.ex_date.delete(0, "end")
        self.ex_time.delete(0, "end")
        self.ex_room.delete(0, "end")

    def _refresh_exam_schedule_view(self):
        for w in self.exam_scroll.winfo_children():
            w.destroy()

        exams = get_all_exam_entries()
        if not exams:
            ctk.CTkLabel(
                self.exam_scroll,
                text="No upcoming exams recorded yet.\nClick 'Launch Examcon Online' to check your official schedule, then log them above for offline access.",
                text_color=UIU_TEXT_MUTED
            ).pack(pady=25)
            return

        for ex in exams:
            row = ctk.CTkFrame(self.exam_scroll, fg_color=UIU_SIDEBAR_BG)
            row.pack(fill="x", pady=3, padx=5)

            ctk.CTkLabel(row, text=f"📝 {ex['course_code']}", width=120, anchor="w", font=ctk.CTkFont(weight="bold"), text_color=UIU_ORANGE).pack(side="left", padx=8)
            ctk.CTkLabel(row, text=f"{ex['exam_type']}", width=110, text_color="white").pack(side="left")
            ctk.CTkLabel(row, text=f"📅 {ex['exam_date']}", width=110, text_color=UIU_TEXT_MUTED).pack(side="left")
            ctk.CTkLabel(row, text=f"⏰ {ex['exam_time']}", width=140, text_color=UIU_TEXT_MUTED).pack(side="left")
            ctk.CTkLabel(row, text=f"🚪 Room: {ex['room_no']}", width=100, font=ctk.CTkFont(weight="bold")).pack(side="left")

            del_btn = ctk.CTkButton(
                row,
                text="✕",
                width=30,
                height=22,
                fg_color="#3A2226",
                hover_color="#5C2529",
                text_color="#FF6B6B",
                command=lambda e_id=ex["id"]: self._remove_exam_schedule(e_id)
            )
            del_btn.pack(side="right", padx=8)

    def _remove_exam_schedule(self, entry_id):
        delete_exam_entry(entry_id)
        self._refresh_exam_schedule_view()

    # --- TAB: PROFILE SETTINGS ---
    def _setup_profile_tab(self):
        frame = self.tab_profile
        ctk.CTkLabel(frame, text="Manage Student Information", font=ctk.CTkFont(size=18, weight="bold"), text_color=UIU_ORANGE).pack(pady=(12, 4))
        ctk.CTkLabel(frame, text="Update your identity anytime. All records persist locally in AppData.", font=ctk.CTkFont(size=12), text_color=UIU_TEXT_MUTED).pack(pady=(0, 15))

        card = ctk.CTkFrame(frame, fg_color=UIU_CARD_BG, corner_radius=10)
        card.pack(fill="x", padx=40, pady=5)

        ctk.CTkLabel(card, text="Full Name:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(15, 2))
        self.prof_tab_name = ctk.CTkEntry(card, width=380)
        self.prof_tab_name.insert(0, self.profile.get("name", ""))
        self.prof_tab_name.pack(padx=20, pady=(0, 10))

        ctk.CTkLabel(card, text="Student ID:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(4, 2))
        self.prof_tab_id = ctk.CTkEntry(card, width=380)
        self.prof_tab_id.insert(0, self.profile.get("student_id", ""))
        self.prof_tab_id.pack(padx=20, pady=(0, 10))

        ctk.CTkLabel(card, text="Department / Program:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(4, 2))
        self.prof_tab_dept = ctk.CTkOptionMenu(
            card,
            values=get_available_departments(),
            width=380,
            fg_color=UIU_SIDEBAR_BG,
            button_color=UIU_ORANGE,
            button_hover_color=UIU_ORANGE_HOVER
        )
        self.prof_tab_dept.set(self.current_dept)
        self.prof_tab_dept.pack(padx=20, pady=(0, 20))

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(pady=15)

        ctk.CTkButton(
            btn_row,
            text="Save Profile Updates",
            fg_color=UIU_ORANGE,
            hover_color=UIU_ORANGE_HOVER,
            width=200,
            command=self._save_from_profile_tab
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_row,
            text="Reset to Guest Mode",
            fg_color="#3A2226",
            hover_color="#5C2529",
            text_color="#FF6B6B",
            width=160,
            command=self._reset_to_guest_action
        ).pack(side="left", padx=10)

    def _save_from_profile_tab(self):
        name = self.prof_tab_name.get().strip() or "UIU Student"
        sid = self.prof_tab_id.get().strip() or "Not Set"
        dept = self.prof_tab_dept.get()

        update_profile(name=name, student_id=sid, department=dept, is_first_run=False)
        self._on_profile_saved()

    def _reset_to_guest_action(self):
        confirm = messagebox.askyesno("Confirm Reset", "Reset identity back to Guest Student?")
        if confirm:
            reset_to_guest()
            self._on_profile_saved()

    # --- TAB 1: ANALYTICS ---
    def _setup_analytics_tab(self):
        frame = self.tab_analytics
        ctk.CTkLabel(frame, text="Academic Trajectory & Trimester Records", font=ctk.CTkFont(size=17, weight="bold"), text_color=UIU_ORANGE).pack(pady=(8, 2))

        self.chart = PerformanceChart(frame, width=700, height=220)
        self.chart.pack(fill="x", padx=15, pady=5)

        entry_row = ctk.CTkFrame(frame, fg_color="transparent")
        entry_row.pack(fill="x", padx=15, pady=5)

        self.tri_name_entry = ctk.CTkEntry(entry_row, placeholder_text="Term (e.g. Spring 24)", width=140)
        self.tri_name_entry.pack(side="left", padx=4)

        self.tri_gpa_entry = ctk.CTkEntry(entry_row, placeholder_text="GPA (e.g. 3.85)", width=110)
        self.tri_gpa_entry.pack(side="left", padx=4)

        self.tri_cr_entry = ctk.CTkEntry(entry_row, placeholder_text="Credits (e.g. 12.0)", width=110)
        self.tri_cr_entry.pack(side="left", padx=4)

        ctk.CTkButton(entry_row, text="+ Log Term", fg_color=UIU_ORANGE, width=100, command=self._add_term).pack(side="left", padx=6)

        self.log_scroll = ctk.CTkScrollableFrame(frame, height=160, fg_color=UIU_CARD_BG)
        self.log_scroll.pack(fill="both", expand=True, padx=15, pady=8)

        self._refresh_analytics_view()

    def _refresh_analytics_view(self):
        records = get_all_trimesters()
        self.chart.draw_chart(records)

        for w in self.log_scroll.winfo_children():
            w.destroy()

        if not records:
            ctk.CTkLabel(self.log_scroll, text="No trimesters recorded yet. Log your completed trimesters above.", text_color=UIU_TEXT_MUTED).pack(pady=20)
            return

        for r in records:
            row = ctk.CTkFrame(self.log_scroll, fg_color=UIU_SIDEBAR_BG)
            row.pack(fill="x", pady=2, padx=4)

            ctk.CTkLabel(row, text=f"📌 {r['name']}", width=160, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=8)
            ctk.CTkLabel(row, text=f"GPA: {r['gpa']:.2f}", width=100, text_color=UIU_ORANGE).pack(side="left")
            ctk.CTkLabel(row, text=f"Credits: {r['credits']:.1f}", width=100, text_color=UIU_TEXT_MUTED).pack(side="left")

            del_btn = ctk.CTkButton(
                row,
                text="✕",
                width=30,
                height=22,
                fg_color="#3A2226",
                hover_color="#5C2529",
                text_color="#FF6B6B",
                command=lambda rec_id=r["id"]: self._remove_term(rec_id)
            )
            del_btn.pack(side="right", padx=8)

    def _add_term(self):
        name = self.tri_name_entry.get().strip()
        gpa_str = self.tri_gpa_entry.get().strip()
        cr_str = self.tri_cr_entry.get().strip()

        if not name or not gpa_str or not cr_str:
            messagebox.showwarning("Incomplete", "Please supply Name, GPA, and Credits.")
            return

        try:
            gpa = float(gpa_str)
            credits = float(cr_str)
            if not (0.0 <= gpa <= 4.0):
                messagebox.showerror("Invalid Range", "GPA must be between 0.00 and 4.00.")
                return

            add_trimester_record(name, gpa, credits)
            self._sync_metrics()
            self._update_sidebar_stats()
            self._refresh_analytics_view()
            self._compute_degree()

            self.tri_name_entry.delete(0, "end")
            self.tri_gpa_entry.delete(0, "end")
            self.tri_cr_entry.delete(0, "end")
        except ValueError:
            messagebox.showerror("Type Error", "GPA and Credits must be numbers.")

    def _remove_term(self, rec_id):
        delete_trimester_record(rec_id)
        self._sync_metrics()
        self._update_sidebar_stats()
        self._refresh_analytics_view()
        self._compute_degree()

    def _update_sidebar_stats(self):
        self.cgpa_lbl.configure(text=f"CGPA: {self.current_cgpa:.2f}")
        self.cr_lbl.configure(text=f"Earned: {self.total_credits:.1f} Cr")
        standing = check_probation_status(self.current_cgpa)
        self.standing_badge.configure(
            text=f"● {standing['status']}",
            text_color="#2ECC71" if not standing["is_on_probation"] else "#E74C3C"
        )

    # --- TAB 2: ROUTINE CLASH & CSV EXPORT ---
    def _setup_clash_tab(self):
        frame = self.tab_clash
        ctk.CTkLabel(frame, text="Course Routine & Section Clash Detector", font=ctk.CTkFont(size=17, weight="bold"), text_color=UIU_ORANGE).pack(pady=(8, 2))
        ctk.CTkLabel(frame, text="Day codes: ST (Sun/Tue), MW (Mon/Wed), RA (Thu/Sat) | Time format: 08:30-10:00", font=ctk.CTkFont(size=11), text_color=UIU_TEXT_MUTED).pack(pady=(0, 6))

        self.clash_inputs = []
        scroll = ctk.CTkScrollableFrame(frame, height=220, fg_color=UIU_CARD_BG)
        scroll.pack(fill="x", padx=15, pady=4)

        defaults = [
            ("CSE 2213", "A", "ST", "08:30 - 10:00"),
            ("CSE 2215", "B", "ST", "10:05 - 11:35"),
            ("MATH 2183", "A", "MW", "08:30 - 10:00"),
            ("ACT 1111", "C", "MW", "10:05 - 11:35"),
            ("", "", "ST", "08:30 - 10:00")
        ]

        for i in range(1, 6):
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(row, text=f"Slot {i}:", width=55, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=2)
            c_code = ctk.CTkEntry(row, placeholder_text="Course (e.g. CSE2213)", width=130)
            c_code.insert(0, defaults[i-1][0])
            c_code.pack(side="left", padx=3)

            c_sec = ctk.CTkEntry(row, placeholder_text="Sec (A)", width=60)
            c_sec.insert(0, defaults[i-1][1])
            c_sec.pack(side="left", padx=3)

            c_days = ctk.CTkOptionMenu(row, values=["ST", "MW", "RA", "SR", "SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"], width=75, fg_color=UIU_ORANGE, button_color=UIU_ORANGE_HOVER)
            c_days.set(defaults[i-1][2])
            c_days.pack(side="left", padx=3)

            c_time = ctk.CTkEntry(row, placeholder_text="08:30 - 10:00", width=140)
            c_time.insert(0, defaults[i-1][3])
            c_time.pack(side="left", padx=3)

            self.clash_inputs.append((c_code, c_sec, c_days, c_time))

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(pady=8)

        ctk.CTkButton(btn_row, text="Detect Schedule Overlaps", fg_color=UIU_ORANGE, hover_color=UIU_ORANGE_HOVER, command=self._detect_clash).pack(side="left", padx=6)
        ctk.CTkButton(btn_row, text="📊 Export Routine to CSV", fg_color=UIU_CARD_BG, hover_color=UIU_SIDEBAR_BG, command=self._export_routine).pack(side="left", padx=6)

        card = ctk.CTkFrame(frame, fg_color=UIU_CARD_BG, corner_radius=8)
        card.pack(fill="both", expand=True, padx=20, pady=5)
        self.clash_result_lbl = ctk.CTkLabel(card, text="Enter course slots above and click Detect Schedule Overlaps.", font=ctk.CTkFont(size=12), justify="left")
        self.clash_result_lbl.pack(padx=15, pady=12)

    def _get_active_slots(self):
        slots = []
        for code_e, sec_e, days_o, time_e in self.clash_inputs:
            code = code_e.get().strip()
            if not code: continue
            slots.append({
                "code": code,
                "section": sec_e.get().strip(),
                "days": days_o.get().strip(),
                "time": time_e.get().strip()
            })
        return slots

    def _detect_clash(self):
        slots = self._get_active_slots()
        if len(slots) < 2:
            self.clash_result_lbl.configure(text="Please supply at least 2 course slots to evaluate clashes.", text_color=UIU_TEXT_MUTED)
            return

        res = check_schedule_conflicts(slots)
        if res.get("error"):
            self.clash_result_lbl.configure(text=f"❌ Error: {res['error']}", text_color="#E74C3C")
            return

        if not res["has_conflict"]:
            self.clash_result_lbl.configure(
                text="✅ NO SCHEDULE CLASH DETECTED!\nAll selected sections have independent, non-overlapping time slots.",
                text_color="#2ECC71"
            )
        else:
            lines = [f"⚠️ SCHEDULE CLASH IDENTIFIED ({res['conflict_count']} conflict(s) found):\n"]
            for idx, c in enumerate(res["conflicts"], 1):
                days = ", ".join(c["clashing_days"])
                lines.append(f"{idx}. {c['course_1']} clashes with {c['course_2']}")
                lines.append(f"   ➔ Clashing Days: {days} | Overlap Duration: {c['overlap_minutes']} minutes\n")
            self.clash_result_lbl.configure(text="\n".join(lines), text_color="#E74C3C")

    def _export_routine(self):
        slots = self._get_active_slots()
        if not slots:
            messagebox.showwarning("Empty", "No courses to export.")
            return
        file_path = export_schedule_csv(slots)
        messagebox.showinfo("Export Successful", f"Routine spreadsheet saved at:\n{file_path}")

    # --- TAB 3: DEGREE AUDIT ---
    def _setup_degree_tab(self):
        frame = self.tab_degree
        ctk.CTkLabel(frame, text="Universal Degree Audit & Graduation Tracker", font=ctk.CTkFont(size=17, weight="bold"), text_color=UIU_ORANGE).pack(pady=10)

        self.audit_bar = ctk.CTkProgressBar(frame, width=450, progress_color=UIU_ORANGE)
        self.audit_bar.set(0)
        self.audit_bar.pack(pady=10)

        card = ctk.CTkFrame(frame, fg_color=UIU_CARD_BG, corner_radius=8)
        card.pack(fill="x", padx=30, pady=5)

        self.degree_lbl = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=13), justify="left")
        self.degree_lbl.pack(padx=20, pady=15)
        self._compute_degree()

    def _compute_degree(self):
        audit = check_degree_progress(self.total_credits, self.current_dept)
        self.audit_bar.set(audit["progress_percentage"] / 100.0)

        msg = (
            f"Program Name         : {audit['program_name']}\n"
            f"Faculty Division     : {audit['faculty']}\n"
            f"----------------------------------------------------------\n"
            f"Completion Rate      : {audit['progress_percentage']:.1f}%\n"
            f"Completed Credits    : {audit['completed']:.1f} / {audit['total_required']:.1f}\n"
            f"Remaining Credits    : {audit['remaining']:.1f}\n"
            f"Estimated Terms Left : ~{round(audit['remaining']/12.0, 1)} Trimesters (at 12 cr/term)"
        )
        self.degree_lbl.configure(text=msg)

    # --- TAB 4: TUITION & STATEMENT EXPORT ---
    def _setup_tuition_tab(self):
        frame = self.tab_tuition
        ctk.CTkLabel(frame, text="Departmental Tuition & 3-Installment Schedule", font=ctk.CTkFont(size=17, weight="bold"), text_color=UIU_ORANGE).pack(pady=10)

        ctk.CTkLabel(frame, text="Enrolled Credits for Upcoming Trimester:").pack(pady=(4, 2))
        self.tuition_cr = ctk.CTkEntry(frame, width=200)
        self.tuition_cr.insert(0, "9.0")
        self.tuition_cr.pack()

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(pady=10)

        ctk.CTkButton(btn_row, text="Compute Tuition Schedule", fg_color=UIU_ORANGE, hover_color=UIU_ORANGE_HOVER, command=self._compute_tuition).pack(side="left", padx=5)
        ctk.CTkButton(btn_row, text="📄 Print / Export HTML Bill", fg_color=UIU_CARD_BG, hover_color=UIU_SIDEBAR_BG, command=self._export_tuition_statement).pack(side="left", padx=5)

        card = ctk.CTkFrame(frame, fg_color=UIU_CARD_BG, corner_radius=8)
        card.pack(fill="x", padx=25, pady=8)
        self.tuition_lbl = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=13), justify="left")
        self.tuition_lbl.pack(padx=15, pady=12)
        self._compute_tuition()

    def _compute_tuition(self):
        try:
            cr = float(self.tuition_cr.get())
            waiver = check_waiver_eligibility(self.current_cgpa)
            t_data = calculate_tuition(cr, waiver["percentage"], self.current_dept)
            inst = calculate_installments(t_data["total_payable"])

            out = (
                f"Department / Program : {t_data['department']}\n"
                f"Tuition Rate         : {t_data['cost_per_credit']:,.2f} BDT / credit\n"
                f"Applied Merit Waiver : {waiver['percentage']}%\n"
                f"Gross Tuition Fee    : {t_data['gross_tuition']:,.2f} BDT\n"
                f"Trimester Activities : +{t_data['trimester_fee']:,.2f} BDT\n"
                f"Net Payable Total    : {t_data['total_payable']:,.2f} BDT\n"
                f"----------------------------------------------------------\n"
                f"1st Installment ({inst[0]['percentage']}%) : {inst[0]['amount']:,.2f} BDT [{inst[0]['deadline']}]\n"
                f"2nd Installment ({inst[1]['percentage']}%) : {inst[1]['amount']:,.2f} BDT [{inst[1]['deadline']}]\n"
                f"3rd Installment ({inst[2]['percentage']}%) : {inst[2]['amount']:,.2f} BDT [{inst[2]['deadline']}]"
            )
            self.tuition_lbl.configure(text=out)
            self._last_tuition_data = (t_data, inst)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _export_tuition_statement(self):
        if not hasattr(self, "_last_tuition_data"):
            self._compute_tuition()
        t_data, inst = self._last_tuition_data
        file_path = export_academic_summary_html(self.profile, t_data, inst)
        webbrowser.open(file_path.as_uri())
        messagebox.showinfo("Exported", f"Billing statement opened in browser.\nSaved at: {file_path}")

    # --- TAB 5: GPA CALCULATOR ---
    def _setup_gpa_tab(self):
        frame = self.tab_gpa
        ctk.CTkLabel(frame, text="Trimester Coursework Calculator", font=ctk.CTkFont(size=17, weight="bold"), text_color=UIU_ORANGE).pack(pady=10)

        self.gpa_inputs = []
        scroll = ctk.CTkScrollableFrame(frame, height=270, fg_color=UIU_CARD_BG)
        scroll.pack(fill="x", padx=15, pady=5)

        for i in range(1, 6):
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=f"Course {i}:", width=65, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=4)
            code = ctk.CTkEntry(row, placeholder_text="Code (e.g. ACT1111)", width=130)
            code.pack(side="left", padx=4)
            grade = ctk.CTkOptionMenu(row, values=["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"], width=80, fg_color=UIU_ORANGE, button_color=UIU_ORANGE_HOVER)
            grade.pack(side="left", padx=4)
            cr = ctk.CTkEntry(row, placeholder_text="Credits", width=80)
            cr.insert(0, "3.0")
            cr.pack(side="left", padx=4)
            self.gpa_inputs.append((code, grade, cr))

        ctk.CTkButton(frame, text="Calculate Term GPA", fg_color=UIU_ORANGE, hover_color=UIU_ORANGE_HOVER, command=self._compute_gpa).pack(pady=12)
        self.gpa_result_lbl = ctk.CTkLabel(frame, text="GPA: --", font=ctk.CTkFont(size=18, weight="bold"))
        self.gpa_result_lbl.pack()

    def _compute_gpa(self):
        courses = []
        try:
            for c_e, g_o, cr_e in self.gpa_inputs:
                code = c_e.get().strip()
                if not code: continue
                courses.append(CourseResult(course_code=code, grade=g_o.get(), credits=float(cr_e.get())))
            if not courses:
                messagebox.showwarning("Notice", "Please enter at least one course.")
                return
            gpa = calculate_gpa(courses)
            self.gpa_result_lbl.configure(text=f"Calculated Term GPA: {gpa:.2f}", text_color=UIU_ORANGE)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- TAB 6: TARGET PLANNER ---
    def _setup_target_tab(self):
        frame = self.tab_target
        ctk.CTkLabel(frame, text="Target CGPA Feasibility Planner", font=ctk.CTkFont(size=17, weight="bold"), text_color=UIU_ORANGE).pack(pady=10)

        ctk.CTkLabel(frame, text="Target CGPA:").pack(pady=(8, 2))
        self.target_entry = ctk.CTkEntry(frame, placeholder_text="e.g. 3.50", width=200)
        self.target_entry.pack()

        ctk.CTkLabel(frame, text="Future Credits Planned:").pack(pady=(8, 2))
        self.future_cr_entry = ctk.CTkEntry(frame, placeholder_text="e.g. 15.0", width=200)
        self.future_cr_entry.insert(0, "15.0")
        self.future_cr_entry.pack()

        ctk.CTkButton(frame, text="Evaluate Feasibility", fg_color=UIU_ORANGE, hover_color=UIU_ORANGE_HOVER, command=self._compute_target).pack(pady=15)
        self.planner_result = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=13))
        self.planner_result.pack(pady=5)

    def _compute_target(self):
        try:
            tgt = float(self.target_entry.get())
            future_cr = float(self.future_cr_entry.get())
            req = calculate_target_cgpa(self.current_cgpa, self.total_credits, tgt, future_cr)
            reach = can_reach_target_cgpa(self.current_cgpa, self.total_credits, tgt, future_cr)

            if reach:
                self.planner_result.configure(text=f"Required Future Term GPA: {req:.2f}\n\nStatus: ✅ TARGET REACHABLE", text_color="#2ECC71")
            else:
                self.planner_result.configure(text=f"Required Future Term GPA: {req:.2f}\n\nStatus: ❌ UNREACHABLE (> 4.00 required)", text_color="#E74C3C")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- TAB 7: EXAM TARGET ---
    def _setup_exam_tab(self):
        frame = self.tab_exam
        ctk.CTkLabel(frame, text="Final Exam Target Marks Calculator", font=ctk.CTkFont(size=17, weight="bold"), text_color=UIU_ORANGE).pack(pady=10)

        ctk.CTkLabel(frame, text="Continuous Marks: Attendance (5) + Quiz (25) + Midterm (30) = 60", text_color=UIU_TEXT_MUTED).pack(pady=2)

        self.att_entry = ctk.CTkEntry(frame, placeholder_text="Attendance (out of 5)", width=220)
        self.att_entry.insert(0, "5.0")
        self.att_entry.pack(pady=4)

        self.quiz_entry = ctk.CTkEntry(frame, placeholder_text="Quiz / Assign (out of 25)", width=220)
        self.quiz_entry.insert(0, "21.0")
        self.quiz_entry.pack(pady=4)

        self.mid_entry = ctk.CTkEntry(frame, placeholder_text="Midterm (out of 30)", width=220)
        self.mid_entry.insert(0, "24.0")
        self.mid_entry.pack(pady=4)

        self.target_grade_opt = ctk.CTkOptionMenu(frame, values=["A", "A-", "B+", "B", "B-", "C+", "C", "D"], fg_color=UIU_ORANGE, button_color=UIU_ORANGE_HOVER, width=120)
        self.target_grade_opt.pack(pady=6)

        ctk.CTkButton(frame, text="Calculate Required Final Score", fg_color=UIU_ORANGE, hover_color=UIU_ORANGE_HOVER, command=self._compute_exam).pack(pady=12)
        self.exam_res_lbl = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=13))
        self.exam_res_lbl.pack()

    def _compute_exam(self):
        try:
            att = float(self.att_entry.get())
            quiz = float(self.quiz_entry.get())
            mid = float(self.mid_entry.get())
            res = calculate_final_exam_target(att, quiz, mid, self.target_grade_opt.get())

            if res["is_achievable"]:
                self.exam_res_lbl.configure(
                    text=f"Continuous Score: {res['current_total']:.1f}/60\n\n✅ Needed in Final: {res['needed_in_final']:.1f} / 40.0",
                    text_color="#2ECC71"
                )
            else:
                self.exam_res_lbl.configure(text=f"Continuous Score: {res['current_total']:.1f}/60\n\n❌ {res['reason']}", text_color="#E74C3C")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- TAB 8: BUS SCHEDULE ---
    def _setup_bus_tab(self):
        frame = self.tab_bus
        ctk.CTkLabel(frame, text="Campus Shuttle & Regional Transport", font=ctk.CTkFont(size=17, weight="bold"), text_color=UIU_ORANGE).pack(pady=10)

        search_row = ctk.CTkFrame(frame, fg_color="transparent")
        search_row.pack(fill="x", padx=20, pady=4)

        self.bus_query = ctk.CTkEntry(search_row, placeholder_text="Enter pickup stoppage (e.g. Mirpur, Kazipara, Uttara)...", width=380)
        self.bus_query.pack(side="left", padx=(0, 8))

        ctk.CTkButton(search_row, text="Filter", fg_color=UIU_ORANGE, width=90, command=self._filter_bus).pack(side="left")
        ctk.CTkButton(search_row, text="Reset", fg_color=UIU_CARD_BG, width=80, command=self._reset_bus).pack(side="left", padx=4)

        self.bus_scroll = ctk.CTkScrollableFrame(frame, height=310, fg_color=UIU_CARD_BG)
        self.bus_scroll.pack(fill="both", expand=True, padx=20, pady=8)
        self._render_buses(get_all_routes())

    def _render_buses(self, routes):
        for w in self.bus_scroll.winfo_children(): w.destroy()
        if not routes:
            ctk.CTkLabel(self.bus_scroll, text="No matching transit routes identified.", text_color=UIU_TEXT_MUTED).pack(pady=20)
            return
        for r in routes:
            card = ctk.CTkFrame(self.bus_scroll, fg_color=UIU_SIDEBAR_BG)
            card.pack(fill="x", pady=4, padx=5)
            ctk.CTkLabel(card, text=f"🚌 {r['route_name']}", font=ctk.CTkFont(size=13, weight="bold"), text_color=UIU_ORANGE).pack(anchor="w", padx=10, pady=(6, 2))
            ctk.CTkLabel(card, text=f"Route: {' ➔ '.join(r['pickup_stops'])}", font=ctk.CTkFont(size=11), wraplength=600, justify="left", text_color="white").pack(anchor="w", padx=10, pady=2)
            ctk.CTkLabel(card, text=f"Campus Departure: {', '.join(r['departure_from_campus'])}", font=ctk.CTkFont(size=10), text_color=UIU_TEXT_MUTED).pack(anchor="w", padx=10, pady=(2, 6))

    def _filter_bus(self):
        q = self.bus_query.get().strip()
        self._render_buses(find_routes_by_stop(q) if q else get_all_routes())

    def _reset_bus(self):
        self.bus_query.delete(0, "end")
        self._render_buses(get_all_routes())

    # --- TAB 9: PREREQUISITES ---
    def _setup_courses_tab(self):
        frame = self.tab_courses
        ctk.CTkLabel(frame, text="Prerequisite Validation Engine", font=ctk.CTkFont(size=17, weight="bold"), text_color=UIU_ORANGE).pack(pady=10)

        self.target_code = ctk.CTkEntry(frame, placeholder_text="Target Course (e.g. CSE2215 / ACT2111)", width=240)
        self.target_code.pack(pady=4)

        self.completed_codes = ctk.CTkEntry(frame, placeholder_text="Completed Courses (comma separated)", width=340)
        self.completed_codes.pack(pady=4)

        ctk.CTkButton(frame, text="Validate Prerequisites", fg_color=UIU_ORANGE, hover_color=UIU_ORANGE_HOVER, command=self._validate_course).pack(pady=12)
        self.course_lbl = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=13))
        self.course_lbl.pack()

    def _validate_course(self):
        code = self.target_code.get().strip()
        if not code: return
        done = [c.strip() for c in self.completed_codes.get().split(",") if c.strip()]
        res = check_prerequisites(code, done)

        if res["can_take"]:
            self.course_lbl.configure(text=f"✅ ELIGIBLE to enroll in {normalize_code(code)}", text_color="#2ECC71")
        else:
            self.course_lbl.configure(text=f"❌ INELIGIBLE: Missing {', '.join(res['missing'])}", text_color="#E74C3C")


def launch_gui():
    app = UIUAssistantGUI()
    app.mainloop()


if __name__ == "__main__":
    launch_gui()
