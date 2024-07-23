'use client';
import { useState, useEffect, useRef } from "react";
import ChatInterface from "@/components/ChatInterface";
import { usePathname } from 'next/navigation'
import { log } from "console";

export default function EducationBot() {
    interface ChatLogItem {
        type: 'bot' | 'user';
        message: any;
    }
    const currentPage = usePathname();

    const educationFAQs = [
        "How many credits does Information Technology Falcuty program have?",
        "What are orientations of English department?",
        "What subjects does General-knowledge Block contains?"
    ];

    const [inputQuestion, setInputQuestion] = useState('');
    const [chatLog, setChatLog] = useState<ChatLogItem[]>([
        { type: 'bot', message: 'Ask me anything about the educational program of Hanoi University.' }
    ]);
    const [isLoading, setIsLoading] = useState(false);

    const chatEnd = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (chatEnd.current) {
            chatEnd.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [chatLog]);

    const handleSubmit = (event: any) => {
        event.preventDefault();
        if (!inputQuestion.trim()) {
            return;
        }
        setChatLog(prevChatLog => [...prevChatLog, { type: 'user', message: inputQuestion }]);
        fetchDocuments(inputQuestion);
        setInputQuestion('');
    }

    const [selectedQuestion, setSelectedQuestion] = useState(null);

    const clearChat = () => {
        console.log("Clearing chat...");
        // if (chatLog.length > 1) {
        setChatLog([{ type: 'bot', message: 'Ask me anything about the educational program of Hanoi University.' }]);
        sessionStorage.removeItem('botMessages_education');
        setSelectedQuestion(null)
        // }
    };
    

    async function fetchDocuments(question: string) {
        const url = 'http://localhost:8080/hanu-chatbot/educational-program';
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question })
            });
            if (!response.ok) {
                console.log(response)
                throw new Error('Failed to fetch documents');
            }
            const docsData = await response.json();
            console.log('Documents:', docsData);
            sendMessage(question, docsData);
        } catch (error) {
            console.error('Error fetching documents:', error);
        }
    }

    const sendMessage = async (question: string, docsData: any) => {

        const url = '/api/chat';
        let docsContext = "";
        let systemMessage;
        let assistant;

        if (docsData && docsData.relevant_docs && docsData.relevant_docs.length > 0) {
            for (const document of docsData.relevant_docs) {
                docsContext += `${document}\n`; // Assuming each document is a string
            }
        }
        // console.log(docsContext);

        const storedResponses = JSON.parse(sessionStorage.getItem('botMessages_education') || '[]');
        const recentResponses = storedResponses.slice(Math.max(storedResponses.length - 5, 0));
        const hasRecentResponses = recentResponses.length > 0;

        console.log(recentResponses);

        if (docsData && docsData.relevant_docs && docsData.relevant_docs.length > 0) {
            systemMessage = `
                You are a friendly chatbot of Hanoi University.
                ${hasRecentResponses ? 'You must refer to HISTORY (your previous responses) for understanding the question if necessary.' : ''}
                You must filter all relevant content in HANU documents to answer the questions.
                You must always use English to answer.
                You respond with a concise, technically credible tone.
                You automatically make currency exchange based on the language asked, if not provided specific currency.
            `;
            const contextContent = hasRecentResponses ? `HISTORY: ${recentResponses}; ` : '';
            assistant = {
                role: 'assistant',
                content: `${contextContent}\nHANU documents: ${docsContext}`
            };
        } else {
            systemMessage = `
                You are a friendly chatbot of Hanoi University.
                You respond in a concise, technically credible tone.
                You must always use English to answer.
            `;
            assistant = null;
        }

        const data = {
            messages: [
                {
                    role: "system",
                    content: systemMessage
                },
                {
                    role: "user",
                    content: question
                },
                assistant
            ].filter(message => message !== null)
        };

        setIsLoading(true);

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            // Check the content type of the response
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                // If the response is JSON, parse it as JSON
                const responseData = await response.json();
                sessionStorage.setItem('botMessages_education', JSON.stringify([responseData.message, ...recentResponses]));
                // Assuming responseData is an object with the bot's message
                setChatLog(prevChatLog => [...prevChatLog, { type: 'bot', message: responseData.message }]);
            } else {
                // If the response is not JSON, treat it as plain text
                const responseText = await response.text();
                sessionStorage.setItem('botMessages_education', JSON.stringify([responseText, ...recentResponses, ]));

                // Assuming responseText contains the bot's message
                setChatLog(prevChatLog => [...prevChatLog, { type: 'bot', message: responseText }]);
            }
        } catch (error) {
            console.error('Error:', error);
            setChatLog(prevChatLog => [...prevChatLog, { type: 'bot', message: "There is an error when processing your request. Please try again later." }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <ChatInterface
            clearChat={clearChat}
            chatLog={chatLog}
            isLoading={isLoading}
            inputQuestion={inputQuestion}
            setInputQuestion={setInputQuestion}
            handleSubmit={handleSubmit}
            chatEnd={chatEnd}
            currentPage={currentPage}
            FAQs={educationFAQs}
            selectedQuestion={selectedQuestion}
            setSelectedQuestion={setSelectedQuestion}
        />

    );
};



