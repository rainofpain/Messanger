import types

def user_url_rules(app_module: types.ModuleType):
    app_module.user.add_url_rule(
        rule = '/registration',
        view_func = app_module.render_registration,
        methods = ['GET','POST']
        
    )

    app_module.user.add_url_rule(
        rule = "/authorization",
        view_func = app_module.render_authorization,
        methods = ['GET','POST']
    )

    app_module.user.add_url_rule(
        rule = "/redirect_to_email",
        view_func = app_module.render_redirect_to_email,
        methods = ['GET','POST']
    )

    app_module.user.add_url_rule(
        rule = "/logout",
        view_func = app_module.logout
    )

    app_module.user.add_url_rule('/confirm/<token>', view_func= app_module.confirm_email , methods=['GET'])