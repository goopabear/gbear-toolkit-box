from src import ProjectWorkspace

app = ProjectWorkspace('gbear-toolkit')

folder_path = app.user_select('folder')
app.write_csv(folder_path, prefix = 'file')