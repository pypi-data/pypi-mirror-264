class ScoringFunction:
    """Description"""  # Description should be at the class level, this is passed to the config GUI
    return_metrics = []  # Name of metrics returned so that they can be selected in the config GUI
    
    def __init__(self, prefix: str, **kwargs):
        # Typing and default values are passed to the config GUI  
        # PyCharm style docstring should be used for parameters only (example below), these are passed to the config GUI
        # Additional choices can be specified in square brackets, for example, [Choice 1, Choice 2, Choice 3]. This will result in a dropdown list in the config GUI. Hence, avoid the use of square brackets otherwise
        """
        :param prefix: Description
        """
        self.prefix = prefix.strip().replace(' ', '_')  # Prefix to seperate multiple uses of the same class
    
    def __call__(self, smiles: list, file_names, directory, **kwargs) -> list[dict]:
        return results  
        # Results should be a list of dictionaries. Each dictionary corresponds to an input SMILES and should 'smiles' key. Every other key should be '<prefix>_<return_metric>'
        # For example,
        # [{'smiles': 'c1ccccc1', 'prefix_docking_score': -7.8},
        #  {'smiles': 'c1ccccc1C(=O)O', 'prefix_docking_score': -9.0]