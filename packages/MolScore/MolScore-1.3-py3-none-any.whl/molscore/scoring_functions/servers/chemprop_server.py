import os
import pickle as pkl
import argparse
import logging
import numpy as np
from importlib import resources
from flask import Flask, request, jsonify

import chemprop

logger = logging.getLogger('chemprop_server')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

app = Flask(__name__)

class ChemProp:
    """
    This particular class uses the QSAR model from Lib-INVENT in a stand alone environment to avoid conflict dependencies.
    """
    def __init__(self, prefix: str, model_dir: os.PathLike, **kwargs):
        """
        :param prefix: Prefix to identify scoring function instance (e.g., DRD2)
        :param model_path: Path to pre-trained model (specifically clf.pkl)
        """
        self.model_path = model_dir
        self.prefix = prefix.replace(" ", "_")

        arguments = [
            '--test_path', '/dev/null',
            '--preds_path', '/dev/null',
            '--checkpoint_dir', self.model_dir
        ]
        self.args = chemprop.args.PredictArgs().parse_args(arguments)

        logger.debug(f"Loading model from {self.model_dir}")
        self.model_objects = chemprop.train.load_model(args=args)
        logger.debug(f"Model loaded: {self.model_objects}")

        #smiles = [['CCC'], ['CCCC'], ['OCC']]
        #preds = chemprop.train.make_predictions(args=args, smiles=smiles, model_objects=model_objects)
        # Invalids are removed, return_invalid_smiles=True, return_index_dict=True
        #smiles = [['CCCC'], ['CCCCC'], ['COCC']]
        #preds = chemprop.train.make_predictions(args=args, smiles=smiles, model_objects=model_objects)


@app.route('/', methods=['POST'])
def compute():
    # Get smiles from request
    logger.debug('POST request received')
    smiles = request.get_json().get('smiles', [])
    logger.debug(f'Reading SMILES:\n\t{smiles}')
    results = [{'smiles': smi, f'{model.prefix}_pred_proba': 0.0} for smi in smiles]

    # Make predictions
    # Preds & uncs are -> {idx: pred, idx2: pred2}
    # while individual pred/uncd is shape(tasks)
    preds, uncs = chemprop.train.make_predictions(
        args=args,
        smiles=[[smi] for smi in smiles],
        model_objects=model.model_objects,
        return_invalid_smiles=True,
        return_index_dict=True,
        return_uncertainty=True
    )
    # Returns format

    return jsonify(results)


def get_args():
    parser = argparse.ArgumentParser(description='Run a scoring function server')
    parser.add_argument('--port', type=int, default=8000, help='Port to run server on')
    parser.add_argument('--prefix', type=str, help='Prefix to identify scoring function instance (e.g., DRD2)')
    parser.add_argument('--model_dir', type=str, help='Path to pre-trained model (e.g., clf.pkl)')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    model = ChemProp(**args.__dict__)
    app.run(port=args.port)