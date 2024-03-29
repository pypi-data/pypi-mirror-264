import example_functions as aiq
import csv

def to_csv(output_checks):
    with open('output_checks.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['output', 'outcome']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for check in output_checks:
            writer.writerow(check)

function_list = [
    aiq.get_quant_linguistics_signals(),
    aiq.get_bulk_signals(),
    aiq.get_bulk_signals_yearly(),
    aiq.get_models_spindex(),
    aiq.get_bulk_model(),
    aiq.get_company_identifiers_map(),
    aiq.get_spindex_factors_map(),
    aiq.get_bulk_mapping(),
    aiq.get_compass_questions_map(),
    aiq.get_spinsights_explorer_spindex_summary(),
    aiq.get_spinsights_report_content(),
    aiq.get_spinsights_report_pdf(),
    aiq.get_compass_explorer_question_answer(),
    aiq.get_compass_report_content(),
    aiq.get_compass_report_pdf()
]

output_checks= []
i=0
for function in function_list:
    i+=1
    print(f'Trying function --> {i}')
    if "data" in function:
        outcome = 'Pass'
    elif "errors" in function:
        outcome = 'Fail'
    output_checks.append({'output':function, 'outcome': outcome})

# print(f'Result of tests: {output_checks}')

to_csv(output_checks)