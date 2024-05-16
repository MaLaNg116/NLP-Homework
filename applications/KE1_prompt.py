KNOWLEDGE_EXTRACT_METRICS = {
    "Head Entity": """Head Entity: Refers to the subject of the description in the knowledge triad, usually the name of an entity or thing. The head entity is the starting point of the knowledge point and it emits a relation pointing to the tail entity. """,
    "Relationship": """Relationship: Relationship is a bridge between the head entity and the tail entity, which describes a particular connection or role between the head entity and the tail entity. For example, "belongs to", "is located in", "creates", etc. are some examples of relationships. """,
    "Tail Entity": """Tail Entity: It is usually the entity or object associated with the head entity that is the target of the relationship's action. In a triad, the tail entity is usually the object pointed to by the head entity through the relationship.""",
}

KNOWLEDGE_EXTRACT_GENERAL_PROMPT_PATTERN = """
[Task Description] 
Here is a {{TASK_NAME}} task. All [Input] and [Output] are in {{Language}}.
{{MORE_TASK_DEFINITION}}
Your are required to acted as an expert in general knowledge to extract general knowledge from the given {{TEXT}} in [Input].
Your extraction should follow the [Criteria] and  [Guidance]. 
The output format should follow the [Output Format].

[Guidance]
You should strictly follow my guidance:
1. Extract the triads of general life knowledge from the given text, each of which should be in the format (Head Entity, Relationship, Tail Entity).
2. If any of the elements of (Head Entity, Relationship, Tail Entity) is null, the triad is invalid and is not included in the final result.
3. Text types are not restricted. Ensure that the extracted triples are concise and cover a wide range of common sense knowledge.
4. The number of extracted triples should be as large as possible and the length of the extracted text should be as concise and general as possible.
5. Contextual information can be taken into account when extracting knowledge triples and there is no need to include additional explanatory text or examples in the output.
6. When dealing with complex sentences or fuzzy relationships, please provide a most likely triad.
7. You should strictly follow the given output format and can't output other information.
8. Returns the final result to me in the form of a json code block in markdown format, while avoiding any errors that might prevent it from being read successfully.
{{MORE_GUIDANCE}}
If you break my guidance, you will be penalized.

[Criteria]
{{Criteria}}

{{In-Context Examples}}

[Output Format]
Your output should strictly follow this format and can be directly decoded by Markdown:
```json
{{Output}}
```

[Input]
'''
{
    "{{TEXT}}": {{TEXT_VALUE}},
}
'''

"""
