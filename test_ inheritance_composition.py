"""
test_oop_principles.py

Comprehensive tests for OOP principles: Inheritance, Polymorphism, and Composition.
Tests verify the proper implementation of object-oriented design patterns.
"""
import pytest
import os
import json
from src.analyzer import Analyzer
from src.article import Article
from src.glossary import Glossary
from src.risk_scorer import RiskScorer
from src.base_report import BaseReport
from src.csv_report import CSVReport
from src.json_report import JSONReport
from src.html_report import HTMLReport


# ==================== INHERITANCE TESTS ====================

class TestInheritance:
    """Test inheritance relationships and parent-child behavior."""
    
    def test_all_reports_inherit_from_base(self):
        """Test that all report classes inherit from BaseReport."""
        assert issubclass(CSVReport, BaseReport)
        assert issubclass(JSONReport, BaseReport)
        assert issubclass(HTMLReport, BaseReport)
    
    def test_base_report_is_abstract(self):
        """Test that BaseReport cannot be instantiated directly."""
        analyzer = Analyzer()
        article = analyzer.add_article("Test article", "https://test.com")
        
        # Should raise TypeError because export() is not implemented
        with pytest.raises(TypeError):
            BaseReport(article, {"total": 0}, [], [])
    
    def test_inherited_properties_available(self):
        """Test that child classes inherit all parent properties."""
        analyzer = Analyzer(report_class=CSVReport)
        article = analyzer.add_article("Coffee cures headaches.", "https://test.com")
        report = analyzer.analyze_article(article)
        
        # All these properties should be inherited from BaseReport
        assert hasattr(report, 'score')
        assert hasattr(report, 'mismatches')
        assert hasattr(report, 'citations')
        assert hasattr(report, 'evidence_map')
        assert isinstance(report.score, dict)
    
    def test_inherited_methods_available(self):
        """Test that child classes inherit parent methods."""
        analyzer = Analyzer(report_class=JSONReport)
        article = analyzer.add_article("Test text", "https://test.com")
        report = analyzer.analyze_article(article)
        
        # These methods are defined in BaseReport
        assert hasattr(report, 'summary')
        assert hasattr(report, 'get_risk_level')
        assert callable(report.summary)
        assert callable(report.get_risk_level)
    
    def test_method_overriding(self):
        """Test that child classes can override parent methods."""
        analyzer = Analyzer()
        article = analyzer.add_article("Test", "https://test.com")
        
        # Create different report types
        csv_report = CSVReport(article, {"total": 1}, [], [])
        json_report = JSONReport(article, {"total": 1}, [], [])
        html_report = HTMLReport(article, {"total": 1}, [], [])
        
        # Each overrides summary() differently
        csv_summary = csv_report.summary()
        json_summary = json_report.summary()
        html_summary = html_report.summary()
        
        # CSV adds "format": "CSV"
        assert csv_summary.get("format") == "CSV"
        
        # JSON adds more metadata
        assert json_summary.get("format") == "JSON"
        assert "timestamp" in json_summary
        assert "machine_readable" in json_summary
        
        # HTML adds different metadata
        assert html_summary.get("format") == "HTML"
        assert "viewable_in_browser" in html_summary
    
    def test_super_calls_in_overridden_methods(self):
        """Test that overridden methods properly call parent implementation."""
        analyzer = Analyzer(report_class=JSONReport)
        article = analyzer.add_article("Test", "https://test.com")
        report = analyzer.analyze_article(article)
        
        summary = report.summary()
        
        # Should have base fields from parent
        assert "domain" in summary
        assert "claims_found" in summary
        assert "citations_found" in summary
        assert "risk_total" in summary
        
        # And additional fields from child
        assert "format" in summary
        assert "timestamp" in summary


# ==================== POLYMORPHISM TESTS ====================

