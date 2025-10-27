from printer import Printer
import pandas as pd

class Analyzer:
    def __init__(self, data) -> None:
        self.printer = Printer().printer
        self.data = data
        if self.data is None or self.data.empty:
            self.printer("No data loaded.", "error")
            return

    def analyze(self):
        # Run basic analysis if data is present
        if self.data.empty:
            self.printer("No data to analyze.", "error")
            return

        # Example analysis: print basic descriptive statistics for numeric columns
        self.printer("Basic Statistics:", "info")
        self.printer(self.data.describe().to_json(indent=2), "json")

    def check_data_quality(self):
        """Analyze data quality: missing values, duplicates, unique values per column"""
        if self.data.empty:
            self.printer("No data loaded.", "error")
            return
        
        # Missing values analysis
        missing = self.data.isnull().sum()
        missing_pct = (missing / len(self.data)) * 100
        
        # Duplicates analysis
        duplicates = self.data.duplicated().sum()
        
        # Unique values per column
        unique_counts = self.data.nunique()
        
        quality_report = {
            "total_rows": len(self.data),
            "total_columns": len(self.data.columns),
            "missing_values": missing.to_dict(),
            "missing_percentages": missing_pct.to_dict(),
            "duplicate_rows": int(duplicates),
            "unique_values": unique_counts.to_dict()
        }
        
        self.printer("Data Quality Report:", "info")
        self.printer(quality_report, "json")

    
    def group_analysis(self):
        """Perform groupby analysis on selected columns"""
        if self.data.empty:
            self.printer("No data loaded.", "error")
            return
        
        # Show numeric columns
        numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns.tolist()
        self.printer("Available numeric columns:", "info")
        self.printer([{"column": col} for col in numeric_cols], "table")
        
        # Get group by column
        group_col = input("Enter column name to group by: ").strip()
        if group_col not in self.data.columns:
            self.printer(f"Column '{group_col}' not found.", "error")
            return
        
        # Get aggregation column
        agg_col = input("Enter column to aggregate (press Enter for all numeric columns): ").strip()
        if agg_col and agg_col not in numeric_cols:
            self.printer(f"Column '{agg_col}' is not numeric.", "error")
            return
        
        # Perform groupby analysis
        if agg_col:
            result = self.data.groupby(group_col)[agg_col].agg(['mean', 'median', 'std', 'count']).round(2)
        else:
            result = self.data.groupby(group_col)[numeric_cols].agg(['mean', 'median', 'std', 'count']).round(2)
        
        self.printer(f"\nGroup analysis by '{group_col}':", "info")
        self.printer(result.to_dict('index'), "json")

    def correlation_analysis(self):
        """Analyze correlations between numeric columns"""
        if self.data.empty:
            self.printer("No data loaded.", "error")
            return
        
        # Get numeric columns
        numeric_cols = self.data.select_dtypes(include=['int64', 'float64'])
        if numeric_cols.empty:
            self.printer("No numeric columns found for correlation analysis.", "error")
            return
        
        # Calculate correlations
        correlations = numeric_cols.corr().round(2)
        
        self.printer("Correlation Matrix:", "info")
        self.printer(correlations.to_dict('index'), "json")

    def analyze_distribution(self):
        """Analyze value distributions in columns"""
        if self.data.empty:
            self.printer("No data loaded.", "error")
            return
        
        # Show available columns
        self.printer("Available columns:", "info")
        self.printer([{"column": col} for col in self.data.columns], "table")
        
        # Get column choice
        col_name = input("Enter column name to analyze: ").strip()
        if col_name not in self.data.columns:
            self.printer(f"Column '{col_name}' not found.", "error")
            return
        
        # Calculate distribution statistics
        stats = {
            "value_counts": self.data[col_name].value_counts().head(10).to_dict(),
            "basic_stats": {
                "mean": float(self.data[col_name].mean()) if pd.api.types.is_numeric_dtype(self.data[col_name]) else None,
                "median": float(self.data[col_name].median()) if pd.api.types.is_numeric_dtype(self.data[col_name]) else None,
                "mode": self.data[col_name].mode().tolist(),
                "unique_values": int(self.data[col_name].nunique()),
                "null_count": int(self.data[col_name].isnull().sum())
            }
        }
        
        self.printer(f"\nDistribution analysis for '{col_name}':", "info")
        self.printer(stats, "json")

    def time_series_analysis(self):
        """Analyze time-based patterns in the data"""
        if self.data.empty:
            self.printer("No data loaded.", "error")
            return
        
        # Show datetime columns
        datetime_cols = self.data.select_dtypes(include=['datetime64']).columns.tolist()
        if not datetime_cols:
            self.printer("No datetime columns found. Would you like to convert a column to datetime?", "info")
            col_name = input("Enter column name to convert (or press Enter to cancel): ").strip()
            if not col_name:
                return
            if col_name not in self.data.columns:
                self.printer(f"Column '{col_name}' not found.", "error")
                return
            try:
                self.data[col_name] = pd.to_datetime(self.data[col_name])
                datetime_cols = [col_name]
            except Exception as e:
                self.printer(f"Error converting to datetime: {str(e)}", "error")
                return
        
        # Select datetime column
        if len(datetime_cols) > 1:
            self.printer("Available datetime columns:", "info")
            self.printer([{"column": col} for col in datetime_cols], "table")
            date_col = input("Enter datetime column name: ").strip()
            if date_col not in datetime_cols:
                self.printer(f"Column '{date_col}' is not a datetime column.", "error")
                return
        else:
            date_col = datetime_cols[0]
        
        # Time-based analysis
        analysis = {
            "temporal_distribution": {
                "by_year": self.data[date_col].dt.year.value_counts().to_dict(),
                "by_month": self.data[date_col].dt.month.value_counts().to_dict(),
                "by_day_of_week": self.data[date_col].dt.day_name().value_counts().to_dict()
            },
            "time_range": {
                "start": self.data[date_col].min().strftime("%Y-%m-%d"),
                "end": self.data[date_col].max().strftime("%Y-%m-%d"),
                "total_days": (self.data[date_col].max() - self.data[date_col].min()).days
            }
        }
        
        self.printer(f"\nTime series analysis for '{date_col}':", "info")
        self.printer(analysis, "json")
