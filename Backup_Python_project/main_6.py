import pandas as pd
from datetime import datetime
import numpy


pd.options.display.float_format = '{:,.2f}'.format  # excellent - comma, expo to int format and all at once

Excel_path = "purchase_registers_raw.xlsx"
font_name = "Cambria"
font_size = "11"
full_border = True


def generate_purchase_type_wise(path):
    excel_file = path

    # read Excel file using pandas
    excel_file_pd = pd.read_excel(excel_file, sheet_name="Sheet1")

    # create pivot table
    purchase_type_wise_pd = pd.pivot_table(excel_file_pd, index=["Valuation Class", "Valuation Class Text"], values="GR Amt.in loc.cur.", aggfunc=numpy.sum, margins=True, margins_name="Grand Total", sort=True)
    print(purchase_type_wise_pd)  # - Pivot check -Success

    # reset "indices created during pivot table creation" - for merging
    purchase_type_wise_pd = purchase_type_wise_pd.reset_index()
    print(purchase_type_wise_pd)  # need to test this line - and adding index 0 1 2 3 etc

    # read previous quarters final working file
    previous_quarter_final_file = "Previous_Quarter_Final_File.xlsx"
    previous_quarter_final_file_pd = pd.read_excel(previous_quarter_final_file, sheet_name="Purchase Type Wise Comparatives", usecols="A,B,D")
    print(previous_quarter_final_file_pd)  # Success - prints with Nan

    # replace Nan with blank
    previous_quarter_final_file_pd = previous_quarter_final_file_pd.replace(numpy.nan, '', regex=True)
    print(previous_quarter_final_file_pd)   # Success - replaces Nan with blank ''

    # merging present and previous quarter purchase type wise data
    purchase_type_wise_comparatives_pd = pd.merge(purchase_type_wise_pd, previous_quarter_final_file_pd, how="outer", on=["Valuation Class", "Valuation Class Text"])
    print(previous_quarter_final_file_pd)

    # replacing all Nan's with zeros in Present and previous Quarter's values columns
    purchase_type_wise_comparatives_pd = purchase_type_wise_comparatives_pd.replace(numpy.nan, 0, regex=True)
    print(previous_quarter_final_file_pd)

    # create a new column - Success
    purchase_type_wise_comparatives_pd['variance'] = 0
    # print(purchase_type_wise_comparatives_pd)  # variance column with 0's

    # To Remove SettingWithCopyWarning error
    pd.options.mode.chained_assignment = None

    # variance formula implementation using index
    for index in purchase_type_wise_comparatives_pd.index:
        present_quarter = purchase_type_wise_comparatives_pd['GR Amt.in loc.cur.'][index]
        previous_quarter = purchase_type_wise_comparatives_pd['Q3 FY 21-22'][index]
        variance = (present_quarter - previous_quarter) / previous_quarter
        variance = format(variance, '.2%')
        purchase_type_wise_comparatives_pd['variance'][index] = variance

    print(purchase_type_wise_comparatives_pd)

    # ignoring index numbers and save to output excel
    purchase_type_wise_comparatives_pd.to_excel('Purchase_Output.xlsx', sheet_name="Purchase Type Wise Comparatives", index=False)
    print("Purchase type Wise Comparatives is created in Purchase_Output.xlsx")