class TestPolymorphism:
    """Test polymorphic behavior - different objects responding to same interface."""
    
    def test_all_reports_implement_export(self):
        """Test that all report types implement the export() method."""
        analyzer = Analyzer()
        article = analyzer.add_article("Test article text", "https://test.com")
        
        csv_report = CSVReport(article, {"total": 1}, [], [])
        json_report = JSONReport(article, {"total": 1}, [], [])
        html_report = HTMLReport(article, {"total": 1}, [], [])
        
        # All should have export method
        assert hasattr(csv_report, 'export')
        assert hasattr(json_report, 'export')
        assert hasattr(html_report, 'export')
        assert callable(csv_report.export)
        assert callable(json_report.export)
        assert callable(html_report.export)
    
    def test_polymorphic_export_behavior(self):
        """Test that export() behaves differently for each report type."""
        analyzer = Analyzer()
        article = analyzer.add_article("Coffee always cures everything!", "https://test.com")
        
        # Create all three report types
        csv_report = CSVReport(article, {"total": 2}, [], [])
        json_report = JSONReport(article, {"total": 2}, [], [])
        html_report = HTMLReport(article, {"total": 2}, [], [])
        
        # Export each type
        csv_path = csv_report.export("test_poly.csv")
        json_path = json_report.export("test_poly.json")
        html_path = html_report.export("test_poly.html")
        
        # Verify files were created
        assert os.path.exists(csv_path)
        assert os.path.exists(json_path)
        assert os.path.exists(html_path)
        
        # Verify different content/format
        assert csv_path.endswith('.csv')
        assert json_path.endswith('.json')
        assert html_path.endswith('.html')
        
        # Cleanup
        os.remove(csv_path)
        os.remove(json_path)
        os.remove(html_path)
    
    def test_polymorphic_function_parameter(self):
        """Test that functions can accept any report type polymorphically."""
        def process_report(report: BaseReport) -> dict:
            """Function that accepts any BaseReport subclass."""
            return {
                "risk": report.get_risk_level(),
                "summary": report.summary(),
                "score": report.score.get("total", 0)
            }
        
        analyzer = Analyzer()
        article = analyzer.add_article("Miracle cure!", "https://test.com")
        
        # Create different report types
        csv_report = CSVReport(article, {"total": 3}, [], [])
        json_report = JSONReport(article, {"total": 3}, [], [])
        html_report = HTMLReport(article, {"total": 3}, [], [])
        
        # All should work with the same function
        csv_result = process_report(csv_report)
        json_result = process_report(json_report)
        html_result = process_report(html_report)
        
        # All should return valid results
        assert csv_result["risk"] == "High"
        assert json_result["risk"] == "High"
        assert html_result["risk"] == "High"
    
    def test_liskov_substitution_principle(self):
        """Test that any report subclass can replace BaseReport without breaking."""
        analyzer = Analyzer()
        article = analyzer.add_article("Test", "https://test.com")
        
        report_classes = [CSVReport, JSONReport, HTMLReport]
        
        for ReportClass in report_classes:
            # Should work with any report class
            report = ReportClass(article, {"total": 1}, [], [])
            
            # All should support these operations
            assert isinstance(report.score, dict)
            assert isinstance(report.get_risk_level(), str)
            assert isinstance(report.summary(), dict)
            assert report.get_risk_level() in ["Low", "Medium", "High"]
    
    def test_runtime_report_switching(self):
        """Test that report format can be changed at runtime (Strategy Pattern)."""
        analyzer = Analyzer(report_class=CSVReport)
        article = analyzer.add_article("Test article", "https://test.com")
        
        # Analyze with CSV format
        report1 = analyzer.analyze_article(article)
        assert isinstance(report1, CSVReport)
        
        # Switch to JSON format at runtime
        analyzer.set_report_format(JSONReport)
        report2 = analyzer.analyze_article(article)
        assert isinstance(report2, JSONReport)
        
        # Switch to HTML format
        analyzer.set_report_format(HTMLReport)
        report3 = analyzer.analyze_article(article)
        assert isinstance(report3, HTMLReport)
        
        # All are still BaseReport instances (polymorphism)
        assert isinstance(report1, BaseReport)
        assert isinstance(report2, BaseReport)
        assert isinstance(report3, BaseReport)
    
    def test_collection_of_different_report_types(self):
        """Test that we can store different report types in same collection."""
        analyzer = Analyzer()
        article = analyzer.add_article("Test", "https://test.com")
        
        # Create mixed collection of reports
        reports = [
            CSVReport(article, {"total": 1}, [], []),
            JSONReport(article, {"total": 2}, [], []),
            HTMLReport(article, {"total": 3}, [], []),
            CSVReport(article, {"total": 1}, [], []),
        ]
        
        # Should be able to call same method on all
        for report in reports:
            risk = report.get_risk_level()
            assert risk in ["Low", "Medium", "High"]
            
        # Each behaves according to its actual type
        assert isinstance(reports[0], CSVReport)
        assert isinstance(reports[1], JSONReport)
        assert isinstance(reports[2], HTMLReport)


