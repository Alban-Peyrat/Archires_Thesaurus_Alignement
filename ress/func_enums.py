# -*- coding: utf-8 -*- 

# Etxernal import
from typing import List

# Internal import
from ress.enums import Step

def step_for_output(step:Step, steps:List[Step]=[]) -> str:
    """Returns the step as a string for the output"""
    if steps != []:
        return f"[N°{steps.index(step)+1} - ID {step.value}] {step.name}"
    return f"[{step.value}] {step.name}"

