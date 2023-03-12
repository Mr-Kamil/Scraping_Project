
import pandas as pd
import openpyxl

student = [{"Name": "Vishvajit Rao", "age": 23, "Occupation": "Developer","Skills": "Python"},
{"Name": "John", "age": 33, "Occupation": "Front End Developer","Skills": "Angular"},
{"Name": "Harshita", "age": 21, "Occupation": "Tester","Skills": "Selenium"},
{"Name": "Mohak", "age": 30, "Occupation": "Full Stack","Skills": "Python, React and MySQL"}]

# convert into dataframe
df = pd.DataFrame(data=student)

#convert into excel
df.to_excel("students.xlsx", index=False)
print("Dictionary converted into excel...")



# def write_data(data_file_path, duplicates_data_list, fieldnames):
#     data_list = duplicates_data_list
#     output_list = []
#     exists = False
#
#     if os.path.exists(data_file_path):
#         reader_list = csv_to_dict_list(data_file_path)
#         exists = True
#
#     with open(data_file_path, 'a', newline='', encoding='utf-8') as data_file_csv_write:
#         writer = csv.DictWriter(data_file_csv_write, fieldnames=fieldnames, lineterminator='\n')
#
#         if not exists:
#             writer.writeheader()
#         writer.writerow({'DATA': today})
#
#         for data_list_row in data_list:
#             if exists:
#                 if data_list_row['LINK'] not in reader_list:
#                     output_list.append(data_list_row)
#             else:
#                 output_list.append(data_list_row)
#
#         for output_list_row in output_list:
#             writer.writerow(output_list_row)