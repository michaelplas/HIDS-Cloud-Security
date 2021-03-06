from logger.settings import *
from logger.hids import Hids, ComputerList, FileList
from logger.config import Config

# create db with the tables in models
@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()


api.add_resource(Hids, '/hids')
api.add_resource(FileList, '/files')
api.add_resource(ComputerList, '/computers')
api.add_resource(Config, '/config/<string:uuid>')

# Run Server
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=4000, debug=True)
