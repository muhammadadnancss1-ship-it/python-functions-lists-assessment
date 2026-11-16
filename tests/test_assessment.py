"""Runnable standard-library tests for both actual application files."""

import contextlib
import io
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = []
RECORDED_RUNS = {}


def add_case(task, title, description, expected, inputs, contains=(), counts=None):
    prefix = "R" if task == "result" else "E"
    number = sum(case["task"] == task for case in SCENARIOS) + 1
    SCENARIOS.append({
        "id": f"{prefix}{number:02}",
        "task": task,
        "scenario": title,
        "inputs_description": description,
        "expected": expected,
        "inputs": [str(value) for value in inputs],
        "contains": list(contains),
        "counts": counts or {},
    })


def card_input(marks, name="Adnan", roll="24"):
    return [name, roll, *marks]


add_case("result", "Original worked example", "Adnan; roll 24; 89,78,90,56,80",
         "393/500; 78.60%; B; Pass", card_input([89,78,90,56,80]),
         ["Total Marks  : 393/500", "Percentage   : 78.60%", "Grade        : B", "Result       : Pass"])
add_case("result", "Name formatting and leading-zero roll", "Padded adnan ali; roll 001; all marks 80",
         "Adnan Ali; roll 001 retained; A/Pass", card_input([80]*5,"  adnan ali  ","001"),
         ["Student Name : Adnan Ali", "Roll Number  : 001", "Grade        : A", "Result       : Pass"])
for bad, label in [("123","Numeric name"),("","Empty name"),("   ","Spaces-only name"),
                   ("Ali123","Alphanumeric name"),("Ali-Khan","Punctuation in name")]:
    add_case("result", label, f"Name {bad!r}, then Ali; other fields valid",
             "Name rejected once; corrected name accepted", [bad,"Ali","24",*[80]*5],
             ["Student Name : Ali"], {"Invalid name!":1})
for bad, label in [("abc","Alphabetic roll"),("","Empty roll"),("12A","Alphanumeric roll"),("   ","Spaces-only roll")]:
    add_case("result", label, f"Roll {bad!r}, then 001; other fields valid",
             "Roll rejected once; 001 retained", ["Adnan",bad,"001",*[80]*5],
             ["Roll Number  : 001"], {"Invalid roll number!":1})
add_case("result", "Roll follows isdigit semantics", "Superscript digit ² as roll; all marks 80",
         "Roll stays text; ² accepted by isdigit; A/Pass",card_input([80]*5,roll="²"),
         ["Roll Number  : ²","Result       : Pass"])
for bad, label in [("abc","Text mark"),("-1","Negative mark"),("101","Mark above 100"),
                   ("1.5","Fractional mark"),("","Empty mark"),("   ","Spaces-only mark"),
                   ("²","Non-decimal digit regression")]:
    add_case("result",label,f"English {bad!r}, then 80; other marks 80",
             "Invalid mark rejected once; corrected marks give A/Pass",
             ["Adnan","24",bad,"80",*[80]*4],
             ["Total Marks  : 400/500","Grade        : A","Result       : Pass"],{"Invalid marks!":1})
add_case("result","Unicode decimal marks","Arabic-Indic ٨٠ in every subject",
         "Each mark converts to 80; 400/500; A/Pass",card_input(["٨٠"]*5),
         ["Total Marks  : 400/500","Grade        : A"])
add_case("result","Oversized marks regression","5000 nines, then 80; other marks 80",
         "Oversized mark rejected without conversion crash",
         ["Adnan","24","9"*5000,"80",*[80]*4],["Total Marks  : 400/500"],{"Invalid marks!":1})
add_case("result","Leading zeros before a mark","5000 ASCII zeros followed by 80",
         "Leading zeros stripped safely; mark 80 accepted",
         ["Adnan","24","0"*5000+"80",*[80]*4],["Total Marks  : 400/500"],{"Invalid marks!":0})
add_case("result","All zero marks","0,0,0,0,0","0/500; 0.00%; Fail",
         card_input([0]*5),["Total Marks  : 0/500","Percentage   : 0.00%","Grade        : Fail","Result       : Fail"])
