from st_pages import Page, show_pages

def run():

    show_pages(
        [
            Page("./pages/Estoque.py", "Estoque", "📦"),
            Page("./pages/Laboratorio.py", "Laboratorio", "👓"),       
        ]
    )

run()