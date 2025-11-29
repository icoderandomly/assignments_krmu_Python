import logging
from library_manager.inventory import LibraryInventory

def setup_logging():
    logging.basicConfig(filename="library.log", level=logging.INFO)

def prompt(x): return input(x).strip()

def menu():
    print("\nLibrary Inventory Manager")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All")
    print("5. Search Title")
    print("6. Search ISBN")
    print("7. Exit")

def run():
    setup_logging()
    inv=LibraryInventory("catalog.json")
    while True:
        menu()
        c=prompt("Enter choice: ")
        if c=="1":
            t=prompt("Title: ")
            a=prompt("Author: ")
            i=prompt("ISBN: ")
            try:
                b=inv.add_book(t,a,i)
                print("Added:",b)
            except Exception as e:
                print("Error:",e)
        elif c=="2":
            i=prompt("ISBN: ")
            print("Issued." if inv.issue_book(i) else "Cannot issue.")
        elif c=="3":
            i=prompt("ISBN: ")
            print("Returned." if inv.return_book(i) else "Cannot return.")
        elif c=="4":
            for x in inv.display_all(): print("-",x)
        elif c=="5":
            q=prompt("Title keyword: ")
            r=inv.search_by_title(q)
            for x in r: print("-",x)
        elif c=="6":
            i=prompt("ISBN: ")
            b=inv.search_by_isbn(i)
            print(b if b else "Not found.")
        elif c=="7":
            break

if __name__=="__main__":
    run()
