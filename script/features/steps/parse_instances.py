# import json
# from lettuce import step, world
#
# @step('a json with required data """(.*)"""')
# def step_impl(step_instance, data):
# 	world.data = json.loads(data)
#
#
# @step("the list of instances is addr1, addr2")
# def step_impl(step_instance):
# 	pass