from src import TakeStock
from src import TakeStock_Reporter
import sys


def main():
    if sys.argv[1:]:
        TakeStock_Reporter.main()
    else:
        TakeStock.main()

if __name__ == "__main__":
    main()