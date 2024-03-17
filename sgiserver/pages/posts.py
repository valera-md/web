print() # /n
file = open("templates/header.html")
header = file.read()
file = open("templates/footer.html")
footer = file.read()
print(header)
print('<h1 style="text-align: center";>MINI SOCIAL / POSTS</h1>')
print(footer)
