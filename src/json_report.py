"""
json_report.py

JSON format report implementation with detailed metadata.
"""
import json
from datetime import datetime
from src.base_report import BaseReport


class JSONReport(BaseReport):
    """
    Exports analysis results to JSON format with full metadata.
    
    JSON format provides more structure and is ideal for:
    - API responses
    - Data pipelines
    - Machine-readable outputs
    """
    
    def export(self, path: str = "report_output.json") -> str:
        """
        Export complete analysis to JSON with timestamp and metadata.
        
        Args:
            path (str): Output JSON file path
            
        Returns:
            str: Path to the exported JSON file
        """
        data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "analyzer_version": "1.0.0",
                "format": "JSON"
            },
            "article": {
                "domain": self._article.domain,
                "text_preview": self._article.text[:200] + "..." if len(self._article.text) > 200 else self._article.text,
                "text_length": len(self._article.text),
                "clean_text_length": len(self._article.clean_text) if self._article.clean_text else 0
            },
            "analysis": {
                "risk_score": self._score,
                "risk_level": self.get_risk_level(),
                "claims": self._article.claims,
                "citations": self._citations,
                "glossary_mismatches": [
                    {"term": term, "status": status} 
                    for term, status in self._mismatches
                ],
                "evidence_map": self._evidence_map
            },
            "summary": {
                "total_claims": len(self._article.claims),
                "total_citations": len(self._citations),
                "total_mismatches": len(self._mismatches),
                "risk_total": self._score.get("total", 0)
            }
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return path
    
    def summary(self):
        """
        Return JSON-specific summary with additional metadata.
        """
        base_summary = super().summary()
        base_summary.update({
            "format": "JSON",
            "risk_level": self.get_risk_level(),
            "timestamp": datetime.now().isoformat(),
            "machine_readable": True
        })
        return base_summary
