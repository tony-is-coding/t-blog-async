# from applications.admin import blueprint as admin_bp
from applications.user import blueprint as user_bp
# from applications.article import blueprint as article_bp
from sanic.blueprint_group import BlueprintGroup

bpg = BlueprintGroup()
bpg.append(user_bp)
# bpg.append(admin_bp)
# bpg.append(article_bp)
