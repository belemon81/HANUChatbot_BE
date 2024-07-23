import OpenAI from 'openai';
import { OpenAIStream, StreamingTextResponse } from 'ai';
 
const openai = new OpenAI({
  apiKey: process.env.NEXT_PUBLIC_OPENAI_API_KEY,
});
 
export const runtime = 'edge';
 
export async function POST(req: Request) {
  const { messages } = await req.json();
 
  if (!messages) {
    throw new Error('Question is missing');
  }

  const response = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo-0125',
    max_tokens: 1200,
    stream: true,
    temperature: 0,
    messages,
  });
 
  const stream = OpenAIStream(response);
  return new StreamingTextResponse(stream);
}





