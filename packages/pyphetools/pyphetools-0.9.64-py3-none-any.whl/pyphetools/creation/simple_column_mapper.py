from .hp_term import HpTerm
from .column_mapper import ColumnMapper
from .hpo_cr import HpoConceptRecognizer
from typing import List
import pandas as pd
import re
from collections import defaultdict


def get_separate_hpos_from_df(df, hpo_cr):
    """Loop through all the cells in a dataframe or series and try to parse each cell as HPO term.
    Useful when the separate HPO terms are in the cells themselves.

    :param df: dataframe with phenotypic data
    :type df: pd.DataFrame
    :param hpo_cr: instance of HpoConceptRecognizer to match HPO term and get label/id
    :type hpo_cr: HpoConceptRecognizer
    :returns: list of lists with the additional HPO terms per individual
    :rtype: List[List[HpTerm]]
    """
    additional_hpos = []

    for i in range(len(df)):
        temp_hpos = []
        for y in range(df.shape[1]):
            hpo_term = hpo_cr.parse_cell(df.iloc[i, y])
            if len(hpo_term) > 0:
                temp_hpos.extend(hpo_term)
        additional_hpos.append(list(set(temp_hpos)))
    return additional_hpos


class SimpleColumnMapper(ColumnMapper):
    """ColumnMapper for columns that contain information about a single phenotypic abnormality only
    :param column_name: name of the column in the pandas DataFrame
    :type column_name: str
    :param hpo_id: HPO  id, e.g., HP:0004321
    :type hpo_id: str
    :param hpo_label: Corresponding term label
    :type hpo_label: str
    :param observed: symbol used in table if the phenotypic feature was observed
    :type observed: str
    :param excluded: symbol used if the feature was excluded
    :type excluded: str
    :param non_measured: symbol used if the feature was not measured or is N/A. Defaults to None, optional
    :type non_measured: str
    """
    def __init__(self, column_name, hpo_id, hpo_label, observed=None, excluded=None, non_measured=None):
        """
        Constructor
        """
        super().__init__(column_name=column_name)
        self._hpo_id = hpo_id
        self._hpo_label = hpo_label
        if observed is None or excluded is None:
            raise ValueError(
                    "Need to provide arguments for both observed and excluded")
        self._observed = observed
        self._excluded = excluded
        self._not_measured = non_measured

    def map_cell(self, cell_contents) -> List[HpTerm]:
        if not isinstance(cell_contents, str):
            raise ValueError(
                f"Error: cell_contents argument ({cell_contents}) must be string but was {type(cell_contents)} -- coerced to string")
        contents = cell_contents.strip()
        # first check if the cell contents represent a valid iso8601, which represents age of onset.
        if ColumnMapper.is_valid_iso8601(contents):
            return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, onset=contents)]
        if contents in self._observed:
            return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label)]
        elif contents in self._excluded:
            return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, observed=False)]
        else:
            return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, measured=False)]

    def preview_column(self, df:pd.DataFrame) -> pd.DataFrame:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("df argument must be pandas DataFrame, but was {type(column)}")
        column = df[self._column_name]
        mapping_counter = defaultdict(int)
        for _, value in column.items():
            cell_contents = str(value)
            value = self.map_cell(cell_contents)
            hpterm = value[0]
            mapped = f"original value: \"{cell_contents}\" -> HP: {hpterm.hpo_term_and_id} ({hpterm.display_value})"
            mapping_counter[mapped] += 1
        dlist = []
        for k, v in mapping_counter.items():
            d = {"mapping": k, "count": str(v)}
            dlist.append(d)
        return pd.DataFrame(dlist)

class SimpleColumnMapperGenerator:
    """Convenience tool to provide mappings automatically

    Try to map the columns in a dataframe by matching the name of the column to correct HPO term.
    This class can be used to generate SimpleColumn mappers for exact matches found in the columns names.

    :param df: dataframe with phenotypic data
    :type df: pd.DataFrame
    :param observed: symbol used in table if the phenotypic feature was observed
    :type observed: str
    :param excluded: symbol used if the feature was excluded
    :type excluded: str
    :param hpo_cr: instance of HpoConceptRecognizer to match HPO term and get label/id
    :type hpo_cr: HpoConceptRecognizer
    """
    def __init__(self, df:pd.DataFrame, observed:str, excluded:str, hpo_cr:HpoConceptRecognizer) -> None:
        """
        Constructor
        """
        self._df = df
        self._observed = observed
        self._excluded = excluded
        self._hpo_cr = hpo_cr
        self._mapped_columns = []
        self._unmapped_columns = []
        self._error_messages = []


    def try_mapping_columns(self) -> List[ColumnMapper]:
        """As a side effect, this class initializes three lists of mapped, unmapped, and error columns

        :returns: A dictionary with successfully mapped columns
        :rtype: Dict[str,ColumnMapper]
        """
        simple_mapper_list = list()
        hpo_id_re = r"(HP:\d+)"
        for col in self._df.columns:
            colname = str(col)
            result = re.search(r"(HP:\d+)", colname)
            if self._hpo_cr.contains_term_label(colname):
                hpo_term_list = self._hpo_cr.parse_cell(colname)
                hpo_term = hpo_term_list[0]
                scm = SimpleColumnMapper(column_name=colname,
                                        hpo_id=hpo_term.id,
                                        hpo_label=hpo_term.label,
                                        observed=self._observed,
                                        excluded=self._excluded)
                simple_mapper_list.append(scm)
            elif result:
                hpo_id = result.group(1)
                if self._hpo_cr.contains_term(hpo_id):
                    hterm = self._hpo_cr.get_term_from_id(hpo_id)
                    scm = SimpleColumnMapper(column_name=colname,
                                            hpo_id=hterm.id,
                                            hpo_label=hterm.label,
                                            observed=self._observed,
                                            excluded=self._excluded)
                    simple_mapper_list.append(scm)
                else:
                    self._unmapped_columns.append(colname)
            else:
                self._unmapped_columns.append(colname)
        self._mapped_columns = [scm.get_column_name() for scm in simple_mapper_list]
        return simple_mapper_list


    def get_unmapped_columns(self):
        """
        :returns: A list of names of the columns that could not be mapped
        :rtype: List[str]
        """
        return self._unmapped_columns

    def get_mapped_columns(self) -> List[str]:
        """
        :returns: A list of names of the columns that were mapped
        :rtype: List[str]
        """
        return self._mapped_columns

    def to_html(self):
        """create an HTML table with names of mapped and unmapped columns
        """
        table_items = []
        table_items.append('<table style="border: 2px solid black;">\n')
        table_items.append("""<tr>
            <th>Result</th>
            <th>Columns</th>
        </tr>
        """)
        mapped_str = "; ".join(self._mapped_columns)
        unmapped_str = "; ".join([f"<q>{colname}</q>" for colname in self._unmapped_columns])
        def two_item_table_row(cell1, cell2):
            return f"<tr><td>{cell1}</td><td>{cell2}</td></tr>"
        table_items.append(two_item_table_row("Mapped", mapped_str))
        table_items.append(two_item_table_row("Unmapped", unmapped_str))
        table_items.append('</table>\n') # close table content
        return "\n".join(table_items)
