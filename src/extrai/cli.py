import argparse

from extrai.batch import process_batch


def main():

    parser = argparse.ArgumentParser(description="Run LLM extraction batch")

    parser.add_argument("--input", required=True)

    parser.add_argument("--prompt", required=True)

    parser.add_argument("--property", default="content")

    parser.add_argument("--model", required=True)

    parser.add_argument("--output", required=True)

    parser.add_argument(
        "--start-line",
        type=int,
        default=1,
        help="Line number where processing should start",
    )

    args = parser.parse_args()

    process_batch(
        input_file=args.input,
        prompt_file=args.prompt,
        json_property=args.property,
        model=args.model,
        output_file=args.output,
        start_line=args.start_line,
    )


if __name__ == "__main__":
    main()
