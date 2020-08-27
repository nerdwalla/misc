
import requests
import PyPDF2
import io

pdf_url = 'http://www.scwmls.com/public/millrates/dane/dane_19.pdf'
max_columns = 4

standard_labels_row =  ['Cities', 'Villages', 'Towns']
# CSV file 
out_filename = "Dane_county_property_Taxes_1.csv"
headers = "place,mill_rate,value per 1000 \n"

#HTML file
out_filename_html = "Taxes_in_dane_county_WI_1.html"
htmlStr = "<html>"
htmlStr += "<head><style>table, th, td {   padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse; border: 1px solid black;} th { padding-top: 12px;  padding-bottom: 12px;  text-align: left;  background-color: #4CAF50;  color: white;} tr:nth-child(even){background-color: #f2f2f2;} tr:hover {background-color: #ddd;} tr.muncipality {background-color: #f0a49e; font-size: 25px; font-weight: bold;}</style></head>"
htmlStr += "<body> <table> <tr> <th>Places </th> <th>School District </th> <th> Mill rate per $1000 </th> <th> Accessed to <br/>Market Value Ratio</th> </tr>"

f = open(out_filename, "w")
f.write(headers)

contents_to_avoid = ['Rate', '\n','Assessed to', 'Municipality', 'School District', '(Per $1000)', 'Market Value Ratio', 'DANE COUNTY 2019 TAX RATES', '**Compliments of the South Central Wisconsin MLS Corporation**', 'Sources: Dane County and City of Madison Treasurers and WI Dept of Revenue Website', '1-6-20', ' (continued)', '']
r = requests.get(pdf_url)
pdf_file = io.BytesIO(r.content)

reader = PyPDF2.PdfFileReader(pdf_file)
print('Total Pages',reader.numPages)
i = 0
column_counter = 0


while (i < reader.numPages):
    j= int(i)
    contents = reader.getPage(j).extractText().split('\n')
    i = i+1
    for content in contents:
        if content not in contents_to_avoid:
            if content in standard_labels_row:
                column_counter = 0
                f.write("\n")
                htmlStr += "<tr class='muncipality'><td colspan='4'>"+content+"</td></tr>"
                f.write(content)
                f.write("\n")
                f.write("\n")
                htmlStr += "<tr>"
                column_counter = column_counter + 1;
            else:
                if column_counter % max_columns == 1:
                    htmlStr += "<tr>"
                htmlStr += "<td>"+content+"</td>"
                f.write(content)
                if column_counter % max_columns == 0:
                    column_counter = 0
                    f.write("\n")
                    htmlStr += "</tr>"
                else:
                    f.write(",")
                    
                column_counter = column_counter + 1;  
                   
f.close() 

htmlStr +="</table></body></html>"
html_file = open(out_filename_html, "w")
html_file.write(htmlStr)
html_file.close()
print("Process finished")