add_case("result","All maximum marks","100,100,100,100,100","500/500; 100.00%; A+/Pass",
         card_input([100]*5),["Total Marks  : 500/500","Percentage   : 100.00%","Grade        : A+","Result       : Pass"])
add_case("result","Subject threshold alone is not enough","40 in all five subjects",
         "40.00% overall; Fail even though no subject is below 40",
         card_input([40]*5),["Percentage   : 40.00%","Grade        : Fail","Result       : Fail"])
add_case("result","Just below overall pass threshold","49,50,50,50,50",
         "249/500; 49.80%; Fail",card_input([49,50,50,50,50]),
         ["Total Marks  : 249/500","Percentage   : 49.80%","Grade        : Fail"])
add_case("result","Exact overall pass threshold","50 in every subject",
         "250/500; 50.00%; D/Pass",card_input([50]*5),
         ["Total Marks  : 250/500","Percentage   : 50.00%","Grade        : D","Result       : Pass"])
add_case("result","Exact subject pass threshold","40,53,53,52,52",
         "One subject at 40; overall 50.00%; D/Pass",card_input([40,53,53,52,52]),
         ["Percentage   : 50.00%","Grade        : D","Result       : Pass"])
for index,subject in enumerate(["English","Math","Physics","Chemistry","Computer"]):
    marks=[80]*5;marks[index]=39
    add_case("result",f"{subject} fails alone",f"{subject} 39; all other subjects 80",
             "Final grade and result become Fail",card_input(marks),
             ["Grade        : Fail","Result       : Fail"])
add_case("result","Several subject failures","39,20,80,80,80",
         "Multiple subjects below 40; final Fail",card_input([39,20,80,80,80]),
         ["Grade        : Fail","Result       : Fail"])
add_case("result","High percentage cannot override a failed subject","39,100,100,100,100",
         "87.80% overall; final grade/result Fail",card_input([39,100,100,100,100]),
         ["Percentage   : 87.80%","Grade        : Fail","Result       : Fail"])
for cutoff,upper,lower in [(90,"A+","A"),(80,"A","B"),(70,"B","C"),(60,"C","D")]:
    add_case("result",f"Exact {cutoff}% grade boundary",f"{cutoff} in all subjects",
             f"{cutoff:.2f}%; {upper}/Pass",card_input([cutoff]*5),
             [f"Percentage   : {cutoff:.2f}%",f"Grade        : {upper}","Result       : Pass"])
    add_case("result",f"Just below {cutoff}% grade boundary",f"{cutoff-1},{cutoff},{cutoff},{cutoff},{cutoff}",
             f"{cutoff-0.2:.2f}%; {lower}/Pass",card_input([cutoff-1,*[cutoff]*4]),
             [f"Percentage   : {cutoff-0.2:.2f}%",f"Grade        : {lower}","Result       : Pass"])
add_case("result","Several invalid fields in one run","Bad name, bad roll, text/out-of-range English; then all 50",
         "All corrections requested; one D/Pass card",
         ["123","Adnan","12A","001","abc","101",*[50]*5],
         ["Roll Number  : 001","Percentage   : 50.00%","Grade        : D","Result       : Pass"],
         {"Invalid name!":1,"Invalid roll number!":1,"Invalid marks!":2,"STUDENT RESULT CARD":1})

add_case("electricity","Three-household worked example","3 households; units 100,150,250",
         "Bills 1000,1750,3500; processed 3; revenue 6250",
         [3,100,150,250],
         ["Electricity Bill: Rs. 1000","Electricity Bill: Rs. 1750","Electricity Bill: Rs. 3500",
          "Households Processed: 3","Total Revenue: Rs. 6250"])
for units,bill in [(0,0),(1,10),(99,990),(100,1000),(101,1015),
                   (199,2485),(200,2500),(201,2520),(250,3500),(1000,18500)]:
    add_case("electricity",f"Units boundary {units}",f"1 household; {units} units",
             f"Bill/revenue Rs. {bill}; processed 1",[1,units],
             [f"Electricity Bill: Rs. {bill}",f"Total Revenue: Rs. {bill}","Households Processed: 1"])
