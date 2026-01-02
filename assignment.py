import requests
def fetch_advice(topic):
    url = f"https://api.adviceslip.com/advice/search/{topic}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('slips', [])
        else:
            return []
    except Exception as e:
        print("Something went wrong:", e)
        return []
def process_advice(slips, min_length):
    filtered = []

    for slip in slips:
        advice = slip['advice']
        if len(advice) >= min_length:
            filtered.append(advice)
    filtered.sort(key=len, reverse=True)
    return filtered


def display_advice(advice_list, topic):
    if not advice_list:
        print("No advice found.")
        return
    save_to_txt(advice_list, topic)

    print("\n--- Advice Results ---")
    for i, advice in enumerate(advice_list, start=1):
        print(f"{i}. {advice}")


def save_to_txt(advice_list, topic):
    filename = f"{topic}_advice.txt"
    with open(filename, "w") as file:
        for advice in advice_list:
            file.write(advice + "\n")
    print(f"Saved to {filename}")
   # save_to_txt(advice_list, topic)


#def main():
print("=== Advice Finder App ===")

topic = input("Enter a topic: ").strip()
if not topic:
    print("Topic cannot be empty.")
        
try:
     min_length = int(input("Minimum advice length: "))
except ValueError:
        print("Invalid number.")

slips = fetch_advice(topic)
advice_list = process_advice(slips, min_length)
display_advice(advice_list,topic)

