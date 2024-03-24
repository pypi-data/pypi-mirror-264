from time import time, sleep
from datetime import datetime, timedelta
from threading import Thread
from uuid import UUID, uuid4
from sched import scheduler
from typing import Callable, Optional
from .validators import DictValidator


class Scheduler:
	__queue: dict = {}
	__weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
	__validator: dict = {
		"weekday": ([str, Optional], lambda x, *a: x in Scheduler.__weekdays),
		"day": ([int, Optional], lambda x, *a: x >= 0 and x < 32),
		"hour": ([int, Optional], lambda x, *a: x >= 0 and x < 24),
		"minute": ([int, Optional], lambda x, *a: x >= 0 and x < 60),
		"second": ([int, Optional], lambda x, *a: x >= 0 and x < 60),
	}
	__running = False
	__thread = None

	def __init__(self):
		self.__sched = scheduler(time, sleep)

	def delay(self, delay, callback: Callable, args=()) -> UUID:
		return self.__create(delay, callback, args)

	def at(self, date: datetime, callback: Callable, args=()) -> UUID:
		delay = (date - datetime.now()) / timedelta(seconds=1)
		if delay <= 0:
			raise ValueError("Time has passed")
		return self.__create(delay, callback, args)

	def every(self, callback: Callable, args=(), **kwargs) -> UUID:
		print(kwargs)
		if template := self.__check(kwargs):
			return self.__create(self.__next(template), callback, args, template)
		print(kwargs)
		raise ValueError("Invalid parameters only [day,weekday,hour,minute,second] possible")

	def clear(self):
		queue_copy = self.__queue.copy()
		# print("q", queue_copy)
		for key in queue_copy:
			self.__sched.cancel(self.__queue.pop(key))
		# map(self.__sched.cancel, self.__sched.queue)
		print(self.__running, self.__thread)

	def cancel(self, event):
		if event := self.__queue.pop(event, None):
			self.__sched.cancel(event)
		else:
			raise ReferenceError("Invalid cancel self")

	def __wrap(self, uuid: UUID, callback: Callable, template: dict):
		def wrap(*args, **kwargs):
			callback(*args, **kwargs)
			self.__queue.pop(uuid)

		def wrap_every(*args, **kwargs):
			# def empty(*args, **kwargs):
			# 	pass

			# if uuid not in self.__queue:
			# 	return empty(*args, **kwargs)
			self.__queue[uuid] = self.__sched.enter(
				self.__next(template), 1, wrap_every, argument=args, kwargs=kwargs
			)
			callback(*args, **kwargs)
		return wrap_every if template else wrap

	def __create(self, delay, callback, args, template=None):
		uuid = uuid4()
		self.__queue[uuid] = None
		wrap = self.__wrap(uuid, callback, template)
		print("create", delay)
		op = self.__sched.enter(delay, 1, wrap, argument=args)
		print("entered", delay, "at", time())
		self.__queue[uuid] = op
		if not self.__running:
			print("t")
			self.__thread = Thread(target=self.__run, args=(True,))
			self.__thread.start()
		return uuid

	def __run(self, *args):
		self.__running = True
		self.__sched.run()
		self.__running = False

	@staticmethod
	def __check(template: dict) -> dict | None:
		if (
			not len(template.keys()) or
			not DictValidator.check(template, Scheduler.__validator, exact_keys=True)
		):
			return None
		if "day" in template and "weekday" in template:
			raise ValueError("Only one of parameters [day,weekday] can be specified at the time")
		template["day"] = template.get("day", None)
		wd = template.get("weekday", None)
		template["weekday"] = Scheduler.__weekdays.index(wd) if isinstance(wd, str) else wd
		template["hour"] = template.get("hour", None)
		template["minute"] = template.get("minute", None)
		template["second"] = template.get("second", 0)
		return template

	@staticmethod
	def __next(template: dict, offset = None):
		now = datetime.now()
		if offset:
			now = now - offset
		month = None
		if "weekday" in template and isinstance(template["weekday"], int):
			da = template["weekday"] - now.weekday()
			if da < 0:
				da += 7
			weekday = now + timedelta(da if da > 0 else da + 7)
			template["day"], month = weekday.day, weekday.month
		run_date = datetime(
			now.year,
			now.month if month is None else month,
			now.day if template["day"] is None else template["day"],
			now.hour if template["hour"] is None else template["hour"],
			now.minute if template["minute"] is None else template["minute"],
			template["second"],
		)
		while run_date <= datetime.now():
			if template["weekday"] is not None:
				run_date += timedelta(days=7)
			elif template["day"] is not None:
				run_date = datetime(
					run_date.year, run_date.month + 1, run_date.day,
					run_date.hour, run_date.minute, run_date.second
				)
			elif template["hour"] is not None:
				run_date += timedelta(days=1)
			elif template["minute"] is not None:
				run_date += timedelta(hours=1)
			else:
				run_date += timedelta(minutes=1)
		return (run_date - datetime.now()).total_seconds()
