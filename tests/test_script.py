
import finanzenpy as ff

import datetime
import pandas as pd
start_date = datetime.datetime(2007, 1, 1)
end_date = datetime.datetime(2020, 6, 21)

# test_id = 'fundamentals'
test_id = 'historic'

#bmw_fundamentals = stocks.get_fundamentals("DE0005190003")

#bmw_historic = ff.stocks.get_historic("DE000A1EWWW0", start_date, end_date)

# bmw_historic = ff.stocks.get_historic("DE0007100000", "17/05/2019", "21/06/2020")
if test_id == 'historic':
    #bmw_historic = ff.commodity.get_historic("Goldpreis", start_date, end_date)
    bmw_historic = ff.stocks.get_historic("DE000A1EWWW0", start_date, end_date)
    print(bmw_historic)



if test_id == 'fundamentals':
    bmw_fundamentals = ff.stocks.get_fundamentals("bmw")
    print(bmw_fundamentals)


    df = []
    for key_global, value_global in bmw_fundamentals.items():
        print(key_global)
        for key, value in value_global.items():
            print(key)
            if key == 'Ergebnis je Aktie (unverwässert, nach Steuern)':
                column_name = 'Basic EPS'
            elif key == 'Ergebnis je Aktie (verwässert, nach Steuern)':
                column_name = 'Diluted EPS'
            elif key == 'Dividende je Aktie':
                column_name = 'div'
            elif key == 'Gesamtdividendenausschüttung in Mio.':
                column_name = 'div_total'
            elif key == 'Umsatz je Aktie':
                column_name = 'revenue per share'
            elif key == 'KGV (Jahresendkurs)':
                column_name = 'PE ratio'
            elif key == 'Dividendenrendite Jahresende in %':
                column_name = 'PE ratio diluted'
            elif key == 'Dividendenrendite Jahresende in %':
                column_name = 'dividend yield'
            elif key == 'Eigenkapitalquote in %':
                column_name = 'equity ratio'
            elif key == 'Fremdkapitalquote in %':
                column_name = 'debt ratio'
            elif key == 'Umsatzerlöse':
                column_name = 'revenues'
            elif key == 'Umsatzveränderung in %':
                column_name = 'change in revenues'
            elif key == 'Bruttoergebnis vom Umsatz':
                column_name = 'gross profit from sales'
            elif key == 'Bruttoergebnisveränderung in %':
                column_name = 'gross profit change'
            elif key == 'Operatives Ergebnis':
                column_name = 'revenues'
            elif key == 'Veränderung Operatives Ergebnis in %	':
                column_name = 'revenues'
            elif key == 'Ergebnis vor Steuern':
                column_name = 'revenues'
            elif key == 'Veränderung Ergebnis vor Steuern in %':
                column_name = 'revenues'
            elif key == 'Ergebnis nach Steuer	':
                column_name = 'revenues'
            elif key == 'Veränderung Ergebnis nach Steuer in %	':
                column_name = 'revenues'




            else:
                column_name = key

            if len(df) == 0:
                df = pd.DataFrame.from_dict(value, orient='index', columns=[column_name])
            else:
                df_temp = pd.DataFrame.from_dict(value, orient='index', columns=[column_name])
                #print(df)
                print(df_temp)
                if column_name in df.columns:
                    print('column already exists --> will be skiped')
                else:
                   df = df.join(df_temp)


    print(df)





# data = bmw_fundamentals['Quotes']
# # for x in data:
# #     print(data[x])
#
# df = []