for bad,label in [("0","Zero households"),("-1","Negative households"),("abc","Text household count"),
                  ("2.5","Fractional household count"),("","Empty household count"),("²","Non-decimal household digit")]:
    add_case("electricity",label,f"Count {bad!r}, then 1; units 100",
             "Invalid count rejected once; one valid bill for Rs. 1000",
             [bad,1,100],["Households Processed: 1","Total Revenue: Rs. 1000"],{"Invalid input!":1})
for bad,label in [("-1","Negative units"),("abc","Text units"),("1.5","Fractional units"),
                  ("","Empty units"),("²","Non-decimal unit digit")]:
    add_case("electricity",label,f"1 household; units {bad!r}, then 100",
             "Retry the same household; processed 1; revenue Rs. 1000",
             [1,bad,100],["Households Processed: 1","Total Revenue: Rs. 1000"],
             {"Invalid input!":1,"--- Household 1 ---":1})
add_case("electricity","Combined invalid count and units","abc,0,2 households; -1,bad,100 units; then 201",
         "Four errors; both households billed; revenue Rs. 3520",
         ["abc",0,2,-1,"bad",100,201],["Households Processed: 2","Total Revenue: Rs. 3520"],{"Invalid input!":4})
add_case("electricity","Zero units included in processed count","3 households; units 0,50,100",
         "Zero bill still counted; processed 3; revenue Rs. 1500",
         [3,0,50,100],["Households Processed: 3","Total Revenue: Rs. 1500"])
add_case("electricity","All zero-unit households","2 households; units 0,0",
         "Two households processed; revenue Rs. 0",
         [2,0,0],["Households Processed: 2","Total Revenue: Rs. 0"],{"Electricity Bill: Rs. 0":2})
add_case("electricity","Oversized household count","5000 nines, then 1; units 100",
         "Digit guard rejects input without a conversion crash",
         ["9"*5000,1,100],["Households Processed: 1","Total Revenue: Rs. 1000"],{"Invalid input!":1})
add_case("electricity","Oversized units","1 household; 5000 nines, then 100 units",
         "Digit guard retries; one bill for Rs. 1000",
         [1,"9"*5000,100],["Households Processed: 1","Total Revenue: Rs. 1000"],{"Invalid input!":1})
add_case("electricity","Leading ASCII zeros","Count 0001; units 000150",
         "Count becomes 1; units become 150; revenue Rs. 1750",
         ["0001","000150"],["Households Processed: 1","Total Revenue: Rs. 1750"])
add_case("electricity","Unicode decimal units","Count ٢; units ١٠٠ and ٢٠٠",
         "Two households; bills 1000/2500; revenue Rs. 3500",
         ["٢","١٠٠","٢٠٠"],["Households Processed: 2","Total Revenue: Rs. 3500"])
add_case("electricity","Maximum integer input length","1 household; 18 nines as units",
         "Exact integer bill Rs. 19999999999999998480",
         [1,"9"*18],["Electricity Bill: Rs. 19999999999999998480","Total Revenue: Rs. 19999999999999998480"])
add_case("electricity","Nineteen-digit count","19 nines, then 1; units 100",
         "Overlong count rejected once; valid count accepted",
         ["9"*19,1,100],["Households Processed: 1"],{"Invalid input!":1})
add_case("electricity","Whitespace around numeric input","Count ' 1 '; units ' 150 '",
         "Whitespace trimmed; one bill for Rs. 1750",
         [" 1 "," 150 "],["Households Processed: 1","Total Revenue: Rs. 1750"])


def run_session(filename, inputs):
    """Run the actual guarded entry point and echo each provided input."""
    values=iter(inputs)
    output=io.StringIO()
    def reader(prompt=""):
        try:
            value=next(values)
        except StopIteration as error:
            raise AssertionError(f"Unexpected prompt: {prompt}") from error
        print(prompt+value)
        return value
    with contextlib.redirect_stdout(output),patch("builtins.input",reader):
        runpy.run_path(str(ROOT/filename),run_name="__main__")
    remaining=list(values)
    if remaining:
        raise AssertionError(f"Unused scripted inputs: {remaining}")
    return output.getvalue()


class ProgramScenarios(unittest.TestCase):
    """One independently named test per console scenario."""


