import os
import json

class SimpleConfig:
    def __init__(self, appname):
        self.working_directory = os.path.join(os.getenv('APPDATA'), appname)
        if not os.path.isdir(self.working_directory): os.mkdir(self.working_directory)

        self.filepath = os.path.join(self.working_directory, 'cfg.json')
        if not os.path.isfile(self.filepath):
            with open(self.filepath, 'w+') as f:
                f.write('{}')

        with open(self.filepath, 'r+') as f:
            try: self.cfg = json.load(f)
            except Exception as error:
                print(error)
                print('malformed json, clearing file')
                self.clear()

    def __repr__(self):
        return str(self.cfg)

    def __getitem__(self, index):
        return self.cfg.get(index, None)

    def save(self):
        with open(self.filepath, 'w+') as file: json.dump(self.cfg, file, sort_keys=True, indent=4)

    def clear(self):
        self.cfg = {}