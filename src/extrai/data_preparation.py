import argparse
import pandas as pd


def create_content_column(input_file, output_file):

    df = pd.read_json(input_file)

    cols = df.columns

    df["content"] = df.apply(
        lambda row: "; ".join([f"{col}: {row[col]}" for col in cols]), axis=1
    )

    df.to_json(output_file, orient="records", lines=True, force_ascii=False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Add a content field and convert JSON to JSONL"
    )

    parser.add_argument("--input", required=True, help="Input JSON file")

    parser.add_argument("--output", required=True, help="Output JSONL file")

    args = parser.parse_args()

    create_content_column(args.input, args.output)
