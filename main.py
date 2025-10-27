import pandas as pd
from printer import Printer
from loader import DataLoader
from viewer import Viewer
from menu_selector import MenuSelector, menu
from analyzer import Analyzer
import os

class DataAnalysis:
    """
    Simple data analysis helper that loads a dataset and exposes a few actions
    (analyze, list_columns) which can be selected interactively.
    """

    def __init__(self, data_file: str):
        # initialize the data loader and load the data immediately
        self.data_loader = DataLoader(data_file)
        self.data = self.data_loader.load_data()
        self.printer = Printer().printer
        self.viewer = Viewer(self.data)
        self.analyzer = Analyzer(self.data)
        
        # Build menu automatically from decorated methods
        self.menu = MenuSelector()
        self.menu.discover(self)

    
    # Viewer wrappers so they can be auto-discovered into the "View" submenu
    @menu("preview_rows", order=2, section="View")
    def preview_rows(self):
        self.viewer.preview_rows()

    @menu("preview_column", order=3, section="View")
    def preview_column(self):
        self.viewer.preview_column()

    @menu("preview_multiple_columns", order=4, section="View")
    def preview_multiple_columns(self):
        self.viewer.preview_multiple_columns()
    
    @menu("list_columns", order=1, section="View")
    def list_columns(self):
        self.viewer.list_columns()
    
    @menu("analyze", order=1, section="Analyze")
    def analyze(self):
        self.analyzer.analyze()
    
    @menu("check_data_quality", order=2, section="Analyze")
    def check_data_quality(self):
        self.analyzer.check_data_quality()
    
    @menu("group_analysis", order=3, section="Analyze")
    def group_analysis(self):
        self.analyzer.group_analysis()
    
    @menu("correlation_analysis", order=4, section="Analyze")
    def correlation_analysis(self):
        self.analyzer.correlation_analysis()
    
    @menu("analyze_distribution", order=5, section="Analyze")
    def analyze_distribution(self):
        self.analyzer.analyze_distribution()
    
    @menu("time_series_analysis", order=6, section="Analyze")
    def time_series_analysis(self):
        self.analyzer.time_series_analysis()

    def run(self):
        if self.menu.is_empty():
            self.printer("No actions available.", "error")
            return

        current_section: str | None = None
        while True:
            title = "Data Analysis Menu" if not current_section else f"Data Analysis Menu / {current_section}"
            self.printer(f"{title} (press 'q' to quit)", "info")
            self.printer(self.menu.items_table(section=current_section), "table")

            prompt = "Select an option by id"
            if current_section:
                prompt += " ('0' to go back)"
            prompt += ": "

            choice = input(prompt).strip().lower()
            if choice in ("q", "quit", "exit"):
                self.printer("Exiting.", "info")
                break
            if current_section and choice in ("b", "back"):
                current_section = None
                continue

            result = self.menu.select(choice, section=current_section)
            if not result:
                self.printer("Invalid choice. Please try again.", "error")
                continue

            kind, payload = result
            if kind == "section":
                current_section = payload  # navigate into submenu
                continue
            if kind == "back":
                current_section = None
                continue
            if kind == "action":
                try:
                    payload()  # call the function
                except Exception as e:
                    self.printer(f"Error while executing action: {e}", "error")

if __name__ == "__main__":
    data_folder = "data/"
    #list all csv files in the data folder
    import os
    csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
    print("Available CSV files:")
    for i, file in enumerate(csv_files, 1):
        print(f"{i}. {file}")
    file_choice = input("Enter the number of the CSV file to load: ").strip()
    try:
        file_index = int(file_choice) - 1
        if 0 <= file_index < len(csv_files):
            data_file = os.path.join(data_folder, csv_files[file_index])
        else:
            print("Invalid selection. Exiting.")
            exit(1)
    except ValueError:
        print("Invalid input. Exiting.")
        exit(1)

    # Create the analysis object and start interactive mode
    analysis = DataAnalysis(data_file)
    analysis.run()