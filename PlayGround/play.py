sss= "<html lang=\"en\"><head><meta charset=\"utf-8\"><title>Search</title><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><link href=\"https://fonts.googleapis.com/css?family=Open+Sans\" rel=\"stylesheet\"></head><body class=\"align\"><div class=\"grid\"><form action=\"\" method=\"get\" class=\"search\"><div class=\"form__field\"><input type=\"search\" name=\"search\" placeholder=\"What are you looking for?\" class=\"form__input\"><input type=\"submit\" value=\"Search\" class=\"button\"></div></form></div></body></html>"
from bottle import route, run, template

@route('/]hello')
def index():
    return template('<b>Hello </b>!')

run(host='localhost', port=8080)