def generate_plant_type_wise(path):
    excel_file = path
    excel_file_pd = pd.read_excel(excel_file, sheet_name="Sheet1")

    # create pivot table
    plant_type_wise_pd = pd.pivot_table(excel_file_pd, index=["Plant"], values="GR Amt.in loc.cur.", aggfunc=numpy.sum, margins=True, margins_name="Grand Total", sort=True)
    print(plant_type_wise_pd)  # - Pivot check -Success

    # reset index created after pivot table creation for merging
    plant_type_wise_pd = plant_type_wise_pd.reset_index()
    print(plant_type_wise_pd)  # need to test this line - and adding index 0 1 2 3 etc

    # read previous quarters final working file
    previous_quarter_final_file = "Previous_Quarter_Final_File.xlsx"
    previous_quarter_final_file_pd = pd.read_excel(previous_quarter_final_file, sheet_name="Plant Wise Comparatives", usecols="A,C")
    print(previous_quarter_final_file_pd)

    # merging present and previous quarter purchase type wise data
    plant_type_wise_comparatives_pd = pd.merge(plant_type_wise_pd, previous_quarter_final_file_pd, how="outer", on=["Plant"])
    print(plant_type_wise_comparatives_pd)

    # replacing all Nan's with zeros in Present and previous values columns - not necessary but if a new plant is added
    # Nan's will be formed in previous quarter columns, eliminates NaN error
    plant_type_wise_comparatives_pd = plant_type_wise_comparatives_pd.replace(numpy.nan, 0, regex=True)

    # create a new column - Success
    plant_type_wise_comparatives_pd['variance'] = 0
    #  print(plant_type_wise_comparatives_pd)  # variance column with 0's

    # To Remove SettingWithCopyWarning error
    pd.options.mode.chained_assignment = None

    # variance formula implementation using index
    for index in plant_type_wise_comparatives_pd.index:
        present_quarter = plant_type_wise_comparatives_pd['GR Amt.in loc.cur.'][index]
        previous_quarter = plant_type_wise_comparatives_pd['Q3 FY 21-22'][index]
        variance = (present_quarter - previous_quarter) / previous_quarter
        variance = format(variance, '.2%')
        plant_type_wise_comparatives_pd['variance'][index] = variance

    print(plant_type_wise_comparatives_pd)

    # ignoring index numbers and save to output excel
    plant_type_wise_comparatives_pd.to_excel('Plant_Output.xlsx', sheet_name="Plant Wise Comparatives", index=False)
    print("Plant Type Wise Comparatives is created in Plant_Output.xlsx")


def generate_month_wise(path):
    excel_file = path
    excel_file_pd = pd.read_excel(excel_file, sheet_name="Sheet1")

    #  Create Month column
    excel_file_pd['Month'] = pd.DatetimeIndex(excel_file_pd['GR Posting Date']).month_name().str[:3]

    #  selecting only required columns
    excel_file_pd = excel_file_pd[["GR Posting Date", "GR Amt.in loc.cur.", "Month"]]
    print(excel_file_pd)

    # create pivot table, sort = False to not sort Month as per alphabetical order
    month_wise_pd = pd.pivot_table(excel_file_pd, index=["Month"], values="GR Amt.in loc.cur.", aggfunc=numpy.sum, margins=True, margins_name="Grand Total", sort=False)
    print(month_wise_pd)  # - Pivot check -Success

    # reset month index after pivot table creation for concatenation
    month_wise_pd = month_wise_pd.reset_index()
    print(month_wise_pd)  # success - and adding index 0 1 2 3 etc

    # read from previous quarters final working file
    previous_quarter_final_file = "Previous_Quarter_Final_File.xlsx"
    previous_quarter_final_file_pd = pd.read_excel(previous_quarter_final_file, sheet_name="Month Wise Comparatives", usecols="C,D")
    print(previous_quarter_final_file_pd)

    # concatenation instead of merge as there are no common Columns to merge.
    month_wise_comparatives_pd = pd.concat([month_wise_pd, previous_quarter_final_file_pd], axis=1)
    print(month_wise_comparatives_pd)

    # create a new column - Success
    month_wise_comparatives_pd['variance'] = 0
    print(month_wise_comparatives_pd)  # variance column with 0's

    # To Remove SettingWithCopyWarning error
    pd.options.mode.chained_assignment = None

    # variance formula implementation using index
    for index in month_wise_comparatives_pd.index:
        present_quarter = month_wise_comparatives_pd['GR Amt.in loc.cur.'][index]
        previous_quarter = month_wise_comparatives_pd['Q3 FY 21-22'][index]
        variance = (present_quarter - previous_quarter) / previous_quarter
        variance = format(variance, '.2%')
        month_wise_comparatives_pd['variance'][index] = variance

    print(month_wise_comparatives_pd)

    # ignoring index numbers and save to output excel
    month_wise_comparatives_pd.to_excel('Month_Output.xlsx', sheet_name="Month Wise Comparatives", index=False)
    print("Month Wise Comparatives is created in Month_Output.xlsx")


