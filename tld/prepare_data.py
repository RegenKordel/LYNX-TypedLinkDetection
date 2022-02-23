from tqdm.auto import tqdm
import pandas as pd
from tld.config import preprocessed_data_dir


def build_joined_data(tracker: str):
    joined_out_file = preprocessed_data_dir / f'joined_{tracker}.csv'
    if joined_out_file.is_file():
        return

    issue_df = pd.read_csv(preprocessed_data_dir / f'issues_{tracker}.csv', sep=';').set_index('issue_id')
    link_df = pd.read_csv(preprocessed_data_dir / f'links_plus_{tracker}.csv', sep=';')[['linktype', 'issue_id_1', 'issue_id_2']]

    joined_df = link_df \
        .join(issue_df.add_suffix('_1'), on='issue_id_1') \
        .join(issue_df.add_suffix('_2'), on='issue_id_2')

    joined_df.to_csv(joined_out_file)


if __name__ == '__main__':
    trackers = {issues_file.stem[len('issues_'):] for issues_file in preprocessed_data_dir.glob('issues_*.csv')}

    for tracker in tqdm(trackers):
        # TODO: Add conversion from raw to preprocessed
        build_joined_data(tracker)
