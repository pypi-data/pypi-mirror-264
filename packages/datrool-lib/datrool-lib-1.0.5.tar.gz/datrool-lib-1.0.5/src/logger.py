# -*- coding: utf-8 -*-
from datetime import datetime
from logging import (
	getLogger,
	Formatter,
	StreamHandler,
	INFO
)
from logging.handlers import TimedRotatingFileHandler


def set_logger(name, screen=False, path="", level=INFO, formatter=""):
	logger = getLogger(name)
	formatter = formatter or '%(asctime)s|%(name)s|%(levelname)s: %(message)s'
	if screen:
		sh = StreamHandler()
		sh.setLevel(level)
		sh.setFormatter(Formatter(formatter))
		logger.addHandler(sh)
	if path:
		today = datetime.utcnow().isoformat().split("T")[0]
		fh = TimedRotatingFileHandler(
			"%s/%s-%s.log" % (path[:-1] if path[-1] == "/" else path, name, today),
			when="midnight",
			utc=True
		)
		fh.setLevel(level)
		fh.setFormatter(Formatter(formatter))
		logger.addHandler(fh)
	return logger

