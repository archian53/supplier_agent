from openai import OpenAI
import json
from logger_config import logger
import os

class AIProcessor:
    def __init__(self):
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        self.model = "gpt-4o"

    def analyze_product_data(self, existing_data, scraped_content, questions):
        try:
            prompt = self._construct_analysis_prompt(existing_data, scraped_content, questions)
            
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a product data analyst expert. Analyze the provided information and generate accurate answers to the questions based on historical data and scraped content."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            raise

    def validate_ai_responses(self, responses, questions):
        try:
            validation_prompt = self._construct_validation_prompt(responses, questions)
            
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data validation expert. Verify the accuracy and consistency of the provided answers."},
                    {"role": "user", "content": validation_prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            validation_result = json.loads(response.choices[0].message.content)
            return validation_result
        except Exception as e:
            logger.error(f"Error in AI validation: {str(e)}")
            raise

    def _construct_analysis_prompt(self, existing_data, scraped_content, questions):
        return f"""
        Analyze the following information and generate answers for {len(questions)} questions:

        Historical Data:
        {json.dumps(existing_data, indent=2)}

        Scraped Content:
        {scraped_content}

        Generate answers in the following JSON format:
        {{
            "question_1": "answer_1",
            "question_2": "answer_2",
            ...
        }}

        Ensure all answers are:
        1. Consistent with historical data patterns
        2. Supported by scraped content when available
        3. Tagged with "AI generated" where appropriate
        """

    def _construct_validation_prompt(self, responses, questions):
        return f"""
        Validate the following AI-generated responses:
        {json.dumps(responses, indent=2)}

        For each response, verify:
        1. Logical consistency
        2. Data format compliance
        3. Business rule adherence

        Return validation results in the following format:
        {{
            "is_valid": boolean,
            "validation_details": {{
                "question_1": {{
                    "valid": boolean,
                    "issues": [list of issues if any]
                }},
                ...
            }}
        }}
        """
