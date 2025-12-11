"""
csv_report.py

CSV format report implementation.
"""
from src.base_report import BaseReport
from src.misinfo_library import export_flagged_claims


class CSVReport(BaseReport):
    """
    Exports analysis results to CSV format.
    
    This is the original report format - maintains backward compatibility
    with the existing codebase.
    """
    
    def export(self, path: str = "report_output.csv") -> str:
        """
        Export all flagged claims and risk scores to CSV.
        
        Args:
            path (str): Output CSV file path
            
        Returns:
            str: Path to the exported CSV file
        """
        return export_flagged_claims(
            self._article.claims,
            self._score,
            output_path=path
        )
    
    def summary(self):
        """
        Return CSV-specific summary with file format info.
        """
        base_summary = super().summary()
        base_summary["format"] = "CSV"
        return base_summary
