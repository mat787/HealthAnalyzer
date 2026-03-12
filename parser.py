from lxml import etree as ET
import pandas as pd

# input_file = 'test.xml'  #plik do testow parsera

def parseHeartRate(file):
    file.seek(0)
    global row
    data = []

    print("Rozpoczynam ekstrakcję tętna...")

    context = ET.iterparse(file, events=('end',), tag='Record')  # input_file - plik wejsciowy, events - dla end dochodzimy do konca rekordu, tag - szukamy tylko po wpisanych rekordach

    for event, elem in context:
        # Sprawdzamy kazdy element czy jest taki jak szukamy
        record_type = elem.get('type')


        if record_type == 'HKQuantityTypeIdentifierHeartRate':
            row = {
            'startDate': elem.get('startDate'),
            'endDate': elem.get('endDate'),
            'value': elem.get('value'),
            'unit': elem.get('unit')
        }
            data.append(row)

        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    df = pd.DataFrame(data) #dodajemy do df zeby mozna bylo zapisac do csv
    output_file = 'heart_rate.csv'
    df.to_csv(output_file, index=False)
    print(f"Sukces! Wyekstrahowano {len(df)} rekordów do pliku {output_file}.")

def parseSleep(file):
        file.seek(0)
        global sleep_row
        sleep_data = []

        print("Rozpoczynam ekstrakcję snu")

        context = ET.iterparse(file, events=('end',),tag='Record')  # input_file - plik wejsciowy, events - dla end dochodzimy do konca rekordu, tag - szukamy tylko po wpisanych rekordach

        for event, elem in context:
            # Sprawdzamy kazdy element czy jest taki jak szukamy
            record_type = elem.get('type')

            if record_type == 'HKCategoryTypeIdentifierSleepAnalysis':
                sleep_row = {
                'startDate': elem.get('startDate'),
                'endDate': elem.get('endDate'),
                'value': elem.get('value'), # Tu będą wartości 0, 1, 2, 3 oznaczające fazy
                'source': elem.get('sourceName')
                }
                sleep_data.append(sleep_row)

            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

        df_sleep = pd.DataFrame(sleep_data)  # dodajemy do df zeby mozna bylo zapisac do csv
        output_file = 'sleep.csv'
        df_sleep.to_csv(output_file, index=False)
        print(f"Sukces! Wyekstrahowano {len(df_sleep)} rekordów do pliku {output_file}.")



