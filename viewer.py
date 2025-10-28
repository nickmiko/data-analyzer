from printer import Printer

class Viewer:
    def __init__(self, data) -> None:
        self.printer = Printer().printer
        self.rows = 5
        self.data = data
        if self.data is None or self.data.empty:
            self.printer("No data loaded.", "error")
            return
        self.data_output_style = "table"

    def preview_rows(self):
        num_rows = self.rows
        # Display  few rows of the dataset
        self.printer(f"Displaying {num_rows} rows of the dataset:", "info")
        self.printer(self.data.head(num_rows).to_dict('records'), self.data_output_style)
    
    def preview_column(self):
        num_rows = self.rows
        column_name = input("Enter the column name to preview: ").strip()
        # Display  few entries of a specific column
        if self.data.empty:
            self.printer("No data loaded.", "error")
            return
        if column_name not in self.data.columns:
            self.printer(f"Column '{column_name}' not found in the dataset.", "error")
            return
        self.printer(f"Displaying {num_rows} entries of column '{column_name}':", "info")
        self.printer([{"value": val} for val in self.data[column_name].head(num_rows)], self.data_output_style)

    def preview_multiple_columns(self):
        num_rows = self.rows
        column_names = input("Enter the column names to preview (comma-separated): ").strip().split(",")
        column_names = [name.strip() for name in column_names]
        # Display  few entries of specific columns
        if self.data.empty:
            self.printer("No data loaded.", "error")
            return
        missing_columns = [name for name in column_names if name not in self.data.columns]
        if missing_columns:
            self.printer(f"Columns '{', '.join(missing_columns)}' not found in the dataset.", "error")
            return
        self.printer(f"Displaying {num_rows} entries of columns '{', '.join(column_names)}':", "info")
        first_col = column_names[0]
        result = self.data[column_names].head(num_rows).set_index(first_col).to_dict('index')
        self.printer(result, self.data_output_style)
    
    def list_columns(self):
        self.printer("Columns in the dataset:", "info")
        # Show columns in a table format
        self.printer([{"column": col} for col in self.data.columns.tolist()], self.data_output_style)