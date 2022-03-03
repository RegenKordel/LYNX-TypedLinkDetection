import argparse

from tld.models.bert.training import main

parser = argparse.ArgumentParser()
parser.add_argument('--model', required=True)
parser.add_argument('--tracker', required=True)
parser.add_argument('--target', default='linktype')
parser.add_argument('--non-links', action=argparse.BooleanOptionalAction, default=True)
parser.add_argument('--train-batch-size', type=int, required=True)
parser.add_argument('--eval-batch-size', type=int, required=True)
parser.add_argument('--n-epochs', type=int, required=True)

args = parser.parse_args()

main(
    model_name=args.model,
    tracker=args.tracker,
    target=args.target,
    include_non_links=args.non_links,
    train_batch_size=args.train_batch_size,
    eval_batch_size=args.eval_batch_size,
    n_epochs=args.n_epochs,
)
