# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from composabl_core.agent.scenario.scenario import Scenario
from composabl_core.agent.skill.skill import Skill
from composabl_core.examples.demo_env.agent import scenarios
from composabl_core.examples.demo_env.agent.controller import (
    ControllerExpert,
    ControllerRandom,
)
from composabl_core.examples.demo_env.agent.teacher import (
    Teacher,
    TeacherSpaceBox,
    TeacherSpaceDictionary,
    TeacherSpaceDiscrete,
    TeacherSpaceMultiBinary,
    TeacherSpaceMultiDiscrete,
    TeacherSpaceTuple,
)

expert_skill_controller = Skill("expert-controller", ControllerExpert)
random_skill_controller = Skill("random-controller", ControllerRandom)

target_skill_nested_scenario = Skill("teacher-skill-nested-scenario", Teacher)
target_skill_box = Skill("teacher-skill-box", TeacherSpaceBox)
target_skill_discrete = Skill("teacher-skill-discrete", TeacherSpaceDiscrete)
target_skill_multi_discrete = Skill("teacher-skill-multi-discrete", TeacherSpaceMultiDiscrete)
target_skill_multi_binary = Skill("teacher-skill-multi-binary", TeacherSpaceMultiBinary)
target_skill_dictionary = Skill("teacher-skill-dictionary", TeacherSpaceDictionary)
target_skill_tuple = Skill("teacher-skill-tuple", TeacherSpaceTuple)

target_skills = [
    target_skill_nested_scenario,
    target_skill_box,
    target_skill_discrete,
    target_skill_multi_discrete,
    target_skill_multi_binary,
    target_skill_dictionary,
    target_skill_tuple,
]

for ts in target_skills:
    for scenario_dict in scenarios:
        ts.add_scenario(Scenario(scenario_dict))

target_skill_nested_scenario.add_scenario({
    "test": "test",
    "nested": {
        "test": "test",
        "double_nested": {
            "test": "test"
        }
    }
})

skills_for_space = {
    "box": target_skill_box,
    "discrete": target_skill_discrete,
    "multidiscrete": target_skill_multi_discrete,
    "multibinary": target_skill_multi_binary,
    "dictionary": target_skill_dictionary,
    "tuple": target_skill_tuple
}
