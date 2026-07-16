import types

def url_rules(app_module: types.ModuleType):
    app_module.chat.add_url_rule(
        rule = '/chat',
        view_func = app_module.render_chat,
        methods = ['GET','POST','DELETE']
    )