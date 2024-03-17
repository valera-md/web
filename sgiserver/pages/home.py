print() # /n
file = open("templates/header.html")
header = file.read()
file = open("templates/footer.html")
footer = file.read()
print(header)
print('<h1 style="text-align: center";>Welcome to our MINI SOCIAL !!!</h1>')
print(footer)
#print("<h1>Welcome to our MINI SOCIAL PROJECT!!!</h1>")
