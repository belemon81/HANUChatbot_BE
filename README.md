# HANUChatbot_BE: Coop project used for dissertation
- 4/5/2024: Finish project
- 23/7/2024: New update Docker
    1) The original project was modified to adapt routing rules of Linux. Please refer to previous commit to run the project in Win.
    2) If you want to run chatbot directly:
        + Step 1: unzip db-data
        + Step 2: add valid openai api key in docker-compose.yml
        + Step 3: run docker-compose.yml
    3) If you want to know its flow:
        + Step 1: uncomment 1st command in docker-compose.yml > app-hanu-gpt-backend 
        + Step 2: commnent 2nd command
        + Step 3: run docker-compose.yml
        + Step 4: switch to use 2nd command
        + Step 5: add valid openai api key in docker-compose.yml
        + Step 6: run docker-compose.yml
- HANUChatbot_BE (hanu-gpt) is cloned from my teammate's work: https://github.com/nantruong/hanu-gpt