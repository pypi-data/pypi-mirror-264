from typing import Optional, List
import fnmatch

import numpy as np

from .rooproc_hybrid_action import RooProcHybridAction
from .formatter import ListFormatter
from quickstats.interface.root import RDataFrameBackend

from quickstats.utils.common_utils import is_valid_file
from quickstats.utils.data_conversion import root_datatypes, get_rdf_column_type, ConversionMode, reduce_vector_types

class RooProcOutputAction(RooProcHybridAction):

    PARAM_FORMATS = {
        'columns': ListFormatter
    }
    
    def __init__(self, filename:str, 
                 columns:Optional[List[str]],
                 **kwargs):
        super().__init__(filename=filename,
                         columns=columns,
                         **kwargs)
        
    @classmethod
    def parse(cls, main_text:str, block_text:Optional[str]=None):
        kwargs = cls.parse_as_kwargs(main_text)
        return cls._try_create(**kwargs)
    
    def get_valid_columns(self, rdf, processor, columns:Optional[List[str]]=None,
                          mode:ConversionMode=ConversionMode.REMOVE_NON_STANDARD_TYPE):
        all_columns = list([str(col) for col in rdf.GetColumnNames()])
        if columns is None:
            columns = all_columns
        else:
            columns_ = []
            for column in columns:
                if "*" in column:
                    matched_columns = fnmatch.filter(all_columns, column)
                    if not matched_columns:
                        processor.stdout.warning(f'No columns matching the expression "{column}". '
                                                 'It will be excluded from the output')
                    columns_.extend(matched_columns)
                elif column not in all_columns:
                    processor.stdout.warning(f'Column "{column}" does not exist. '
                                             'It will be excluded from the output')
                else:
                    columns_.append(column)
            columns = columns_
        mode = ConversionMode.parse(mode)
        if mode in [ConversionMode.REMOVE_NON_STANDARD_TYPE,
                    ConversionMode.REMOVE_NON_ARRAY_TYPE]:
            column_types = np.array([get_rdf_column_type(rdf, col) for col in columns])

            if mode == ConversionMode.REMOVE_NON_ARRAY_TYPE:
                column_types = reduce_vector_types(column_types)
            new_columns = list(np.array(columns)[np.where(np.isin(column_types, root_datatypes))])
            removed_columns = np.setdiff1d(columns, new_columns)
            if len(removed_columns) > 0:
                col_str = ", ".join(removed_columns)
                processor.stdout.warning("The following column(s) will be excluded from the output as they have "
                                         f"data types incompatible with the output format: {col_str}")
            columns = new_columns
        return columns