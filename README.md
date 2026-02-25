# Anthropic_Claude
Sample app developed in claude for telecomm industry

Execute the following in the terminal:

unzip telecom-ai-agent.zip && cd telecom-ai-agent
pip install -r requirements.txt
cp .env.example .env   # add your AWS bedrock keys
python main.py         # → http://localhost:8000/docs
pytest                 # run test suite
