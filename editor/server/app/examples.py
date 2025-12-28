# SPDX-License-Identifier: MIT

import copy
import os
from pathlib import Path
import re

from flask import (
    Blueprint,
    json,
    abort,
    redirect,
)

from cloudflare_error_page import ErrorPageParams
from .utils import (
    render_extended_template,
)


bp = Blueprint('examples', __name__, url_prefix='/')
examples_dir = Path(__file__).parent / 'data' / 'examples'
param_cache: dict[str, dict] = {}

if not os.path.exists(examples_dir):
    print('"example" directory does not exist. Run "hatch build" to generate.')
    exit(1)


def get_page_params(name: str) -> ErrorPageParams:
    name = re.sub(r'[^\w]', '', name)
    params = param_cache.get(name)
    if params is not None:
        return copy.deepcopy(params)
    try:
        with open(os.path.join(examples_dir, f'{name}.json')) as f:
            params = json.load(f)
        param_cache[name] = params
        return copy.deepcopy(params)
    except Exception as _:
        return None


@bp.route('/')
@bp.route('/<path:name>')
def index(name: str = ''):
    lower_name = name.lower()
    if lower_name == '':
        return redirect('default', code=301)
    elif name != lower_name:
        return redirect(lower_name, code=301)
    else:
        name = lower_name

    params = get_page_params(name)
    if params is None:
        abort(404)

    # Render the error page
    return render_extended_template(params=params)
