"""
html_report.py

HTML format report implementation with visual styling.
"""
from datetime import datetime
from src.base_report import BaseReport


class HTMLReport(BaseReport):
    """
    Exports analysis results to HTML format with styling and visualization.
    
    HTML format provides:
    - Human-readable output
    - Color-coded risk levels
    - Browser-viewable reports
    - Easy sharing and presentation
    """
    
    def export(self, path: str = "report_output.html") -> str:
        """
        Export analysis to styled HTML document.
        
        Args:
            path (str): Output HTML file path
            
        Returns:
            str: Path to the exported HTML file
        """
        risk_level = self.get_risk_level()
        risk_class = risk_level.lower()
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Article Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .risk-badge {{
            display: inline-block;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 18px;
            margin: 20px 0;
        }}
        .risk-low {{
            background-color: #2ecc71;
            color: white;
        }}
        .risk-medium {{
            background-color: #f39c12;
            color: white;
        }}
        .risk-high {{
            background-color: #e74c3c;
            color: white;
        }}
        .metric {{
            background-color: #ecf0f1;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }}
        .metric-label {{
            font-weight: bold;
            color: #7f8c8d;
        }}
        .metric-value {{
            font-size: 24px;
            color: #2c3e50;
        }}
        .claim-list, .citation-list, .mismatch-list {{
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }}
        .claim-item, .citation-item, .mismatch-item {{
            padding: 10px;
            margin: 8px 0;
            background-color: white;
            border-left: 3px solid #3498db;
            border-radius: 3px;
        }}
        .mismatch-item {{
            border-left-color: #e74c3c;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 14px;
            margin-top: 30px;
            text-align: center;
        }}
        .score-breakdown {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .score-item {{
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 Health Article Analysis Report</h1>
        
        <div class="metric">
            <div class="metric-label">Source Domain</div>
            <div class="metric-value">{self._article.domain or 'Unknown'}</div>
        </div>
        
        <div class="risk-badge risk-{risk_class}">
            Risk Level: {risk_level}
        </div>
        
        <h2>📊 Score Breakdown</h2>
        <div class="score-breakdown">
            <div class="score-item">
                <div class="metric-label">Total Risk Score</div>
                <div class="metric-value">{self._score.get('total', 0)}</div>
            </div>
            <div class="score-item">
                <div class="metric-label">Clickbait Score</div>
                <div class="metric-value">{self._score.get('clickbait', 0)}</div>
            </div>
            <div class="score-item">
                <div class="metric-label">Absolute Language</div>
                <div class="metric-value">{self._score.get('absolute', 0)}</div>
            </div>
            <div class="score-item">
                <div class="metric-label">No Evidence</div>
                <div class="metric-value">{self._score.get('no_evidence', 0)}</div>
            </div>
            <div class="score-item">
                <div class="metric-label">Glossary Mismatches</div>
                <div class="metric-value">{self._score.get('mismatch', 0)}</div>
            </div>
        </div>
        
        <h2>📝 Claims Detected ({len(self._article.claims)})</h2>
        <div class="claim-list">
            {self._generate_claim_html()}
        </div>
        
        <h2>📚 Citations Found ({len(self._citations)})</h2>
        <div class="citation-list">
            {self._generate_citation_html()}
        </div>
        
        <h2>⚠️ Glossary Mismatches ({len(self._mismatches)})</h2>
        <div class="mismatch-list">
            {self._generate_mismatch_html()}
        </div>
        
        <div class="timestamp">
            Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>"""
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return path
    
    def _generate_claim_html(self) -> str:
        """Generate HTML for claims list."""
        if not self._article.claims:
            return '<p style="color: #7f8c8d;">No claims detected.</p>'
        
        html_parts = []
        for claim in self._article.claims:
            claim_text = claim.get('text', 'Unknown claim')
            html_parts.append(f'<div class="claim-item">{claim_text}</div>')
        
        return '\n'.join(html_parts)
    
    def _generate_citation_html(self) -> str:
        """Generate HTML for citations list."""
        if not self._citations:
            return '<p style="color: #7f8c8d;">No citations found.</p>'
        
        html_parts = []
        for citation in self._citations:
            # If it's a URL, make it clickable
            if citation.startswith('http'):
                html_parts.append(
                    f'<div class="citation-item">'
                    f'<a href="{citation}" target="_blank">{citation}</a>'
                    f'</div>'
                )
            else:
                html_parts.append(f'<div class="citation-item">"{citation}"</div>')
        
        return '\n'.join(html_parts)
    
    def _generate_mismatch_html(self) -> str:
        """Generate HTML for glossary mismatches."""
        if not self._mismatches:
            return '<p style="color: #2ecc71;">✓ No glossary mismatches detected.</p>'
        
        html_parts = []
        for term, status in self._mismatches:
            html_parts.append(
                f'<div class="mismatch-item">'
                f'<strong>{term}</strong>: {status}'
                f'</div>'
            )
        
        return '\n'.join(html_parts)
    
    def summary(self):
        """
        Return HTML-specific summary.
        """
        base_summary = super().summary()
        base_summary.update({
            "format": "HTML",
            "risk_level": self.get_risk_level(),
            "viewable_in_browser": True,
            "includes_styling": True
        })
        return base_summary
