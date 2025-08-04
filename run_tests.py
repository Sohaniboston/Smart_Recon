#!/usr/bin/env python3
"""
SmartRecon Test Runner

Comprehensive test runner for SmartRecon project.
Runs unit tests, integration tests, and generates test reports.

Author: SmartRecon Development Team
Date: 2025-07-28
"""

import unittest
import sys
import os
import time
from datetime import datetime
import json
from io import StringIO

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import test modules
from tests.unit.test_data_ingestion import TestDataIngestion, TestDataIngestionEdgeCases
from tests.unit.test_data_cleaning import TestDataCleaner, TestDataCleanerConfiguration
from tests.unit.test_exact_matching import TestExactMatchingEngine, TestExactMatchingEngineConfiguration
from tests.unit.test_fuzzy_matching import TestFuzzyMatcher, TestFuzzyMatcherConfiguration
from tests.unit.test_config import TestConfig, TestConfigurationEdgeCases
from tests.integration.test_workflow_integration import TestEndToEndWorkflow, TestModuleIntegration


class TestRunner:
    """Main test runner class."""
    
    def __init__(self):
        self.results = {
            'start_time': None,
            'end_time': None,
            'duration': 0,
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0,
            'test_results': {},
            'summary': ""
        }
    
    def run_unit_tests(self):
        """Run all unit tests."""
        print("🧪 Running Unit Tests...")
        print("=" * 50)
        
        unit_test_classes = [
            ('Data Ingestion', [TestDataIngestion, TestDataIngestionEdgeCases]),
            ('Data Cleaning', [TestDataCleaner, TestDataCleanerConfiguration]),
            ('Exact Matching', [TestExactMatchingEngine, TestExactMatchingEngineConfiguration]),
            ('Fuzzy Matching', [TestFuzzyMatcher, TestFuzzyMatcherConfiguration]),
            ('Configuration', [TestConfig, TestConfigurationEdgeCases])
        ]
        
        unit_results = {}
        
        for module_name, test_classes in unit_test_classes:
            print(f"\n📋 Testing {module_name}...")
            
            suite = unittest.TestSuite()
            for test_class in test_classes:
                tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
                suite.addTests(tests)
            
            # Capture test output
            stream = StringIO()
            runner = unittest.TextTestRunner(stream=stream, verbosity=2)
            result = runner.run(suite)
            
            unit_results[module_name] = {
                'tests_run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'skipped': len(result.skipped) if hasattr(result, 'skipped') else 0,
                'success_rate': ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0,
                'output': stream.getvalue()
            }
            
            # Print summary for this module
            print(f"  ✅ Tests run: {result.testsRun}")
            print(f"  ❌ Failures: {len(result.failures)}")
            print(f"  ⚠️  Errors: {len(result.errors)}")
            print(f"  ⏭️  Skipped: {unit_results[module_name]['skipped']}")
            print(f"  📊 Success rate: {unit_results[module_name]['success_rate']:.1f}%")
            
            if result.failures:
                print(f"  🔍 Failures:")
                for test, trace in result.failures:
                    print(f"    - {test}")
            
            if result.errors:
                print(f"  🔍 Errors:")
                for test, trace in result.errors:
                    print(f"    - {test}")
        
        return unit_results
    
    def run_integration_tests(self):
        """Run integration tests."""
        print("\n🔗 Running Integration Tests...")
        print("=" * 50)
        
        integration_test_classes = [
            ('End-to-End Workflow', [TestEndToEndWorkflow]),
            ('Module Integration', [TestModuleIntegration])
        ]
        
        integration_results = {}
        
        for module_name, test_classes in integration_test_classes:
            print(f"\n📋 Testing {module_name}...")
            
            suite = unittest.TestSuite()
            for test_class in test_classes:
                tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
                suite.addTests(tests)
            
            # Capture test output
            stream = StringIO()
            runner = unittest.TextTestRunner(stream=stream, verbosity=2)
            result = runner.run(suite)
            
            integration_results[module_name] = {
                'tests_run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'skipped': len(result.skipped) if hasattr(result, 'skipped') else 0,
                'success_rate': ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0,
                'output': stream.getvalue()
            }
            
            # Print summary for this module
            print(f"  ✅ Tests run: {result.testsRun}")
            print(f"  ❌ Failures: {len(result.failures)}")
            print(f"  ⚠️  Errors: {len(result.errors)}")
            print(f"  ⏭️  Skipped: {integration_results[module_name]['skipped']}")
            print(f"  📊 Success rate: {integration_results[module_name]['success_rate']:.1f}%")
            
            if result.failures:
                print(f"  🔍 Failures:")
                for test, trace in result.failures:
                    print(f"    - {test}")
            
            if result.errors:
                print(f"  🔍 Errors:")
                for test, trace in result.errors:
                    print(f"    - {test}")
        
        return integration_results
    
    def generate_test_data(self):
        """Generate test data if needed."""
        print("\n📁 Generating Test Data...")
        
        try:
            from tests.data.generate_test_data import save_test_datasets
            
            # Generate test data
            test_data_dir = os.path.join(os.path.dirname(__file__), 'tests', 'data')
            metadata = save_test_datasets(test_data_dir)
            
            print(f"✅ Test data generated successfully")
            print(f"📊 Generated {len(metadata['datasets'])} test datasets")
            
            return True
        except Exception as e:
            print(f"❌ Failed to generate test data: {e}")
            return False
    
    def run_performance_tests(self):
        """Run performance-specific tests."""
        print("\n⚡ Running Performance Tests...")
        print("=" * 50)
        
        # Performance test would be a subset of integration tests
        # focusing on timing and resource usage
        
        performance_results = {
            'large_dataset_processing': 'Not implemented',
            'memory_usage': 'Not implemented',
            'concurrent_processing': 'Not implemented'
        }
        
        print("⏭️  Performance tests not fully implemented yet")
        print("📋 Placeholder for future performance testing")
        
        return performance_results
    
    def generate_test_report(self, unit_results, integration_results, performance_results):
        """Generate comprehensive test report."""
        
        # Calculate totals
        total_tests = 0
        total_failures = 0
        total_errors = 0
        total_skipped = 0
        
        all_results = {**unit_results, **integration_results}
        
        for module_results in all_results.values():
            total_tests += module_results['tests_run']
            total_failures += module_results['failures']
            total_errors += module_results['errors']
            total_skipped += module_results['skipped']
        
        total_passed = total_tests - total_failures - total_errors - total_skipped
        overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        # Update results
        self.results.update({
            'end_time': datetime.now(),
            'duration': (datetime.now() - self.results['start_time']).total_seconds(),
            'total_tests': total_tests,
            'passed': total_passed,
            'failed': total_failures,
            'errors': total_errors,
            'skipped': total_skipped,
            'test_results': {
                'unit_tests': unit_results,
                'integration_tests': integration_results,
                'performance_tests': performance_results
            }
        })
        
        # Generate summary
        summary = f"""
SmartRecon Test Suite Results
============================

📊 Overall Summary:
  • Total Tests: {total_tests}
  • Passed: {total_passed} ✅
  • Failed: {total_failures} ❌
  • Errors: {total_errors} ⚠️
  • Skipped: {total_skipped} ⏭️
  • Success Rate: {overall_success_rate:.1f}%
  • Duration: {self.results['duration']:.2f} seconds

📋 Unit Tests Summary:
"""
        
        for module_name, results in unit_results.items():
            summary += f"  • {module_name}: {results['success_rate']:.1f}% ({results['tests_run']} tests)\n"
        
        summary += "\n🔗 Integration Tests Summary:\n"
        for module_name, results in integration_results.items():
            summary += f"  • {module_name}: {results['success_rate']:.1f}% ({results['tests_run']} tests)\n"
        
        # Add recommendations
        summary += f"\n💡 Recommendations:\n"
        
        if total_failures > 0:
            summary += f"  • Investigate {total_failures} test failures\n"
        
        if total_errors > 0:
            summary += f"  • Fix {total_errors} test errors\n"
        
        if overall_success_rate < 95:
            summary += f"  • Improve test coverage to reach 95%+ success rate\n"
        
        if overall_success_rate >= 95:
            summary += f"  • Excellent test coverage! Consider adding more edge cases\n"
        
        self.results['summary'] = summary
        
        return self.results
    
    def save_test_report(self, output_dir='test_reports'):
        """Save test report to file."""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON report
        json_file = os.path.join(output_dir, f'test_report_{timestamp}.json')
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Save text summary
        txt_file = os.path.join(output_dir, f'test_summary_{timestamp}.txt')
        with open(txt_file, 'w') as f:
            f.write(self.results['summary'])
        
        print(f"\n📄 Test reports saved:")
        print(f"  📋 JSON Report: {json_file}")
        print(f"  📝 Summary: {txt_file}")
        
        return json_file, txt_file
    
    def run_all_tests(self):
        """Run complete test suite."""
        self.results['start_time'] = datetime.now()
        
        print("🚀 Starting SmartRecon Test Suite")
        print("=" * 60)
        print(f"⏰ Started at: {self.results['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Generate test data
        self.generate_test_data()
        
        # Run tests
        unit_results = self.run_unit_tests()
        integration_results = self.run_integration_tests()
        performance_results = self.run_performance_tests()
        
        # Generate and display report
        report = self.generate_test_report(unit_results, integration_results, performance_results)
        
        print("\n" + "=" * 60)
        print("🏁 Test Suite Complete!")
        print(report['summary'])
        
        # Save reports
        self.save_test_report()
        
        return report


def main():
    """Main function to run tests."""
    
    # Parse command line arguments for specific test types
    import argparse
    
    parser = argparse.ArgumentParser(description='SmartRecon Test Runner')
    parser.add_argument('--unit', action='store_true', help='Run only unit tests')
    parser.add_argument('--integration', action='store_true', help='Run only integration tests')
    parser.add_argument('--performance', action='store_true', help='Run only performance tests')
    parser.add_argument('--generate-data', action='store_true', help='Only generate test data')
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.generate_data:
        runner.generate_test_data()
        return
    
    if args.unit:
        runner.results['start_time'] = datetime.now()
        unit_results = runner.run_unit_tests()
        report = runner.generate_test_report(unit_results, {}, {})
        print(report['summary'])
        runner.save_test_report()
    elif args.integration:
        runner.results['start_time'] = datetime.now()
        integration_results = runner.run_integration_tests()
        report = runner.generate_test_report({}, integration_results, {})
        print(report['summary'])
        runner.save_test_report()
    elif args.performance:
        runner.results['start_time'] = datetime.now()
        performance_results = runner.run_performance_tests()
        report = runner.generate_test_report({}, {}, performance_results)
        print(report['summary'])
        runner.save_test_report()
    else:
        # Run all tests
        runner.run_all_tests()


if __name__ == '__main__':
    main()
