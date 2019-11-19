from flask_restful import Resource, reqparse
from models.computer import ComputerModel
from models.user import UserModel
from models.file import FileModel
from models.config import ConfigModel
from flask_restful import Resource


class Hids(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument('uuid',
                        type=str,
                        required=False,
                        help="Every file- needs a guid!"
                        )
    parser.add_argument('computer',
                        type=str,
                        required=False,
                        help="Every file- needs a computer!"
                        )
    parser.add_argument('files',
                        type=list,
                        required=False,
                        location='json',
                        help="Every file- needs a file!"
                        )

    def post(self):
        data = Hids.parser.parse_args()

        # if FileModel.find_by_name(data['name']) and (data['hash']):
        # hier maak ik een log aan voor de analyser

        # return {"message": "A file with that name already exists"}
        print(data)
        # file.save_to_db()
        UserModel(data.uuid).save_to_db()
        ComputerModel(data.computer).save_to_db()
        for file in data["files"]:
            FileModel(file).save_to_db()
            print(file)

        return {"message": "file created successfully"}, 201


class Config(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('uuid',
                        type=str,
                        required=False,
                        help="Every config needs a uuid!"
                        )
    parser.add_argument('computer_name',
                        type=str,
                        required=False,
                        help="Every config needs a computer_name!"
                        )
    parser.add_argument('interval',
                        type=int,
                        required=False,
                        help="Every config needs a interval!"
                        )
    parser.add_argument('path',
                        type=str,
                        required=False,
                        help="Every config needs a path!"
                        )
    parser.add_argument('whitelist',
                        type=str,
                        required=False,
                        location='json',
                        help="Every config needs a whitelist!"
                        )
    parser.add_argument('logger_url',
                        type=str,
                        required=False,
                        help="Every config needs a logger_url!"
                        )

    def get(self, uuid):
        item = ConfigModel.find_by_uuid(uuid)
        if item:
            return item.json()
        return {'message': 'config not found'},404

    def put(self, uuid):
        data = Config.parser.parse_args()
        item = ConfigModel.find_by_uuid(uuid)
        if item is None:
            item = ConfigModel(**data)
        else:
            item.computer_name = data['computer_name']
            item.interval = data['interval']
            item.path = data['path']
            item.whitelist = data['whitelist']
            item.logger_url = data['logger_url']
        item.save_to_db()
        return item.json(), 201


class ComputerList(Resource):
    def get(self):
        return {'stores': [store.json() for store in ComputerModel.query.all()]}


class FileList(Resource):
    def get(self):
        return {'items': [item.json() for item in FileModel.query.all()]}