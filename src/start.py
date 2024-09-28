from src.ui.UI import UserInterface
from  src.repository.ErrorRepository import RepositoryError

if __name__ == "__main__":
    ui = UserInterface()
    while True:
        try:
            ui.Print_Menu()
        except ValueError as ve:
            print(ve)
        except RepositoryError as re:
            print(re)

