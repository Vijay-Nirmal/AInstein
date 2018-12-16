from flask import Flask, jsonify, request, Markup, render_template
import markdown
import ChatBase as cb

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/api", methods=["GET"])
def apiHome():
    with open('API/templates/endpoints.md') as file:
        homeContent = file.read()
    homeContent = Markup(markdown.markdown(homeContent))
    return render_template("generic.html", content=homeContent)

@app.route("/api/textback/", methods=["GET"])
def textBack():
    if "query" in request.args:
        query = request.args['query']
    else:
        return "Error: No query field provided. Please specify a query"
    response = {}
    response['response'] = cb.responceFor(query)

    return jsonify(response)
    

app.run()