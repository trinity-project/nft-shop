from .. import app
from flask import request,jsonify,render_template
from ..utils import make_api_response,wrap_template_name

@app.errorhandler(404)
def resource_not_found(e):
    if request.path.startswith('/api'):
        data = make_api_response(
            code=0,
            status=404,
            message=e.description
        )
        return jsonify(data[0]), data[1]
    return render_template(wrap_template_name('error/404.html')), 404

# @app.errorhandler(405)
# def method_not_allowed(e):
#     return render_template('405.html'), 405

@app.route('/unauthorized')
def unauthorized():
    return render_template(wrap_template_name('error/unauthorized.html')), 403
