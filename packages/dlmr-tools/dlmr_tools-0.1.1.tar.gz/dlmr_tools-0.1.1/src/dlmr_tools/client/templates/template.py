from dlmr_tools.data_tool import Data
from dlmr_tools.graph_tool import Graph_1D

from dataclasses import dataclass


@dataclass
class GraphManager:
    __datasheet_name: str = "spreadsheet.xlsx"
    __output_folder: str = "results"
    __sheet_names = ["Sheet 1", "Sheet 2"]
    __data = dict()
    
    def __post_init__(self) -> None:
        self.__spreadsheet = Data(
            data_path=self.__datasheet_name,
            sheet_name=self.__sheet_names
        )
        
        self.__data["x_values"] : list = self.__spreadsheet.get_list(sheet_name=self.__sheet_names[0], list_name="Label x")
        self.__data["y_values"]: list = self.__spreadsheet.get_list(sheet_name=self.__sheet_names[0], list_name="Label y")
        
    def plot_graphs(self) -> None:
        """
        Call all the plot functions.
        """
        self.plot_example()
        
    def plot_example(self) -> None:
        """
        Example of a plot function.
        """
        graph = Graph_1D(figsize=(5, 3), fontsize=9)
        graph.setup_axis(xlabel="x [SI]", ylabel="y [SI]", sci=False)
        graph.plot(x=self.__data["x_values"], y=self.__data["y_values"], label="Curve 1", marker='', linestyle='-', color='chartjs_blue')
        graph.save(filename=self.__output_folder + "/example.png", dx=0.15)
        graph.delete()

if __name__ == "__main__":
    graph_manager = GraphManager()
    graph_manager.plot_graphs()