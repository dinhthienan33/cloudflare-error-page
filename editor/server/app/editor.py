# SPDX-License-Identifier: MIT

from os import abort
from flask import (
    Blueprint,
    send_from_directory,
)
from . import static_dir

bp = Blueprint('editor', __name__, url_prefix='/')


@bp.route('/', defaults={'path': 'index.html'})
@bp.route('/<path:path>')
def index(path: str):
    if not static_dir:
        abort(500)
    return send_from_directory(static_dir, path)
