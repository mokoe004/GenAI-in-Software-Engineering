import tkinter as tk
from tkinter import ttk

class VisualConfigurator:
    def __init__(self, root):
        self.root = root
        self.root.title("Copilot Implementation Simulator")
        self.root.geometry("800x600")  # Set initial size of the window

        # Define phases and milestones
        self.phases = {
            "Iteration 1: Planning and Foundation": [
                "Stakeholder analysis",
                "Workflow mapping",
                "Technical infrastructure assessment",
                "Training and KPI definition",
            ],
            "Iteration 2: Pilot Implementation": [
                "Pilot project setup",
                "Controlled deployment",
                "Feedback collection",
                "Performance review",
            ],
            "Iteration 3: Refinement and Optimization": [
                "Feedback review",
                "Issue resolution",
                "Advanced training",
                "Workflow updates",
            ],
            "Iteration 4: Full Integration and Sustainability": [
                "Phased rollout",
                "Cultural integration",
                "Continuous improvement",
                "Final evaluation",
            ],
        }

        # Critical Success Factors (CSFs)
        self.csfs = {
            "Technical Infrastructure": 50,
            "Employee Acceptance": 50,
            "ROI": 50,
            "Code Quality": 50,
            "Data Privacy": 50,
        }

        # Build UI
        self.create_ui()

    def create_ui(self):
        # Create main frames
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_frame = ttk.Frame(self.root)
        right_frame.pack(side="right", fill="y", padx=10, pady=10)

        # Add each phase with its milestones
        canvas = tk.Canvas(left_frame)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for phase, milestones in self.phases.items():
            phase_label = ttk.Label(scrollable_frame, text=phase, font=("Arial", 14, "bold"))
            phase_label.pack(anchor='w', pady=10)

            for milestone in milestones:
                var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(scrollable_frame, text=milestone, variable=var)
                checkbox.pack(anchor='w', padx=20, pady=5)

        # Add CSF sliders
        ttk.Label(right_frame, text="Critical Success Factors", font=("Arial", 14, "bold")).pack(pady=10)

        self.csfs_vars = {}
        for csf, value in self.csfs.items():
            frame = ttk.Frame(right_frame)
            frame.pack(fill="x", pady=5)

            label = ttk.Label(frame, text=csf, font=("Arial", 12))
            label.pack(side="left")

            slider = ttk.Scale(frame, from_=0, to=100, orient="horizontal")
            slider.set(value)
            slider.pack(side="right", fill="x", expand=True)
            self.csfs_vars[csf] = slider

        # Progress section
        ttk.Label(right_frame, text="Progress Overview", font=("Arial", 14, "bold")).pack(pady=10)

        self.progress_bar = ttk.Progressbar(right_frame, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack(pady=5)

        self.progress_text = ttk.Label(right_frame, text="Progress: 0%", font=("Arial", 12))
        self.progress_text.pack(pady=5)

        update_button = ttk.Button(right_frame, text="Update Progress", command=self.update_progress)
        update_button.pack(pady=10)

    def update_progress(self):
        # Calculate overall progress based on CSFs
        total_weight = len(self.csfs_vars)
        progress = sum(slider.get() for slider in self.csfs_vars.values()) / total_weight

        self.progress_bar["value"] = progress

        # Update progress text with specific milestones
        if progress >= 100:
            progress_status = "Progress: 100% - Complete"
        elif progress >= 76:
            progress_status = "Progress: 76% - Near Completion"
        elif progress >= 50:
            progress_status = "Progress: 50% - Halfway There"
        elif progress >= 25:
            progress_status = "Progress: 25% - Just Started"
        else:
            progress_status = "Progress: 0% - Not Started"

        self.progress_text.config(text=progress_status)
        print(progress_status)

if __name__ == "__main__":
    root = tk.Tk()
    app = VisualConfigurator(root)
    root.mainloop()
