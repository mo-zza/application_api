import logging

from src import create_app

# logging.basicConfig(filename='../logs/zolbo.log', level = logging.DEBUG)

app = create_app()
app.run(debug=True, threaded=True, host='0.0.0.0', port=4058)