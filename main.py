import csv
import re
from enum import Enum

class ExpenseType(Enum):
    Supermaket = 0
    Cantina = 1
    Benzina = 2
    Bicicleta = 3
    Utilitati = 4
    Gaming = 5
    Sport = 6
    Cultura = 7
    Ingrijire = 8
    Horeca = 9
    Medicamente = 10
    Altele = 11
    Emag = 12

class RowType(Enum):
    Unknown = 0
    Date = 1
    CardNumber = 2
    Terminal = 3
    ActualDate = 4

months = ("ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", "iulie", "august",
          "septembrie", "octombrie", "noiembrie", "decembrie")

# Define the regular expression pattern
pattern = re.compile(r'(\d{2})\s(' + '|'.join(months) + r')\s(\d{4})')

data = [(ExpenseType.Supermaket,[r'LIDL',r'MEGAIMAGE',r'KAUFLAND',r'CARREFOUR', r'MAGNOLIA']),
        (ExpenseType.Horeca,[r'MCD',r'GAMBRINUS', r'Haplea', r'LUADO']),
        (ExpenseType.Cantina,[r'BUSINESS PARK AUTOSERVIRE', r'BUSINESS PARK CAFENEA']),
        (ExpenseType.Benzina,[r'OMV',r'PETROM', r'rompetrol']),
        (ExpenseType.Bicicleta,[r'MPY\*mosionroata']),
        (ExpenseType.Utilitati,[r'ENEL',r'GDF']),
        (ExpenseType.Gaming,[r'STEAM', r'Xsolla']),
        (ExpenseType.Utilitati, [r'DIGI_ROMANIA_SA']),
        (ExpenseType.Sport, [r'DECATHLON']),
        (ExpenseType.Cultura, [r'CARTURESTI']),
        (ExpenseType.Ingrijire, [r'FARMACIA', r'MPY\*saltmed']),
        (ExpenseType.Medicamente, [r'CATENA', r'SENSIBLU', r'SECOM HEALTHCARE', r'dona']),
        (ExpenseType.Emag, [r'PAYU\*EMAG.RO'])
       ]

def parse_comma_float(value):
    # Replace comma with dot
    value = value.replace(',', '.')
    # Convert to float
    return float(value)

total_cost = {}

for entry in data:
    #print(entry[0].name)
    total_cost[entry[0]] = 0.0
    #for terminal in entry[1]:
        #print(terminal)

# Open the CSV file
with open('input.csv', mode='r') as file:
    # Create a CSV reader
    csv_reader = csv.reader(file)
    last_row = RowType.Unknown
    last_entry_cost = 0
    # Iterate over the rows in the CSV file
    for row in csv_reader:
        if last_row == RowType.Date:
            # skip processing card number
            last_row = RowType.CardNumber
        elif last_row == RowType.CardNumber:
            # print("terminal is",row[3].split("Terminal: ")[1])
            found = False
            for entry in data:
                for terminal in entry[1]:
                    if terminal.lower() in row[3].lower():
                        if(found == False):
                            total_cost[entry[0]] += last_entry_cost
                            # print("Adding", last_entry_cost, "to", entry[0].name, "for", row[3].split("Terminal: ")[1])
                            found = True
                        else:
                            print("Error: Multiple terminals found for",row[3].split("Terminal: ")[1])
            if(found == False):
                print(last_entry_cost,"for",row[3].split("Terminal: ")[1],"on",actual_date)
            last_row = RowType.Terminal
        elif last_row == RowType.Terminal:
            # process actual date if required
            actual_date = row[3].split("Data: ")[1].split("Autorizare:")[0]
            last_row = RowType.ActualDate
        elif last_row == RowType.ActualDate or last_row == RowType.Unknown:
            match = pattern.match(row[0])
            if match and row[3] == "Cumparare POS":
                last_row = RowType.Date
                last_entry_cost = parse_comma_float(row[4])
                # print("Cost is ", entry_cost)
            elif match:
                print("Unmanaged entry ", row[3])
            # else:
            #     print("Error",row[3])

# for every entry in total_cost print the total cost
for entry in data:
    print("Total cost for", entry[0].name, "is", total_cost[entry[0]])