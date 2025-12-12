import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",       # usually localhost
        user="root",            # your MySQL username
        password="Sruju@16", # replace with your MySQL password
        database="expense_tracker" # your database name
    )
    return conn


def add_expense():
    student_name = input("Enter your name: ").strip().lower()
    amount = float(input("Enter amount spent: "))
    
    # Select category
    categories = ['food', 'travel', 'academic', 'other']
    print("Select category:")
    for i, cat in enumerate(categories, start=1):
        print(f"{i}. {cat.capitalize()}")
    cat_choice = int(input("Enter choice number: "))
    category = categories[cat_choice - 1]
    
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    description = input("Enter short description: ")
    
    from datetime import datetime
    if date == "":
        date = datetime.now().strftime("%Y-%m-%d")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (student_name, amount, category, date, description)
        VALUES (%s, %s, %s, %s, %s)
    """, (student_name, amount, category, date, description))
    conn.commit()
    conn.close()
    
    print("\n✔ Expense added successfully!\n")


def view_expenses_by_month():
    student_name = input("Enter your name: ").strip().lower()
    
    # Ask user for month and year
    month = int(input("Enter month (1-12): "))
    year = int(input("Enter year (YYYY): "))
    
    # Calculate start and end date of the month
    from datetime import datetime
    import calendar
    start_date = datetime(year, month, 1).strftime("%Y-%m-%d")
    last_day = calendar.monthrange(year, month)[1]
    end_date = datetime(year, month, last_day).strftime("%Y-%m-%d")
    
    # Fetch data from MySQL
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT amount, category, date, description
        FROM expenses
        WHERE student_name=%s AND date BETWEEN %s AND %s
    """, (student_name, start_date, end_date))
    
    records = cursor.fetchall()
    conn.close()
    
    if not records:
        print(f"\n❌ No expenses found for {month}/{year}!\n")
        return
    
    # Initialize totals
    total = 0
    category_totals = {'food': 0, 'travel': 0, 'academic': 0, 'other': 0}
    
    print(f"\n----- Expenses for {month}/{year} -----")
    for amount, category, date, description in records:
        print(f"Amount: {amount}, Category: {category}, Date: {date}, Description: {description}")
        total += amount
        cat_lower = category.lower()
        if cat_lower in category_totals:
            category_totals[cat_lower] += amount
        else:
            category_totals['other'] += amount
    
    print("\n----- Category-wise Spending -----")
    for cat, amt in category_totals.items():
        print(f"{cat.capitalize()}: ₹{amt}")
    
    print(f"\nTotal spent in {month}/{year}: ₹{total}\n")


def main():
    while True:
        print("===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Last Month Expenses")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses_by_month()
        elif choice == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid option. Try again.\n")

# Run the program
main()