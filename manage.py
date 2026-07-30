import Project

def main():
    try:
        Project.execute()
        Project.socket_app.run(app = Project.project, debug = True, port= 8000)
    except Exception as error:
        print(error)

if __name__ == "__main__":
    main()