#!/usr/bin/env python

import sys
sys.path.append("./")

from application import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
