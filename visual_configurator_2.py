import tkinter as tk
from tkinter import ttk

class VisualConfigurator:
    def __init__(self, root):
        self.root = root
        self.root.title("Copilot Implementation Configurator")

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

        # Build UI
        self.create_ui()

    def create_ui(self):
        # Create a notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)

        # Create a tab for each phase
        for phase, milestones in self.phases.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=phase)

            # Add milestones as a checklist
            label = ttk.Label(frame, text=f"Milestones for {phase}", font=("Arial", 14))
            label.pack(pady=10)

            for milestone in milestones:
                var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(frame, text=milestone, variable=var)
                checkbox.pack(anchor='w', padx=20, pady=5)

        # Add a progress section
        progress_label = ttk.Label(self.root, text="Progress Overview", font=("Arial", 16))
        progress_label.pack(pady=10)
        
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=5)

        update_button = ttk.Button(self.root, text="Update Progress", command=self.update_progress)
        update_button.pack(pady=10)

    def update_progress(self):
        # Mock-up progress calculation for demonstration purposes
        total_milestones = sum(len(milestones) for milestones in self.phases.values())
        completed_milestones = total_milestones // 2  # Replace with actual logic for milestone completion
        progress = (completed_milestones / total_milestones) * 100
        
        self.progress_bar["value"] = progress
        print(f"Progress updated: {progress}%")

if __name__ == "__main__":
    root = tk.Tk()
    app = VisualConfigurator(root)
    root.mainloop()
