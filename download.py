import requests
import csv


def main():
    with open("./private/pdfs.csv", "r") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            if i == 0:
                continue
            file_idx = line[0]
            url = line[1]
            r = requests.get(url, allow_redirects=True)
            open("./private/files/" + file_idx + ".pdf", "wb").write(r.content)


if __name__ == "__main__":
    main()