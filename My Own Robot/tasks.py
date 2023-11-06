from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.PDF import PDF
from RPA.Tables import Tables

@task
def order_robots_from_RobotSpareBin():
    browser.configure(
        slowmo=100,
    )
    open_robot_order_website()
    orders = get_orders()
    close_annoying_modal()
    

def open_robot_order_website():
    """Opens the order website"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def get_orders():
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)
    
    library = Tables()
    orders = library.read_table_from_csv(
        "orders.csv", columns = ["Order Number", "Head", "Body", "Legs", "Adress"]
    )

    customers = library.group_table_by_column(orders, "Order Number")
    
    for order in orders:
        fill_the_form(order)
    return customers
        
def close_annoying_modal():
    page = browser.page()
    page.click("button.btn:nth-child(3)")

def fill_the_form(order_data):
    page = browser.page()
    
    page.select_option("#head", order_data["Head"])
    page.select_option("#id-body", order_data["Body"])
    
    