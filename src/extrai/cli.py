import argparse

from extrai.batch import process_batch


def main():

    parser = argparse.ArgumentParser(description="Run LLM extraction batch")

    parser.add_argument("--input", required=True)

    parser.add_argument("--prompt", required=True)

    parser.add_argument("--property", default="content")

    parser.add_argument("--model", required=True)

    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    process_batch(
        input_file=args.input,
        prompt_file=args.prompt,
        json_property=args.property,
        model=args.model,
        output_file=args.output,
    )


if __name__ == "__main__":
    main()
