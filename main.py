
# Input
# class CommandLineTool(InputRequest, RequestUserCredentials):
#     def main(self):
#         user = self.read_user()

# Arguments
# class CommandLineTool(SimpleArgumentsRequest, RequestUserCredentials):
#     def main(self):
#         user = self.read_user()


class UserDatabaseMixin(object):
    pass


class CommandLineTool(SimpleArgumentsRequest, RequestUserCredentials):
    def main(self):
        user = self.read_user()
#

cmd = CommandLineTool()
cmd.main()
print(cmd.username)
