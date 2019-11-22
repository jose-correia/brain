from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from jeec_brain import create_app, db
import os, os.path


app = create_app()
manager = Manager(app)
current_path = os.path.dirname(os.path.realpath(__file__))
migrations_dir = os.path.join(current_path, 'jeec_brain', 'database', 'migrations')
migrate = Migrate(app, db, directory=migrations_dir)


# @manager.command
# def count_files():
#     current_path = os.path.dirname(os.path.realpath(__file__))
#     directory =  os.path.join(current_path, 'app', 'storage')
#     print('Number of files in storage: ' + str(len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])))
#     exit()


# @manager.command
# def dump_ist_ids():
#     current_path = os.path.dirname(os.path.realpath(__file__))
#     directory =  os.path.join(current_path, 'app', 'storage')  

#     output_file = open('submissions_info', 'w+')
        
#     for dirpath, dirnames, filenames in os.walk(directory):
#         for filename in filenames:
#             start = 3
#             end = len(filename) - 4
#             output_file.write(filename[start:end] + '\n')
        
#     output_file.close()
#     print("Info file was created sucessfully!")
#     exit()


@manager.option('-u', '--username', default="admin", help='New user username')
@manager.option('-r', '--role', default="admin", help='Role of access of the user')
def create_user(username, role):
    from jeec_brain.handlers.users_handler import UsersHandler

    user = UsersHandler.create_user(
        username=username,
        role=role
    )

    if user is None:
        print("Failed to create new user!")
        exit()

    UsersHandler.generate_new_user_credentials(user)
    print(f'Username: {user.username}')
    print(f'Role: {user.role.name}')
    print(f'Password: {user.password}')
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
    manager.add_command('runserver', Server('0.0.0.0', port=8081))
    manager.run()