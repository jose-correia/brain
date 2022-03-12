from flask_script import Manager, Server, Option
from flask_migrate import Migrate, MigrateCommand
from jeec_brain import create_app, db
import os, os.path

# import eventlet
# eventlet.monkey_patch()

app = create_app()
manager = Manager(app)
current_path = os.path.dirname(os.path.realpath(__file__))
migrations_dir = os.path.join(current_path, "jeec_brain", "database", "migrations")
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


@manager.option("-n", "--name", default="admin", help="New user name")
@manager.option("-u", "--username", default="admin", help="New user username")
@manager.option("-r", "--role", default="admin", help="Role of access of the user")
def create_user(name, username, role):
    from jeec_brain.handlers.users_handler import UsersHandler

    user = UsersHandler.create_user(name=name, username=username, role=role)

    if user is None:
        print("Failed to create new user!")
        exit()

    UsersHandler.generate_new_user_credentials(user)
    print(f"Name: {user.name}")
    print(f"Username: {user.username}")
    print(f"Role: {user.role.name}")
    print(f"Password: {user.password}")
    exit()


@manager.shell
def shell_context():
    import pprint
    import flask

    context = dict(pprint=pprint.pprint)
    context.update(vars(flask))
    context.update(vars(app))

    return context


# class _Server(Server):
#     help = description = 'Runs the Socket.IO web server'

#     def get_options(self):
#         options = (
#             Option('-h', '--host',
#                    dest='host',
#                    default=self.host),

#             Option('-p', '--port',
#                    dest='port',
#                    type=int,
#                    default=self.port),

#             Option('-d', '--debug',
#                    action='store_true',
#                    dest='use_debugger',
#                    help=('enable the Werkzeug debugger (DO NOT use in '
#                          'production code)'),
#                    default=self.use_debugger),
#             Option('-D', '--no-debug',
#                    action='store_false',
#                    dest='use_debugger',
#                    help='disable the Werkzeug debugger',
#                    default=self.use_debugger),

#             Option('-r', '--reload',
#                    action='store_true',
#                    dest='use_reloader',
#                    help=('monitor Python files for changes (not 100%% safe '
#                          'for production use)'),
#                    default=self.use_reloader),
#             Option('-R', '--no-reload',
#                    action='store_false',
#                    dest='use_reloader',
#                    help='do not monitor Python files for changes',
#                    default=self.use_reloader),
#         )
#         return options

#     def __call__(self, app, host, port, use_debugger, use_reloader):
#         # override the default runserver command to start a Socket.IO server
#         if use_debugger is None:
#             use_debugger = app.debug
#             if use_debugger is None:
#                 use_debugger = True
#         if use_reloader is None:
#             use_reloader = app.debug
#         socketIO.run(app,
#                      host=host,
#                      port=port,
#                      debug=use_debugger,
#                      use_reloader=use_reloader,
#                      **self.server_options)

if __name__ == "__main__":
    manager.add_command("db", MigrateCommand)
    manager.add_command("runserver", Server(host="127.0.0.1", port=8081))
    # manager.add_command("runserver", _Server(host='0.0.0.0', port=8081))
    manager.run()
