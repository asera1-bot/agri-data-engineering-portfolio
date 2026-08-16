from src.extract.harvest import load_raw_harvest
from src.transform.harvest import transform_harvest
from src.validate.harvest import validate_harvest
from src.load.harvest import load_harvest

def main():
    raw = load_raw_harvest()
    transformed = transform_harvest(raw)
    validated = validate_harvest(transformed)
    load_harvest(validated)

if __name__ == "__main__":
    main()