def generate_domestic_and_import_wise(path):
    excel_file = path

    # read Excel file using pandas
    excel_file_pd = pd.read_excel(excel_file, sheet_name="Sheet1")

    # create a new column 'Purchase Type'
    excel_file_pd['Purchase Type'] = ''

    # Setting Type of purchase column values using currency key column on condition
    excel_file_pd.loc[excel_file_pd['Currency Key'] == "INR", 'Purchase Type'] = "Domestic"
    excel_file_pd.loc[excel_file_pd['Currency Key'] != "INR", 'Purchase Type'] = "Import"

    #  selecting only required columns
    excel_file_pd = excel_file_pd[['Purchase Type', 'GR Amt.in loc.cur.']]
    print(excel_file_pd)

    # create pivot table - sorting not required
    domestic_and_import_wise_pd = pd.pivot_table(excel_file_pd, index=["Purchase Type"], values="GR Amt.in loc.cur.", aggfunc=numpy.sum, margins=True, margins_name="Grand Total")
    print(domestic_and_import_wise_pd)  # - Pivot check -Success

    # reset month index after pivot table creation for concatenation
    domestic_and_import_wise_pd = domestic_and_import_wise_pd.reset_index()
    print(domestic_and_import_wise_pd)  # success - and adding index 0 1 2 3 etc

    # read previous quarters final working file
    previous_quarter_final_file = "Previous_Quarter_Final_File.xlsx"
    previous_quarter_final_file_pd = pd.read_excel(previous_quarter_final_file, sheet_name="Dom&Imp Wise Comparatives", usecols="A,C")
    print(previous_quarter_final_file_pd)  # Success

    # merging present and previous quarter purchase type wise data
    domestic_and_import_wise_comparatives_pd = pd.merge(domestic_and_import_wise_pd, previous_quarter_final_file_pd, how="outer", on=["Purchase Type"])
    print(domestic_and_import_wise_comparatives_pd)

    # create a new column - Success
    domestic_and_import_wise_comparatives_pd['variance'] = 0
    print(domestic_and_import_wise_comparatives_pd)  # variance column with 0's

    # To Remove SettingWithCopyWarning error
    pd.options.mode.chained_assignment = None

    # variance formula implementation using index
    for index in domestic_and_import_wise_comparatives_pd.index:
        present_quarter = domestic_and_import_wise_comparatives_pd['GR Amt.in loc.cur.'][index]
        previous_quarter = domestic_and_import_wise_comparatives_pd['Q3 FY 21-22'][index]
        variance = (present_quarter - previous_quarter) / previous_quarter
        variance = format(variance, '.2%')
        domestic_and_import_wise_comparatives_pd['variance'][index] = variance

    print(domestic_and_import_wise_comparatives_pd)

    # ignoring index numbers and save to output excel
    domestic_and_import_wise_comparatives_pd.to_excel('domestic_and_import_wise_Output.xlsx', sheet_name="Purchase Type Wise Comparatives", index=False)
    print("domestic and import Wise Comparatives is created in domestic_and_import_wise_Output.xlsx")


def main():
    print("starting purchase type wise at " + datetime.now().strftime("%H:%M:%S"))
    generate_purchase_type_wise(Excel_path)
    print("Completed purchase type wise at " + datetime.now().strftime("%H:%M:%S"))

    print("starting month wise at " + datetime.now().strftime("%H:%M:%S"))
    generate_month_wise(Excel_path)
    print("Completed month wise at " + datetime.now().strftime("%H:%M:%S"))

    print("starting plant type wise at " + datetime.now().strftime("%H:%M:%S"))
    generate_plant_type_wise(Excel_path)
    print("Completed plant type wise at " + datetime.now().strftime("%H:%M:%S"))

    print("starting Domestic and import type wise at " + datetime.now().strftime("%H:%M:%S"))
    generate_domestic_and_import_wise(Excel_path)
    print("Completed Domestic and import type wise at " + datetime.now().strftime("%H:%M:%S"))


main()
