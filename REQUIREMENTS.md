# Requirements, Source Review and Assumptions

## Source decision

The assessment-brief field contains a placeholder, so no official marking rubric, deadline or submission portal was supplied. Both uploaded Python files and the README were read in full.

The README describes a Class Marks Analyzer, but the uploaded second application is an electricity-bill calculator. This package follows the **two supplied Python programs** and corrects the README to match them. It does not add an unprovided class analyzer. The original folder name from the README is retained.

## Complete requirement inventory

| Requirement | Delivered implementation |
| --- | --- |
| Task 1 | Student Result Card Generator; functions, strings and a list of marks |
| Exact Task 1 file | result_card_generator.py at repository root |
| Required helpers | format_name(name), get_valid_marks(subject), calculate_percentage(total, max_total), get_grade(percentage) |
| Student fields | Name, digits-only roll string, English/Math/Physics/Chemistry/Computer marks |
| Name handling | Letter/space validation; strip() and title(); inner spaces retained |
| Roll rule | Use isdigit(); keep the identifier as text, including leading zeros |
| Mark rule | Whole numbers from 0 through 100; retry invalid entries |
| Result calculations | Sum five marks; calculate percentage out of 500 |
| Percentage grades | 90+ A+, 80+ A, 70+ B, 60+ C, 50+ D, otherwise Fail |
| Subject override | Any subject below 40 forces final grade and result to Fail |
| Card output | Name, roll, all subject marks, total, percentage with two decimals, grade, Pass/Fail |
| Task 2 | Smart Electricity Bill Calculator; for/range, accumulators, conditions inside the loop |
| Exact Task 2 file | smart_electricity_bill.py at repository root |
| Household input | Assumed positive whole number; units are whole numbers of 0 or more |
| Progressive rate 1 | First 100 units at Rs. 10 each |
| Progressive rate 2 | Next 100 units at Rs. 15 each |
| Progressive rate 3 | Only units above 200 at Rs. 20 each |
| Tariff status | Fictional practice values, not a source of real electricity tariffs |
| Loop and totals | Bill each household; accumulate exact integer revenue and completed count |
| Invalid units | Retry the same household; do not skip it or count an unbilled entry |
| Required source layout | Two independent program files plus README.md at root |
| Folder/repository name | python-functions-lists-assessment, retained from uploaded README |
| Official grading criteria / weights | Not provided; no grade or unseen-rubric guarantee |
| Submission format | Public GitHub repository URL, following the user's requested upload workflow |
| Code quality | Named constants, clear names/comments, small functions and input validation |
| Testability | Both programs have main() and an if __name__ == '__main__' guard; importing is silent |
| Runnable tests | tests/test_assessment.py; standard-library unittest |
| Actual verification | 83 passing checks: 44 result-card scenarios, 32 electricity scenarios, 3 helper checks, 4 process/import checks |
| Required test coverage | Normal cases, exact/near boundaries, isolated failures, combined failures, malformed input, long digits and Unicode digits |
| Syntax | Both applications and test file compile successfully on Python 3.12.14 |
| Real README samples | Captured from passing executions; test reader echoes the supplied values |
| Banner | assets/banner.svg, 1000×260; title, subtitle, concept chips, highlighted actual code |
| Overview | assets/overview.svg; one card per uploaded task with file, topic, inputs, rules, outputs and concepts |
| Flows | result_card_generator_flow.svg and smart_electricity_bill_flow.svg; validation/retry and processing loops |
| UML | Procedural module diagram showing real constants/functions and calls |
| SVG rules | White canvases, interior banner gradient, system sans-serif text, no external resources; semantic colors |
| SVG verification | XML/marker/text-bound checks, PNG rendering and visual review |
| Exact README order | Banner; overview/table/image; real folder tree; two task sections; UML; concepts; run; real samples; test tables; author footer |
| Per-task README sections | Summary, rules, program flow, method table, input validation, expected results |
| Names and links | All application names, functions and relative asset links match delivered files |
| Complete delivery | Named repository folder and one complete ZIP |
| HTML preview | One offline previews/README-preview.html outside repository; light/dark switch and embedded diagrams |
| Added repository folders | assets/, tests/, .github/workflows/; all disclosed in README |
| Extra root document | REQUIREMENTS.md, this inventory and source-change review |
| Companion files | source/ with unchanged uploads and comparison patches; preview, upload checklist and verification note outside repo |

## Source changes

1. Kept all four required result-card helpers and the five subject names.
2. Added main() entry points and guards to both files; imports no longer print or request input.
3. Replaced repeated marks/rates/thresholds with named constants.
4. Replaced unsafe numeric conversion with decimal-text validation and a length guard. Superscript digit symbols no longer crash mark entry.
5. Added household-count and unit retry loops. A negative unit entry is corrected within the same household instead of being skipped.
6. Counted completed bills explicitly and retained the original progressive if/elif/else calculations inside the for loop.
7. Retained roll-number isdigit() semantics and string storage, including leading zeros. Marks and numeric billing values use isdecimal() before int().

Original Python uploads are unchanged in source/. The patch files show the changes; tests/regression_evidence.json contains actual original/updated runs.

## Assumptions and boundaries

- The two uploaded .py files define this package's scope; the old class-analyzer README section is replaced with the actual electricity task.
- Repository name is taken from the uploaded README. No official brief has confirmed another name.
- GitHub username muhammadadnancss1-ship-it is reused from the user's earlier clone command; it replaces the different account in the supplied README. Author name remains YOUR_NAME.
- Electricity household count must be at least 1; zero units are valid.
- Numeric integer input is limited to 18 decimal digits after stripping leading ASCII zeros. Unicode decimal digits are supported; non-ASCII leading zeros count toward the limit. Marks must also be within 0–100.
- Name validation permits letters and ordinary spaces. strip() removes outer whitespace; title() uses Python's general casing and does not collapse repeated internal spaces.
- Roll values are identifiers, not quantities: Python isdigit() accepts some digit symbols that numeric isdecimal() does not. No integer conversion is performed for a roll.
- calculate_percentage() expects a positive max_total; the application always passes 500. Floating-point percentage output is formatted to two decimals.
- Electricity money is calculated as exact integers using fictional practice rates. No fixed fees, taxes, discounts or saved records were specified.
- Application runtime and tests use only the standard library. CI is configured for Python 3.10/3.12/3.13; local verification used Python 3.12.14. Remote CI has not run here.
- No live repository was created or published. Create the repository and submit its URL using the actual course instructions.
- HTML structure, embedded assets and button logic are checked. Browser visual inspection is unavailable in this environment.

No supplied official brief required an exception; that brief was absent. Missing identity/rubric information and the source mismatch are disclosed rather than guessed.
