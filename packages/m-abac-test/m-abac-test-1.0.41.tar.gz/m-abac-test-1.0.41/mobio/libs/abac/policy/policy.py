"""
    Policy class
"""
import json
from marshmallow import Schema, fields, post_load, ValidationError, validate, EXCLUDE
from .conditions.schema import ConditionSchema
from .utils import Utils
from .conditions.base import ConditionBase
from .exceptions import *
from copy import deepcopy

class AccessType:
    DENY_ACCESS = "deny"
    ALLOW_ACCESS = "allow"


class Policy(object):
    """
        Policy class containing rules and targets
    """

    def __init__(
            self,
            effect: str,
            # action: list,
            # resource: list,
            condition: list,
            request_access: dict, **kwargs
    ):
        self.effect = effect
        # self.action = action
        # self.resource = resource
        self.condition = deepcopy(condition)
        self.condition_convert = []
        self.request_access = request_access

    def is_allowed(self):
        """
            {
                "operator": "StringEquals",
                "field": "user:staff_code",
                "values": ["A123456"],
                "qualifier": "ForAnyValue",
                "if_exists": false,
                "ignore_case": false,
            }
        :return:
        """
        for item in self.condition:
            cond_schema = self.validate_item_condition(item)
            # print("abac_sdk cond_schema: {}".format(json.dumps(cond_schema)))
            if cond_schema.get("sub_resource"):
                # kiem tra tung phan tu sub resource co thoa man dieu kien ko,
                # neu ko co phan tu nao thoa ma dk thi return false, co 1 phan tu thoa man dk thi chay dk tiep theo
                sub_result = False
                self.condition_convert.append(item)
                data_sub_resource = self.get_sub_resource_value(
                    cond_schema.get("field"), cond_schema.get("sub_resource"))
                if cond_schema.get("operator") == "Null":
                    for item_sub in data_sub_resource:
                        what_check = self.get_sub_resource_value_from_field(cond_schema.get("field"), item_sub)
                        if what_check is None:
                            sub_result = True
                            break
                    if not sub_result:
                        return False
                else:
                    resource_name, resource_key = Utils.split_delemiter_resource(cond_schema.get("field"))
                    if_exists = cond_schema.get("if_exists")
                    for item_sub in data_sub_resource:
                        what_check = self.get_sub_resource_value_from_field(cond_schema.get("field"), item_sub)
                        if if_exists:
                            if not what_check and what_check not in [0, False]:
                                sub_result = True
                                break
                        if cond_schema.get("operator") in ["Exists", "NotExists"]:
                            item.update({
                                "values": item_sub,
                                "what": resource_key,
                            })
                        else:
                            if not what_check and isinstance(what_check, str):
                                what_check = None
                            values = []
                            for v in cond_schema.get("values"):
                                value_from_variable = self.get_value_from_variable(v)
                                if not value_from_variable and isinstance(value_from_variable, str):
                                    value_from_variable = None
                                if isinstance(value_from_variable, list):
                                    values.extend(value_from_variable)
                                else:
                                    values.append(value_from_variable)
                            item.update({
                                "values": values,
                                "what": what_check,
                            })
                        check_schema = ConditionSchema().load(item)
                        if check_schema._is_satisfied():
                            sub_result = True
                            break
                    if not sub_result:
                        return False
            else:
                if cond_schema.get("operator") == "Null":
                    self.condition_convert.append(item)
                    what_check = self.get_value_from_field(cond_schema.get("field"))
                    if what_check is not None:
                        return False
                else:
                    if_exists = cond_schema.get("if_exists")
                    what_check = self.get_value_from_field(cond_schema.get("field"))
                    if if_exists:
                        if not what_check and what_check not in [0, False]:
                            continue
                    if cond_schema.get("operator") in ["Exists", "NotExists"]:
                        resource_name, resource_key = Utils.split_delemiter_resource(cond_schema.get("field"))
                        data_resource = {}
                        if resource_name:
                            if self.request_access.get(resource_name) and isinstance(
                                    self.request_access.get(resource_name), dict):
                                data_resource = self.request_access.get(resource_name)
                        item.update({
                            "values": data_resource,
                            "what": resource_key,
                        })
                    else:
                        if not what_check and isinstance(what_check, str):
                            what_check = None
                        values = []
                        for v in cond_schema.get("values"):
                            value_from_variable = self.get_value_from_variable(v)
                            if not value_from_variable and isinstance(value_from_variable, str):
                                value_from_variable = None
                            if isinstance(value_from_variable, list):
                                values.extend(value_from_variable)
                            else:
                                values.append(value_from_variable)
                        item.update({
                            "values": values,
                            "what": what_check,
                        })
                    self.condition_convert.append(item)
                    check_schema = ConditionSchema().load(item)
                    if not check_schema._is_satisfied():
                        return False
        return True

    @classmethod
    def get_sub_resource_value_from_field(cls, field_key, data_sub_resource):
        resource_name, resource_key = Utils.split_delemiter_resource(field_key)
        if resource_name and resource_key:
            if isinstance(data_sub_resource, dict):
                value = Utils.get_nested_value(data_sub_resource, resource_key)
                return value
        return None

    def get_sub_resource_value(self, field_key, sub_resource):
        resource_name, resource_key = Utils.split_delemiter_resource(field_key)
        if resource_name and resource_key:
            if self.request_access.get(resource_name) and isinstance(self.request_access.get(resource_name), dict):
                if isinstance(self.request_access.get(resource_name).get(sub_resource), list):
                    return self.request_access.get(resource_name).get(sub_resource)
        return []

    def get_condition_convert(self):
        return self.condition_convert

    def get_value_from_variable(self, str_variable):
        if isinstance(str_variable, str) and Utils.check_field_is_variable(str_variable):
            variables = Utils.get_field_key_from_variable(str_variable)
            if variables:
                if len(variables) == 1:
                    field_value = self.get_value_from_field(variables[0])
                    if field_value is None:
                        # raise GetValueNoneException("{} get value is None".format(variables[0]))
                        return field_value
                    if isinstance(field_value, str):
                        field_value_format = Utils.replace_variable_to_value(variables[0], field_value, str_variable)
                        return field_value_format
                    return field_value
                for field_key in variables:
                    field_value = self.get_value_from_field(field_key)
                    if field_value is None:
                        # raise GetValueNoneException("{} get value is None".format(field_key))
                        field_value = ""
                    field_value = str(field_value)
                    str_variable = Utils.replace_variable_to_value(field_key, field_value, str_variable)
        return str_variable

    def get_value_from_field(self, field_key):
        resource_name, resource_key = Utils.split_delemiter_resource(field_key)
        if resource_name and resource_key:
            if self.request_access.get(resource_name) and isinstance(self.request_access.get(resource_name), dict):
                data_resource = self.request_access.get(resource_name)
                value = Utils.get_nested_value(data_resource, resource_key)
                return value
        return None

    def validate_item_condition(self, obj):
        try:
            return ConditionValidateSchema().load(obj)
        except Exception as err:
            raise InvalidConditionException("validate_item_condition: {}".format(err))


class ConditionValidateSchema(Schema):
    operator = fields.String(required=True, allow_none=False)
    field = fields.String(required=True, allow_none=False)
    values = fields.List(fields.Raw(required=True, allow_none=False), required=True, allow_none=False)
    qualifier = fields.String(default=ConditionBase.Qualifier.ForAnyValue,
                              validate=validate.OneOf(ConditionBase.Qualifier.ALL))
    if_exists = fields.Boolean(default=False)
    ignore_case = fields.Boolean(default=False)
    sub_resource = fields.String(default="")

    class Meta:
        unknown = EXCLUDE


class PolicySchema(Schema):
    """
        JSON schema for policy
    """
    effect = fields.String(required=True, validate=validate.OneOf([AccessType.DENY_ACCESS, AccessType.ALLOW_ACCESS]))
    # action = fields.List(fields.String(required=True, allow_none=False),required=True, allow_none=False)
    # resource = fields.List(fields.String(required=True, allow_none=False),required=True, allow_none=False)
    condition = fields.List(fields.Raw(required=True, allow_none=False), required=True, allow_none=False)
    request_access = fields.Dict(default={}, missing={}, allow_none=False)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return Policy(**data)
