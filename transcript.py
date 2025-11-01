from youtube_transcript_api import YouTubeTranscriptApi
import json
from groq import Groq
from google import genai
from dotenv import load_dotenv
import os   
load_dotenv()
os.environ["GENAI_API_KEY"] = os.getenv("GEMINI_API_KEY")
client = genai.Client()



video_id="-7TxYcgioxg"
ytt_api = YouTubeTranscriptApi()
transcript_list = ytt_api.list(video_id)
fetched_transcript = ytt_api.fetch(video_id, languages=['hi'])

transcript_formatted = [
    {
        "start": seg.start,
        "end": seg.start + seg.duration,
        "text": seg.text
    }
    for seg in fetched_transcript
]

print(transcript_formatted)


def helper(content: str):
    first = content.find('{')
    last = content.rfind('}')
    if first == -1 or last == -1 or last < first:
        return None  
    return content[first:last + 1]

def topic(content:str):

    chat_completion = client.models.generate_content(
       
            contents= f'''
                    Based on the following:
                        {content}

                        Extract each of the main topics or segments discussed.

                        For each topic/segment, provide:
                        1. A short, descriptive title (max 5 words)
                        2. A list of related keywords (max 5 keywords)

                       Format the response as a JSON object with an 'output' field that is a list of objects, each containing 'title' and 'keywords'.

                        
                
                ''',
            model="gemini-2.5-flash"
    )
    response=chat_completion.text
    print(response)
    response=helper(response)
    response_json=json.loads(response)
    print(type(response_json))
    return response_json

topic_extraction=topic(transcript_formatted)

def create_clips(topic_extraction,transcript_formatted):
    chat_completion = client.models.generate_content(
            contents= f'''
                    For each of the following topics/segments, find the most relevant part in the transcript:
                    {json.dumps(topic_extraction)}

                    Transcript:
                    {json.dumps(transcript_formatted)}

                    For each topic/segment:
                    1. Find the part that best represents the topic/segment.
                    2. Aim for a clip duration of  60-120 seconds, but prioritize capturing the complete discussion or segment.
                    3. If the relevant content exceeds 120 seconds, include it entirely to avoid cutting off important information.
                    4. Ensure that the segment captures complete thoughts and ideas. Do not cut off in the middle of a sentence or a speaker's point.
                    5. It's better to include slightly more content than to risk cutting off important information.

                    Provide the results as a JSON array of objects, each containing:
                    - title: The topic/segment title
                    - start: Start time of the clip (in seconds)
                    - end: End time of the clip (in seconds)

                    The clips can overlap if necessary to capture complete discussions or segments.

                ''',
        model="gemini-2.5-flash"
    )
    response=chat_completion.text
    print(response)
    return response
    



create_clips(topic_extraction,transcript_formatted)

    
