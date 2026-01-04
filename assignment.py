import requests

def fetch_book_data(topic):
    url = "https://openlibrary.org/search.json"
    params = {
        "q": topic, 
        "limit": 100, 
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        print("Network Error: Could not reach the library.")
        return None

def process_and_filter(data, max_editions):
    if not data or 'docs' not in data:
        return []

    filtered_book_list = []
    for doc in data['docs']:
        edition_count = doc.get('edition_count', 0)
        
        if edition_count <= max_editions:
            filtered_book_list.append({
                'title': doc.get('title', 'Untitled'),
                'author': doc.get('author_name', ['Unknown'])[0],
                'year': doc.get('first_publish_year', 'N/A'),
                'edition_count': edition_count
            })
    return filtered_book_list

def calculate_statistics(results):
    if not results:
        return None
    count = len(results)
    total_editions = sum(book['edition_count'] for book in results)
    average = total_editions / count
    max_val = max(book['edition_count'] for book in results)
    
    return {
        "total": count,
        "avg": round(average, 2),
        "max": max_val
    }

def save_to_file(results, topic,statistics):
    filename = f"{topic}_limited_report.txt"
    with open(f"{topic}_limited_report.txt", "w") as file:
        file.write(f"Books for '{topic}' with low edition counts\n")
        file.write(f"Total Books: { statistics['total']}\n")
        file.write(f"Average Editions: { statistics['avg']}\n")
        file.write(f"Highest Edition Count: { statistics['max']}\n")
        file.write("-" * 50 + "\n")
        for book in results:
            file.write(f"[{book['edition_count']} eds] {book['title']} - {book['author']}\n")
    print(f"\nReport saved to {filename}")
print("--- Professional Book edition_count Filter ---")
user_topic = input("Enter the topic (e.g., Python, Rome, Science, love ): ").strip()

try:
    max_edition = int(input("Enter the maximum Edition Count allowed: higher is better:  "))
    
    print("\nConnecting to library...")
    raw_results = fetch_book_data(user_topic)
    final_books = process_and_filter(raw_results, max_edition)
    
    if not final_books:
        print(f"No books found for '{user_topic}' with {max_edition} or fewer editions.")
    else:
        print(f"\nResults for {user_topic} (Filtered by max {max_edition} editions):")
        print(f"{'EDS':<5} | {'YEAR':<6} | {'TITLE'}")
        print("-" * 50)
        for book in final_books:
            print(f"{book['edition_count']:<5} | {book['year']:<6} | {book['title']}")
        statistics = calculate_statistics(final_books)
        
        print(f"\n--- Analysis Summary for {user_topic} ---")
        print(f"Items Found: { statistics['total']}")
        print(f"Average Editions: { statistics['avg']}")
        print(f"Max Editions Found: { statistics['max']}")
        print("-" * 40)
        
        save_to_file(final_books, user_topic,statistics)

except ValueError:
    print("Error: Please enter a whole number for the edition_count.")
