from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from jeec_brain import create_app, db
import os, os.path


app = create_app()
manager = Manager(app)
current_path = os.path.dirname(os.path.realpath(__file__))
migrations_dir = os.path.join(current_path, 'app', 'database', 'migrations')
migrate = Migrate(app, db, directory=migrations_dir)


@manager.command
def count_files():
    current_path = os.path.dirname(os.path.realpath(__file__))
    directory =  os.path.join(current_path, 'app', 'storage')
    print('Number of files in storage: ' + str(len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])))
    exit()


@manager.command
def dump_istids():
    current_path = os.path.dirname(os.path.realpath(__file__))
    directory =  os.path.join(current_path, 'app', 'storage')  

    output_file = open('submissions_info', 'w+')
        
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            start = 3
            end = len(filename) - 4
            output_file.write(filename[start:end] + '\n')
        
    output_file.close()
    print("Info file was created sucessfully!")
    exit()


@manager.shell
def shell_context():
    import pprint
    import flask

    context = dict(pprint=pprint.pprint)
    context.update(vars(flask))
    context.update(vars(app))

    return context


if __name__ == '__main__':
    manager.add_command('db', MigrateCommand)
    manager.add_command('runserver', Server('127.0.0.1', port=8000))
    manager.run()