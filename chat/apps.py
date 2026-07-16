import flask

chat = flask.Blueprint(
    name= 'chat',
    import_name= 'chat',
    static_folder= 'static',
    static_url_path= '/chat/static',
    template_folder= 'templates'
)