def scenario_test(case):
    def test(self):
        filename="result_card_generator.py" if case["task"]=="result" else "smart_electricity_bill.py"
        output=run_session(filename,case["inputs"])
        for fragment in case["contains"]:
            self.assertIn(fragment,output)
        for fragment,count in case["counts"].items():
            self.assertEqual(output.count(fragment),count,fragment)
        RECORDED_RUNS[case["id"]]={**case,"file":filename,"stdout":output,"status":"PASS"}
    return test


for scenario in SCENARIOS:
    setattr(ProgramScenarios,f"test_{scenario['id']}",scenario_test(scenario))


class HelperChecks(unittest.TestCase):
    def test_R_format_name(self):
        namespace=runpy.run_path(str(ROOT/"result_card_generator.py"),run_name="helper_import")
        self.assertEqual(namespace["format_name"]("  aLI  khan  "),"Ali  Khan")

    def test_R_percentage(self):
        namespace=runpy.run_path(str(ROOT/"result_card_generator.py"),run_name="helper_import")
        self.assertAlmostEqual(namespace["calculate_percentage"](393,500),78.6)

    def test_R_grade_is_percentage_only(self):
        namespace=runpy.run_path(str(ROOT/"result_card_generator.py"),run_name="helper_import")
        self.assertEqual(namespace["get_grade"](87.8),"A")
        # The main program, not this percentage helper, checks failed subjects.


class ProcessChecks(unittest.TestCase):
    def test_P01_result_card_real_stdin(self):
        completed=subprocess.run(
            [sys.executable,str(ROOT/"result_card_generator.py")],
            input="Adnan\n24\n89\n78\n90\n56\n80\n",
            text=True,capture_output=True,timeout=10,
        )
        self.assertEqual(completed.returncode,0,completed.stderr)
        self.assertIn("Percentage   : 78.60%",completed.stdout)
        self.assertIn("Result       : Pass",completed.stdout)

    def test_P02_electricity_real_stdin(self):
        completed=subprocess.run(
            [sys.executable,str(ROOT/"smart_electricity_bill.py")],
            input="3\n100\n150\n250\n",text=True,capture_output=True,timeout=10,
        )
        self.assertEqual(completed.returncode,0,completed.stderr)
        self.assertIn("Total Revenue: Rs. 6250",completed.stdout)
        self.assertIn("Households Processed: 3",completed.stdout)

    def test_P03_both_imports_are_silent(self):
        code=(
            "import runpy,sys; from unittest.mock import patch; "
            "block=patch('builtins.input',side_effect=AssertionError('input during import')); "
            "block.start(); a=runpy.run_path(sys.argv[1],run_name='card_import'); "
            "b=runpy.run_path(sys.argv[2],run_name='bill_import'); block.stop(); "
            "assert callable(a['main']) and callable(b['main'])"
        )
        completed=subprocess.run(
            [sys.executable,"-c",code,str(ROOT/"result_card_generator.py"),str(ROOT/"smart_electricity_bill.py")],
            text=True,capture_output=True,timeout=10,
        )
        self.assertEqual(completed.returncode,0,completed.stderr)
        self.assertEqual(completed.stdout,"")
        self.assertEqual(completed.stderr,"")

    def test_P04_imported_main_functions_are_callable(self):
        code=(
            "import runpy,sys; "
            "a=runpy.run_path(sys.argv[1],run_name='card_import'); "
            "b=runpy.run_path(sys.argv[2],run_name='bill_import'); "
            "a['main'](); b['main']()"
        )
        with tempfile.TemporaryDirectory() as directory:
            completed=subprocess.run(
                [sys.executable,"-c",code,str(ROOT/"result_card_generator.py"),str(ROOT/"smart_electricity_bill.py")],
                input="Ali\n001\n50\n50\n50\n50\n50\n1\n100\n",
                text=True,capture_output=True,timeout=10,cwd=directory,
            )
            self.assertEqual(completed.returncode,0,completed.stderr)
            self.assertIn("Grade        : D",completed.stdout)
            self.assertIn("Total Revenue: Rs. 1000",completed.stdout)
            self.assertEqual(list(Path(directory).iterdir()),[])


if __name__=="__main__":
    unittest.main(verbosity=2)