# ==================== COMPOSITION TESTS ====================

class TestComposition:
    """Test composition - objects containing other objects."""
    
    def test_analyzer_contains_glossary(self):
        """Test that Analyzer HAS-A Glossary (composition)."""
        analyzer = Analyzer()
        
        # Analyzer contains a Glossary instance
        assert hasattr(analyzer, '_glossary')
        assert isinstance(analyzer.glossary, Glossary)
        
        # Can use the composed glossary
        analyzer.glossary.add_term("test", ["phrase"])
        assert "test" in analyzer.glossary.terms
    
    def test_analyzer_contains_articles_list(self):
        """Test that Analyzer HAS-A list of Articles."""
        analyzer = Analyzer()
        
        # Initially empty
        assert hasattr(analyzer, '_articles')
        assert isinstance(analyzer._articles, list)
        assert len(analyzer._articles) == 0
        
        # Add articles
        article1 = analyzer.add_article("Text 1", "https://site1.com")
        article2 = analyzer.add_article("Text 2", "https://site2.com")
        
        # Analyzer now contains articles
        assert len(analyzer._articles) == 2
        assert isinstance(analyzer._articles[0], Article)
        assert isinstance(analyzer._articles[1], Article)
    
    def test_analyzer_contains_reports_list(self):
        """Test that Analyzer HAS-A list of Reports."""
        analyzer = Analyzer()
        
        assert hasattr(analyzer, '_reports')
        assert len(analyzer._reports) == 0
        
        # Add and analyze article
        article = analyzer.add_article("Test", "https://test.com")
        report = analyzer.analyze_article(article)
        
        # Analyzer now contains report
        assert len(analyzer._reports) == 1
        assert isinstance(analyzer._reports[0], BaseReport)
    
    def test_report_contains_article(self):
        """Test that Report HAS-A Article (composition)."""
        analyzer = Analyzer()
        article = analyzer.add_article("Test article", "https://test.com")
        report = analyzer.analyze_article(article)
        
        # Report contains the article
        assert hasattr(report, '_article')
        assert report._article is article
        
        # Can access article's properties through report
        assert report._article.domain == "test.com"
    
    def test_report_contains_score_dict(self):
        """Test that Report HAS-A score dictionary."""
        analyzer = Analyzer()
        article = analyzer.add_article("Always cures!", "https://test.com")
        report = analyzer.analyze_article(article)
        
        # Report contains score
        assert hasattr(report, '_score')
        assert isinstance(report.score, dict)
        assert 'total' in report.score
    
    def test_analyzer_uses_risk_scorer(self):
        """Test that Analyzer uses RiskScorer internally (composition in method)."""
        analyzer = Analyzer()
        article = analyzer.add_article("Miracle cure!", "https://test.com")
        
        # Analyzer creates and uses RiskScorer internally
        report = analyzer.analyze_article(article)
        
        # The result comes from RiskScorer's calculations
        assert 'total' in report.score
        assert 'clickbait' in report.score
        assert 'absolute' in report.score
    
    def test_composition_vs_inheritance(self):
        """Test understanding: composition (HAS-A) vs inheritance (IS-A)."""
        analyzer = Analyzer()
        article = analyzer.add_article("Test", "https://test.com")
        report = CSVReport(article, {"total": 1}, [], [])
        
        # Inheritance (IS-A): CSVReport IS-A BaseReport
        assert isinstance(report, BaseReport)
        assert isinstance(report, CSVReport)
        
        # Composition (HAS-A): Report HAS-A Article
        assert hasattr(report, '_article')
        assert isinstance(report._article, Article)
        # But Report is NOT an Article
        assert not isinstance(report, Article)
    
    def test_deep_composition_chain(self):
        """Test composition through multiple levels."""
        analyzer = Analyzer()
        
        # Analyzer HAS-A Glossary
        assert isinstance(analyzer.glossary, Glossary)
        
        # Glossary HAS-A dictionary
        assert isinstance(analyzer.glossary.terms, dict)
        
        # Can navigate the composition chain
        analyzer.glossary.add_term("vaccine", ["immunization"])
        assert "vaccine" in analyzer.glossary.terms
        assert "immunization" in analyzer.glossary.terms["vaccine"]
    
    def test_composition_allows_flexibility(self):
        """Test that composition allows changing components at runtime."""
        # Create analyzer with CSV report
        analyzer1 = Analyzer(report_class=CSVReport)
        assert analyzer1._report_class == CSVReport
        
        # Create analyzer with JSON report (different component)
        analyzer2 = Analyzer(report_class=JSONReport)
        assert analyzer2._report_class == JSONReport
        
        # Can change component at runtime
        analyzer1.set_report_format(HTMLReport)
        assert analyzer1._report_class == HTMLReport


