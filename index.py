from mcstatus import JavaServer
from flask import Flask, render_template, make_response, request
import json

app = Flask("<3")

widget_templates = json.loads(open('templates.json').read())
default_widget_template = "widget"

###FUNCTIONS
###FUNCTIONS
###FUNCTIONS
def get_template(name : str):
    if name == None:
        return f"{default_widget_template}.html"
    
    if name in widget_templates:
        return f"{name}.html"
    else:
        return f"{default_widget_template}.html"

def ping(requrl):
    try:
        javaserver = JavaServer.lookup(requrl)
        return javaserver.status()
    except:
        return None

def pingresilient(requrl):
    i = 0
    while True:
        result = ping(requrl)
        if result != None:
            break
        i = i + 1
        if i > 5:
            break
    if result == None:
        raise ValueError("Server didn't respond")

    return result

def removebreak(str : str):
    result = str.replace("<p>", "<span>")
    result = result.replace("</p>", "</span>")

    result = str.replace("<p>", "")
    result = result.replace("</p>", "")
    return result

###WIDGET ROUTE
@app.route("/widget/<requrl>")
def widget(requrl):
    result = pingresilient(requrl)

    motdhtml = removebreak(result.motd.to_html())

    template = get_template(str(request.args.get('widget')))
    print(template)
    template = render_template(
        str(template), 
        img=result.icon, 
        url=requrl, 
        motd=motdhtml, 
        latency=result.latency,
        playercount=result.players.online,
        maxplayers=result.players.max
    )

    headers = {'Content-Type': 'text/html'}
    return make_response(template, 200, headers)

@app.route("/rawping/<requrl>")
def rawpingendpoint(requrl):
    return str(pingresilient(requrl))



##USERFACING

@app.route("/generate", methods=['GET', 'POST'])
def generateroute():
    prevpage = None

    prevpagereq = request.args.get('prevpage')
    if prevpagereq != None:
        prevpage = prevpagereq

    result = ""
    if request.method == 'POST':
        form = request.form

        result = render_template(
            'iframetemplate.html',
            widgeturl=form['url']
        )
    
    return render_template(
        'generateroute.html',
        iframe=result,
        prevpage=prevpage
    )


@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/example")
def example():
    return render_template("example.html")

@app.route("/examplewidget")
def examplewidget():
    return render_template(
        "examplewidget.html"
    )


app.run(port=8081, host="0.0.0.0", debug=False)