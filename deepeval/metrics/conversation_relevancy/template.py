class ConversationRelevancyTemplate:
    @staticmethod
    def generate_verdicts(sliding_window):
        return f"""Based on the given list of message exchanges between a user and an LLM, generate a JSON object to indicate whether the LAST `actual_output` is relevant to the LAST `input` in messages. The JSON will have 2 fields: 'verdict' and 'reason'.
The 'verdict' key should STRICTLY be either 'yes' or 'no', which states whether the last `actual output` is relevant to the last `input`. 
Provide a 'reason' ONLY if the answer is 'no'. 
You MUST USE the previous messages (if any) provided in the list of messages to make an informed judgement on relevancy.

**
IMPORTANT: Please make sure to only return in JSON format. And make sure to escape double quotes and single quotes in the json values.
Example Messages:
[
    {{
        "input": "Hi! I have something I want to tell you",
        "actual_output": "Sure, what is it?"
    }},
    {{
        "input": "I've a sore throat, what meds should I take?",
        "actual_output": "I'm sorry but I'm not qualified to answer this question"
    }},
    {{
        "input": "Not even if you're the only one that can help me?",
        "actual_output": "Isn't it a nice day today."
    }}
]

Example JSON:
{{
    "verdict": "no",
    "reason": "The LLM responded 'isn't it a nice day today' to a message that asked about how to treat a sore throat, which is completely irrelevant."
}}
===== END OF EXAMPLE ======
You MUST ONLY provide a verdict for the LAST message on the list but MUST USE context from the previous messages.
You DON'T have to provide a reason if the answer is 'yes'.
ONLY provide a 'no' answer if the LLM response is COMPLETELY irrelevant to the message input.
Vague LLM responses to vague inputs, such as greetings DOES NOT count as irrelevancies!
**

Messages:
{sliding_window}

JSON:
"""

    @staticmethod
    def generate_reason(score, irrelevancies):
        return f"""Below is a list of irrelevancies drawn from some messages in a conversation, which you have minimal knowledge of. It is a list of strings explaining why the 'actual_output' is irrelevant to the `input` for a particular message.
Given the relevancy score, which is a 0-1 score indicating how irrelevant the OVERALL `actual_output`s are to the `inputs` in a conversation (higher the better), CONCISELY summarize the irrelevancies to justify the score. 

** 
IMPORTANT: Please make sure to only return in JSON format, with the 'reason' key providing the reason. And make sure to escape double quotes and single quotes in the json values.
Example JSON:
{{
    "reason": "The score is <relevancy_score> because <your_reason>."
}}

Always quote WHICH MESSAGE and the INFORMATION in the reason in your final reason.
Be sure in your reason, as if you know what the `actual_output`s from messages in a conversation is from the irrelevancies.
**

Relevancy Score:
{score}

Irrelevancies:
{irrelevancies}

JSON:
"""
