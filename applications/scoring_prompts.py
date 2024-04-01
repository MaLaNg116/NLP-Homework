


TEXT_EVAL_METRICS = {
    "Fluency": """ Fluency: The fluency of the '{{TGT}}'. """,
    "Relevance": """ Relevance: The semantic consistency and relevance between '{{SRC}}' and '{{TGT}}'. """,
    "Informativeness": """ Informativeness: Does '{{TGT}}' contain sufficient and rational information.""",
}

TEXT_EVAL_GENERAL_PROMPT_PATTERN = """
[Task Description] 
Here is a point-wise {{TASK_NAME}} task. All [Input] are in {{Language}}.
{{MORE_TASK_DEFINITION}}
Your are required to acted as a professional native-speaker human annotator to judge the given {{TGT}} in [Input].
Your evaluation should follow the [Criteria] and  [Guidance]. 
The output format should follow the [Output Format].

[Guidance]
You should strictly follow my guidance:
1. Each score is between {{MIN_SCORE}} (lowest) and {{MAX_SCORE}} (highest).
2. Each score should be {{DATATYPE}} score.
3. You should strictly follow the given output format and can't output other information.
{{MORE_GUIDANCE}}
If you break my guidance, you will be penalized.

[Criteria]
{{Criteria}}

{{In-Context Examples}}

[Output Format]
Your output should strictly follow this format and can be directly decoded by Python:
'''
{{Output}}
'''

[Input]
'''
{
    "{{SRC}}": {{SRC_VALUE}},
    "{{TGT}}": {{TGT_VALUE}}
}
'''
 
"""
