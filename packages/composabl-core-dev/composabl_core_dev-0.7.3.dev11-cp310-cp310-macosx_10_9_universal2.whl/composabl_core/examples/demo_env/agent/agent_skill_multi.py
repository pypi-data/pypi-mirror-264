# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from composabl_core.agent.agent import Agent
from composabl_core.examples.demo_env.agent import (
    expert_skill_controller,
    random_skill_controller,
    sensors_box,
    sensors_dictionary,
    sensors_discrete,
    sensors_multi_binary,
    sensors_multi_discrete,
    sensors_tuple,
    target_skill_box,
    target_skill_dictionary,
    target_skill_discrete,
    target_skill_multi_binary,
    target_skill_multi_discrete,
    target_skill_tuple,
)

agent_dictionary = Agent()
agent_dictionary.add_sensors(sensors_dictionary)
agent_dictionary.add_skill(expert_skill_controller)
agent_dictionary.add_skill(random_skill_controller)
agent_dictionary.add_selector_skill(
    target_skill_dictionary,
    [expert_skill_controller, random_skill_controller],
    fixed_order=True,
    fixed_order_repeat=False
)

agent_box = Agent()
agent_box.add_sensors(sensors_box)
agent_box.add_skill(expert_skill_controller)
agent_box.add_skill(random_skill_controller)
agent_box.add_selector_skill(
    target_skill_box,
    [expert_skill_controller, random_skill_controller],
    fixed_order=True,
    fixed_order_repeat=False
)

agent_discrete = Agent()
agent_discrete.add_sensors(sensors_discrete)
agent_discrete.add_skill(expert_skill_controller)
agent_discrete.add_skill(random_skill_controller)
agent_discrete.add_selector_skill(
    target_skill_discrete,
    [expert_skill_controller, random_skill_controller],
    fixed_order=True,
    fixed_order_repeat=False
)

agent_multidiscrete = Agent()
agent_multidiscrete.add_sensors(sensors_multi_discrete)
agent_multidiscrete.add_skill(expert_skill_controller)
agent_multidiscrete.add_skill(random_skill_controller)
agent_multidiscrete.add_selector_skill(
    target_skill_multi_discrete,
    [expert_skill_controller, random_skill_controller],
    fixed_order=True,
    fixed_order_repeat=False
)

agent_multibinary = Agent()
agent_multibinary.add_sensors(sensors_multi_binary)
agent_multibinary.add_skill(expert_skill_controller)
agent_multibinary.add_skill(random_skill_controller)
agent_multibinary.add_selector_skill(
    target_skill_multi_binary,
    [expert_skill_controller, random_skill_controller],
    fixed_order=True,
    fixed_order_repeat=False
)

agent_tuple = Agent()
agent_tuple.add_sensors(sensors_tuple)
agent_tuple.add_skill(expert_skill_controller)
agent_tuple.add_skill(random_skill_controller)
agent_tuple.add_selector_skill(
    target_skill_tuple,
    [expert_skill_controller, random_skill_controller],
    fixed_order=True,
    fixed_order_repeat=False
)

agent = agent_dictionary

agents_for_space = {
    "box": agent_box,
    "dictionary": agent_dictionary,
    "discrete": agent_discrete,
    "multidiscrete": agent_multidiscrete,
    "multibinary": agent_multibinary,
    "tuple": agent_tuple
}
