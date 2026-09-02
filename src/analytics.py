import tkinter as tk
import customtkinter as ctk

class PerformanceChart(ctk.CTkFrame):
    def __init__(self, master, width=650, height=240, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas_width = width
        self.canvas_height = height

        self.canvas = tk.Canvas(
            self,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#1A222D",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

    def draw_chart(self, records):
        self.canvas.delete("all")

        if not records or len(records) < 1:
            self.canvas.create_text(
                self.canvas_width // 2,
                self.canvas_height // 2,
                text="No academic history yet. Add trimesters to view trend.",
                fill="#9BA1A6",
                font=("Segoe UI", 12)
            )
            return

        padding_x = 60
        padding_y = 35
        graph_width = self.canvas_width - (padding_x * 2)
        graph_height = self.canvas_height - (padding_y * 2)

        # Baseline horizontal grids for UIU GPA benchmarks (2.00, 3.00, 3.50, 4.00)
        grid_marks = [2.00, 3.00, 3.50, 4.00]
        for mark in grid_marks:
            y = self.canvas_height - padding_y - ((mark / 4.0) * graph_height)
            self.canvas.create_line(padding_x, y, self.canvas_width - padding_x, y, fill="#2C3848", dash=(2, 4))
            self.canvas.create_text(padding_x - 15, y, text=f"{mark:.1f}", fill="#9BA1A6", font=("Segoe UI", 9))

        n = len(records)
        step_x = graph_width / (n - 1) if n > 1 else graph_width / 2

        points = []
        for idx, rec in enumerate(records):
            x = (padding_x + (idx * step_x)) if n > 1 else self.canvas_width // 2
            gpa = max(0.0, min(4.0, rec["gpa"]))
            y = self.canvas_height - padding_y - ((gpa / 4.0) * graph_height)
            points.append((x, y, rec))

        # Connecting path
        for i in range(len(points) - 1):
            x1, y1, _ = points[i]
            x2, y2, _ = points[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill="#F26522", width=3, smooth=True)

        # Nodes & labels
        for x, y, rec in points:
            # Outer Ring & Node
            self.canvas.create_oval(x - 6, y - 6, x + 6, y + 6, fill="#F26522", outline="#FFFFFF", width=2)
            # GPA Tag
            self.canvas.create_text(x, y - 14, text=f"{rec['gpa']:.2f}", fill="#FFFFFF", font=("Segoe UI", 10, "bold"))
            # Trimester Label
            self.canvas.create_text(x, self.canvas_height - padding_y + 16, text=rec["name"], fill="#9BA1A6", font=("Segoe UI", 9))
