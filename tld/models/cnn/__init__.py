import argparse
from typing import Dict

from tld.models.cnn.dccnn import build_dccnn_model
from tld.models.cnn.sccnn import build_sccnn_model
from tld.models.cnn.train import main, LinkModelBuilder

builder: Dict[str, LinkModelBuilder] = {
    'sccnn': build_sccnn_model,
    'dccnn': build_dccnn_model,
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, choices=['sccnn', 'dccnn'])
    parser.add_argument('--tracker', required=True)
    parser.add_argument('--non-links', action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    main(
        model_name=args.model,
        build_link_model=builder[args.model],
        source=args.tracker,
        include_non_links=args.non_links,
    )
