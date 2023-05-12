import samgpt.agents.websearch_agent as wa
import json

def main():
    result =wa.make_web_request("Where is the best place to open a pet shop?")
    print(result)

if __name__ == "__main__":
    main()