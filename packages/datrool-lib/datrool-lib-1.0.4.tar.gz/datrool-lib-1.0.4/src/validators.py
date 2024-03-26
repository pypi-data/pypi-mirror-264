# -*- coding: utf-8 -*-
from typing import Optional


class DictValidator:
	@staticmethod
	def check(structure: dict, validator: dict, exact_keys: bool = False) -> bool:
		if DictValidator._not_exact_keys(exact_keys, structure, validator):
			return False
		for key in validator:
			if key not in structure:
				if type(validator[key][0]) in (list, tuple) and Optional in validator[key][0]:
					continue
				else:
					return False
			value = structure[key]
			if DictValidator._not_match_primitive(value, key, validator):
				return False
			if isinstance(validator[key][1], dict):
				if DictValidator._not_match_complex(value, key, validator, exact_keys):
					return False
			elif (
				isinstance(validator[key][1], type) and
				(
					validator[key][0] in (list, tuple) or (type(validator[key][0]) in (list, tuple) and
					(list in validator[key][0] or tuple in validator[key][0]))
				)
			):
				for item in value:
					if not isinstance(item, validator[key][1]):
						return False
			elif not DictValidator._condition(validator[key][1], value, structure):
				return False
		return True

	@staticmethod
	def _not_exact_keys(exact_keys, structure, validator) -> bool:
		if exact_keys:
			for key in structure:
				if key not in validator.keys():
					return True
		return False

	@staticmethod
	def _not_match_primitive(value, key, validator) -> bool:
		if type(validator[key][0]) in (list, tuple) and Optional in validator[key][0]:
			if not DictValidator._type(validator[key][0][0], value) and value is not None:
				return True
		elif type(validator[key][0]) in (list, tuple):
			found = False
			for t in validator[key][0]:
				if DictValidator._type(t, value):
					found = True
					break
			if not found:
				return True
		elif not DictValidator._type(validator[key][0], value):
			return True
		return False

	@staticmethod
	def _not_match_complex(value, key, validator, exact_keys):
		optional = False
		complex = dict
		if type(validator[key][0]) in (list, tuple):
			if Optional in validator[key][0]:
				optional = True
			if list in validator[key][0] or tuple in validator[key][0]:
				complex = list
		else:
			complex = validator[key][0]
		if complex == list:
			if optional and value is None:
				return False
			for item in value:
				if optional and item is None:
					continue
				if (
					not isinstance(item, dict) or
					not DictValidator.check(item, validator[key][1], exact_keys=exact_keys)
				):
					return True
		elif optional and value is None:
			return False
		elif (
			not isinstance(value, dict) or
			not DictValidator.check(value, validator[key][1], exact_keys=exact_keys)
		):
			return True
		return False

	@staticmethod
	def _type(validator, value) -> bool:
		if type(validator) in (list, tuple):
			if type(value) not in validator:
				return False
		elif not isinstance(value, validator):
			return False
		return True

	@staticmethod
	def _condition(validator, value, structure: dict):
		if callable(validator) and not bool(validator(value, structure)):
			return False
		return True


class ListOfDictValidator:
	@staticmethod
	def check(structure: list, validator: dict, exact_keys: bool = False):
		for item in structure:
			if not DictValidator.check(item, validator, exact_keys):
				return False
		return True