# ==================== INTEGRATION TESTS ====================

class TestOOPIntegration:
    """Test that all OOP principles work together correctly."""
    
    def test_full_pipeline_with_polymorphism(self):
        """Test complete analysis pipeline using polymorphism."""
        # Test with all three report types
        report_types = [CSVReport, JSONReport, HTMLReport]
        
        for ReportClass in report_types:
            analyzer = Analyzer(report_class=ReportClass)
            
            # Setup (composition)
            analyzer.glossary.add_term("vaccine", ["immunization"])
            
            # Process article (composition)
            article = analyzer.add_article(
                "This miracle vaccine always cures everything!",
                "https://dubious-site.com"
            )
            
            # Analyze (polymorphism - works with any report type)
            report = analyzer.analyze_article(article)
            
            # Verify inheritance
            assert isinstance(report, BaseReport)
            assert isinstance(report, ReportClass)
            
            # Verify composition
            assert report._article is article
            
            # Verify polymorphism
            assert report.get_risk_level() == "High"
    
    def test_multiple_reports_same_analyzer(self):
        """Test that one analyzer can produce multiple report types."""
        analyzer = Analyzer()
        
        # Setup glossary (composition)
        analyzer.glossary.add_term("cancer", ["carcinoma"])
        
        # Add articles (composition)
        article1 = analyzer.add_article("Text 1", "https://site1.com")
        article2 = analyzer.add_article("Text 2", "https://site2.com")
        
        # Generate different report types (polymorphism)
        analyzer.set_report_format(CSVReport)
        report1 = analyzer.analyze_article(article1)
        
        analyzer.set_report_format(JSONReport)
        report2 = analyzer.analyze_article(article2)
        
        # Both in same collection (polymorphism)
        assert len(analyzer.reports) == 2
        assert isinstance(analyzer.reports[0], CSVReport)
        assert isinstance(analyzer.reports[1], JSONReport)
        
        # Both are BaseReport (inheritance)
        for report in analyzer.reports:
            assert isinstance(report, BaseReport)
    
    def test_oop_principles_summary(self):
        """Summary test showing all three principles in action."""
        # COMPOSITION: Analyzer HAS-A Glossary and Articles
        analyzer = Analyzer(report_class=JSONReport)
        analyzer.glossary.add_term("flu", ["influenza"])
        
        # COMPOSITION: Add article to analyzer
        article = analyzer.add_article("Flu cure!", "https://test.com")
        
        # INHERITANCE & POLYMORPHISM: Create report
        report = analyzer.analyze_article(article)
        
        # INHERITANCE: Report IS-A BaseReport
        assert isinstance(report, BaseReport)
        assert isinstance(report, JSONReport)
        
        # COMPOSITION: Report HAS-A Article
        assert report._article is article
        
        # POLYMORPHISM: Can use base class interface
        risk = report.get_risk_level()
        summary = report.summary()
        
        assert risk in ["Low", "Medium", "High"]
        assert isinstance(summary, dict)
        
        print("\n✅ All OOP Principles Verified:")
        print("   - Inheritance: JSONReport IS-A BaseReport")
        print("   - Polymorphism: All reports respond to same interface")
        print("   - Composition: Analyzer HAS-A Glossary, Articles, Reports")


# ==================== PYTEST CONFIGURATION ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
