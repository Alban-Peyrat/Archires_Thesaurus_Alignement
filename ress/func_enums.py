# -*- coding: utf-8 -*- 

# Etxernal import

# Internal import
from ress.enums import Step

def step_for_output(step:Step) -> str:
    """RReturns the step as a string for the output"""
    return f"[{step.value}] {step.name}"

