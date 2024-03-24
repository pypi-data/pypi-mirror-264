'''Reporting Module.'''
import os
import os.path

from .pylint import PylintReport
from .pytest import CoverageReport


class Report(object):
    """
    Class to summarize the code quality of a package.
    """
    def __init__(self):
        """
        Initialize the report.
        """
        pass

    def _getNum(self, num):
        """
        Converts a number to float or int if a number was given as string.

        Parameters
        ----------
        num: object
            The number as any type.

        Returns
        -------
        int or float
            The number.
        """
        if type(num) is str:
            num = num[:-1] if num[-1] == '%' else num
            return float(num) if '.' in num else int(num)

        return num

    def _getDiffTxt(self, old, new):
        """
        Get the difference between two values in text format.

        Parameters
        ----------
        old: object
            The old value.

        new: object
            The new value.

        Returns
        -------
        str
            The difference in text format.
        """
        if type(old) is str:
            postfix = '%' if old[-1] == '%' else ''
        else:
            postfix = ''
        old = self._getNum(old)
        new = self._getNum(new)
        if type(old) is int:
            txt = ' (%+i%s)' % (new-old, postfix)
        else:
            txt = ' (%+.2f%s)' % (new-old, postfix)
        return txt

    def _getDiffHtml(self, old, new, better=+1):
        """
        Get the difference between two values in HTML format.

        Parameters
        ----------
        old: object
            The old value.
        new: object
            The new value.
        better:
            The direction of improvement (+1: higher better; -1: lower better), or None.

        Returns
        -------
        str
            The difference in HTML format.
        """
        if type(old) is str:
            postfix = '%' if old[-1] == '%' else ''
        else:
            postfix = ''
        old = self._getNum(old)
        new = self._getNum(new)
        color = {-1: 'red',
                 1: 'green',
                 0: '#666'}[-1 if (new-old)*better < 0 else (1 if (new-old)*better > 0 else 0)]
        if type(old) is int:
            html = ' (<span style="color:%s">%+i%s</span>)' % (color, new - old, postfix)
        else:
            html = ' (<span style="color:%s">%+.2f%s</span>)' % (color, new - old, postfix)
        return html
      
    def getReportTemplate(self, report_type='txt'):
        """
        Get the report template.

        Parameters
        ----------
        report_type: str
            The report type ('txt' or 'html').

        Returns
        -------
        str
            The report template.
        """
        # get the abolute path of this script
        script_abs_path = os.path.abspath(__file__)
        # get the directory of this script
        script_dir = os.path.dirname(script_abs_path)
        # get the path of the template
        template_path = os.path.join(script_dir, 'templates/report.%s' % report_type)

        with open(template_path) as f:
            template = f.read()
        return template

    def _replacePlacehlder(self, report, placeholder, actual_results, method_name, previous_results=None, arg=None, better=None):
        """
        Replace a placeholder in the report with the actual results.

        Parameters
        ----------
        report: str
            The report template.

        placeholder: str
            The placeholder to be replaced.

        actual_results: object
            The actual results e.g. for coverage or pylint.

        method_name: str
            The method to be called on results.

        previous_results: object
            The previous results (e.g. for coverage or pylint), or None.

        arg: object
            The argument to be passed to the method, or None.

        better: int
            The direction of improvement (+1: higher better; -1: lower better), or None.

        Returns
        -------
        str
            The filled report.
        """
        if arg is None:
            actual_val = getattr(actual_results, method_name)()
        else:
            actual_val = getattr(actual_results, method_name)()[arg]

        report = report.replace('<%s>' % placeholder,
                                str(actual_val))
        if previous_results:
            if arg is None:
                previous_val = getattr(previous_results, method_name)()
            else:
                previous_val = getattr(previous_results, method_name)()[arg]
            if report[1:5] == 'html':
                report = report.replace('<%s_diff>' % placeholder,
                                        self._getDiffHtml(previous_val, actual_val, better))
            else:
                report = report.replace('<%s_diff>' % placeholder,
                                        self._getDiffTxt(previous_val, actual_val))
        return report

    def _fillTemplate(self, report, package_name, coverage, pylint, previous_coverage=None, previous_pylint=None):
        """
        Fill the report template with the actual results.

        Parameters
        ----------
        report: str
            The report template.

        package_name: str
            Name of the package to be analyzed.

        coverage: CoverageReport
            The coverage report.

        pylint: PylintReport
            The Pylint report.

        previous_coverage: CoverageReport
            The previous coverage report, or None.

        previous_pylint: PylintReport
            The previous Pylint report, or None.

        Returns
        -------
        str
            The filled report.
        """
        report = report.replace('<package_name>', str(package_name))
        report = report.replace('<pytest_report_url>', str(coverage.getTxtUrl()))

        report = self._replacePlacehlder(report, 'coverage', coverage, 'getTotalCoverage', previous_coverage, better=+1)
        report = self._replacePlacehlder(report, 'num_tests', coverage, 'getNumberOfTests', previous_coverage, arg=0, better=+1)
        report = self._replacePlacehlder(report, 'num_errors', coverage, 'getNumberOfTests', previous_coverage, arg=1, better=-1)

        report = self._replacePlacehlder(report, 'pylint_score', pylint, 'getScore', previous_pylint, better=+1)

        report = report.replace('<pylint_report_url>', str(pylint.getTxtUrl()))

        report = self._replacePlacehlder(report, 'missing_docstrings', pylint, 'getMissingDocstrings', previous_pylint, better=-1)

        report = self._replacePlacehlder(report, 'too_complex_num', pylint, 'getTooComplex', previous_pylint, arg=0, better=-1)
        report = self._replacePlacehlder(report, 'too_complex_max', pylint, 'getTooComplex', previous_pylint, arg=1, better=-1)
        report = report.replace('<too_complex_file>', str(pylint.getTooComplex()[2]))
        report = report.replace('<too_complex_obj>', str(pylint.getTooComplex()[3]))
        report = report.replace('<too_complex_line>', str(pylint.getTooComplex()[4]))

        report = self._replacePlacehlder(report, 'func_too_long_num', pylint, 'getTooManyStatements', previous_pylint, arg=0, better=-1)
        report = self._replacePlacehlder(report, 'func_too_long_max', pylint, 'getTooManyStatements', previous_pylint, arg=1, better=-1)
        report = report.replace('<func_too_long_file>', str(pylint.getTooManyStatements()[2]))
        report = report.replace('<func_too_long_obj>', str(pylint.getTooManyStatements()[3]))
        report = report.replace('<func_too_long_line>', str(pylint.getTooManyStatements()[4]))

        report = self._replacePlacehlder(report, 'duplicate_code', pylint, 'getDuplicateCode', previous_pylint, arg=0, better=-1)
        report = report.replace('<duplicate_code_num>', str(pylint.getDuplicateCode()[1]))
        report = report.replace('<duplicate_code_files>', ', '.join(pylint.getDuplicateCode()[2]))
        report = report.replace('<duplicate_code_lines>', str(pylint.getDuplicateCode()[3]))

        report = self._replacePlacehlder(report, 'unused_imports', pylint, 'getUnusedImports', previous_pylint, arg=0, better=-1)
        report = report.replace('<unused_imports_file>', str(pylint.getUnusedImports()[1]))
        report = report.replace('<unused_imports_num>', str(pylint.getUnusedImports()[2]))
        report = report.replace('<unused_imports_items>', ', '.join(pylint.getUnusedImports()[3]))

        report = self._replacePlacehlder(report, 'unused_variables', pylint, 'getUnusedVariables', previous_pylint, arg=0, better=-1)
        report = report.replace('<unused_variables_file>', str(pylint.getUnusedVariables()[1]))
        report = report.replace('<unused_variables_num>', str(pylint.getUnusedVariables()[2]))
        report = report.replace('<unused_variables_items>', ', '.join(pylint.getUnusedVariables()[3]))

        report = self._replacePlacehlder(report, 'unused_arguments', pylint, 'getUnusedArguments', previous_pylint, arg=0, better=-1)
        report = report.replace('<unused_arguments_file>', str(pylint.getUnusedArguments()[1]))
        report = report.replace('<unused_arguments_num>', str(pylint.getUnusedArguments()[2]))
        report = report.replace('<unused_arguments_items>', ', '.join(pylint.getUnusedArguments()[3]))

        report = self._replacePlacehlder(report, 'unreachable_code', pylint, 'getUnreachableCode', previous_pylint, arg=0, better=-1)
        report = report.replace('<unreachable_code_file>', str(pylint.getUnreachableCode()[1]))
        report = report.replace('<unreachable_code_num>', str(pylint.getUnreachableCode()[2]))
        report = report.replace('<unreachable_code_items>', ', '.join(pylint.getUnreachableCode()[3]))

        report = self._replacePlacehlder(report, 'num_py23_incompatible', pylint, 'getNumPy23Incompatibible', previous_pylint, better=-1)


        return report

    def summarizeCodeQuality(self, package_name):
        """
        Summarize the code quality of the package.

        Parameters
        ----------
        package_name: str
            Name of the package to be analyzed.

        Returns
        -------
        None
        """
        coverage = CoverageReport()
        previous_coverage = self._getPreviousCoverage()

        pylint = PylintReport()
        previous_pylint = self._getPreviousPylint()

        for report_type in ['txt', 'html']:
            report = self.getReportTemplate(report_type=report_type)
            report = self._fillTemplate(report, package_name, coverage, pylint, previous_coverage, previous_pylint)
            if report_type == 'txt':
                print(report)
            with open('code_quality_report.%s' % report_type, 'w') as f:
                f.write(report)

    def _getPreviousPylint(self):
        """
        Get the previous Pylint report from file if it exists.

        Returns
        -------
        PylintReport
            The previous Pylint report.
        """
        previous_pylint_file = 'last_run/pylint'
        if os.path.exists(previous_pylint_file + '.txt') and (os.path.getsize(previous_pylint_file + '.json') > 0):
            previous_pylint = PylintReport(txt=previous_pylint_file + '.txt', json=previous_pylint_file + '.json')
        else:
            previous_pylint = None
        return previous_pylint

    def _getPreviousCoverage(self):
        """
        Get the previous coverage report from file if it exists.

        Returns
        -------
        CoverageReport
            The previous coverage report.
        """
        previous_coverage_file = 'last_run/coverage'
        if os.path.exists(previous_coverage_file + '.txt') and (os.path.getsize(previous_coverage_file + '.txt') > 0):
            previous_coverage = CoverageReport(txt=previous_coverage_file + '.txt', xml=previous_coverage_file + '.xml')
        else:
            previous_coverage = None
        return previous_coverage
