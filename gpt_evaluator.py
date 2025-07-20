import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# def evaluate_resume_gpt(resume: str, jd: str) -> str:
#     prompt = f"You are an AI recruiter. Evaluate the following resume against the job description. Provide a score out of 100 and a 1-line summary.\n\nJob Description:\n{jd}\n\nResume:\n{resume}"

#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful resume evaluator."},
#             {"role": "user", "content": prompt}
#         ]
#     )

#     return response.choices[0].message.content

def evaluate_resume_gpt(resume: str, jd: str) -> str:
    try:
        from together import Together
        client = Together()
        prompt = f"You are an AI recruiter. Evaluate the following resume against the job description. Provide a score out of 100 and a 1-line summary.\n\nJob Description:\n{jd}\n\nResume:\n{resume}"

        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-0528-tput",  # good model
            messages=[
                {"role": "system", "content": "You are a helpful resume evaluator."},
                {"role": "user", "content":prompt}
            ]
        )
        #print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        return f"Model Error: {str(e)}"

